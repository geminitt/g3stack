#!/usr/bin/env python3
"""Local fixture checks for skill contract and guarded link lifecycle."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent / "capabilities.py"
spec = importlib.util.spec_from_file_location("g3_capabilities", SCRIPT)
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)


class CapabilityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="g3-capability-test-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.project = self.root / "project"
        self.project.mkdir()
        self.skill = self.root / "vendor" / "skills" / "review-code"
        self.skill.mkdir(parents=True)
        self.make_skill()
        self.patch_home = patch.object(Path, "home", return_value=self.home)
        self.patch_home.start()
        self.addCleanup(self.patch_home.stop)

    def make_skill(self, name="review-code", description="Review changes safely."):
        (self.skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: '{description}'\n---\n# Review\n", encoding="utf-8")
        (self.skill / "reference.md").write_text("guidance", encoding="utf-8")

    def proposed(self, host="codex", scope="user", project=None):
        return cap.plan(self.skill, host, scope, project)

    def invoke(self, command, plan, host="codex", scope="user", project=None):
        class Args:
            pass
        args = Args()
        args.source = str(self.skill)
        args.host = host
        args.scope = scope
        args.project = project
        args.approve_plan = plan["plan_hash"]
        return command(args)

    def test_metadata_and_hash(self):
        result = cap.inspect(self.skill)
        self.assertEqual(result["metadata"]["name"], "review-code")
        self.assertEqual(result["files"], 2)
        self.assertTrue(result["source_sha256"])

    def test_install_verify_and_idempotency(self):
        proposed = self.proposed()
        self.assertEqual(proposed["action"], "link")
        result = self.invoke(cap.install, proposed)
        self.assertEqual(result["status"], "linked")
        self.assertTrue(Path(result["destination"]).is_symlink())
        self.assertEqual(self.invoke(cap.install, self.proposed())["status"], "already-linked")
        class Args: pass
        args = Args(); args.source = str(self.skill); args.host = "codex"; args.scope = "user"; args.project = None
        self.assertEqual(cap.verify(args)["status"], "PASS")
        self.assertEqual(len(cap.inventory("codex", "user", None)["host_inventory"]["codex"]["skills"]), 1)

    def test_stale_hash_prevents_install(self):
        proposed = self.proposed()
        (self.skill / "reference.md").write_text("CHANGED", encoding="utf-8")
        with self.assertRaisesRegex(cap.Guard, "Approval hash"):
            self.invoke(cap.install, proposed)
        self.assertFalse((self.home / ".agents/skills/review-code").exists())

    def test_source_change_during_link_rolls_back(self):
        proposed = self.proposed()
        destination = Path(proposed["destination"])
        original_symlink = Path.symlink_to

        def change_source(path, *args, **kwargs):
            (self.skill / "reference.md").write_text("CHANGED DURING INSTALL", encoding="utf-8")
            return original_symlink(path, *args, **kwargs)

        with patch.object(Path, "symlink_to", change_source):
            with self.assertRaisesRegex(cap.Guard, "source changed"):
                self.invoke(cap.install, proposed)
        self.assertFalse(os.path.lexists(destination))
        self.assertEqual((self.skill / "reference.md").read_text(), "CHANGED DURING INSTALL")

    def test_source_change_preserves_replaced_link(self):
        proposed = self.proposed()
        destination = Path(proposed["destination"])
        original_plan = cap.plan
        replacement_identity = None

        def change_after_link(*args, **kwargs):
            nonlocal replacement_identity
            if destination.is_symlink():
                replacement = destination.with_name("owner-replacement")
                replacement.symlink_to(self.skill, target_is_directory=True)
                replacement_identity = replacement.lstat().st_ino
                os.replace(replacement, destination)
                (self.skill / "reference.md").write_text("CHANGED", encoding="utf-8")
            return original_plan(*args, **kwargs)

        with patch.object(cap, "plan", change_after_link):
            with self.assertRaisesRegex(cap.Guard, "source changed"):
                self.invoke(cap.install, proposed)
        self.assertTrue(destination.is_symlink())
        self.assertEqual(destination.lstat().st_ino, replacement_identity)
        self.assertEqual(destination.resolve(), self.skill)

    def test_missing_approval_cannot_create_dirs(self):
        proposed = self.proposed()
        with self.assertRaises(cap.Guard):
            self.invoke(cap.install, {"plan_hash": "not-approved"})
        self.assertFalse((self.home / ".agents").exists())

    def test_collision_is_blocking(self):
        dest = self.home / ".agents/skills/review-code"
        dest.mkdir(parents=True)
        plan = self.proposed()
        self.assertEqual(plan["action"], "blocked")
        self.assertTrue(plan["conflicts"])
        with self.assertRaises(cap.Guard):
            self.invoke(cap.install, plan)
        self.assertTrue(dest.is_dir())

    def test_project_scope_and_cross_scope_name_conflict(self):
        user_proposal = self.proposed()
        self.invoke(cap.install, user_proposal)
        p = self.proposed("codex", "project", str(self.project))
        self.assertTrue(p["conflicts"])
        self.assertFalse((self.project / ".agents").exists())

    def test_claude_scope_install_and_remove(self):
        p = self.proposed("claude", "project", str(self.project))
        self.invoke(cap.install, p, "claude", "project", str(self.project))
        linked = self.proposed("claude", "project", str(self.project))
        self.assertEqual(self.invoke(cap.remove, linked, "claude", "project", str(self.project))["status"], "unlinked")
        self.assertTrue(self.skill.exists())

    def test_symlink_in_source_rejected(self):
        (self.skill / "dangerous").symlink_to("/etc")
        with self.assertRaisesRegex(cap.Guard, "symlink"):
            self.proposed()

    def test_symlink_in_destination_ancestors_rejected(self):
        (self.home / ".agents").symlink_to(self.root)
        with self.assertRaisesRegex(cap.Guard, "Symlink"):
            self.proposed()

    def test_manual_activation_metadata(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: review-code\ndescription: >\n  Review a bounded diff safely.\n  Do not edit code.\ndisable-model-invocation: true\n---\n", encoding="utf-8")
        result = cap.inspect(self.skill)
        self.assertFalse(result["metadata"]["automatic_invocation"])
        self.assertIn("bounded diff", result["metadata"]["description"])

    def test_activation_metadata_with_inline_comments(self):
        for value, automatic in (("true # user only", False), ("false # automatic", True),
                                 ("'true' # user only", False), ('"false" # automatic', True)):
            with self.subTest(value=value):
                (self.skill / "SKILL.md").write_text(
                    "---\nname: review-code\ndescription: Review code.\n"
                    f"disable-model-invocation: {value}\n---\n", encoding="utf-8")
                result = cap.inspect(self.skill)
                self.assertEqual(result["metadata"]["automatic_invocation"], automatic)
                if not automatic:
                    self.assertTrue(any("manual invocation" in w for w in result["warnings"]))

    def test_metadata_comments_preserve_quoted_hashes(self):
        for description, expected in (
            ('"Review # safely" # note', "Review # safely"),
            ("'Review # safely' # note", "Review # safely"),
            ("'Owner''s # rules' # note", "Owner's # rules"),
            ("Review C# code # note", "Review C# code"),
            ("Review the owner's code # note", "Review the owner's code"),
        ):
            with self.subTest(description=description):
                (self.skill / "SKILL.md").write_text(
                    f"---\nname: review-code # name\ndescription: {description}\n"
                    'disable-model-invocation: "true" # user only\n---\n', encoding="utf-8")
                meta = cap.inspect(self.skill)["metadata"]
                self.assertEqual(meta["description"], expected)
                self.assertFalse(meta["automatic_invocation"])

    def test_invalid_activation_metadata_rejected(self):
        for value in ("maybe", "", "null", "[true]", "*flag", "!!bool true", ">\n  true"):
            with self.subTest(value=value):
                (self.skill / "SKILL.md").write_text(
                    "---\nname: review-code\ndescription: Review code.\n"
                    f"disable-model-invocation: {value}\n---\n", encoding="utf-8")
                with self.assertRaises(cap.Guard):
                    self.proposed()
                self.assertFalse((self.home / ".agents").exists())

    def test_duplicate_activation_metadata_rejected(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: review-code\ndescription: Review code.\n"
            "disable-model-invocation: true\ndisable-model-invocation: false\n---\n",
            encoding="utf-8")
        with self.assertRaisesRegex(cap.Guard, "Duplicate"):
            self.proposed()

    def test_unsupported_activation_key_syntax_rejected(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: review-code\ndescription: Review code.\n"
            '"disable-model-invocation": true\n---\n', encoding="utf-8")
        with self.assertRaisesRegex(cap.Guard, "Unsupported"):
            self.proposed()

    def test_quoted_block_markers_are_literal_text(self):
        for description, expected in (('">"', ">"), ("'|-'", "|-")):
            with self.subTest(description=description):
                (self.skill / "SKILL.md").write_text(
                    f"---\nname: review-code\ndescription: {description}\n---\n", encoding="utf-8")
                self.assertEqual(cap.inspect(self.skill)["metadata"]["description"], expected)

    def test_block_description_header_comment_preserves_body(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: review-code\ndescription: > # folded text\n"
            "  Review C# code.\n  Keep # in the text.\n"
            "disable-model-invocation: true # user only\n---\n", encoding="utf-8")
        meta = cap.inspect(self.skill)["metadata"]
        self.assertEqual(meta["description"], "Review C# code. Keep # in the text.")
        self.assertFalse(meta["automatic_invocation"])

    def test_unsupported_scalar_syntax_rejected(self):
        for value in ('"true" trailing', "'true", '"true\\q"', '"true"#comment'):
            with self.subTest(value=value):
                (self.skill / "SKILL.md").write_text(
                    "---\nname: review-code\ndescription: Review code.\n"
                    f"disable-model-invocation: {value}\n---\n", encoding="utf-8")
                with self.assertRaises(cap.Guard):
                    self.proposed()

    def test_external_relative_resource_warning(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: review-code\ndescription: Review code safely.\n---\n[Sibling](../sibling/SKILL.md)\n", encoding="utf-8")
        scan = cap.inspect(self.skill)
        self.assertTrue(any("outside skill folder" in warning for warning in scan["warnings"]))

    def test_invalid_frontmatter_rejected(self):
        self.make_skill(name="Bad Skill")
        with self.assertRaisesRegex(cap.Guard, "Invalid skill name"):
            self.proposed()

    def test_inventory_and_survey_do_not_modify(self):
        before = sorted(str(p) for p in self.root.rglob("*"))
        survey = cap.survey(self.root / "vendor")
        self.assertEqual(survey["skill_entries"][0]["name"], "review-code")
        self.assertFalse(cap.inventory("both", "user", None)["host_inventory"]["codex"]["skills"])
        self.assertEqual(sorted(str(p) for p in self.root.rglob("*")), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
