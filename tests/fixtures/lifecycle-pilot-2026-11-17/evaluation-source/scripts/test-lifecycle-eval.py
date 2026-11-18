#!/usr/bin/env python3
"""Validate the lifecycle fixture and independent scorer without model calls."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("lifecycle-eval.py").resolve()
spec = importlib.util.spec_from_file_location("lifecycle_eval", SCRIPT)
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)

REFERENCE = '''import csv, json, sys
def main():
    groups = {}
    with open(sys.argv[1], encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"group", "passed", "total"} <= set(reader.fieldnames or []):
            raise ValueError("missing columns")
        for row in reader:
            group = row["group"]
            passed, total = int(row["passed"]), int(row["total"])
            if not group or total <= 0 or passed < 0 or passed > total:
                raise ValueError("invalid row")
            result = groups.setdefault(group, {"passed": 0, "total": 0})
            result["passed"] += passed
            result["total"] += total
    if not groups:
        raise ValueError("empty dataset")
    for value in groups.values():
        value["rate"] = value["passed"] / value["total"]
    print(json.dumps({"groups": groups}))
try:
    main()
except (ValueError, OSError, KeyError) as error:
    print(str(error), file=sys.stderr)
    sys.exit(2)
'''


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="g3-lifecycle-test-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.run = self.base / "candidate"
        evaluation.prepare(self.run)
        self.workspace = self.run / "project"

    def completed_fixture(self, implementation=REFERENCE):
        (self.workspace/"report.py").write_text(implementation, encoding="utf-8")
        (self.workspace/"evidence").mkdir()
        (self.workspace/"evidence/premise.log").write_text(
            "Unequal batches: mean(9/10,1/100)=0.455, pooled=10/110. A1 is false.\n", encoding="utf-8")
        state = json.loads((self.workspace/"PROJECT_STATE.json").read_text())
        state["assumptions"][0].update(status="REJECTED", evidence=["evidence/premise.log"])
        state["decisions"][0]["status"] = "SUPERSEDED"
        state["decisions"].append({"id": "D1", "approach": "Sum counts before dividing"})
        evaluation.save(self.workspace/"PROJECT_STATE.json", state)
        # Synthetic event fixtures test the scorer, not actual model invocation.
        events = [
            {"type": "item.completed", "item": {"type": "command_execution", "command": "python3 -B acceptance.py",
             "status": "completed", "exit_code": 0, "aggregated_output": "PASS public acceptance"}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": "cat .g3stack/kits/pstack/upstream/prove-it-works.md",
             "status": "completed", "exit_code": 0, "aggregated_output": "Verify every output by checking the real thing directly."}},
        ]
        (self.run/"events.jsonl").write_text("\n".join(json.dumps(item) for item in events) + "\n", encoding="utf-8")
        evaluation.save(self.run/"last-message.json", {"status": "completed", "summary": "fixture", "owner_decisions": []})
        evaluation.save(self.run/"run.json", {"exit_code": 0, "timed_out": False, "kind": "scorer unit fixture; no model called"})

    def test_prepare_preserves_prior_evidence_and_source(self):
        original = (self.workspace/"RESEARCH.md").read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            evaluation.prepare(self.run)
        self.assertEqual((self.workspace/"RESEARCH.md").read_bytes(), original)
        compile((self.workspace/"acceptance.py").read_bytes(), "acceptance.py", "exec")
        self.assertFalse((self.workspace/"report.py").exists())

    def test_baseline_and_candidate_differ_only_in_selected_instruction(self):
        baseline = self.base/"baseline"
        evaluation.prepare(baseline, "baseline")
        one = json.loads((self.run/"manifest.json").read_text())["protected"]
        two = json.loads((baseline/"manifest.json").read_text())["protected"]
        self.assertEqual({k:v for k,v in one.items() if k != "AGENTS.md"},
                         {k:v for k,v in two.items() if k != "AGENTS.md"})
        self.assertNotEqual(one["AGENTS.md"], two["AGENTS.md"])
        self.assertEqual((baseline/"project/PROJECT_STATE.json").read_bytes(),
                         (self.workspace/"PROJECT_STATE.json").read_bytes())

    def test_scorer_accepts_correct_artifact_and_complete_receipts(self):
        self.completed_fixture()
        report = evaluation.score(self.run)
        self.assertEqual(report["status"], "PASS", report["checks"])
        self.assertEqual(len(json.loads((self.run/"oracle-receipts.json").read_text())), 12)

    def test_scorer_rejects_incorrect_premise_even_with_success_report(self):
        bad = REFERENCE.replace('result["total"] += total',
            'result["total"] += total\n            result.setdefault("rates", []).append(passed/total)')
        bad = bad.replace('value["rate"] = value["passed"] / value["total"]',
                          'value["rate"] = sum(value["rates"]) / len(value["rates"])')
        self.completed_fixture(bad)
        report = evaluation.score(self.run)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(next(item for item in report["checks"] if item["name"] == "cli_unequal")["passed"])

    def test_artifact_pass_does_not_establish_agent_execution(self):
        self.completed_fixture()
        (self.run/"events.jsonl").write_text("", encoding="utf-8")
        report = evaluation.score(self.run)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(next(item for item in report["checks"] if item["name"] == "public_acceptance_executed")["passed"])

    def test_source_or_goal_drift_is_not_accepted(self):
        self.completed_fixture()
        (self.workspace/"RESEARCH.md").write_text("silently rewritten", encoding="utf-8")
        state = json.loads((self.workspace/"PROJECT_STATE.json").read_text())
        state["goal"] = "Only report a typical batch"
        evaluation.save(self.workspace/"PROJECT_STATE.json", state)
        report = evaluation.score(self.run)
        failed = {item["name"] for item in report["checks"] if not item["passed"]}
        self.assertIn("protected_inputs_unchanged", failed)
        self.assertIn("goal_preserved", failed)

    def test_public_acceptance_exercises_real_cli(self):
        (self.workspace/"report.py").write_text(REFERENCE, encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", "acceptance.py"], cwd=self.workspace,
                             capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        (self.workspace/"report.py").write_text('print("{}")\n', encoding="utf-8")
        failed = subprocess.run([sys.executable, "-B", "acceptance.py"], cwd=self.workspace,
                                capture_output=True, text=True, timeout=10)
        self.assertNotEqual(failed.returncode, 0)

    def test_live_run_requires_authorization_and_bounded_deadline(self):
        with self.assertRaisesRegex(ValueError, "approved"):
            evaluation.run_agent(self.run, 300, False)
        for limit in (0, 301):
            with self.assertRaisesRegex(ValueError, "deadline"):
                evaluation.run_agent(self.run, limit, True)
        self.assertFalse((self.run/"run.json").exists())

    def test_imported_pstack_sources_match_pinned_git_objects(self):
        root = evaluation.ROOT/"kits/pstack"
        manifest = json.loads((root/"provenance.json").read_text())
        self.assertEqual(manifest["license"], "MIT")
        for name, record in manifest["files"].items():
            data = (root/name).read_bytes()
            git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            self.assertEqual(git_blob, record["git_blob_sha"], name)
        self.assertFalse(list(root.rglob("SKILL.md")), "References must not register another native router")


if __name__ == "__main__":
    unittest.main(verbosity=2)
