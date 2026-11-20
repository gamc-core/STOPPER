import unittest
from dataclasses import FrozenInstanceError
from threading import Barrier, Thread

from stopper import ContractError, Execution, SignalError, observe_effects


def complete_all(run):
    for unit in run.snapshot().planned:
        if not run.begin(unit):
            break
        run.complete(unit)
    return run.finish()


class CoreTests(unittest.TestCase):
    def test_ordinary_execution(self):
        result = complete_all(Execution("ordinary", ["one", "two"]))
        self.assertEqual((result.state, result.effect), ("COMPLETED", "NONE"))
        self.assertEqual(result.completed, ("one", "two"))
        self.assertEqual(result.prevented, ())

    def test_received_is_not_worker_cooperation(self):
        run = Execution("job", ["one"])
        receipt = run.request_stop("stop", "job")
        self.assertTrue(receipt.received)
        self.assertTrue(receipt.signal_set)
        self.assertEqual(run.snapshot().state, "RUNNING")
        self.assertEqual(run.snapshot().observed_at, ())

    def test_prevent_before_work(self):
        run = Execution("job", ["one"])
        run.request_stop("stop", "job")
        self.assertFalse(run.begin("one"))
        result = run.finish()
        self.assertEqual(result.effect, "PREVENTED_FUTURE")
        self.assertEqual(result.started, ())
        self.assertEqual(result.prevented, ("one",))

    def test_wrong_target_and_other_instance_unaffected(self):
        first, second = Execution("A", ["one"]), Execution("B", ["one"])
        receipt = first.request_stop("wrong", "B")
        self.assertFalse(receipt.received)
        self.assertEqual(receipt.status, "NOT_RECEIVED")
        self.assertEqual(complete_all(first).effect, "NONE")
        self.assertEqual(complete_all(second).effect, "NONE")

    def test_signal_not_shared_between_instances(self):
        first, second = Execution("A", ["one"]), Execution("B", ["one"])
        first.request_stop("r", "A")
        self.assertEqual(complete_all(first).state, "STOPPED")
        self.assertEqual(complete_all(second).state, "COMPLETED")

    def test_duplicate_is_idempotent(self):
        run = Execution("job", ["one"])
        first = run.request_stop("same", "job")
        second = run.request_stop("same", "job")
        self.assertEqual(first.status, "RECEIVED")
        self.assertEqual(second.status, "DUPLICATE")
        self.assertEqual(complete_all(run).request_ids, ("same",))

    def test_distinct_requests_are_retained(self):
        run = Execution("job", ["one"])
        run.request_stop("a", "job")
        run.request_stop("b", "job")
        self.assertEqual(complete_all(run).request_ids, ("a", "b"))

    def test_active_unit_is_never_reported_prevented(self):
        run = Execution("job", ["one", "two"])
        self.assertTrue(run.begin("one"))
        run.request_stop("stop", "job")
        run.complete("one")
        self.assertFalse(run.begin("two"))
        result = run.finish()
        self.assertEqual(result.completed, ("one",))
        self.assertEqual(result.prevented, ("two",))
        self.assertEqual(result.effect, "INTERRUPTED")
        self.assertTrue(set(result.started).isdisjoint(result.prevented))

    def test_request_during_final_unit_has_no_effect(self):
        run = Execution("job", ["one"])
        run.begin("one")
        run.request_stop("stop", "job")
        run.complete("one")
        result = run.finish()
        self.assertEqual((result.state, result.effect), ("COMPLETED", "NO_EFFECT"))
        self.assertEqual(result.observed_at, ("terminal_boundary",))

    def test_late_request_cannot_rewrite_terminal(self):
        run = Execution("job", ["one"])
        before = complete_all(run)
        late = run.request_stop("late", "job")
        self.assertEqual(late.status, "TOO_LATE")
        self.assertIs(run.finish(), before)
        self.assertEqual(before.request_ids, ())

    def test_snapshot_is_immutable(self):
        result = complete_all(Execution("job", ["one"]))
        with self.assertRaises(FrozenInstanceError):
            result.state = "STOPPED"

    def test_partial_cannot_be_declared_complete(self):
        run = Execution("job", ["one", "two"])
        run.begin("one")
        run.complete("one")
        with self.assertRaises(ContractError):
            run.finish()
        self.assertEqual(run.snapshot().state, "RUNNING")

    def test_out_of_order_and_overlap_rejected(self):
        run = Execution("job", ["one", "two"])
        with self.assertRaises(ContractError):
            run.begin("two")
        run.begin("one")
        with self.assertRaises(ContractError):
            run.begin("two")
        with self.assertRaises(ContractError):
            run.complete("two")

    def test_worker_failure_preserves_unknown_active_work(self):
        run = Execution("job", ["one", "two"])
        run.begin("one")
        result = run.fail("write failed")
        self.assertEqual((result.state, result.effect), ("FAILED", "UNKNOWN"))
        self.assertEqual(result.started, ("one",))
        self.assertEqual(result.completed, ())
        self.assertEqual(result.prevented, ())
        self.assertIn("write failed", result.error)

    def test_signal_read_error_is_not_stop(self):
        class Broken:
            def set(self):
                pass
            def is_set(self):
                raise OSError("read error")
        run = Execution("job", ["one"], signal_factory=Broken)
        run.request_stop("r", "job")
        with self.assertRaises(SignalError):
            run.begin("one")
        self.assertEqual(run.finish().state, "FAILED")
        self.assertEqual(run.finish().effect, "UNKNOWN")

    def test_signal_write_error_is_not_stop(self):
        class Broken:
            def set(self):
                raise OSError("write error")
            def is_set(self):
                return False
        run = Execution("job", ["one"], signal_factory=Broken)
        with self.assertRaises(SignalError):
            run.request_stop("r", "job")
        self.assertEqual(run.finish().state, "FAILED")

    def test_non_boolean_signal_is_error(self):
        class Broken:
            def set(self):
                pass
            def is_set(self):
                return "false"
        run = Execution("job", ["one"], signal_factory=Broken)
        with self.assertRaises(SignalError):
            run.begin("one")
        self.assertEqual(run.finish().effect, "UNKNOWN")

    def test_observation_failure_does_not_confirm_claim(self):
        result = complete_all(Execution("job", ["one"]))
        def broken(_):
            raise OSError("cannot inspect output")
        observation = observe_effects(result, broken)
        self.assertEqual(observation.status, "ERROR")
        self.assertFalse(observation.confirmed)

    def test_mismatch_and_non_boolean_observations(self):
        result = complete_all(Execution("job", ["one"]))
        self.assertEqual(observe_effects(result, lambda _: False).status, "MISMATCH")
        self.assertEqual(observe_effects(result, lambda _: "yes").status, "ERROR")
        self.assertTrue(observe_effects(result, lambda _: True).confirmed)

    def test_observation_before_terminal_rejected(self):
        with self.assertRaises(ContractError):
            observe_effects(Execution("job", ["one"]).snapshot(), lambda _: True)

    def test_empty_or_duplicate_labels_rejected(self):
        for identifier, units in [("", ["a"]), ("job", []),
                                  ("job", ["a", "a"]), ("job", [""])]:
            with self.assertRaises(ContractError):
                Execution(identifier, units)

    def test_concurrent_duplicate_requests_have_single_identity(self):
        run = Execution("job", ["one"])
        barrier = Barrier(5)
        receipts = []
        errors = []
        def ask():
            try:
                barrier.wait(10)
                receipts.append(run.request_stop("same", "job"))
            except Exception as exc:
                errors.append(exc)
        workers = [Thread(target=ask) for _ in range(4)]
        for worker in workers:
            worker.start()
        barrier.wait(10)
        for worker in workers:
            worker.join(10)
        self.assertFalse(any(worker.is_alive() for worker in workers))
        self.assertEqual(errors, [])
        self.assertEqual(sum(r.status == "RECEIVED" for r in receipts), 1)
        self.assertEqual(sum(r.status == "DUPLICATE" for r in receipts), 3)
        self.assertEqual(complete_all(run).request_ids, ("same",))

    def test_execution_identity_is_fixed(self):
        run = Execution("original", ["one"])
        with self.assertRaises(AttributeError):
            run.execution_id = "different"

