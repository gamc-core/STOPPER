"""Run one scenario or all five without installation, network or private data."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
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

TITLES = {
    "E01": "The signal did not reach its target",
    "E02": "Interrupt a copy",
    "E03": "Stop without undoing",
    "E04": "Withhold a result",
    "E05": "Use STOPPER in another operation",
}


def load_example(key):
    path = ROOT / "examples" / SCENARIOS[key] / "example.py"
    spec = importlib.util.spec_from_file_location("stopper_example_" + key, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _count(value):
    return str(len(value)) if isinstance(value, (list, tuple)) else "not recorded"


def format_summary(result):
    """Describe supplied results without changing them or claiming new checks."""
    key = result.get("scenario", "Unknown scenario")
    lines = [key + " - " + TITLES.get(key, "Result"),
             "Recorded result: " + result.get("status", "UNKNOWN")]
    receipt = result.get("receipt")
    if isinstance(receipt, dict):
        lines.append("Stop request: " + receipt.get("status", "UNKNOWN"))
    late = result.get("late_receipt")
    if isinstance(late, dict):
        lines.append("Later request: " + late.get("status", "UNKNOWN"))

    outcomes = result.get("outcomes", {})
    if not outcomes and result.get("status") != "ERROR":
        lines.append("Work: not recorded")
    for name, outcome in outcomes.items():
        lines.append(name.replace("_", " ").capitalize() + ": "
                     + outcome.get("state", "UNKNOWN") + " / "
                     + outcome.get("effect", "UNKNOWN"))
        units = "Files" if name == "copy" else ("Values" if key == "E05" else "Units")
        lines.append("  " + units + " completed: " + _count(outcome.get("completed"))
                     + " of " + _count(outcome.get("planned")))
        lines.append("  Not started: " + _count(outcome.get("not_started"))
                     + "; prevented by stop: " + _count(outcome.get("prevented")))
        lines.append("  Stop requests recorded: " + _count(outcome.get("request_ids")))
        points = outcome.get("observed_at")
        lines.append("  Signal observed: " + (", ".join(points) if points else "none recorded"))

    checks = result.get("checks", {})
    if "change_remains" in checks:
        lines.append("Completed change retained: "
                     + ("confirmed" if checks["change_remains"] is True else "not confirmed"))
    if "delivered" in result:
        lines.append("Presentation: " + ("withheld" if result["delivered"] is None else "delivered"))
    if "underlying_result_preserved" in result:
        value = result["underlying_result_preserved"]
        lines.append("Result file exists: " + ("yes" if value is True else "no" if value is False else "not recorded"))
    for name, label in [("ordinary_values", "Ordinary values"), ("partial_values", "Partial values")]:
        if name in result:
            lines.append(label + ": " + json.dumps(result[name]))

    observation = result.get("physical_observation")
    if isinstance(observation, dict):
        status = observation.get("status", "UNKNOWN")
        lines.append("Local check: " + status)
        if status != "VERIFIED" and observation.get("detail"):
            lines.append("  " + observation["detail"])
    else:
        lines.append("Local check: "
                     + ("not performed" if "physical_observation" in result else "not recorded"))
    failed = [name for name, value in checks.items() if value is not True]
    if failed:
        lines.append("Checks not passed: " + ", ".join(failed))
    if result.get("status") == "ERROR":
        lines.append("Error: " + result.get("error_type", "Unknown error") + ": "
                     + result.get("detail", "No detail recorded"))
    folder = result.get("evidence_directory")
    lines.append("Evidence: " + (folder + "/result.json" if folder else "no saved result reported"))
    return "\n".join(lines)


def main():
    arguments = sys.argv[1:]
    summary = "--summary" in arguments
    selection = [value for value in arguments if value != "--summary"] or ["all"]
    if arguments.count("--summary") > 1 or len(selection) != 1 or selection[0] not in (*SCENARIOS, "all"):
        raise SystemExit("usage: python -I -S -B examples/run.py [E01|E02|E03|E04|E05|all] [--summary]")
    keys = list(SCENARIOS) if selection[0] == "all" else selection
    failed = False
    for key in keys:
        area = workspace(key.lower())
        try:
            result = load_example(key).run(area)
            save_report(area, result)
            result["evidence_directory"] = area.relative_to(ROOT).as_posix()
            print(format_summary(result) if summary else json.dumps(result, sort_keys=True))
            failed = failed or result["status"] != "PASS"
        except Exception as exc:
            error = {"scenario": key, "status": "ERROR",
                     "error_type": type(exc).__name__, "detail": str(exc)}
            print(format_summary(error) if summary else json.dumps(error))
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
