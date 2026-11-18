#!/usr/bin/env python3
"""Check Codex instruction bytes and full converted skill links without writes.

Run with Python 3 from any directory. CODEX_HOME selects the instruction
directory (default: ~/.codex). The user skill link is always under
~/.agents/skills, independent of CODEX_HOME.

Exit 0 means all required checks passed; exit 1 means FAIL or UNKNOWN.
This checks files and link resolution, not live Codex loading or behavior.
"""

import hashlib
import os
from pathlib import Path
import re
import stat


def report(status, check, detail):
    print(f"{status} {check}: {detail}")


def read_bytes(path, check, *, regular_only=False):
    try:
        if regular_only:
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    report("FAIL", check, f"path={str(path)!r}; expected a single-link regular file")
                    return None
                data = stream.read()
        else:
            data = path.read_bytes()
    except (OSError, RuntimeError) as error:
        # Do not print file contents or environment/configuration dumps.
        reason = getattr(error, "strerror", None) or type(error).__name__
        report("FAIL", check, f"path={str(path)!r}; cannot read ({reason})")
        return None
    return data


def fingerprint(data):
    return f"bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}"


def compare(path, expected, check):
    actual = read_bytes(path, check, regular_only=True)
    if actual is None:
        return False
    detail = f"path={str(path)!r}; {fingerprint(actual)}"
    if expected is None:
        report("UNKNOWN", check, detail + "; expected bytes unavailable")
        return False
    matches = actual == expected
    report("PASS" if matches else "FAIL", check,
           detail + ("; matches expected bytes" if matches else
                     "; byte mismatch; expected " + fingerprint(expected)))
    return matches


def skill_sources(root):
    """Discover the maintained library from native manifests, not a registry."""
    library = root / "codex/skills"
    if not library.is_dir() or library.is_symlink():
        raise ValueError("Missing or linked g3stack skill library")
    result = {}
    for source in sorted(library.iterdir()):
        if source.is_symlink() or not source.is_dir():
            raise ValueError(f"Invalid skill directory: {source}")
        manifest = source / "SKILL.md"
        if manifest.is_symlink() or not manifest.is_file():
            raise ValueError(f"Missing or linked skill manifest: {manifest}")
        body = manifest.read_text(encoding="utf-8")
        frontmatter = body.split("---", 2)
        if not body.startswith("---\n") or len(frontmatter) != 3:
            raise ValueError(f"Invalid skill frontmatter: {manifest}")
        name = re.search(r"(?m)^name: ([a-z0-9-]+)$", frontmatter[1])
        description = re.search(r"(?m)^description: (.+)$", frontmatter[1])
        if not name or name.group(1) != source.name or not description:
            raise ValueError(f"Invalid skill identity/description: {manifest}")
        result[source.name] = source
    if not result:
        raise ValueError("Empty g3stack skill library")
    return result


def check_skill(link, source, name):
    check = name + " link"
    detail = f"path={str(link)!r}; expected source={str(source)!r}"
    try:
        # Strict resolution rejects missing targets and symlink loops.
        expected = source.resolve(strict=True)
        if not expected.is_dir():
            report("FAIL", check, detail + "; source is not a directory")
            return False
        if not link.is_symlink():
            report("FAIL", check, detail + "; missing or not a symlink")
            return False
        actual = link.resolve(strict=True)
        detail += f"; resolved={str(actual)!r}"
        if actual != expected:
            report("FAIL", check, detail + "; target mismatch")
            return False
    except (OSError, RuntimeError) as error:
        reason = getattr(error, "strerror", None) or type(error).__name__
        report("FAIL", check, detail + f"; cannot resolve source/link ({reason})")
        return False
    manifest = read_bytes(actual / "SKILL.md", "task-router SKILL.md")
    if manifest is None:
        return False
    if not manifest.strip():
        report("FAIL", check, detail + "; SKILL.md is empty")
        return False
    report("PASS", check, detail + "; SKILL.md " + fingerprint(manifest))
    return True


def check_router(link, source):
    return check_skill(link, source, "task-router")


def main():
    root = Path(__file__).resolve().parent.parent
    try:
        home = Path.home()
        codex_home = Path(os.environ.get("CODEX_HOME") or home / ".codex")
        codex_home = codex_home.expanduser().absolute()
    except (OSError, RuntimeError, ValueError) as error:
        report("FAIL", "global paths", f"cannot determine home ({type(error).__name__})")
        return 1
    print(f"Repository: {str(root)!r}")
    print(f"Codex home: {str(codex_home)!r}")

    source = root / "instructions/personal.md"
    # The global is one source's raw bytes, without concatenation or normalization.
    expected = read_bytes(source, "personal source", regular_only=True)
    if expected is not None and not expected.strip():
        report("FAIL", "personal source", "source is empty")
        expected = None
    if expected is None:
        report("UNKNOWN", "expected artifact", "personal source unavailable or empty")
    else:
        report("PASS", "expected artifact", fingerprint(expected))

    generated_ok = compare(root / "integrations/codex/AGENTS.generated.md",
                           expected, "generated artifact")
    installed_ok = compare(codex_home / "AGENTS.md", expected,
                           "installed global instructions")
    router_ok = check_router(home / ".agents/skills/task-router",
                             root / ".agents/skills/task-router")
    try:
        results = [check_skill(home / ".agents/skills" / name, source, name)
                   for name, source in skill_sources(root).items()]
        library_ok = all(results)
    except (OSError, ValueError) as error:
        report("FAIL", "skill library", str(error))
        library_ok = False
    return 0 if generated_ok and installed_ok and router_ok and library_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
