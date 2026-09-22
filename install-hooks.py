#!/usr/bin/env python3
"""Install the git hooks in hooks/ into this clone.

Git does not track .git/hooks, so a hook committed to the repository does
nothing until it is copied into place. Run this once per clone:

    python install-hooks.py

It only copies; it never overwrites a hook you wrote yourself without saying
so first.
"""
import os
import pathlib
import shutil
import stat
import sys

HERE = pathlib.Path(__file__).parent
SRC = HERE / "hooks"
DST = HERE / ".git" / "hooks"


def main():
    if not DST.is_dir():
        print("No .git/hooks here — is this a git clone?", file=sys.stderr)
        return 1
    if not SRC.is_dir():
        print("No hooks/ directory to install from.", file=sys.stderr)
        return 1

    installed = 0
    for hook in sorted(SRC.iterdir()):
        if not hook.is_file():
            continue
        target = DST / hook.name
        if target.exists() and target.read_bytes() != hook.read_bytes():
            print("  %s already exists and differs — leaving it alone." % hook.name)
            print("    Replace it by hand if you want this one:")
            print("      cp hooks/%s .git/hooks/%s" % (hook.name, hook.name))
            continue
        shutil.copyfile(str(hook), str(target))
        # chmod +x. Git for Windows runs hooks through its bundled sh, where
        # the mode does not matter, but it does everywhere else.
        os.chmod(str(target), os.stat(str(target)).st_mode | stat.S_IXUSR |
                 stat.S_IXGRP | stat.S_IXOTH)
        print("  installed %s" % hook.name)
        installed += 1

    if installed:
        print("\nDone. `git push` now runs check.py first and stops if it fails.")
    else:
        print("\nNothing new to install.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
