#!/usr/bin/env python3
"""Behavioral checks for bounded handoffs; all writes use temporary fixtures."""

from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("handoff.py").resolve()
spec = importlib.util.spec_from_file_location("handoff", SCRIPT)
handoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handoff)


class HandoffTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="g3-handoff-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.workspace = self.root / "project"
        self.workspace.mkdir()
        self.skill = self.root / "vendor" / "inspect-result"
        self.skill.mkdir(parents=True)
        self.manifest = self.skill / "SKILL.md"
        self.manifest.write_text(
            "---\nname: inspect-result\ndescription: Inspect a local result.\n---\n"
            "Read the result and return measured evidence.\n", encoding="utf-8")
        self.log = self.workspace / "check.log"
        self.log.write_text("Observed expected result: 42\n", encoding="utf-8")
        self.envelope = self.prepare()

    def prepare(self, **changes):
        args = dict(source=self.skill, host="codex", workspace=self.workspace,
                    goal="Produce a correct result", task="Inspect the saved result",
                    acceptance=["The observed result is 42"], discovery_evidence="Fixture host catalog")
        args.update(changes)
        return handoff.prepare(**args)

    def result(self):
        return {
            "handoff_id": self.envelope["contract"]["handoff_id"], "status": "completed",
            "summary": "The saved result satisfies C1.",
            "checks": [{"criterion": "C1", "command": "read the saved result", "exit_code": 0,
                        "log": "check.log", "log_sha256": hashlib.sha256(self.log.read_bytes()).hexdigest()}],
            "artifacts": [], "changes": [], "open_issues": [],
        }

    def test_brief_preserves_goal_and_returns_control(self):
        before = sorted(str(path) for path in self.root.rglob("*"))
        envelope = self.prepare()
        self.assertEqual(envelope["contract"]["goal"], "Produce a correct result")
        self.assertEqual(envelope["contract"]["allowed_writes"], [])
        self.assertIn("return control to g3stack", envelope["prompt"])
        self.assertIn("read-only", envelope["prompt"])
        self.assertEqual(sorted(str(path) for path in self.root.rglob("*")), before)

    def test_completed_evidence_still_requires_independent_review(self):
        result = handoff.check(self.envelope, self.result())
        self.assertEqual(result["status"], "READY_FOR_REVIEW")
        self.assertEqual(result["return_to"], "g3stack")
        self.assertEqual(result["goal_achieved"], "NOT_ESTABLISHED")

    def test_failed_check_cannot_be_reported_completed(self):
        result = self.result()
        result["checks"][0]["exit_code"] = 1
        with self.assertRaisesRegex(handoff.Guard, "failed check"):
            handoff.check(self.envelope, result)

    def test_unrun_criterion_is_not_accepted(self):
        result = self.result()
        result["checks"] = []
        with self.assertRaisesRegex(handoff.Guard, "lacks acceptance evidence"):
            handoff.check(self.envelope, result)

    def test_changed_or_missing_evidence_is_rejected(self):
        result = self.result()
        self.log.write_text("Changed observation\n", encoding="utf-8")
        with self.assertRaisesRegex(handoff.Guard, "Evidence changed"):
            handoff.check(self.envelope, result)
        self.log.unlink()
        with self.assertRaisesRegex(handoff.Guard, "Missing evidence file"):
            handoff.check(self.envelope, result)

    def test_changed_skill_requires_new_handoff(self):
        self.manifest.write_text(self.manifest.read_text() + "Different instructions\n", encoding="utf-8")
        with self.assertRaisesRegex(handoff.Guard, "Skill source changed"):
            handoff.check(self.envelope, self.result())

    def test_manual_only_skill_is_not_selected_implicitly(self):
        self.manifest.write_text(self.manifest.read_text().replace(
            "description: Inspect a local result.",
            "description: Inspect a local result.\ndisable-model-invocation: true # manual"), encoding="utf-8")
        with self.assertRaisesRegex(handoff.Guard, "Manual-only"):
            self.prepare()
        explicit = self.prepare(explicit_invocation=True)
        self.assertTrue(explicit["contract"]["capability"]["explicit_invocation"])

    def test_reported_writes_must_stay_in_authorized_scope(self):
        result = self.result()
        result["changes"] = ["source.py"]
        with self.assertRaisesRegex(handoff.Guard, "outside the allowed scope"):
            handoff.check(self.envelope, result)
        self.envelope = self.prepare(allow_write=["output"])
        result = self.result()
        result["changes"] = ["output/result.json"]
        self.assertEqual(handoff.check(self.envelope, result)["status"], "READY_FOR_REVIEW")
        result["changes"] = ["output-other/result.json"]
        with self.assertRaises(handoff.Guard):
            handoff.check(self.envelope, result)

    def test_paths_cannot_escape_workspace(self):
        outside = self.root / "private.log"
        outside.write_text("outside", encoding="utf-8")
        (self.workspace / "escape").symlink_to(self.root, target_is_directory=True)
        for value in ("../private.log", str(outside), "escape/private.log"):
            with self.subTest(path=value):
                result = self.result()
                result["checks"][0].update(log=value, log_sha256=hashlib.sha256(outside.read_bytes()).hexdigest())
                with self.assertRaises(handoff.Guard):
                    handoff.check(self.envelope, result)
                with self.assertRaises(handoff.Guard):
                    self.prepare(allow_write=[value])

    def test_blocked_and_failed_results_return_open_gap(self):
        for status in ("blocked", "failed"):
            with self.subTest(status=status):
                result = self.result()
                result.update(status=status, checks=[], open_issues=["Required runtime is unavailable"])
                checked = handoff.check(self.envelope, result)
                self.assertEqual(checked["status"], status.upper())
                self.assertEqual(checked["goal_achieved"], "NOT_ESTABLISHED")
                self.assertEqual(checked["return_to"], "g3stack")

    def test_wrong_handoff_and_changed_contract_are_rejected(self):
        result = self.result()
        result["handoff_id"] = "another-task"
        with self.assertRaisesRegex(handoff.Guard, "another handoff"):
            handoff.check(self.envelope, result)
        changed = deepcopy(self.envelope)
        changed["contract"]["goal"] = "A different goal"
        with self.assertRaisesRegex(handoff.Guard, "contract changed"):
            handoff.check(changed, self.result())

    def test_commands_in_results_are_never_executed(self):
        result = self.result()
        sentinel = self.workspace / "should-not-exist"
        result["checks"][0]["command"] = f"touch {sentinel}"
        checked = handoff.check(self.envelope, result)
        self.assertEqual(checked["status"], "READY_FOR_REVIEW")
        self.assertFalse(sentinel.exists())

    def test_unknown_duplicate_and_malformed_checks_are_rejected(self):
        for update in ({"criterion": "C9"}, {"exit_code": True}, {"command": ""}):
            with self.subTest(update=update):
                result = self.result()
                result["checks"][0].update(update)
                with self.assertRaises(handoff.Guard):
                    handoff.check(self.envelope, result)
        result = self.result()
        result["checks"].append(deepcopy(result["checks"][0]))
        with self.assertRaises(handoff.Guard):
            handoff.check(self.envelope, result)

    def test_artifact_contents_are_checked(self):
        result = self.result()
        artifact = self.workspace / "metrics.json"
        artifact.write_text('{"value": 42}\n', encoding="utf-8")
        result["artifacts"] = [{"path": "metrics.json", "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()}]
        self.assertEqual(handoff.check(self.envelope, result)["status"], "READY_FOR_REVIEW")
        artifact.write_text('{"value": 41}\n', encoding="utf-8")
        with self.assertRaisesRegex(handoff.Guard, "Evidence changed"):
            handoff.check(self.envelope, result)

    def test_cli_prepare_check_and_rejection_exit_codes(self):
        environment = dict(os.environ, HOME=str(self.root / "unused-home"))
        def cli(*args):
            return subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                                  env=environment, capture_output=True, text=True, timeout=10)
        prepared = cli("prepare", str(self.skill), "--host", "codex", "--workspace", str(self.workspace),
                       "--goal", "Produce a correct result", "--task", "Inspect the saved result",
                       "--acceptance", "The observed result is 42", "--discovery-evidence", "Fixture host catalog")
        self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
        self.envelope = json.loads(prepared.stdout)
        contract_path = self.workspace / "handoff.json"
        contract_path.write_text(prepared.stdout, encoding="utf-8")
        result_path = self.workspace / "result.json"
        result_path.write_text(json.dumps(self.result()), encoding="utf-8")
        checked = cli("check", str(contract_path), str(result_path))
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["status"], "READY_FOR_REVIEW")
        rejected = self.result()
        rejected["checks"] = []
        result_path.write_text(json.dumps(rejected), encoding="utf-8")
        checked = cli("check", str(contract_path), str(result_path))
        self.assertEqual(checked.returncode, 2)
        self.assertEqual(json.loads(checked.stdout)["status"], "REJECTED")
        blocked = self.result()
        blocked.update(status="blocked", checks=[], open_issues=["Tool unavailable"])
        result_path.write_text(json.dumps(blocked), encoding="utf-8")
        self.assertEqual(cli("check", str(contract_path), str(result_path)).returncode, 1)
        self.assertFalse((self.root / "unused-home").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
