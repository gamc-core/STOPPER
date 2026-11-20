"""E01: deliver a request to an object whose execution ID does not match."""
from dataclasses import asdict
from stopper import Execution
from _support import report


def run(area):
    first = Execution("E01-A", ["task"])
    second = Execution("E01-B", ["task"])
    receipt = first.request_stop("wrong-route", "E01-B")
    actual = []
    for job in (first, second):
        if job.begin("task"):
            actual.append(job.execution_id)
            job.complete("task")
        job.finish()
    return report(
        "E01", {"A": first.finish(), "B": second.finish()},
        {"not_received": not receipt.received,
         "both_completed": actual == ["E01-A", "E01-B"],
         "no_cooperation_claimed": not first.finish().observed_at,
         "other_execution_unaffected": second.finish().effect == "NONE"},
        receipt=asdict(receipt), actual_operations=actual,
        interpretation="Wrong delivery is not a received-but-ineffective request; see E04.",
    )
