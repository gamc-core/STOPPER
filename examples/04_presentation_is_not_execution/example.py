"""E04: local suppression does not stop an indivisible active operation."""
from dataclasses import asdict
from threading import Event
from stopper import Execution, observe_effects
from _support import ActiveGate, coordinate, report, write_new


def run(area):
    target = area / "computed.txt"
    job = Execution("E04-local-operation", ["compute"])
    gate = ActiveGate()
    hidden = Event()

    def worker():
        if job.begin("compute"):
            gate.worker_wait()
            write_new(target, b"local result: 42\n")
            job.complete("compute")
        return job.finish()

    def controller():
        hidden.set()
        return job.request_stop("while-active", "E04-local-operation")

    box = coordinate(job, worker, gate, controller)
    outcome = box["outcome"]
    delivered = None if hidden.is_set() else target.read_text(encoding="utf-8")
    late = job.request_stop("after-terminal", "E04-local-operation")
    observation = observe_effects(
        outcome, lambda result: target.read_bytes() == b"local result: 42\n"
        and result.state == "COMPLETED" and result.completed == ("compute",),
    )
    return report(
        "E04", {"local_work": outcome},
        {"underlying_work_completed": outcome.state == "COMPLETED",
         "request_received_without_prevention": box["receipt"].received and not outcome.prevented,
         "presentation_suppressed": delivered is None,
         "late_request_does_not_rewrite": late.status == "TOO_LATE" and job.finish() is outcome,
         "not_reported_interrupted": outcome.effect == "NO_EFFECT"},
        observation, receipt=asdict(box["receipt"]), late_receipt=asdict(late),
        delivered=delivered, underlying_result_preserved=target.exists(),
        interpretation="Local work completed despite suppression. No provider or remote cancellation is involved.",
    )
