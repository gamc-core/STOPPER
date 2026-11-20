"""Run one scenario or all five without installation, network or private data."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).absolute().parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "examples")]
from _support import save_report, workspace

SCENARIOS = {
    "E01": "01_signal_not_received",
    "E02": "02_interrupt_copy",
    "E03": "03_stop_is_not_undo",
    "E04": "04_presentation_is_not_execution",
    "E05": "05_independent_reuse",
}


def load_example(key):
    path = ROOT / "examples" / SCENARIOS[key] / "example.py"
    spec = importlib.util.spec_from_file_location("stopper_example_" + key, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    selection = sys.argv[1:] or ["all"]
    if len(selection) != 1 or selection[0] not in (*SCENARIOS, "all"):
        raise SystemExit("usage: python -I -S -B examples/run.py [E01|E02|E03|E04|E05|all]")
    keys = list(SCENARIOS) if selection[0] == "all" else selection
    failed = False
    for key in keys:
        area = workspace(key.lower())
        try:
            result = load_example(key).run(area)
            save_report(area, result)
            result["evidence_directory"] = area.relative_to(ROOT).as_posix()
            print(json.dumps(result, sort_keys=True))
            failed = failed or result["status"] != "PASS"
        except Exception as exc:
            print(json.dumps({"scenario": key, "status": "ERROR",
                              "error_type": type(exc).__name__, "detail": str(exc)}))
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
