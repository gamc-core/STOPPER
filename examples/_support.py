"""Shared coordination and bounded synthetic workspace helpers."""
from dataclasses import asdict
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
from threading import Event, Thread

PROJECT = Path(__file__).absolute().parents[1]
REPARSE = 0x400


def reject_link(path):
    info = path.lstat()
    if path.is_symlink() or getattr(info, "st_file_attributes", 0) & REPARSE:
        raise ValueError("linked/reparse paths are not example workspaces")


def guarded_directory(path):
    path = Path(path).absolute()
    path.relative_to(PROJECT)
    current = path
    while True:
        if current.exists() or current.is_symlink():
            reject_link(current)
        if current == PROJECT:
            break
        current = current.parent
    path.mkdir(parents=True, exist_ok=True)
    reject_link(path)
    if not path.is_dir():
        raise ValueError("expected a directory")
    return path


def workspace(label):
    root = guarded_directory(PROJECT / ".runs")
    return Path(tempfile.mkdtemp(prefix=label + "-", dir=str(root)))


def write_new(path, content):
    path = Path(path)
    guarded_directory(path.parent)
    with path.open("xb") as stream:
        stream.write(content)


def copy_one(source, destination):
    source, destination = Path(source), Path(destination)
    source.relative_to(PROJECT)
    reject_link(source)
    guarded_directory(destination.parent)
    # Exclusive creation prevents accidental replacement of an existing file.
    with source.open("rb") as incoming, destination.open("xb") as outgoing:
        while True:
            block = incoming.read(65536)
            if not block:
                break
            outgoing.write(block)


def digest(path):
    reject_link(path)
    return sha256(path.read_bytes()).hexdigest()


class ActiveGate:
    """A declared test checkpoint, not a timing-based stop guarantee."""
    def __init__(self):
        self.active = Event()
        self.release = Event()

    def worker_wait(self):
        self.active.set()
        if not self.release.wait(10):
            raise RuntimeError("controller did not release the active checkpoint")

    def wait_active(self):
        if not self.active.wait(10):
            raise RuntimeError("worker did not reach its active checkpoint")


def coordinate(run, worker, gate, controller):
    box = {}
    def target():
        try:
            box["outcome"] = worker()
        except Exception as exc:
            box["error"] = type(exc).__name__ + ": " + str(exc)
            box["outcome"] = run.fail(box["error"])
    thread = Thread(target=target, name="stopper-example-worker", daemon=True)
    thread.start()
    try:
        gate.wait_active()
        box["receipt"] = controller()
    finally:
        gate.release.set()
        thread.join(10)
    if thread.is_alive():
        raise RuntimeError("worker did not settle; no successful stop is claimed")
    if "error" in box:
        raise RuntimeError(box["error"])
    return box


def report(name, outcomes, checks, observation=None, **facts):
    checks = dict(checks)
    if observation is not None:
        checks["physical_observation_confirmed"] = observation.confirmed
    return {
        "scenario": name,
        "status": "PASS" if checks and all(value is True for value in checks.values()) else "FAIL",
        "outcomes": {key: value.to_dict() for key, value in outcomes.items()},
        "checks": checks,
        "physical_observation": observation.to_dict() if observation else None,
        **facts,
    }


def save_report(folder, result):
    write_new(folder / "result.json", (json.dumps(result, indent=2) + "\n").encode("utf-8"))
