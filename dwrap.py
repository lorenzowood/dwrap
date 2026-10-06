#!/usr/bin/env python3
"""dwrap - wrap in directory.

For every argument that is a file (not a directory), create a directory named
after it and move the file inside.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

__version__ = "0.1.0"


def unique_dir(parent, name, file, reserved):
    """Return a directory path under parent that doesn't clash with anything.

    The file being wrapped doesn't count as a clash, since it is moved out of
    the way before the directory takes its name.
    """
    candidate = parent / name
    n = 0
    while (candidate.exists() and candidate != file) or candidate in reserved:
        n += 1
        candidate = parent / f"{name} ({n})"
    return candidate


def wrap(file, preserve_extensions, dry_run, reserved):
    parent = file.parent
    name = file.name if preserve_extensions else file.stem
    target = unique_dir(parent, name, file, reserved)
    reserved.add(target)
    if target.name != name:
        print(f"warning: {parent / name} exists; using {target.name}", file=sys.stderr)
    print(f"{file} -> {target / file.name}")
    if dry_run:
        return
    # Build in a temporary directory then rename it, so that a directory may
    # take the same name as the file it contains.
    tmp = Path(tempfile.mkdtemp(prefix=".dwrap-", dir=parent))
    try:
        file.rename(tmp / file.name)
        tmp.rename(target)
    except BaseException:
        if (tmp / file.name).exists() and not file.exists():
            (tmp / file.name).rename(file)
        tmp.rmdir()
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="dwrap",
        description="Wrap each file in a directory of the same name.",
    )
    parser.add_argument("paths", nargs="+", metavar="PATH", help="files to wrap (directories are ignored)")
    parser.add_argument("--dry-run", action="store_true", help="show what would be done without doing it")
    parser.add_argument(
        "--preserve-extensions",
        action="store_true",
        help="name the directory after the full file name, including its extension",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    status = 0
    reserved = set()
    for p in args.paths:
        path = Path(p)
        if not os.path.lexists(path):
            print(f"dwrap: {p}: no such file or directory", file=sys.stderr)
            status = 1
        elif path.is_dir():
            continue
        else:
            try:
                wrap(path, args.preserve_extensions, args.dry_run, reserved)
            except OSError as e:
                print(f"dwrap: {p}: {e}", file=sys.stderr)
                status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
