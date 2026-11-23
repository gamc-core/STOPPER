"""Presentation tests use current synthetic scenarios, never private records."""
import copy
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from _support import save_report, workspace

ROOT = Path(__file__).absolute().parents[1]


def load_driver():
    spec = importlib.util.spec_from_file_location(
        "stopper_presentation_driver", ROOT / "examples/run.py"
    )
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = load_driver()
        cls.raw = {}
        cls.display = {}
        for key in cls.driver.SCENARIOS:
            area = workspace("test-presentation-" + key.lower())
            result = cls.driver.load_example(key).run(area)
            if result["status"] != "PASS":
                raise AssertionError("synthetic scenario failed: " + key)
            save_report(area, result)
            cls.raw[key] = copy.deepcopy(result)
            cls.display[key] = {
                **result, "evidence_directory": area.relative_to(ROOT).as_posix()
            }

    def sample(self, key="E02"):
        return copy.deepcopy(self.display[key])

    def cli(self, args, records=None, error=None, area=None, save_error=None):
        areas = []
        records = self.raw if records is None else records

        def new_area(_):
            chosen = area if area is not None else workspace("test-cli")
            areas.append(chosen)
            return chosen

        def load(key):
            if error:
                raise error
            return SimpleNamespace(run=lambda _: copy.deepcopy(records[key]))

        out = io.StringIO()
        with patch.object(self.driver.sys, "argv", ["examples/run.py", *args]):
            with patch.object(self.driver, "workspace", side_effect=new_area):
                with patch.object(self.driver, "load_example", side_effect=load):
                    with patch.object(self.driver, "save_report",
                                      side_effect=save_error if save_error else save_report):
                        with redirect_stdout(out):
                            exit_code = self.driver.main()
        return exit_code, out.getvalue(), areas

    def test_all_five_have_their_heading_and_real_outcome(self):
        for key, result in self.display.items():
            with self.subTest(key=key):
                text = self.driver.format_summary(copy.deepcopy(result))
                self.assertTrue(text.startswith(key + " - " + self.driver.TITLES[key]))
                self.assertIn("Recorded result: " + result["status"], text)
                for outcome in result["outcomes"].values():
                    self.assertIn(outcome["state"] + " / " + outcome["effect"], text)

    def test_copy_counts_are_read_from_data(self):
        result = self.sample()
        result["outcomes"]["copy"].update(
            planned=["a", "b", "c", "d"], completed=["a"],
            not_started=["b", "c", "d"], prevented=["c", "d"],
        )
        text = self.driver.format_summary(result)
        self.assertIn("Files completed: 1 of 4", text)
        self.assertIn("Not started: 3; prevented by stop: 2", text)

    def test_received_is_not_reported_as_interruption(self):
        text = self.driver.format_summary(self.sample("E04"))
        self.assertIn("Stop request: RECEIVED", text)
        self.assertIn("COMPLETED / NO_EFFECT", text)
        self.assertIn("Presentation: withheld", text)
        self.assertIn("Result file exists: yes", text)
        self.assertIn("Later request: TOO_LATE", text)
        self.assertNotIn("INTERRUPTED", text)

    def test_wrong_target_and_unperformed_check_are_distinct(self):
        text = self.driver.format_summary(self.sample("E01"))
        self.assertIn("Stop request: NOT_RECEIVED", text)
        self.assertIn("Local check: not performed", text)
        self.assertIn("Signal observed: none recorded", text)

    def test_retained_change_and_reused_values_are_visible(self):
        self.assertIn("Completed change retained: confirmed",
                      self.driver.format_summary(self.sample("E03")))
        reuse = self.driver.format_summary(self.sample("E05"))
        self.assertIn("Ordinary values: [4, 9, 16, 25, 36]", reuse)
        self.assertIn("Partial values: [4, 9]", reuse)

    def test_mismatch_and_error_are_never_shown_as_verified(self):
        for state in ("MISMATCH", "ERROR"):
            with self.subTest(state=state):
                result = self.sample()
                result["status"] = "FAIL"
                result["physical_observation"] = {
                    "status": state, "detail": "controlled observation problem"
                }
                result["checks"]["physical_observation_confirmed"] = False
                text = self.driver.format_summary(result)
                self.assertIn("Recorded result: FAIL", text)
                self.assertIn("Local check: " + state, text)
                self.assertIn("controlled observation problem", text)
                self.assertIn("Checks not passed: physical_observation_confirmed", text)
                self.assertNotIn("VERIFIED", text)

    def test_missing_data_is_not_default_success(self):
        text = self.driver.format_summary({"scenario": "E02"})
        self.assertIn("Recorded result: UNKNOWN", text)
        self.assertIn("Work: not recorded", text)
        self.assertIn("Local check: not recorded", text)
        self.assertIn("Evidence: no saved result reported", text)
        self.assertNotIn("PASS", text)

    def test_formatter_does_not_mutate_record_or_saved_bytes(self):
        result = self.sample()
        expected = copy.deepcopy(result)
        path = ROOT / result["evidence_directory"] / "result.json"
        before = path.read_bytes()
        self.driver.format_summary(result)
        self.assertEqual(result, expected)
        self.assertEqual(path.read_bytes(), before)

    def test_default_json_serialization_and_saved_shape_are_unchanged(self):
        status, output, areas = self.cli(["E02"])
        self.assertEqual(status, 0)
        expected_saved = self.raw["E02"]
        self.assertEqual(
            (areas[0] / "result.json").read_bytes(),
            (json.dumps(expected_saved, indent=2) + "\n").encode("utf-8"),
        )
        expected_stdout = {
            **expected_saved, "evidence_directory": areas[0].relative_to(ROOT).as_posix()
        }
        self.assertEqual(output, json.dumps(expected_stdout, sort_keys=True) + "\n")
        self.assertNotIn("evidence_directory",
                         json.loads((areas[0] / "result.json").read_text(encoding="utf-8")))

    def test_summary_mode_preserves_full_result_json(self):
        status, output, areas = self.cli(["E02", "--summary"])
        self.assertEqual(status, 0)
        self.assertIn("Files completed: 2 of 5", output)
        self.assertIn(areas[0].relative_to(ROOT).as_posix() + "/result.json", output)
        self.assertEqual(
            (areas[0] / "result.json").read_bytes(),
            (json.dumps(self.raw["E02"], indent=2) + "\n").encode("utf-8"),
        )

    def test_default_without_arguments_still_prints_five_json_lines(self):
        status, output, _ = self.cli([])
        rows = [json.loads(line) for line in output.splitlines()]
        self.assertEqual(status, 0)
        self.assertEqual([row["scenario"] for row in rows], list(self.driver.SCENARIOS))

    def test_all_summaries_and_flag_order(self):
        status, output, _ = self.cli(["all", "--summary"])
        self.assertEqual(status, 0)
        self.assertEqual(output.count("Recorded result: PASS"), 5)
        status, output, _ = self.cli(["--summary", "E02"])
        self.assertEqual(status, 0)
        self.assertTrue(output.startswith("E02 - "))

    def test_failed_result_keeps_failure_exit_in_both_modes(self):
        records = copy.deepcopy(self.raw)
        records["E02"]["status"] = "FAIL"
        records["E02"]["checks"]["completed_units_match"] = False
        for args in (["E02"], ["E02", "--summary"]):
            with self.subTest(args=args):
                status, output, areas = self.cli(args, records=records)
                self.assertEqual(status, 1)
                self.assertEqual(
                    json.loads((areas[0] / "result.json").read_text(encoding="utf-8")),
                    json.loads(json.dumps(records["E02"])),
                )
                if "--summary" in args:
                    self.assertIn("Recorded result: FAIL", output)
                    self.assertIn("completed_units_match", output)
                else:
                    self.assertEqual(json.loads(output)["status"], "FAIL")

    def test_exception_json_keeps_original_error_fields(self):
        status, output, areas = self.cli(["E02"], error=RuntimeError("controlled failure"))
        self.assertEqual(status, 1)
        self.assertEqual(json.loads(output), {
            "scenario": "E02", "status": "ERROR",
            "error_type": "RuntimeError", "detail": "controlled failure",
        })
        self.assertFalse((areas[0] / "result.json").exists())

    def test_exception_summary_reports_error_without_claiming_evidence(self):
        status, output, _ = self.cli(
            ["E02", "--summary"], error=RuntimeError("controlled failure")
        )
        self.assertEqual(status, 1)
        self.assertIn("Recorded result: ERROR", output)
        self.assertIn("RuntimeError: controlled failure", output)
        self.assertIn("Evidence: no saved result reported", output)

    def test_save_failure_has_no_successful_summary(self):
        status, output, _ = self.cli(
            ["E02", "--summary"], save_error=OSError("controlled save error")
        )
        self.assertEqual(status, 1)
        self.assertIn("Recorded result: ERROR", output)
        self.assertIn("controlled save error", output)
        self.assertNotIn("Local check: VERIFIED", output)

    def test_existing_evidence_is_not_overwritten(self):
        area = workspace("test-cli-existing")
        path = area / "result.json"
        path.write_bytes(b"pre-existing synthetic evidence")
        status, output, _ = self.cli(["E02", "--summary"], area=area)
        self.assertEqual(status, 1)
        self.assertIn("FileExistsError", output)
        self.assertEqual(path.read_bytes(), b"pre-existing synthetic evidence")

    def test_invalid_arguments_fail_before_running(self):
        for args in (["E02", "E03"], ["--unknown"], ["E02", "--summary", "--summary"]):
            with self.subTest(args=args):
                with self.assertRaises(SystemExit):
                    self.cli(args)

    def test_workspace_failure_does_not_print_a_success(self):
        output = io.StringIO()
        with patch.object(self.driver.sys, "argv", ["examples/run.py", "E02", "--summary"]):
            with patch.object(self.driver, "workspace", side_effect=OSError("workspace denied")):
                with redirect_stdout(output):
                    with self.assertRaises(OSError):
                        self.driver.main()
        self.assertEqual(output.getvalue(), "")
