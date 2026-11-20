"""E03: a completed synthetic modification remains after stop."""
from dataclasses import asdict
from stopper import Execution, observe_effects
from _support import ActiveGate, coordinate, digest, report, write_new


def run(area):
    target = area / "synthetic.txt"
    marker = area / "validation-started.txt"
    write_new(target, b"before\n")
    before = digest(target)
    job = Execution("E03-phases", ["modify", "validate"])
    gate = ActiveGate()

    def worker():
        if job.begin("modify"):
            target.write_bytes(b"after\n")  # Only this newly created synthetic file.
            job.complete("modify")
        gate.worker_wait()
        if job.begin("validate"):
            write_new(marker, b"validation started\n")
            job.complete("validate")
        return job.finish()

    box = coordinate(job, worker, gate, lambda: job.request_stop("phase-stop", "E03-phases"))
    outcome = box["outcome"]
    observation = observe_effects(
        outcome,
        lambda result: target.read_bytes() == b"after\n" and not marker.exists()
        and result.completed == ("modify",) and result.prevented == ("validate",),
    )
    return report(
        "E03", {"phases": outcome},
        {"change_remains": digest(target) != before,
         "validation_not_started": not marker.exists(),
         "partial_not_complete": outcome.state == "STOPPED"},
        observation, receipt=asdict(box["receipt"]), before_sha256=before,
        after_sha256=digest(target),
        interpretation="The completed modification remains. STOPPER did not roll it back.",
    )
