"""Source integrity regressions in disposable fixtures; no provider calls."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("engineering_check", ROOT / "kits/engineering/check.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class SourceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="g3-engineering-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        path = self.root / "fixture/guide.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"retained source\n")
        self.source = path
        self.manifest = {"format": "g3stack-vendored-sources-v1", "sources": {"fixture": {
            "files": [{"path": "fixture/guide.md", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}]}}}
        self.save()

    def save(self):
        (self.root / "source-manifest.json").write_text(json.dumps(self.manifest))

    def test_complete_source_passes(self):
        self.assertEqual(checker.verify(self.root)["status"], "PASS")

    def test_missing_source_fails(self):
        self.source.unlink()
        self.assertEqual(checker.verify(self.root)["status"], "FAIL")

    def test_modified_source_fails(self):
        self.source.write_bytes(b"changed source\n")
        self.assertEqual(checker.verify(self.root)["status"], "FAIL")

    def test_extra_executable_fails(self):
        (self.source.parent / "extra.py").write_text("print('unexpected')\n")
        self.assertEqual(checker.verify(self.root)["status"], "FAIL")

    def test_linked_source_fails(self):
        saved = self.root / "retained.md"
        self.source.rename(saved)
        self.source.symlink_to(saved)
        self.assertEqual(checker.verify(self.root)["status"], "FAIL")

    def test_manifest_cannot_escape_source_root(self):
        for value in ("", "../outside.md", "/tmp/outside.md", "SKILL.md"):
            with self.subTest(value=value):
                self.manifest["sources"]["fixture"]["files"][0]["path"] = value
                self.save()
                with self.assertRaises(ValueError):
                    checker.verify(self.root)

    def test_duplicate_or_empty_manifest_fails(self):
        files = self.manifest["sources"]["fixture"]["files"]
        files.append(dict(files[0]))
        self.save()
        with self.assertRaises(ValueError):
            checker.verify(self.root)
        files.clear()
        self.save()
        with self.assertRaises(ValueError):
            checker.verify(self.root)

    def test_cli_failure_status_is_nonzero(self):
        self.source.unlink()
        run = subprocess.run([sys.executable, "-B", str(ROOT / "kits/engineering/check.py"),
                              "--root", str(self.root)],capture_output=True,text=True,timeout=5)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(json.loads(run.stdout)["status"], "FAIL")

    def test_bundled_sources_match_pinned_manifest(self):
        result = checker.verify(ROOT / "vendor")
        self.assertEqual(result["status"], "PASS", result["errors"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
