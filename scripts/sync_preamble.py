#!/usr/bin/env python3
"""Stamp shared preambles into the templates (and optionally into notes).

Usage:
    python3 scripts/sync_preamble.py                 # every templates/*.tex with markers
    python3 scripts/sync_preamble.py --check         # exit 1 if anything is out of date
    python3 scripts/sync_preamble.py Course/notes/X.tex   # also update a note with markers

A file takes part if it has the two marker lines. The start marker names the shared file:
    % >>> SHARED PREAMBLE (templates/_exam_preamble.tex, do not edit here)
    % <<< SHARED PREAMBLE
Shared files: templates/_exam_preamble.tex (exam sheets) and
templates/_report_preamble.tex (lab reports, reports, proposals, essays, scripts).
Everything between the markers is replaced. Nothing outside them changes.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
START = re.compile(r"^% >>> SHARED PREAMBLE \((templates/[\w.]+), do not edit here\)$", re.M)
END = "% <<< SHARED PREAMBLE"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    files = [pathlib.Path(a).resolve() for a in args] or sorted((ROOT / "templates").glob("*.tex"))
    stale = 0
    for f in files:
        s = f.read_text(encoding="utf-8")
        m = START.search(s)
        if not m or END not in s[m.end():]:
            continue
        shared = (ROOT / m.group(1)).read_text(encoding="utf-8").rstrip("\n")
        tail = s[m.end():].split(END, 1)[1]
        new = s[:m.end()] + "\n" + shared + "\n" + END + tail
        if new != s:
            stale += 1
            rel = f.relative_to(ROOT) if f.is_relative_to(ROOT) else f
            print(f"{'out of date' if check else 'synced'}: {rel}  <- {m.group(1)}")
            if not check:
                f.write_text(new, encoding="utf-8")
    if check:
        print("all in sync" if not stale else f"{stale} file(s) out of date")
        sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
