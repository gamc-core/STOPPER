"""E05: a caller-owned arithmetic batch; no copy-example imports."""
from stopper import Execution, observe_effects
from _support import report


def square_batch(values, execution_id, stop_after=None):
    values = list(values)
    job = Execution(execution_id, [f"value-{index}" for index in range(len(values))])
    results = []
    for index, value in enumerate(values):
        unit = f"value-{index}"
        if not job.begin(unit):
            break
        results.append(value * value)
        job.complete(unit)
        if stop_after is not None and len(results) == stop_after:
            job.request_stop("batch-stop", job.execution_id)
    return results, job.finish()


def run(area):
    values = [2, 3, 4, 5, 6]
    control, full = square_batch(values, "E05-control")
    partial, stopped = square_batch(values, "E05-stopped", stop_after=2)
    observation = observe_effects(
        stopped,
        lambda result: partial == [4, 9] and len(partial) == len(result.completed)
        and result.prevented == ("value-2", "value-3", "value-4"),
    )
    return report(
        "E05", {"ordinary": full, "stopped": stopped},
        {"ordinary_batch_complete": control == [4, 9, 16, 25, 36] and full.state == "COMPLETED",
         "stopped_batch_partial": partial == [4, 9] and stopped.state == "STOPPED",
         "completed_values_remain": partial == control[:2]},
        observation, ordinary_values=control, partial_values=partial,
        interpretation="Reuse is this caller-owned loop. It does not depend on the file-copy worker.",
    )
