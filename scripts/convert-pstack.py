#!/usr/bin/env python3
"""Reproduce the full pinned pstack -> g3stack/Codex conversion; no installs.

The original vendor tree is immutable. Source fixtures, executable scripts and
binary assets are copied byte for byte. Markdown receives mechanical identity
and sibling-path translations, plus explicit links to the Codex/goal contracts.
No workflow body is summarized or discarded. --check detects missing, modified
or extra distribution resources and also verifies the original vendor hashes.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
LOCAL = {"CODEX.md", "GOAL.md", "README.md"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def converted(root):
    source = root / "vendor/pstack"
    record = json.loads((root / "vendor/source-manifest.json").read_text())["sources"]["pstack"]
    originals = {item["path"].removeprefix("pstack/"): item for item in record["files"]}
    actual = {str(p.relative_to(source)) for p in source.rglob("*") if p.is_file()}
    if actual != set(originals) or any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("Pinned pstack file set changed")
    names = {p.name: "g3-" + p.name for p in (source / "skills").iterdir() if p.is_dir()}
    names.update({"poteto-mode": "g3stack", "poteto-help": "g3-help", "setup-pstack": "g3-setup"})
    patterns = sorted(names, key=len, reverse=True)
    paths = re.compile(r"(?<=/)(?:" + "|".join(map(re.escape, patterns)) + r")(?=/)")
    commands = re.compile(r"(?<![\w/])/(" + "|".join(map(re.escape, patterns)) + r")(?![\w/-])")
    bold = re.compile(r"\*\*(" + "|".join(map(re.escape, patterns)) + r")\*\*")
    outputs, files = {}, []
    for relative, item in sorted(originals.items()):
        path = source / relative
        data = path.read_bytes()
        if sha(data) != item["sha256"]:
            raise ValueError("Pinned source changed: " + relative)
        parts = list(Path(relative).parts)
        if parts[0] == "skills":
            parts[1] = names[parts[1]]
        if relative == "agents/poteto-agent.md":
            parts[-1] = "g3-agent.md"
        parts[-1] = parts[-1].replace("poteto-mode", "g3stack")
        destination = str(Path(*parts))
        if relative == "README.md":
            destination = "docs/upstream-readme.md"
        elif relative in ("plugin.json", ".cursor-plugin/plugin.json"):
            destination = "upstream/" + relative
        changes = []
        # Fixtures and helper programs are retained exactly, including byte-level
        # experimental inputs. The adapter scopes their environment assumptions.
        if path.suffix == ".md":
            text = data.decode("utf-8")
            # Keep attribution/source URLs exact. Translate only local notation.
            urls = []
            def save_url(match):
                urls.append(match.group())
                return "G3SOURCEURLTOKEN" + str(len(urls) - 1) + "END"
            text = re.sub(r"https?://[^\s<>\])]+", save_url, text)
            text = paths.sub(lambda m: names[m.group()], text)
            text = commands.sub(lambda m: "$" + names[m.group(1)], text)
            text = bold.sub(lambda m: "**" + names[m.group(1)] + "**", text)
            for old, new in (("poteto-mode", "g3stack"), ("poteto-agent", "g3-agent"),
                             ("poteto-help", "g3-help"), ("setup-pstack", "g3-setup")):
                text = text.replace(old, new)
            text = re.sub(r"(?<!g3-)principle-", "g3-principle-", text)
            for index, url in enumerate(urls):
                text = text.replace("G3SOURCEURLTOKEN" + str(index) + "END", url)
            if relative == "README.md":
                text = re.sub(r"(\[[^\]]*\]\()((?!https?://|#|/)[^)]+)(\))",
                              lambda m: m[1] + "../" + m[2] + m[3], text)
            if text != data.decode("utf-8"):
                changes.append("local-skill-identities-and-paths")
            is_skill = len(Path(relative).parts) == 3 and path.name == "SKILL.md"
            if is_skill:
                front, body = text.split("---", 2)[1:]
                # Preserve the full description, including a folded YAML value.
                lines = front.strip().splitlines()
                desc = []
                capturing = False
                for line in lines:
                    if line.startswith("description:"):
                        capturing = True
                        desc.append(line)
                    elif capturing and line[:1].isspace():
                        desc.append(line)
                    else:
                        capturing = False
                name = names[path.parent.name]
                if name == "g3stack":
                    desc = ["description: Own a delegated project goal across Research, Engineering and verification using full playbooks. Choose and execute justified steps until the accepted outcome is supported; complete standalone bounded requests directly."]
                elif name == "g3-setup":
                    desc = ["description: Inspect Codex capabilities and propose authorized role/model configuration. Preserve the configured model by default; do not install Cursor rules."]
                metadata = "---\nname: " + name + "\n" + "\n".join(desc) + "\n---\n"
                preface = ("\nRead [Codex execution mapping](../../CODEX.md) before following this\n"
                           "procedure. It governs source-host tools, models, permissions and paths.\n")
                if name == "g3stack":
                    preface += ("Read [g3stack goal ownership](../../GOAL.md) for delegated project goals.\n"
                                "That contract governs continuation across playbooks and premise recovery.\n")
                    body = body.replace("# Poteto mode", "# g3stack")
                # Retain explicit-only selection from upstream, except the main
                # entry which must support the owner's goal-only interaction.
                manual = "disable-model-invocation: true" in front and name != "g3stack"
                outputs["skills/" + name + "/agents/openai.yaml"] = (
                    "policy:\n  allow_implicit_invocation: " + ("false" if manual else "true") + "\n").encode()
                text = metadata + preface + body
                changes += ["codex-frontmatter-and-invocation-policy", "required-codex-mapping"]
            elif relative.startswith("agents/"):
                # These are prompt resources, not registered agents or model config.
                text = re.sub(r"(?m)^(?:model|is_background):[^\n]*\n", "", text)
                text = "Read CODEX.md and skills/g3stack/worker.md from this distribution first.\n\n" + text
                changes.append("worker-brief-host-mapping")
            elif relative == "skills/poteto-mode/worker.md":
                text = ("Apply ../../CODEX.md (resolved from the main skill directory) before\n"
                        "these worker rules. Owner authorization and host limits govern any\n"
                        "source instruction to never ask, commit, open a PR or change scope.\n\n") + text
                changes.append("worker-authorization-mapping")
            data = text.encode("utf-8")
        if destination in outputs:
            raise ValueError("Duplicate converted destination: " + destination)
        outputs[destination] = data
        files.append({"source": "vendor/pstack/" + relative, "source_sha256": item["sha256"],
                      "destination": destination, "sha256": sha(data), "mode": path.stat().st_mode & 0o777, "changes": changes})
    manifest = {"format": "g3stack-full-pstack-conversion-v1", "repository": record["repository"],
                "commit": record["commit"], "version": "0.15.43", "skills": names,
                "files": files, "local_contracts": sorted(LOCAL),
                "generated_metadata": sorted(set(outputs) - {f["destination"] for f in files})}
    outputs["provenance.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = converted(ROOT)
        distribution = ROOT / "codex"
        if args.check:
            expected = set(outputs) | LOCAL
            actual = {str(p.relative_to(distribution)) for p in distribution.rglob("*") if p.is_file()}
            errors = ["Missing: " + p for p in sorted(expected - actual)]
            errors += ["Unexpected: " + p for p in sorted(actual - expected)]
            errors += ["Changed: " + p for p, data in outputs.items()
                       if not (distribution / p).is_file() or (distribution / p).read_bytes() != data]
            records = json.loads(outputs["provenance.json"])["files"]
            errors += ["Mode changed: " + item["destination"] for item in records
                       if (distribution / item["destination"]).is_file()
                       and (distribution / item["destination"]).stat().st_mode & 0o777 != item["mode"]]
            errors += ["Linked resource: " + str(p) for p in distribution.rglob("*") if p.is_symlink()]
            if errors:
                raise ValueError("\n".join(errors))
            print("PASS full conversion: 551 source files, 58 skills, 22 playbooks; no body summaries")
        else:
            for path, data in outputs.items():
                target = distribution / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            for item in json.loads(outputs["provenance.json"])["files"]:
                (distribution / item["destination"]).chmod(item["mode"])
            print("Generated full g3stack/Codex distribution; no installation or activation")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
