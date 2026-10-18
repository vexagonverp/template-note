#!/usr/bin/env python3
"""Build a long .tex one section at a time to find a hang, an error, or ugly pages.

Usage:
    python3 scripts/build_sections.py Course/notes/Sheet.tex            # split at \\section
    python3 scripts/build_sections.py Course/notes/Sheet.tex --at examPart
    python3 scripts/build_sections.py Sheet.tex --timeout 60

Each piece = the file's preamble + one chunk + \\end{document}, written to
.temp/sections/<name>/part_NN.tex and built with tectonic under a timeout.
Prints OK / FAIL / HANG and the Overfull warnings per piece. Cross-references
(\\pageref) will be '??' in pieces; that is expected.
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--at", default="section", help="command to split at (section, examPart, part)")
    ap.add_argument("--timeout", type=int, default=90)
    a = ap.parse_args()
    src = pathlib.Path(a.tex).resolve()
    s = src.read_text(encoding="utf-8")
    pre, body = s.split("\n\\begin{document}", 1)
    body = body.rsplit("\\end{document}", 1)[0]
    cuts = [m.start() for m in re.finditer(r"(?m)^\\" + re.escape(a.at) + r"\*?\{", body)]
    chunks = [body[i:j] for i, j in zip([0] + cuts, cuts + [len(body)])]
    root = pathlib.Path(__file__).resolve().parent.parent
    out = root / ".temp" / "sections" / src.stem
    out.mkdir(parents=True, exist_ok=True)
    for f in src.parent.iterdir():  # images / .sty the sheet may need
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".sty", ".cls", ".bib"} and f.stem != src.stem:
            shutil.copy2(f, out / f.name)
    bad = 0
    for n, chunk in enumerate(chunks):
        title = (re.search(r"\{([^}]*)\}", chunk) or [None, "(preamble text)"])[1][:60]
        p = out / f"part_{n:02d}.tex"
        p.write_text(pre + "\n\\begin{document}\n" + chunk + "\n\\end{document}\n", encoding="utf-8")
        try:
            r = subprocess.run(["tectonic", p.name], cwd=out, capture_output=True, text=True, timeout=a.timeout)
            log = r.stdout + r.stderr
            status = "OK  " if r.returncode == 0 else "FAIL"
        except subprocess.TimeoutExpired:
            log, status = "", "HANG"
        if status != "OK  ":
            bad += 1
        print(f"{status} part_{n:02d}  {title}")
        for line in sorted(set(l for l in log.splitlines() if "Overfull" in l or "error" in l.lower())):
            print("       " + line.strip()[:150])
    print(f"\n{len(chunks)} pieces in {out.relative_to(root)}/, {bad} failed or hung")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
