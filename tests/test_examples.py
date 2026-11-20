import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).absolute().parents[1]
from _support import copy_one, workspace, write_new


def scenario(key):
    spec = importlib.util.spec_from_file_location("example_driver", ROOT / "examples/run.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver.load_example(key)


class FileExampleTests(unittest.TestCase):
    def test_signal_not_received(self):
        result = scenario("E01").run(workspace("test-e01"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["receipt"]["status"], "NOT_RECEIVED")

    def test_copy_report_matches_actual_files(self):
        area = workspace("test-e02")
        result = scenario("E02").run(area)
        self.assertEqual(result["status"], "PASS")
        actual = sorted(p.name for p in (area / "destination").iterdir())
        self.assertEqual(actual, ["sample-0.txt", "sample-1.txt"])
        self.assertEqual(result["outcomes"]["copy"]["completed"], tuple(actual))
        self.assertEqual(result["physical_observation"]["status"], "VERIFIED")

    def test_copy_control_without_stop(self):
        from stopper import Execution
        area = workspace("test-control")
        source, destination = area / "in.txt", area / "out.txt"
        write_new(source, b"ordinary copy control")
        job = Execution("control", ["copy"])
        self.assertTrue(job.begin("copy"))
        copy_one(source, destination)
        job.complete("copy")
        self.assertEqual(job.finish().state, "COMPLETED")
        self.assertEqual(source.read_bytes(), destination.read_bytes())

    def test_existing_destination_is_not_overwritten(self):
        area = workspace("test-exclusive")
        source, destination = area / "in.txt", area / "out.txt"
        write_new(source, b"new")
        write_new(destination, b"existing")
        with self.assertRaises(FileExistsError):
            copy_one(source, destination)
        self.assertEqual(destination.read_bytes(), b"existing")

    def test_parent_traversal_is_rejected_before_mkdir(self):
        from unittest.mock import patch
        from _support import guarded_directory
        with patch.object(Path, "mkdir") as mkdir:
            with self.assertRaises(ValueError):
                guarded_directory(ROOT / ".runs" / ".." / ".." / "never-create")
            mkdir.assert_not_called()

    def test_reparse_flag_is_rejected(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from _support import reject_link
        with patch.object(Path, "lstat", return_value=SimpleNamespace(st_file_attributes=0x400)):
            with patch.object(Path, "is_symlink", return_value=False):
                with self.assertRaises(ValueError):
                    reject_link(ROOT / "not-opened")

    def test_same_copy_without_request_completes_all_files(self):
        area = workspace("test-e02-control")
        result = scenario("E02").run(area, request_stop=False)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(list((area / "destination").iterdir())), 5)
        self.assertEqual(result["outcomes"]["copy"]["effect"], "NONE")

    def test_stop_does_not_undo_physical_change(self):
        area = workspace("test-e03")
        result = scenario("E03").run(area)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual((area / "synthetic.txt").read_bytes(), b"after\n")
        self.assertFalse((area / "validation-started.txt").exists())

    def test_presentation_suppression_keeps_computed_result(self):
        area = workspace("test-e04")
        result = scenario("E04").run(area)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual((area / "computed.txt").read_bytes(), b"local result: 42\n")
        self.assertIsNone(result["delivered"])
        self.assertEqual(result["outcomes"]["local_work"]["effect"], "NO_EFFECT")

    def test_independent_reuse_and_ordinary_control(self):
        result = scenario("E05").run(workspace("test-e05"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["partial_values"], [4, 9])
        self.assertEqual(result["ordinary_values"], [4, 9, 16, 25, 36])

    def test_physical_mismatch_is_not_confirmed(self):
        from stopper import Execution, observe_effects
        area = workspace("test-physical-mismatch")
        output = area / "result.txt"
        write_new(output, b"unexpected bytes")
        job = Execution("check", ["write"])
        job.begin("write")
        job.complete("write")
        observation = observe_effects(job.finish(), lambda _: output.read_bytes() == b"expected bytes")
        self.assertEqual(observation.status, "MISMATCH")
        self.assertFalse(observation.confirmed)
