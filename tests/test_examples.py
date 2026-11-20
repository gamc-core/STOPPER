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
