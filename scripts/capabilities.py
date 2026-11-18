#!/usr/bin/env python3
"""Inspect and optionally link already-reviewed local Agent Skills into Codex/Claude.

No downloading, shell execution, external plugin installation, or global policy edits.
Inspect/plan/inventory/verify are read-only. Install/remove require explicit approval.
A successful static check does NOT establish native host invocation.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_FILES = 10000
MAX_TOTAL_BYTES = 128 * 1024 * 1024
REPO = Path(__file__).resolve().parent.parent


class Guard(Exception):
    pass


def fail_if(test, message):
    if test:
        raise Guard(message)


def output(value):
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def path_exists(path):
    return os.path.lexists(path)


def absolute(path):
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def scalar(value):
    """Read a one-line plain or quoted scalar with an optional YAML comment.

    Double-quoted values support JSON escapes. Other YAML escapes and
    malformed quoted values are rejected rather than guessed.
    """
    value = value.strip()
    if not value:
        return ""
    if value[0] == '"':
        try:
            result, end = json.JSONDecoder().raw_decode(value)
        except ValueError as ex:
            raise Guard("Unsupported or malformed double-quoted metadata scalar") from ex
        tail = value[end:]
    elif value[0] == "'":
        found = re.fullmatch(r"'((?:[^']|'')*)'(.*)", value)
        fail_if(found is None, "Malformed single-quoted metadata scalar")
        result = found.group(1).replace("''", "'")
        tail = found.group(2)
    else:
        # A hash within a plain token (for example C#) is not a comment.
        return re.split(r"\s+#|^#", value, maxsplit=1)[0].rstrip()
    fail_if(bool(tail) and (not tail[0].isspace() or not tail.lstrip().startswith("#")),
            "Unsupported text after quoted metadata scalar")
    return result


def metadata(skill_file):
    """Read simple frontmatter with unquoted keys and one-line activation flags."""
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as ex:
        raise Guard(f"Cannot read skill metadata: {skill_file} ({type(ex).__name__})") from ex
    chunks = text.splitlines()
    fail_if(not chunks or chunks[0].strip() != "---", f"Missing YAML frontmatter: {skill_file}")
    end = next((i for i in range(1, min(len(chunks), 120)) if chunks[i].strip() == "---"), None)
    fail_if(end is None, f"Unclosed frontmatter: {skill_file}")
    data = {}
    i = 1
    while i < end:
        line = chunks[i]
        found = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if found:
            key, value = found.groups()
            fail_if(key in data, f"Duplicate metadata key: {key}")
            quoted = value.startswith(('"', "'"))
            value = scalar(value)
            if not quoted and value in (">", "|", ">-", "|-"):
                fail_if(key == "disable-model-invocation",
                        "disable-model-invocation must be a one-line true or false value")
                body = []
                i += 1
                while i < end and (chunks[i].startswith(" ") or not chunks[i].strip()):
                    if chunks[i].strip():
                        body.append(chunks[i].strip())
                    i += 1
                data[key] = " ".join(body) if value.startswith(">") else "\n".join(body)
                continue
            data[key] = value
        elif line.strip() and not line.startswith((" ", "\t", "#")):
            raise Guard("Unsupported metadata syntax; use unquoted top-level keys")
        i += 1
    name, description = data.get("name"), data.get("description")
    fail_if(not isinstance(name, str) or not SKILL_NAME.fullmatch(name), f"Invalid skill name: {name!r}")
    fail_if(not isinstance(description, str) or not description.strip(), f"Missing skill description: {skill_file}")
    disabled = data.get("disable-model-invocation", "false").lower()
    fail_if(disabled not in ("true", "false"),
            "disable-model-invocation must be true or false; unsupported YAML syntax is not accepted")
    return {"name": name, "description": description.strip(),
            "automatic_invocation": disabled != "true"}


def source_inventory(source):
    """Fingerprint an entire self-contained skill folder, rejecting symlink entries."""
    source = absolute(source)
    fail_if(not source.is_dir() or source.is_symlink(), f"Expected a real skill folder: {source}")
    items = []
    size = 0
    for base, dirs, files in os.walk(source, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            p = base_path / name
            st = p.lstat()
            fail_if(stat.S_ISLNK(st.st_mode), f"Source contains a symlink; review/package it separately: {p}")
            fail_if(not (stat.S_ISREG(st.st_mode) or stat.S_ISDIR(st.st_mode)), f"Unsupported source entry: {p}")
        dirs[:] = sorted(dirs)
        for name in sorted(files):
            p = base_path / name
            content = p.read_bytes()
            size += len(content)
            fail_if(size > MAX_TOTAL_BYTES or len(items) >= MAX_FILES, "Source too large for safe single-skill linking")
            relative = p.relative_to(source).as_posix()
            items.append([relative, hashlib.sha256(content).hexdigest(), len(content)])
    fail_if(not (source / "SKILL.md").is_file(), "Missing SKILL.md")
    meta = metadata(source / "SKILL.md")
    digest = hashlib.sha256(json.dumps(items, separators=(",", ":")).encode()).hexdigest()
    return source, meta, digest, len(items), size


def source_warnings(source, meta):
    md = (source / "SKILL.md").read_text(encoding="utf-8")
    warnings = ["Source content is untrusted; review instructions and helper scripts before enabling.",
                "Static discovery is not evidence that Codex or Claude invoked the skill."]
    # Only flag explicit relative markdown paths that escape the installed skill folder.
    for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md):
        if "://" in link or link.startswith(("#", "/")):
            continue
        p = link.split("#", 1)[0].split("?", 1)[0]
        if not p or "${" in p:
            continue
        destination = (source / p).resolve(strict=False)
        if not destination.is_relative_to(source):
            warnings.append(f"Reference outside skill folder: {link} (may need a complete kit/native installer)")
        elif not destination.exists():
            warnings.append(f"Unresolved local reference: {link}")
    if meta["name"] in {"poteto-mode", "devflow", "superpowers", "task-router"}:
        warnings.append("Orchestrator-like skill: do not delegate project-level authority or bypass g3stack Core.")
    if not meta["automatic_invocation"]:
        warnings.append("Skill is explicitly marked for manual invocation; do not assume automatic selection.")
    return sorted(set(warnings))


def skill_roots(host, scope, project):
    if scope == "user":
        home = Path.home()
        return [home / (".agents/skills" if host == "codex" else ".claude/skills")]
    fail_if(not project, "--project is required for project scope")
    project = absolute(project)
    fail_if(not project.is_dir() or project.is_symlink(), f"Project directory not found: {project}")
    return [project / (".agents/skills" if host == "codex" else ".claude/skills")]


def inspect(source):
    src, meta, digest, nfiles, size = source_inventory(source)
    return {"source": str(src), "metadata": meta, "source_sha256": digest,
            "files": nfiles, "bytes": size, "warnings": source_warnings(src, meta)}


def entries(root):
    if not root.exists():
        return []
    fail_if(not root.is_dir() or root.is_symlink(), f"Unsafe discovery root: {root}")
    result = []
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        real = p.resolve(strict=False)
        skill_file = real / "SKILL.md"
        if not skill_file.is_file():
            continue
        try:
            meta = metadata(skill_file)
            result.append({"path": str(p), "target": str(real), "kind": "symlink" if p.is_symlink() else "directory", **meta})
        except Guard as ex:
            result.append({"path": str(p), "error": str(ex)})
    return result


def inventory(host, scope, project):
    hosts = ["codex", "claude"] if host == "both" else [host]
    found = {}
    for h in hosts:
        root = skill_roots(h, scope, project)[0]
        values = entries(root)
        groups = {}
        for value in values:
            if "name" in value:
                groups.setdefault(value["name"], []).append(value["path"])
        found[h] = {"root": str(root), "skills": values,
                    "duplicate_names": {name: paths for name, paths in groups.items() if len(paths) > 1}}
    return {"host_inventory": found,
            "limits": "This checks local filesystem roots only; host plugins, built-ins, system skills, MCP, and runtime activation are not enumerated."}


def survey(directory):
    """Enumerate metadata from an already-downloaded kit; no installation."""
    root = absolute(directory)
    fail_if(not root.is_dir() or root.is_symlink(), f"Expected a local kit directory: {root}")
    found = []
    skip = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
    count = 0
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in sorted(dirs) if name not in skip and not (Path(base) / name).is_symlink()]
        count += len(dirs) + len(files)
        fail_if(count > MAX_FILES, "Kit has too many entries for bounded survey")
        if "SKILL.md" in files:
            path = Path(base) / "SKILL.md"
            try:
                info = metadata(path)
                found.append({"path": str(path.parent), **info})
            except Guard as ex:
                found.append({"path": str(path.parent), "error": str(ex)})
            dirs[:] = []  # Do not double-register bundled examples inside a skill.
    names = {}
    for item in found:
        if item.get("name"):
            names.setdefault(item["name"], []).append(item["path"])
    return {"kit": str(root), "skill_entries": found,
            "duplicate_names": {k: v for k,v in names.items() if len(v) > 1},
            "limits": "Metadata inventory only; does not enumerate executable dependencies, host plugins, or activation."}


def ensure_directory(root):
    """Fail closed on symlinks in the destination ancestry."""
    for p in [*reversed(root.parents), root]:
        if path_exists(p):
            fail_if(p.is_symlink() or not p.is_dir(), f"Symlink/non-directory in destination parent: {p}")
    fail_if(root.exists() and not os.access(root, os.R_OK | os.X_OK), f"Cannot inspect discovery root: {root}")


def plan(source, host, scope, project):
    fail_if(host == "both", "Install one host at a time")
    scan = inspect(source)
    root = skill_roots(host, scope, project)[0]
    ensure_directory(root.parent)
    ensure_directory(root)
    target = root / scan["metadata"]["name"]
    fail_if(root.is_relative_to(Path(scan["source"])), "Destination is inside the source package")
    installed = entries(root)
    duplicates = [v for v in installed if v.get("name") == scan["metadata"]["name"] and v["path"] != str(target)]
    if scope == "project":
        user_root = skill_roots(host, "user", None)[0]
        if user_root != root and user_root.exists():
            duplicates += [v for v in entries(user_root) if v.get("name") == scan["metadata"]["name"]]
    conflict = ["Another discovered skill has the same metadata name"] if duplicates else []
    if path_exists(target):
        if target.is_symlink() and target.resolve(strict=False) == Path(scan["source"]):
            action = "already-linked"
        else:
            action = "blocked"
            conflict.append("Destination already exists; never overwrite it")
    else:
        action = "link"
    payload = {"host": host, "scope": scope, "project": str(absolute(project)) if project else None,
               "source": scan["source"], "source_sha256": scan["source_sha256"],
               "name": scan["metadata"]["name"], "destination": str(target), "action": action,
               "conflicts": conflict, "warnings": scan["warnings"],
               "file_count": scan["files"], "bytes": scan["bytes"]}
    payload["plan_hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    payload["authorization"] = "Fingerprint is NOT user approval. Install only after inspecting the source and target."
    return payload


def install(args):
    before = plan(args.source, args.host, args.scope, args.project)
    fail_if(before["conflicts"], "; ".join(before["conflicts"]))
    fail_if(args.approve_plan != before["plan_hash"], "Approval hash does not match the current plan")
    if before["action"] == "already-linked":
        return {"status": "already-linked", "destination": before["destination"],
                "verification": "static-only"}
    target = Path(before["destination"])
    root = target.parent
    # Do not create a home-level discovery root before the authorization check.
    root.mkdir(parents=True, exist_ok=True)
    ensure_directory(root)
    # Re-evaluate against newly discovered state after potential mkdir.
    after = plan(args.source, args.host, args.scope, args.project)
    fail_if(after["plan_hash"] != before["plan_hash"], "Plan changed after directory setup")
    try:
        target.symlink_to(before["source"], target_is_directory=True)
    except FileExistsError as ex:
        raise Guard(f"Destination concurrently created: {target}") from ex
    created_link = target.lstat()
    try:
        check = plan(args.source, args.host, args.scope, args.project)
        fail_if(check["source_sha256"] != before["source_sha256"],
                "Skill source changed during installation; rerun plan before installing")
        fail_if(check["action"] != "already-linked" or check["conflicts"], "Post-install static verification failed")
    except Exception:
        try:
            current_link = target.lstat()
        except FileNotFoundError:
            pass
        else:
            if (stat.S_ISLNK(current_link.st_mode)
                    and (current_link.st_dev, current_link.st_ino) == (created_link.st_dev, created_link.st_ino)
                    and os.readlink(target) == before["source"]):
                target.unlink()
        raise
    return {"status": "linked", "destination": str(target), "source": before["source"],
            "verification": "Static symlink and metadata verified; restart/check host catalog and invoke in a fresh session."}


def verify(args):
    proposal = plan(args.source, args.host, args.scope, args.project)
    return {"status": "PASS" if proposal["action"] == "already-linked" and not proposal["conflicts"] else "FAIL",
            "source_sha256": proposal["source_sha256"], "destination": proposal["destination"],
            "action": proposal["action"], "conflicts": proposal["conflicts"],
            "limits": "Verified filesystem link only; not host discovery or model execution."}


def remove(args):
    proposal = plan(args.source, args.host, args.scope, args.project)
    fail_if(proposal["action"] != "already-linked" or proposal["conflicts"], "Expected matching managed-style link not found")
    fail_if(args.approve_plan != proposal["plan_hash"], "Approval hash does not match matching link")
    target = Path(proposal["destination"])
    fail_if(not target.is_symlink() or target.resolve(strict=False) != Path(proposal["source"]), "Link changed")
    target.unlink()
    return {"status": "unlinked", "destination": str(target), "source_retained": proposal["source"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    inspect_p = subs.add_parser("inspect", help="Read-only inspection of one local skill directory")
    inspect_p.add_argument("source")
    survey_p = subs.add_parser("survey", help="Read-only scan of skill entries inside an external kit checkout")
    survey_p.add_argument("directory")
    inv_p = subs.add_parser("inventory", help="Read-only discovery of user/project skill roots")
    inv_p.add_argument("--host", choices=["codex", "claude", "both"], default="both")
    inv_p.add_argument("--scope", choices=["user", "project"], default="user")
    inv_p.add_argument("--project")
    for operation in ("plan", "install", "verify", "remove"):
        p = subs.add_parser(operation)
        p.add_argument("source", help="Already-reviewed local skill directory containing SKILL.md")
        p.add_argument("--host", choices=["codex", "claude"], required=True)
        p.add_argument("--scope", choices=["user", "project"], default="user")
        p.add_argument("--project", help="Existing project directory when --scope project")
        if operation in ("install", "remove"):
            p.add_argument("--approve-plan", required=True, help="Exact current plan_hash, after separate user approval")
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect(args.source)
        elif args.command == "survey":
            result = survey(args.directory)
        elif args.command == "inventory":
            result = inventory(args.host, args.scope, args.project)
        elif args.command == "plan":
            result = plan(args.source, args.host, args.scope, args.project)
        elif args.command == "install":
            result = install(args)
        elif args.command == "verify":
            result = verify(args)
        else:
            result = remove(args)
        output(result)
        if args.command == "verify":
            return int(result["status"] != "PASS")
        return 0 if not result.get("conflicts") else 2
    except (Guard, OSError, ValueError) as ex:
        output({"status": "FAIL", "error": str(ex)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
