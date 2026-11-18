"""Read-only integrity verification for pinned bundled Engineering sources."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


def verify(root):
    root = Path(root).resolve(strict=True)
    manifest = json.loads((root / "source-manifest.json").read_text())
    if manifest.get("format") != "g3stack-vendored-sources-v1":
        raise ValueError("Unsupported source manifest")
    expected, errors = set(), []
    for source in manifest["sources"].values():
        for record in source["files"]:
            relative = Path(record["path"])
            if not relative.parts or relative.is_absolute() or ".." in relative.parts or relative.parts[0] not in manifest["sources"]:
                raise ValueError("Source path escapes the vendor tree")
            if relative.as_posix() in expected:
                raise ValueError("Duplicate source path")
            expected.add(relative.as_posix())
            path = root / relative
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
                errors.append({"path": relative.as_posix(), "error": "missing or linked file"})
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
                errors.append({"path": relative.as_posix(), "error": "source changed"})
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append({"path": path.relative_to(root).as_posix(), "error": "linked source entry"})
        elif path.is_file() and path != root / "source-manifest.json":
            actual.add(path.relative_to(root).as_posix())
    for name in sorted(actual - expected):
        errors.append({"path": name, "error": "unlisted source file"})
    if not expected:
        raise ValueError("Empty source manifest")
    return {"status": "FAIL" if errors else "PASS", "files": len(expected), "errors": errors,
            "limits": "Source integrity only; does not establish host activation, command execution or agent quality."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2] / "vendor")
    args = parser.parse_args()
    try:
        result = verify(args.root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {"status": "FAIL", "errors": [str(error)]}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
