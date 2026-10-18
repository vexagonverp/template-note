#!/usr/bin/env python3
"""Apply exact text replacements to a file, safely. Dry run unless --write.

Usage:
    python3 scripts/apply_patches.py notes/Sheet.tex .temp/patches.py          # show diff
    python3 scripts/apply_patches.py notes/Sheet.tex .temp/patches.py --write  # apply

The patch file is Python that defines a list R of (old, new) pairs:

    R = [
        (r"It is important to note that the dual", r"The dual"),
        (r"\\textbf{Step 1.}", r"\\step{1}{Lagrangian}"),
    ]

Every `old` must appear EXACTLY ONCE in the file, otherwise nothing is written.
That stops a wording pass from silently hitting the wrong place.
Before a big restructure, keep a copy: .temp/<name>_before_<step>.tex
"""
import difflib
import runpy
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    path, patch, write = sys.argv[1], sys.argv[2], "--write" in sys.argv
    s0 = open(path, encoding="utf-8").read()
    s = s0
    pairs = runpy.run_path(patch)["R"]
    problems = []
    for k, (old, new) in enumerate(pairs, 1):
        n = s.count(old)
        if n != 1:
            problems.append(f"pair {k}: found {n} times: {old[:70]!r}")
            continue
        s = s.replace(old, new)
    if problems:
        print("\n".join(problems))
        sys.exit("nothing written: fix the pairs above")
    diff = difflib.unified_diff(s0.splitlines(), s.splitlines(), path, path + " (patched)", lineterm="", n=1)
    print("\n".join(diff))
    if write:
        open(path, "w", encoding="utf-8").write(s)
        print(f"\nwrote {len(pairs)} change(s) to {path}")
    else:
        print(f"\n(dry run: {len(pairs)} change(s) ok; add --write to apply)")


if __name__ == "__main__":
    main()
