#!/usr/bin/env python3
"""Plan, install, or restore this repository's Codex integration (Linux/WSL).

Python 3.11+; standard library only. No arguments means read-only plan.
Obtain owner authorization separately, then review plan's paths/changes and
select that exact observed state with its fingerprint:
    python3 -B scripts/manage-codex-integration.py install --approve-plan HASH
Restore a backup produced by THIS tool, in the same HOME/CODEX_HOME/repository:
    python3 -B scripts/manage-codex-integration.py restore --backup PATH

--approve-plan matches state; it cannot authenticate or prove human approval.
Install requires owner authorization as well as a matching plan fingerprint;
conflicting symlinks, directories, overrides, and unsupported settings block it.
Backups retain immutable before/after payloads and a checksummed manifest. A
missing result.json in codex-deploy-* denotes an interrupted operation; restore
its verified backup before another install. Pre-application codex-prepare-*
directories are retained and reported, not applied or silently deleted. Only a
verified preparation is atomically promoted before resource changes can begin.
Legacy incomplete codex-deploy-* directories remain blocked for manual review.
Recovery refuses intervening edits and removes only empty
directories created by the recorded operation. Backups are never deleted.

This is static installation verification, not native Codex runtime verification.
CLI/project/cloud overrides cannot all be predicted. Checksums detect corruption,
not malicious rewriting by the same user. Do not edit sources or destinations
concurrently; locking serializes this tool, not arbitrary external writers.
Restore does not rewind repository sources; the Router follows the checkout.
"""

import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import stat
import sys
import tomllib
import uuid


SOURCE = "instructions/personal.md"
ARTIFACT = "integrations/codex/AGENTS.generated.md"
MAX_BYTES = 4 * 1024 * 1024
ROOT = Path(__file__).resolve().parent.parent
LEGACY_NAMES = (
    "g3-build", "g3-debug", "g3-design", "g3-diagram", "g3-experiment", "g3-formal",
    "g3-measure", "g3-plan", "g3-prototype", "g3-recover", "g3-refactor",
    "g3-research", "g3-review", "g3-security", "g3-ui", "g3-verify",
)

SYSTEM_UID = Path("/").stat().st_uid  # Also supports a user-namespace-mapped root.


class Conflict(Exception):
    """An unsafe or unsupported state; do not repair it implicitly."""


