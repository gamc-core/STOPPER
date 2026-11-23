"""Real NTFS links are confined to disposable synthetic checkouts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from _support import guarded_directory, workspace, write_new

ROOT = Path(__file__).resolve().parents[1]

class CheckoutPathTests(unittest.TestCase):
    def junction(self, alias, target):
        command = [os.environ["COMSPEC"], "/d", "/c", "mklink", "/J", str(alias), str(target)]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertTrue(alias.lstat().st_file_attributes & 0x400)
        self.assertEqual(alias.resolve(), target.resolve())
        def unlink_only():
            if alias.exists():
                self.assertTrue(alias.lstat().st_file_attributes & 0x400)
                self.assertEqual(alias.resolve(), target.resolve())
                alias.rmdir()
        self.addCleanup(unlink_only)

    @unittest.skipUnless(os.name == "nt", "real NTFS junction regression")
    def test_legitimate_checkout_junction_runs_both_presentations(self):
        area = workspace("test-checkout-entry")
        checkout = area / "synthetic checkout"
        checkout.mkdir()
        for name in ("src/stopper/__init__.py", "src/stopper/core.py",
                     "examples/_support.py", "examples/run.py",
                     "examples/01_signal_not_received/example.py"):
            target = checkout / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        alias = area / "entry link"
        self.junction(alias, checkout)
        for mode in ([], ["--summary"]):
            with self.subTest(mode=mode):
                command = [sys.executable, "-I", "-S", "-B", str(alias / "examples/run.py"), "E01", *mode]
                completed = subprocess.run(command, cwd=alias, capture_output=True, text=True, timeout=20)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                if mode:
                    self.assertIn("Recorded result: PASS", completed.stdout)
                else:
                    result = json.loads(completed.stdout)
                    self.assertEqual(result["status"], "PASS")
                    self.assertTrue((checkout / result["evidence_directory"] / "result.json").is_file())
        self.assertEqual(len(list((checkout / ".runs").glob("e01-*/result.json"))), 2)

    @unittest.skipUnless(os.name == "nt", "real NTFS junction regression")
    def test_output_junction_remains_rejected(self):
        area = workspace("test-output-junction")
        target = area / "target"
        target.mkdir()
        alias = area / "output link"
        self.junction(alias, target)
        with self.assertRaises(ValueError):
            write_new(alias / "never-created.txt", b"forbidden")
        self.assertEqual(list(target.iterdir()), [])

    def test_external_directory_and_existing_destination_remain_rejected(self):
        with patch.object(Path, "mkdir") as mkdir:
            with self.assertRaises(ValueError):
                guarded_directory(ROOT.parent / "outside-checkout-never-create")
            mkdir.assert_not_called()
        area = workspace("test-exclusive-again")
        target = area / "existing.txt"
        write_new(target, b"original")
        with self.assertRaises(FileExistsError):
            write_new(target, b"replacement")
        self.assertEqual(target.read_bytes(), b"original")
