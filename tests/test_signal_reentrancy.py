"""Signal callbacks may observe snapshots but cannot mutate their execution."""
import unittest
from stopper import ContractError, Execution, SignalError

class CallbackSignal:
    def __init__(self):
        self.read_callback = None
        self.set_callback = None
        self.pending = False
    def set(self):
        callback, self.set_callback = self.set_callback, None
        if callback:
            callback()
        self.pending = True
    def is_set(self):
        callback, self.read_callback = self.read_callback, None
        if callback:
            callback()
        return self.pending

class SignalReentrancyTests(unittest.TestCase):
    def make_run(self, units=("u1", "u2", "u3")):
        signal = CallbackSignal()
        return Execution("e", units, signal_factory=lambda: signal), signal

    def assert_accounted(self, outcome):
        self.assertEqual(len(outcome.started), len(set(outcome.started)))
        self.assertTrue(set(outcome.started).isdisjoint(outcome.not_started))
        self.assertEqual(set(outcome.started) | set(outcome.not_started), set(outcome.planned))

    def test_read_callback_cannot_duplicate_the_next_unit(self):
        run, signal = self.make_run()
        signal.read_callback = lambda: run.begin("u1")
        with self.assertRaises(SignalError):
            run.begin("u1")
        terminal = run.finish()
        self.assertEqual((terminal.state, terminal.effect), ("FAILED", "UNKNOWN"))
        self.assertEqual(terminal.started, ())
        self.assertEqual(terminal.not_started, ("u1", "u2", "u3"))
        self.assert_accounted(terminal)
        self.assertFalse(run.begin("u1"))
        self.assertIs(run.finish(), terminal)

    def test_read_callback_rejects_each_mutating_operation(self):
        callbacks = {
            "begin": lambda run: run.begin("u1"),
            "complete": lambda run: run.complete("u1"),
            "request_stop": lambda run: run.request_stop("nested", "e"),
            "finish": lambda run: run.finish(),
            "fail": lambda run: run.fail("nested"),
        }
        for name, callback in callbacks.items():
            with self.subTest(operation=name):
                run, signal = self.make_run()
                signal.read_callback = lambda: callback(run)
                with self.assertRaises(SignalError):
                    run.begin("u1")
                terminal = run.finish()
                self.assertEqual(terminal.state, "FAILED")
                self.assertEqual(terminal.started, ())
                self.assert_accounted(terminal)

    def test_set_callback_cannot_complete_active_work(self):
        run, signal = self.make_run()
        self.assertTrue(run.begin("u1"))
        signal.set_callback = lambda: run.complete("u1")
        with self.assertRaises(SignalError):
            run.request_stop("outer", "e")
        terminal = run.finish()
        self.assertEqual((terminal.state, terminal.effect), ("FAILED", "UNKNOWN"))
        self.assertEqual(terminal.started, ("u1",))
        self.assertEqual(terminal.completed, ())
        self.assertEqual(terminal.request_ids, ("outer",))
        self.assert_accounted(terminal)

    def test_caught_reentrant_attempt_leaves_one_start_and_releases_guard(self):
        run, signal = self.make_run()
        rejected = []
        def callback():
            try:
                run.begin("u1")
            except ContractError:
                rejected.append(True)
        signal.read_callback = callback
        self.assertTrue(run.begin("u1"))
        self.assertEqual(rejected, [True])
        self.assertEqual(run.snapshot().started, ("u1",))
        run.complete("u1")
        for unit in ("u2", "u3"):
            self.assertTrue(run.begin(unit))
            run.complete(unit)
        self.assertEqual(run.finish().state, "COMPLETED")

    def test_signal_callback_may_read_a_snapshot(self):
        run, signal = self.make_run(("u1",))
        seen = []
        signal.read_callback = lambda: seen.append(run.snapshot())
        self.assertTrue(run.begin("u1"))
        self.assertEqual(seen[0].started, ())
        run.complete("u1")
        self.assertEqual(run.finish().state, "COMPLETED")

    def test_finish_callback_cannot_replace_a_terminal_transition(self):
        run, signal = self.make_run(("u1",))
        run.begin("u1")
        run.complete("u1")
        signal.read_callback = lambda: run.fail("nested")
        with self.assertRaises(SignalError):
            run.finish()
        terminal = run.finish()
        self.assertEqual((terminal.state, terminal.effect), ("FAILED", "UNKNOWN"))
        self.assertEqual(terminal.completed, ("u1",))
        self.assertIs(run.fail("later"), terminal)
