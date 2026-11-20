"""E02: a real, bounded copy cooperates between files."""
from dataclasses import asdict
from stopper import Execution, observe_effects
from _support import ActiveGate, coordinate, copy_one, digest, guarded_directory, report, write_new


def run(area, request_stop=True):
    source = guarded_directory(area / "source")
    destination = guarded_directory(area / "destination")
    names = [f"sample-{index}.txt" for index in range(5)]
    expected_hashes = {}
    for index, name in enumerate(names):
        write_new(source / name, (f"synthetic STOPPER data {index}\n" * 20).encode("ascii"))
        expected_hashes[name] = digest(source / name)
    job = Execution("E02-copy", names)
    gate = ActiveGate()

    def worker():
        for index, name in enumerate(names):
            if not job.begin(name):
                break
            if index == 1:
                gate.worker_wait()
            copy_one(source / name, destination / name)
            job.complete(name)
        return job.finish()

    box = coordinate(job, worker, gate, lambda: job.request_stop("copy-stop", "E02-copy") if request_stop else None)
    outcome = box["outcome"]

    expected = names[:2] if request_stop else names

    def check_files(observed):
        actual = sorted(path.name for path in destination.iterdir())
        return (
            actual == sorted(observed.completed)
            and actual == expected
            and all(digest(destination / name) == expected_hashes[name] for name in actual)
            and all(digest(source / name) == expected_hashes[name] for name in names)
            and not any((destination / name).exists() for name in observed.prevented)
        )
    observation = observe_effects(outcome, check_files)
    return report(
        "E02", {"copy": outcome},
        {"expected_terminal": outcome.state == ("STOPPED" if request_stop else "COMPLETED"),
         "completed_units_match": outcome.completed == tuple(expected),
         "future_files_match": outcome.prevented == (tuple(names[2:]) if request_stop else ())},
        observation, receipt=asdict(box["receipt"]) if box["receipt"] else None,
        actual_files=sorted(path.name for path in destination.iterdir()),
        source_sha256=expected_hashes,
        interpretation=("Stop was requested inside the second active unit; it finished. The next three never started."
                        if request_stop else "The same copy completed all five files without a stop request."),
    )
