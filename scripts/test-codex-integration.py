#!/usr/bin/env python3
"""Standard-library regressions; all installation writes use temporary fixtures.

Run: python3 -B scripts/test-codex-integration.py
"""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="g3stack-safety-")
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        self.repo, self.home = base / "repo", base / "home"
        self.home.mkdir()
        for relative in ("instructions", "integrations/codex", "archive", "codex", "docs", "kits", "vendor",
                         ".agents/skills/task-router"):
            shutil.copytree(ROOT / relative, self.repo / relative)
        (self.repo / "scripts").mkdir()
        for name in ("manage-codex-integration.py", "check-codex-integration.py", "convert-pstack.py"):
            shutil.copy2(ROOT / "scripts" / name, self.repo / "scripts" / name)
        self.script = self.repo / "scripts/manage-codex-integration.py"
        spec = importlib.util.spec_from_file_location("fixture_manager", self.script)
        self.manager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.manager)
        self.codex = self.home / "custom-codex"
        self.codex.mkdir()
        self.installed = self.codex / "AGENTS.md"
        self.installed.write_bytes(b"legacy instructions\n")
        self.installed.chmod(0o640)
        self.config = self.codex / "config.toml"
        self.config.write_bytes(b'model = "fixture"\n')
        self.artifact = self.repo / "integrations/codex/AGENTS.generated.md"
        self.artifact.write_bytes(b"old generated artifact\n")
        self.link = self.home / ".agents/skills/task-router"
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.codex))
        self.environment = patch.dict(os.environ, self.env)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.ctx = self.manager.context()
        self.base = Path(self.ctx["backup_base"])
        self.original = self.snapshot()

    def snapshot(self):
        return {str(p): self.manager.state(p)
                for p in (self.installed, self.artifact, self.link, self.config)}

    def quiet(self, function, *args):
        with contextlib.redirect_stdout(io.StringIO()):
            return function(*args)

    def plan(self):
        return self.manager.plan(self.ctx)

    def install(self):
        return self.quiet(self.manager.install, self.ctx, self.plan()["plan_hash"])

    def crash(self, phase, backup=""):
        # Independent process: no exception handler can disguise a hard exit.
        program = '''import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("fixture", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
phase = sys.argv[2]
if phase == "preparation":
    original = m.atomic_file
    def write(path, *args, **kwargs):
        if path.name == "manifest.json": os._exit(89)
        return original(path, *args, **kwargs)
    m.atomic_file = write
else:
    original = m.apply_state
    def apply(path, *args):
        if phase == "ready": os._exit(89)
        original(path, *args)
        if path.name == "AGENTS.md": os._exit(89)
    m.apply_state = apply
ctx = m.context()
if phase == "restoring": m.restore(ctx, sys.argv[3])
else: m.install(ctx, m.plan(ctx)["plan_hash"])
'''
        result = subprocess.run([sys.executable, "-B", "-c", program,
                                 str(self.script), phase, str(backup)], cwd=self.home, env=self.env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 89, result.stdout + result.stderr)

    def assert_preparation_retained_and_retryable(self):
        self.assertEqual(self.snapshot(), self.original)
        self.assertFalse((self.home / ".agents").exists())
        proposal = self.plan()
        self.assertEqual(proposal["conflicts"], [])
        retained = proposal["retained_preparations"]
        self.assertEqual(len(retained), 1)
        preparation = Path(retained[0])
        self.assertTrue(preparation.is_dir())
        self.assertEqual(preparation.stat().st_mode & 0o777, 0o700)
        files = {p.name: p.read_bytes() for p in preparation.iterdir()}
        for path in preparation.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        outcome = self.install()
        self.quiet(self.manager.restore, self.ctx, outcome["backup"])
        self.assertEqual(self.snapshot(), self.original)
        self.assertTrue(preparation.is_dir())
        self.assertEqual({p.name: p.read_bytes() for p in preparation.iterdir()}, files)

    def test_preparation_failure_retained_without_blocking_install(self):
        original = self.manager.atomic_file
        def fail(path, *args, **kwargs):
            if path.name == "manifest.json":
                raise OSError("injected backup preparation failure")
            return original(path, *args, **kwargs)
        with patch.object(self.manager, "atomic_file", fail):
            with self.assertRaises(self.manager.Conflict):
                self.install()
        self.assert_preparation_retained_and_retryable()

    def test_preparation_interruption_retained_without_blocking_install(self):
        self.crash("preparation")
        self.assert_preparation_retained_and_retryable()

    def test_failed_verification_does_not_promote_preparation(self):
        original = self.manager.load_backup
        def reject(path, ctx, **kwargs):
            if kwargs.get("preparing"):
                raise self.manager.Conflict("injected backup verification failure")
            return original(path, ctx, **kwargs)
        with patch.object(self.manager, "load_backup", reject):
            with self.assertRaises(self.manager.Conflict):
                self.install()
        self.assertEqual(list(self.base.glob("codex-deploy-*")), [])
        self.assert_preparation_retained_and_retryable()

    def test_legacy_incomplete_backup_remains_blocking(self):
        self.base.mkdir(parents=True, mode=0o700)
        backup = self.base / "codex-deploy-ambiguous-legacy"
        backup.mkdir(mode=0o700)
        self.assertTrue(self.plan()["conflicts"])
        with self.assertRaises((self.manager.Conflict, OSError)):
            self.quiet(self.manager.restore, self.ctx, str(backup))
        self.assertEqual(self.snapshot(), self.original)
        self.assertTrue(backup.is_dir())

    def test_valid_backup_before_apply_still_requires_verified_restore(self):
        self.crash("ready")
        self.assertEqual(self.snapshot(), self.original)
        self.assertTrue(self.plan()["conflicts"])
        backup = next(self.base.glob("codex-deploy-*"))
        self.manager.load_backup(backup, self.ctx)
        self.quiet(self.manager.restore, self.ctx, str(backup))
        self.assertFalse(self.plan()["conflicts"])
        self.assertEqual(self.snapshot(), self.original)

    def test_interrupted_apply_restores_original_resources(self):
        self.crash("applied")
        self.assertNotEqual(self.snapshot(), self.original)
        self.assertTrue(self.plan()["conflicts"])
        backup = next(self.base.glob("codex-deploy-*"))
        self.quiet(self.manager.restore, self.ctx, str(backup))
        self.assertEqual(self.snapshot(), self.original)
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse(self.plan()["conflicts"])

    def test_interrupted_apply_preserves_external_edit(self):
        self.crash("applied")
        self.installed.write_bytes(b"external owner edit\n")
        before = self.snapshot()
        backup = next(self.base.glob("codex-deploy-*"))
        with self.assertRaises(self.manager.Conflict):
            self.quiet(self.manager.restore, self.ctx, str(backup))
        self.assertEqual(self.snapshot(), before)
        self.assertTrue(self.plan()["conflicts"])

    def test_interrupted_restore_remains_blocking_and_recoverable(self):
        original_backup = self.install()["backup"]
        installed = self.snapshot()
        self.crash("restoring", original_backup)
        self.assertTrue(self.plan()["conflicts"])
        backup = next(p for p in self.base.glob("codex-deploy-*")
                      if not (p / "result.json").exists())
        self.assertEqual(self.manager.load_backup(backup, self.ctx)["operation"], "restore")
        self.quiet(self.manager.restore, self.ctx, str(backup))
        self.assertEqual(self.snapshot(), installed)
        self.assertFalse(self.plan()["conflicts"])
        self.quiet(self.manager.restore, self.ctx, original_backup)
        self.assertEqual(self.snapshot(), self.original)

    def test_automatic_recovery_preserves_external_edit(self):
        def fail(*args):
            self.installed.write_bytes(b"intervening edit\n")
            raise OSError("injected verification failure")
        with patch.object(self.manager, "verify_installed", fail):
            with self.assertRaises(self.manager.Conflict):
                self.install()
        self.assertEqual(self.installed.read_bytes(), b"intervening edit\n")
        result = json.loads(next(self.base.glob("codex-deploy-*/result.json")).read_bytes())
        self.assertEqual(result["status"], "recovery-incomplete")
        self.assertIn(str(self.installed), [e["path"] for e in result["details"]["not_restored"]])
        self.assertTrue(self.plan()["conflicts"])

    def test_normal_install_restore_and_idempotence(self):
        self.assertFalse(self.plan()["conflicts"])
        self.assertFalse(self.base.exists(), "plan must not write")
        result = self.install()
        installed = self.snapshot()
        self.assertTrue(self.link.is_symlink())
        self.assertEqual(self.link.resolve(), self.repo / ".agents/skills/task-router")
        backups = set(self.base.iterdir())
        self.assertEqual(self.install()["status"], "already-installed")
        self.assertEqual(self.snapshot(), installed)
        self.assertEqual(set(self.base.iterdir()), backups)
        self.quiet(self.manager.restore, self.ctx, result["backup"])
        self.assertEqual(self.snapshot(), self.original)
        self.assertEqual(self.quiet(self.manager.restore, self.ctx, result["backup"])["status"],
                         "already-restored")

    def checker_result(self):
        return subprocess.run([sys.executable, "-B",
                               str(self.repo / "scripts/check-codex-integration.py")],
                              cwd=self.home, env=self.env, capture_output=True,
                              text=True, timeout=15)

    def test_installs_only_personal_source_without_normalizing_bytes(self):
        personal = self.repo / "instructions/personal.md"
        payload = b"# Personal agreements\r\n\r\nExact source bytes.\r\n"
        personal.write_bytes(payload)
        self.install()
        self.assertEqual(self.installed.read_bytes(), payload)
        self.assertEqual(self.artifact.read_bytes(), payload)
        self.assertEqual(self.checker_result().returncode, 0)

    def test_orchestration_changes_do_not_change_global_bytes(self):
        personal = self.repo / "instructions/personal.md"
        personal.write_bytes(b"# Personal agreements\n")
        self.install()
        before = self.installed.read_bytes()
        core = self.repo / "instructions/core.md"
        core.write_bytes(core.read_bytes() + b"\nOrchestration-only change.\n")
        self.assertEqual(self.checker_result().returncode, 0)
        self.assertEqual(self.plan()["changes"], [])
        self.assertEqual(self.installed.read_bytes(), before)

    def test_personal_source_change_invalidates_approved_plan(self):
        personal = self.repo / "instructions/personal.md"
        personal.write_bytes(b"# Personal agreements\n")
        approved = self.plan()["plan_hash"]
        personal.write_bytes(b"# Changed personal agreements\n")
        with self.assertRaises(self.manager.Conflict):
            self.quiet(self.manager.install, self.ctx, approved)
        self.assertEqual(self.snapshot(), self.original)

    def test_missing_empty_or_linked_personal_source_blocks_install(self):
        personal = self.repo / "instructions/personal.md"
        for kind in ("missing", "empty", "linked"):
            with self.subTest(kind=kind):
                personal.unlink(missing_ok=True)
                if kind == "empty":
                    personal.write_bytes(b" \n")
                elif kind == "linked":
                    personal.symlink_to(self.repo / "instructions/core.md")
                self.assertTrue(self.plan()["conflicts"])
                with self.assertRaises(self.manager.Conflict):
                    self.install()
                self.assertEqual(self.snapshot(), self.original)

    def test_checker_rejects_symlinked_matching_files(self):
        self.install()
        self.assertEqual(self.checker_result().returncode, 0)
        for target in (self.installed, self.artifact):
            with self.subTest(target=target.name, parent=str(target.parent)):
                data = target.read_bytes()
                saved = target.with_name("matching-target")
                target.rename(saved)
                target.symlink_to(saved)
                result = self.checker_result()
                target.unlink()
                saved.rename(target)
                self.assertEqual(target.read_bytes(), data)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_checker_rejects_hardlinked_matching_files(self):
        self.install()
        for target in (self.installed, self.artifact):
            with self.subTest(target=str(target)):
                alias = target.with_name("hardlink-alias")
                os.link(target, alias)
                result = self.checker_result()
                alias.unlink()
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_each_actual_router_skill_reference_is_checked(self):
        router = self.repo / ".agents/skills/task-router/SKILL.md"
        references = re.findall(r"\[[^\]]*\]\(([^)]+)\)", router.read_text())
        paths = [(router.parent / ref).resolve() for ref in references
                 if "/skills/g3" in ref]
        self.assertTrue(paths, "No actual router skill references found")
        for path in paths:
            with self.subTest(playbook=path.name):
                data = path.read_bytes()
                path.unlink()
                self.assertTrue(self.plan()["conflicts"], f"Missing reference accepted: {path}")
                path.write_bytes(data)
        self.assertFalse(self.plan()["conflicts"])

    def test_shared_vendor_manifest_is_checked_before_install(self):
        router = self.repo / ".agents/skills/task-router/SKILL.md"
        # The source manifest remains a required resource for the native library.
        with router.open("a") as stream:
            stream.write("\n[Recovery](../../../codex/skills/g3-principle-attack-the-premise/SKILL.md)\n")
        self.assertFalse(self.plan()["conflicts"])
        dependency = self.repo / "vendor/source-manifest.json"
        dependency.unlink()
        self.assertTrue(self.plan()["conflicts"])
        with self.assertRaises(self.manager.Conflict):
            self.install()
        self.assertEqual(self.snapshot(), self.original)


    def test_engineering_checker_is_a_required_transitive_source(self):
        router = self.repo / ".agents/skills/task-router/SKILL.md"
        with router.open("a") as stream:
            stream.write("\n[Build](../../../codex/skills/g3-figure-it-out/SKILL.md)\n")
        self.assertFalse(self.plan()["conflicts"])
        (self.repo / "kits/engineering/check.py").unlink()
        self.assertTrue(self.plan()["conflicts"])
        with self.assertRaises(self.manager.Conflict):
            self.install()
        self.assertEqual(self.snapshot(), self.original)

    def test_whole_library_links_install_and_restore(self):
        sources = self.manager.checker()["skill_sources"](self.repo)
        self.assertEqual(len(sources), 58)
        result = self.install()
        for name, source in sources.items():
            link = self.home / ".agents/skills" / name
            self.assertTrue(link.is_symlink(), name)
            self.assertEqual(link.resolve(), source)
        self.assertEqual(self.checker_result().returncode, 0)
        self.quiet(self.manager.restore, self.ctx, result["backup"])
        self.assertFalse((self.home / ".agents").exists())
        self.assertEqual(self.snapshot(), self.original)

    def test_library_collision_blocks_all_installation(self):
        target = self.home / ".agents/skills/g3-tdd"
        target.mkdir(parents=True)
        (target / "owner.txt").write_text("owner data")
        with self.assertRaises(self.manager.Conflict):
            self.install()
        self.assertEqual((target / "owner.txt").read_text(), "owner data")
        self.assertEqual(self.snapshot(), self.original)

    def test_library_edit_invalidates_approved_plan(self):
        approved = self.plan()["plan_hash"]
        source = self.repo / "codex/skills/g3-tdd/SKILL.md"
        source.write_bytes(source.read_bytes() + b"\nChanged procedure.\n")
        with self.assertRaises(self.manager.Conflict):
            self.quiet(self.manager.install, self.ctx, approved)
        self.assertEqual(self.snapshot(), self.original)

    def test_missing_library_manifest_or_shared_source_blocks_install(self):
        for relative in ("codex/skills/g3-create-verification-skill/SKILL.md", "codex/CODEX.md"):
            with self.subTest(source=relative):
                source = self.repo / relative
                data = source.read_bytes()
                source.unlink()
                self.assertTrue(self.plan()["conflicts"])
                with self.assertRaises(self.manager.Conflict):
                    self.install()
                self.assertEqual(self.snapshot(), self.original)
                source.write_bytes(data)

    def test_disabled_library_member_blocks_install(self):
        self.config.write_text('[[skills.config]]\nname = "g3-tdd"\nenabled = false\n')
        original = self.snapshot()
        self.assertTrue(self.plan()["conflicts"])
        with self.assertRaises(self.manager.Conflict):
            self.install()
        self.assertEqual(self.snapshot(), original)

    def test_checker_rejects_missing_library_link(self):
        self.install()
        (self.home / ".agents/skills/g3-create-verification-skill").unlink()
        self.assertNotEqual(self.checker_result().returncode, 0)

    def test_owned_legacy_links_are_retired_and_restorable(self):
        directory = self.home / ".agents/skills"
        directory.mkdir(parents=True)
        for name in self.manager.LEGACY_NAMES:
            (directory / name).symlink_to(self.repo / "skills" / name)
        result = self.install()
        self.assertTrue(all(not (directory / name).is_symlink() for name in self.manager.LEGACY_NAMES))
        self.quiet(self.manager.restore, self.ctx, result["backup"])
        for name in self.manager.LEGACY_NAMES:
            self.assertEqual((directory / name).resolve(), self.repo / "skills" / name)
        self.assertFalse((directory / "g3stack").exists())

    def test_foreign_legacy_name_is_never_retired(self):
        target = self.home / ".agents/skills/g3-build"
        target.mkdir(parents=True)
        (target / "owner.txt").write_text("keep")
        self.assertTrue(self.plan()["conflicts"])
        with self.assertRaises(self.manager.Conflict):
            self.install()
        self.assertEqual((target / "owner.txt").read_text(), "keep")


if __name__ == "__main__":
    unittest.main(verbosity=2)
