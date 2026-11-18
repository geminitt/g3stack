"""Full conversion retention, resource integrity and native skill packaging."""
import hashlib
import json
from pathlib import Path
import re
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
CHECK = runpy.run_path(str(ROOT / 'scripts/check-codex-integration.py'))
CONVERT = runpy.run_path(str(ROOT / 'scripts/convert-pstack.py'))


class LibraryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='g3-library-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / 'codex/skills/g3-example'
        self.source.mkdir(parents=True)
        self.manifest = self.source / 'SKILL.md'
        self.manifest.write_text('---\nname: g3-example\ndescription: A bounded example.\n---\n\nWork.\n')

    def test_native_discovery_uses_manifest_identities(self):
        self.assertEqual(CHECK['skill_sources'](self.root), {'g3-example': self.source})

    def test_invalid_or_missing_native_identity_is_rejected(self):
        for data in ('', '---\nname: wrong\ndescription: Example\n---\n', '---\nname: g3-example\n---\n'):
            self.manifest.write_text(data)
            with self.assertRaises(ValueError):
                CHECK['skill_sources'](self.root)

    def test_linked_source_is_rejected(self):
        self.source.rename(self.root / 'saved')
        self.source.symlink_to(self.root / 'saved', target_is_directory=True)
        with self.assertRaises(ValueError):
            CHECK['skill_sources'](self.root)

    def test_empty_library_is_rejected(self):
        self.manifest.unlink()
        self.source.rmdir()
        with self.assertRaises(ValueError):
            CHECK['skill_sources'](self.root)

    def test_every_source_file_is_accounted_for_and_verified(self):
        expected = CONVERT['converted'](ROOT)
        manifest = json.loads(expected['provenance.json'])
        self.assertEqual(len(manifest['files']), 551)
        self.assertEqual(len(manifest['skills']), 58)
        self.assertEqual(len({item['destination'] for item in manifest['files']}), 551)
        for relative, content in expected.items():
            self.assertEqual((ROOT / 'codex' / relative).read_bytes(), content, relative)
        for item in manifest['files']:
            original = (ROOT / item['source']).read_bytes()
            self.assertEqual(hashlib.sha256(original).hexdigest(), item['source_sha256'])
            self.assertEqual((ROOT/'codex'/item['destination']).stat().st_mode & 0o777,
                             (ROOT/item['source']).stat().st_mode & 0o777)
            if not item['source'].endswith('.md'):
                self.assertEqual((ROOT / 'codex' / item['destination']).read_bytes(), original,
                                 'Helper/fixture/asset changed: ' + item['source'])
        actual = {str(p.relative_to(ROOT/'codex')) for p in (ROOT/'codex').rglob('*') if p.is_file()}
        self.assertEqual(actual, set(expected) | CONVERT['LOCAL'])

    def test_full_skill_bodies_survive_reversible_identity_translation(self):
        # Independent inverse check: all procedural text must survive, including
        # ordering, examples and paragraphs. A dropped paragraph fails this test.
        manifest = json.loads((ROOT/'codex/provenance.json').read_text())
        for original, renamed in manifest['skills'].items():
            old = (ROOT/'vendor/pstack/skills'/original/'SKILL.md').read_text().split('---',2)[2].strip()
            new = (ROOT/'codex/skills'/renamed/'SKILL.md').read_text().split('---',2)[2]
            new = new.split('procedure. It governs source-host tools, models, permissions and paths.\n', 1)[1]
            if renamed == 'g3stack':
                new = new.split('That contract governs continuation across playbooks and premise recovery.\n', 1)[1]
            new = new.strip()
            for source, target in sorted(manifest['skills'].items(), key=lambda x:len(x[1]), reverse=True):
                new = new.replace(target, source)
                new = new.replace('$'+source, '/'+source)
            new = new.replace('g3-agent', 'poteto-agent').replace('g3-principle-', 'principle-')
            if original == 'poteto-mode':
                new = new.replace('# poteto-mode', '# Poteto mode')
            self.assertEqual(new, old, renamed)

    def test_all_static_local_markdown_links_resolve(self):
        sources = CHECK['skill_sources'](ROOT)
        self.assertEqual(len(sources), 58)
        self.assertIn('g3stack', sources)
        for path in (ROOT/'codex').rglob('*.md'):
            for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
                if '://' in ref or ref.startswith(('#','/')) or any(c in ref for c in ('<','{','`')):
                    continue
                target = (path.parent/ref.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT), str(path)+': '+ref)
                self.assertTrue(target.exists(), str(path)+': '+ref)
        self.assertEqual(len(list((ROOT/'codex/skills/g3stack/playbooks').glob('*.md'))), 22)

    def test_author_notice_and_explicit_invocation_policy_survive(self):
        self.assertEqual((ROOT/'codex/LICENSE').read_bytes(), (ROOT/'vendor/pstack/LICENSE').read_bytes())
        for old in (ROOT/'vendor/pstack/skills').iterdir():
            renamed = json.loads((ROOT/'codex/provenance.json').read_text())['skills'][old.name]
            policy = (ROOT/'codex/skills'/renamed/'agents/openai.yaml').read_text()
            manual = 'disable-model-invocation: true' in (old/'SKILL.md').read_text() and renamed != 'g3stack'
            self.assertIn('false' if manual else 'true', policy)


if __name__ == '__main__':
    unittest.main(verbosity=2)