def require(condition, message):
    if not condition:
        raise Conflict(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def emit(value):
    print(encoded(value).decode(), end="")


def read_regular(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                f"Not a single-link regular file: {path}")
        data = stream.read(MAX_BYTES + 1)
        require(len(data) <= MAX_BYTES, f"Resource exceeds 4 MiB: {path}")
        after = os.fstat(stream.fileno())
        require((info.st_size, info.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
                f"File changed while reading: {path}")
        return data


def state(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"kind": "absent"}
    result = {"uid": info.st_uid, "gid": info.st_gid,
              "mode": stat.S_IMODE(info.st_mode)}
    if stat.S_ISLNK(info.st_mode):
        return dict(result, kind="symlink", target=os.readlink(path))
    if stat.S_ISREG(info.st_mode):
        data = read_regular(path)
        return dict(result, kind="file", sha256=digest(data), size=len(data),
                    mtime_ns=info.st_mtime_ns)
    if stat.S_ISDIR(info.st_mode):
        return dict(result, kind="directory")
    raise Conflict(f"Unsupported filesystem object: {path}")


def matches(actual, expected):
    # Desired new files omit mtime; backups preserve old file mtime exactly.
    return all(actual.get(key) == value for key, value in expected.items())


def ancestors(path):
    """Reject symlink parents, foreign owners, and writable shared parents."""
    for parent in reversed(path.parent.parents):
        check_directory(parent)
    check_directory(path.parent)


def check_directory(path):
    info = state(path)
    if info["kind"] == "absent":
        return
    require(info["kind"] == "directory", f"Invalid directory or symlink: {path}")
    require(info["uid"] in (os.geteuid(), 0, SYSTEM_UID), f"Foreign directory owner: {path}")
    shared_tmp = info["uid"] in (0, SYSTEM_UID) and info["mode"] & stat.S_ISVTX
    require(not info["mode"] & 0o022 or shared_tmp,
            f"Group/world-writable directory: {path}")


def context():
    home = Path.home()
    codex = Path(os.environ.get("CODEX_HOME") or home / ".codex").expanduser()
    require(home.is_absolute() and codex.is_absolute(),
            "HOME and CODEX_HOME must be absolute paths")
    require(".." not in codex.parts and home.is_dir(), "Invalid HOME/CODEX_HOME")
    require(home.resolve() == home, "Symlinked HOME is unsupported")
    return {"repository": str(ROOT), "home": str(home), "codex_home": str(codex),
            "backup_base": str(home / ".local/state/g3stack/backups")}


def targets(ctx):
    skills = Path(ctx["home"]) / ".agents/skills"
    locations = {"artifact": ROOT / ARTIFACT,
                 "instructions": Path(ctx["codex_home"]) / "AGENTS.md",
                 "router": skills / "task-router"}
    locations.update({"skill:" + name: skills / name
                      for name in (*checker()["skill_sources"](ROOT), *LEGACY_NAMES)})
    return locations


def missing_parents(paths):
    missing = set()
    for path in paths:
        ancestors(path)
        parent = path.parent
        while state(parent)["kind"] == "absent":
            missing.add(parent)
            parent = parent.parent
    return sorted(missing, key=lambda p: (len(p.parts), str(p)))


def checker():
    # run_path avoids __pycache__; reuse the existing byte/link checks.
    return runpy.run_path(str(ROOT / "scripts/check-codex-integration.py"))


def source_inputs(guards):
    path = ROOT / SOURCE
    ancestors(path)
    require(state(path)["kind"] == "file", f"Missing/invalid source: {path}")
    guards[str(path)] = state(path)
    # One source, copied byte for byte. Core and adapters are not global input.
    expected = read_regular(path)
    require(expected.strip(), "Empty generated instructions")
    # Bind the complete converted distribution and immutable source, not just
    # Markdown links (many upstream links are examples, not package resources).
    converter = runpy.run_path(str(ROOT / "scripts/convert-pstack.py"))
    outputs = converter["converted"](ROOT)
    distribution = ROOT / "codex"
    actual = {str(p.relative_to(distribution)) for p in distribution.rglob("*") if p.is_file()}
    require(actual == set(outputs) | converter["LOCAL"], "Converted resource set differs")
    require(not any(p.is_symlink() for p in distribution.rglob("*")), "Linked converted resource")
    for relative, data in outputs.items():
        require(read_regular(distribution / relative) == data, "Converted resource changed: " + relative)
    paths = list(distribution.rglob("*")) + list((ROOT / "vendor/pstack").rglob("*"))
    paths.extend(ROOT / relative for relative in (
        ".agents/skills/task-router/SKILL.md", ".agents/skills/task-router/agents/openai.yaml",
        "scripts/convert-pstack.py",
        "scripts/check-codex-integration.py", "scripts/manage-codex-integration.py",
        "vendor/source-manifest.json", "kits/engineering/check.py"))
    for path in paths:
        if path.is_dir():
            continue
        ancestors(path)
        require(state(path)["kind"] == "file", f"Required source unavailable: {path}")
        guards[str(path)] = state(path)
    # Validate the compatibility entry's complete, intentionally small graph.
    router = ROOT / ".agents/skills/task-router/SKILL.md"
    for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)", read_regular(router).decode()):
        if "://" not in reference and not reference.startswith("#"):
            target = (router.parent / reference.split("#", 1)[0]).resolve(strict=True)
            require(target.is_relative_to(ROOT) and target.is_file(), "Invalid compatibility resource")
            guards[str(target)] = state(target)
    return expected


def discovery(ctx, guards, expected_size):
    codex = Path(ctx["codex_home"])
    override = codex / "AGENTS.override.md"
    guards[str(override)] = state(override)
    require(guards[str(override)]["kind"] == "absent", f"Global override exists: {override}")
    paths = [codex / "config.toml", Path("/etc/codex/config.toml"),
             Path("/etc/codex/managed_config.toml"), Path("/etc/codex/requirements.toml")]
    if codex.is_dir():
        paths.extend(sorted(codex.glob("*.config.toml")))
    budgets = []
    for path in paths:
        ancestors(path)
        guards[str(path)] = state(path)
        if guards[str(path)]["kind"] == "absent":
            continue
        require(guards[str(path)]["kind"] == "file", f"Invalid configuration: {path}")
        config = tomllib.loads(read_regular(path).decode("utf-8"))
        layers = [config] + list(config.get("profiles", {}).values())
        for layer in layers:
            for key in ("model_instructions_file", "experimental_instructions_file",
                        "developer_instructions", "instructions"):
                require(not layer.get(key), f"Instruction setting requires review: {path}: {key}")
            if "project_doc_max_bytes" in layer:
                limit = layer["project_doc_max_bytes"]
                require(type(limit) is int and limit > 0, f"Invalid instruction budget: {path}")
                budgets.append(limit)
            skills = layer.get("skills", {})
            require(skills.get("include_instructions", True), f"Skill instructions disabled: {path}")
            for rule in skills.get("config", []):
                names = ["task-router", *checker()["skill_sources"](ROOT)]
                match = rule.get("name") in names or any(name in rule.get("path", "") for name in names)
                require(not match or rule.get("enabled", True), f"g3stack skill disabled: {path}")
    budget = min(budgets) if budgets else 32768
    require(expected_size <= budget, f"Artifact exceeds conservative instruction budget ({budget})")
    return budget


def pending_backups(base):
    if not base.exists():
        return []
    require(not base.is_symlink() and base.is_dir(), f"Invalid backup base: {base}")
    pending = []
    for path in sorted(base.glob("codex-deploy-*")):
        info = state(path)
        require(info["kind"] == "directory" and info["uid"] == os.geteuid() and
                info["mode"] == 0o700, f"Unexpected deployment backup object: {path}")
        result = path / "result.json"
        status = json.loads(read_regular(result)).get("status") if result.is_file() else None
        require(status in (None, "installed", "restored", "recovered", "recovery-incomplete"),
                f"Unknown deployment journal status: {path}")
        if status in (None, "recovery-incomplete"):
            pending.append(str(path))
    return pending


def retained_preparations(base):
    """These directories never authorize apply; promotion must happen first.

    A directory may still be in preparation, rather than known to be aborted.
    Report it without claiming that the installation itself is unchanged.
    """
    retained = []
    for path in sorted(base.glob("codex-prepare-*")):
        info = state(path)
        require(info["kind"] == "directory" and info["uid"] == os.geteuid() and
                info["mode"] == 0o700, f"Unexpected preparation object: {path}")
        retained.append(str(path))
    return retained


def plan(ctx):
    guards, entries, conflicts = {}, [], []
    result = {"context": ctx, "conflicts": conflicts, "resources": entries,
              "authorization": "Owner authorization is separate; plan_hash only fingerprints state.",
              "limitations": ["Static filesystem checks only; future CLI/project/cloud overrides unknown.",
                              "Do not edit sources or installation concurrently."]}
    result["installed_state"] = {}
    try:
        locations = targets(ctx)
    except (OSError, ValueError) as error:
        conflicts.append(str(error))
        locations = {}
    for role, path in locations.items():
        try:
            result["installed_state"][role] = {"path": str(path), "state": state(path)}
        except (OSError, Conflict) as error:
            conflicts.append(str(error))
    try:
        expected = source_inputs(guards)
        result["expected_artifact"] = checker()["fingerprint"](expected)
        locations = targets(ctx)
        require(len(set(locations.values())) == len(locations), "Managed paths overlap")
        require(not Path(ctx["backup_base"]).is_relative_to(ROOT), "Backup must be outside repository")
        require(not any(path.is_relative_to(Path(ctx["backup_base"])) for path in locations.values()),
                "Managed integration paths overlap the backup directory")
        directories = missing_parents(locations.values())
        require(not set(directories).intersection(Path(ctx["backup_base"]).parents),
                "New installation directories overlap backup ancestors")
        for path in directories:
            entries.append({"role": "directory", "path": str(path), "before": {"kind": "absent"},
                            "after": {"kind": "directory", "mode": 0o700,
                                      "uid": os.geteuid(), "gid": os.getegid()}})
        for role, path in locations.items():
            before = state(path)
            require(before.get("uid", os.geteuid()) == os.geteuid(), f"Foreign resource owner: {path}")
            if role.startswith("skill:") and role.removeprefix("skill:") in LEGACY_NAMES:
                name = role.removeprefix("skill:")
                source = ROOT / "skills" / name
                require(before["kind"] == "absent" or
                        (before["kind"] == "symlink" and path.resolve(strict=False) == source.resolve(strict=False)),
                        f"Refusing to retire foreign legacy skill object: {path}")
                after = {"kind": "absent"}
            elif role == "router" or role.startswith("skill:"):
                source = (ROOT / ".agents/skills/task-router" if role == "router"
                          else checker()["skill_sources"](ROOT)[role.removeprefix("skill:")])
                require(before["kind"] == "absent" or
                        (before["kind"] == "symlink" and path.resolve(strict=True) == source.resolve(strict=True)),
                        f"Conflicting skill object: {path}")
                after = before if before["kind"] == "symlink" else {
                    "kind": "symlink", "target": str(source), "mode": 0o777,
                    "uid": os.geteuid(), "gid": os.getegid()}
            else:
                require(before["kind"] in ("absent", "file"), f"Conflicting managed object: {path}")
                after = {"kind": "file", "sha256": digest(expected), "size": len(expected),
                         "mode": before.get("mode", 0o644), "uid": os.geteuid(),
                         "gid": before.get("gid", os.getegid())}
                require(not after["mode"] & 0o6022, f"Unsafe managed file mode: {path}")
            entries.append({"role": role, "path": str(path), "before": before, "after": after})
        result["instruction_budget"] = discovery(ctx, guards, len(expected))
        ancestors(Path(ctx["backup_base"]) / "placeholder")
        base_state = state(Path(ctx["backup_base"]))
        require(base_state["kind"] == "absent" or
                (base_state["uid"] == os.geteuid() and base_state["mode"] == 0o700),
                "Backup base must be private (0700) and owned by the current user")
        result["retained_preparations"] = retained_preparations(Path(ctx["backup_base"]))
        unfinished = pending_backups(Path(ctx["backup_base"]))
        require(not unfinished, f"Unfinished deployment backups require restore/review: {unfinished}")
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, AttributeError, Conflict) as error:
        conflicts.append(str(error))
    result["guards"] = guards
    result["plan_hash"] = digest(encoded(result))
    result["changes"] = [e["path"] for e in entries if not matches(e["before"], e["after"])]
    result["backup_destination"] = str(Path(ctx["backup_base"]) / "codex-deploy-<UTC>-<unique-id>")
    return result


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_file(path, data, mode, metadata=None):
    """Stage on the destination filesystem, fsync, then atomically replace."""
    ancestors(path)
    name = ".g3stack-" + uuid.uuid4().hex
    parent = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            if metadata:
                os.fchown(stream.fileno(), metadata["uid"], metadata["gid"])
            os.fchmod(stream.fileno(), mode)
            if metadata and "mtime_ns" in metadata:
                os.utime(stream.fileno(), ns=(metadata["mtime_ns"], metadata["mtime_ns"]))
            os.fsync(stream.fileno())
        # No silent overwrite of a newly appeared path during absent->file.
        if metadata and metadata.get("create_only"):
            os.link(name, path.name, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
            os.unlink(name, dir_fd=parent)
        else:
            os.replace(name, path.name, src_dir_fd=parent, dst_dir_fd=parent)
        os.fsync(parent)
    finally:
        try:
            os.unlink(name, dir_fd=parent)
        except FileNotFoundError:
            pass
        os.close(parent)


def private_directories(path):
    ancestors(path / "placeholder")
    for directory in missing_parents([path / "placeholder"]):
        directory.mkdir(mode=0o700)
        sync_directory(directory.parent)
    info = state(path)
    require(info["kind"] == "directory" and info["uid"] == os.geteuid() and
            info["mode"] == 0o700, f"Backup directory is not private: {path}")


def backup(ctx, entries, operation, desired_bytes, guards):
    base = Path(ctx["backup_base"])
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    suffix = stamp + "-" + uuid.uuid4().hex[:8]
    destination = base / ("codex-prepare-" + suffix)
    destination.mkdir(mode=0o700)
    sync_directory(base)
    print(f"Pre-application preparation (retained on failure): {destination}", flush=True)
    records = []
    for index, entry in enumerate(entries):
        record = dict(entry)
        path = Path(entry["path"])
        require(matches(state(path), entry["before"]), f"Resource changed before backup: {path}")
        for phase in ("before", "after"):
            info = entry[phase]
            if info["kind"] == "file":
                data = read_regular(path) if phase == "before" else desired_bytes[str(path)]
                require(digest(data) == info["sha256"], f"Backup bytes changed: {path}")
                name = f"{index}-{phase}.bin"
                atomic_file(destination / name, data, 0o600)
                record[phase + "_payload"] = name
        records.append(record)
    manifest = {"format": "g3stack-codex-v1", "context": ctx,
                "operation": operation, "resources": records,
                "preflight_guards": guards or {}}
    data = encoded(manifest)
    atomic_file(destination / "manifest.json", data, 0o600)
    atomic_file(destination / "manifest.sha256", (digest(data) + "\n").encode(), 0o600)
    sync_directory(destination)
    load_backup(destination, ctx, preparing=True)
    ready = base / ("codex-deploy-" + suffix)
    require(not os.path.lexists(ready), f"Backup destination already exists: {ready}")
    destination.rename(ready)
    sync_directory(base)
    print(f"Verified backup ready: {ready}", flush=True)
    return ready, manifest


def load_backup(path, ctx, *, preparing=False):
    """Validate integrity, scope, ownership, and payloads before any restoration."""
    prefix = "codex-prepare-" if preparing else "codex-deploy-"
    require(path.is_absolute() and path.parent == Path(ctx["backup_base"]) and
            path.name.startswith(prefix), "Not a ready backup produced by this tool in the current context")
    ancestors(path / "placeholder")
    info = state(path)
    require(info["kind"] == "directory" and info["uid"] == os.geteuid() and
            info["mode"] == 0o700, "Backup directory ownership/permissions invalid")
    for item in path.iterdir():
        item_state = state(item)
        require(item_state["kind"] == "file" and item_state["uid"] == os.geteuid() and
                item_state["mode"] == 0o600, f"Invalid private backup object: {item}")
    data = read_regular(path / "manifest.json")
    require(read_regular(path / "manifest.sha256").decode().strip() == digest(data),
            "Backup manifest checksum mismatch")
    manifest = json.loads(data)
    require(manifest["format"] == "g3stack-codex-v1" and manifest["context"] == ctx,
            "Backup format or repository/HOME/CODEX_HOME does not match")
    allowed = targets(ctx)
    directory_paths = {parent for target in allowed.values() for parent in target.parents}
    seen = set()
    for record in manifest["resources"]:
        target = Path(record["path"])
        require(target.is_absolute() and ".." not in target.parts and target not in seen,
                "Invalid or duplicate backup target")
        seen.add(target)
        if record["role"] == "directory":
            require(target in directory_paths and target not in (Path("/"), Path(ctx["home"]), ROOT),
                    "Backup directory outside integration scope")
            require(record["before"]["kind"] == "absent" and record["after"]["kind"] == "directory" or
                    record["before"]["kind"] == "directory" and record["after"]["kind"] == "absent",
                    "Invalid directory restoration record")
        else:
            require(record["role"] in allowed and target == allowed[record["role"]],
                    "Backup target outside integration scope")
        for phase in ("before", "after"):
            metadata = record[phase]
            require(metadata["kind"] in ("absent", "directory", "file", "symlink"), "Invalid backup type")
            if metadata["kind"] != "absent":
                require(metadata["uid"] == os.geteuid(), "Backup belongs to another user")
            if metadata["kind"] == "file":
                name = record[phase + "_payload"]
                require(Path(name).name == name and name.endswith(".bin"), "Invalid backup payload name")
                payload = read_regular(path / name)
                require(digest(payload) == metadata["sha256"] and len(payload) == metadata["size"],
                        f"Backup payload checksum mismatch: {name}")
    return manifest


def result_file(path, status, details):
    atomic_file(path / "result.json", encoded({"status": status, "details": details}), 0o600)


def apply_state(path, current, wanted, payload):
    ancestors(path)
    require(matches(state(path), current), f"Intervening change; refusing overwrite: {path}")
    if matches(current, wanted):
        return
    kind = wanted["kind"]
    if kind == "absent":
        if current["kind"] == "directory":
            path.rmdir()  # Never remove unrelated children recursively.
        else:
            path.unlink()
    elif kind == "directory":
        require(current["kind"] == "absent", f"Refusing directory replacement: {path}")
        path.mkdir(mode=wanted["mode"])
    elif kind == "symlink":
        require(current["kind"] == "absent", f"Refusing symlink replacement: {path}")
        path.symlink_to(wanted["target"], target_is_directory=True)
    else:
        require(current["kind"] in ("absent", "file"), f"Refusing file replacement: {path}")
        require(digest(payload) == wanted["sha256"], f"Invalid replacement payload: {path}")
        metadata = dict(wanted, create_only=current["kind"] == "absent")
        atomic_file(path, payload, wanted["mode"], metadata)
    sync_directory(path.parent)
    require(matches(state(path), wanted), f"Applied resource verification failed: {path}")


def verify_installed(ctx, expected):
    checks = checker()
    locations = targets(ctx)
    outcomes = [checks["compare"](locations["artifact"], expected, "generated artifact"),
                checks["compare"](locations["instructions"], expected, "installed global instructions"),
                checks["check_router"](locations["router"], ROOT / ".agents/skills/task-router")]
    outcomes.extend(checks["check_skill"](locations["skill:" + name], source, name)
                    for name, source in checks["skill_sources"](ROOT).items())
    outcomes.extend(state(locations["skill:" + name])["kind"] == "absent" for name in LEGACY_NAMES)
    require(all(outcomes), "Installed integration verification failed")


def transaction(ctx, entries, operation, desired_bytes, guards=None, expected=None):
    try:
        path, manifest = backup(ctx, entries, operation, desired_bytes, guards)
    except (Exception, KeyboardInterrupt) as error:
        emit({"status": "backup-failed", "managed_changes_attempted": False,
              "error": str(error), "action": "Inspect the reported backup path before retrying."})
        raise Conflict("Backup preparation failed; no managed changes attempted") from error
    try:
        for resource, info in (guards or {}).items():
            require(matches(state(Path(resource)), info), f"Preflight input changed: {resource}")
        for record in manifest["resources"]:
            target = Path(record["path"])
            payload = read_regular(path / record["after_payload"]) if "after_payload" in record else None
            apply_state(target, record["before"], record["after"], payload)
        for record in manifest["resources"]:
            require(matches(state(Path(record["path"])), record["after"]), "Final resource mismatch")
        for resource, info in (guards or {}).items():
            require(matches(state(Path(resource)), info), f"Preflight input changed: {resource}")
        if expected is not None:
            verify_installed(ctx, expected)
        result_file(path, "installed" if operation == "install" else "restored", [])
        return {"status": "installed" if operation == "install" else "restored", "backup": str(path)}
    except (Exception, KeyboardInterrupt) as error:
        restored, unresolved = [], []
        try:
            load_backup(path, ctx)
            for record in reversed(manifest["resources"]):
                target = Path(record["path"])
                try:
                    current = state(target)
                    if not matches(current, record["before"]):
                        require(matches(current, record["after"]), f"Intervening change retained: {target}")
                        data = read_regular(path / record["before_payload"]) if "before_payload" in record else None
                        apply_state(target, current, record["before"], data)
                    restored.append(str(target))
                except Exception as recovery_error:
                    unresolved.append({"path": str(target), "error": str(recovery_error)})
        except Exception as recovery_error:
            unresolved.append({"backup": str(path), "error": str(recovery_error)})
        outcome = {"error": str(error) or type(error).__name__, "restored_or_unchanged": restored,
                   "not_restored": unresolved, "backup": str(path)}
        try:
            result_file(path, "recovery-incomplete" if unresolved else "recovered", outcome)
        except Exception as result_error:
            outcome["journal_error"] = str(result_error)
        emit(outcome)
        raise Conflict("Operation failed; recovery results are reported above") from error


def install(ctx, approved):
    proposal = plan(ctx)
    emit(proposal)
    require(not proposal["conflicts"], "Preflight failed; nothing installed")
    require(approved == proposal["plan_hash"], "Install requires --approve-plan with the current reviewed plan_hash")
    expected = read_regular(ROOT / SOURCE)
    if not proposal["changes"]:
        verify_installed(ctx, expected)
        return {"status": "already-installed", "changes": []}
    base = Path(ctx["backup_base"])
    private_directories(base)
    lock = os.open(base, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Recheck the exact reviewed state after acquiring the cooperative lock.
        current = plan(ctx)
        require(current["plan_hash"] == approved, "Plan changed; rerun plan before installing")
        entries = [e for e in proposal["resources"] if not matches(e["before"], e["after"])]
        desired = {e["path"]: expected for e in entries if e["after"]["kind"] == "file"}
        return transaction(ctx, entries, "install", desired, proposal["guards"], expected)
    finally:
        os.close(lock)


def restore(ctx, backup_path):
    base = Path(ctx["backup_base"])
    path = Path(backup_path).expanduser().absolute()
    # No directory creation or mutation until the specified backup is validated.
    manifest = load_backup(path, ctx)
    lock = os.open(base, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = load_backup(path, ctx)
        entries, desired = [], {}
        for record in reversed(manifest["resources"]):
            target = Path(record["path"])
            ancestors(target)
            current = state(target)
            require(matches(current, record["before"]) or matches(current, record["after"]),
                    f"Intervening change; refusing restoration: {target}")
            if matches(current, record["before"]):
                continue
            if current["kind"] == "directory" and record["before"]["kind"] == "absent":
                # Children managed by this same backup may be removed first.
                managed = {Path(e["path"]) for e in manifest["resources"]}
                require(all(child in managed for child in target.iterdir()),
                        f"Unrelated directory contents prevent restoration: {target}")
            entries.append({"role": record["role"], "path": str(target),
                            "before": current, "after": record["before"]})
            if record["before"]["kind"] == "file":
                desired[str(target)] = read_regular(path / record["before_payload"])
        outcome = transaction(ctx, entries, "restore", desired) if entries else {"status": "already-restored"}
        # Mark an interrupted original transaction resolved only after success.
        result = path / "result.json"
        if not result.exists() or json.loads(read_regular(result)).get("status") == "recovery-incomplete":
            result_file(path, "recovered", outcome)
        drift = []
        for resource, info in manifest.get("preflight_guards", {}).items():
            try:
                if not matches(state(Path(resource)), info):
                    drift.append(resource)
            except (OSError, Conflict):
                drift.append(resource)
        outcome["input_drift_not_restored"] = drift
        outcome["limitation"] = "Repository sources/configuration are not restored; Router follows the current checkout."
        return outcome
    finally:
        os.close(lock)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=("plan", "install", "restore"), default="plan")
    parser.add_argument("--approve-plan", help="Match reviewed state; owner authorization is separately required")
    parser.add_argument("--backup", help="Verified backup directory produced by this tool (restore only)")
    args = parser.parse_args(argv)
    try:
        ctx = context()
        require(not args.approve_plan or args.command == "install", "--approve-plan is install-only")
        require(not args.backup or args.command == "restore", "--backup is restore-only")
        if args.command == "plan":
            proposal = plan(ctx)
            emit(proposal)
            return int(bool(proposal["conflicts"]))
        if args.command == "install":
            emit(install(ctx, args.approve_plan))
        else:
            require(args.backup, "Restore requires an explicit --backup path")
            emit(restore(ctx, args.backup))
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, AttributeError, Conflict) as error:
        emit({"status": "failed", "error": str(error)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
