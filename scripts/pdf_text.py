#!/usr/bin/env python3
"""Print the text of a PDF page by page, and list pages that look image-only.

Usage:
    python3 scripts/pdf_text.py slides.pdf            # all pages
    python3 scripts/pdf_text.py slides.pdf 5 12       # pages 5..12
    python3 scripts/pdf_text.py slides.pdf > .temp/slides.txt

Uses pypdf if installed, otherwise falls back to `pdftotext` (poppler).
Pages with almost no text are probably diagrams or screenshots: rasterize them
with scripts/pdf_pages.sh and read the image instead of guessing.
"""
import shutil
import subprocess
import sys


def pages_pypdf(path):
    from pypdf import PdfReader  # type: ignore
    return [(p.extract_text() or "").strip() for p in PdfReader(path).pages]


def pages_pdftotext(path):
    out = subprocess.run(["pdftotext", "-layout", path, "-"],
                         capture_output=True, text=True, check=True).stdout
    return [p.strip() for p in out.split("\f")][:-1] or [out.strip()]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    try:
        pages = pages_pypdf(path)
    except ImportError:
        if not shutil.which("pdftotext"):
            sys.exit("Install pypdf (pip install pypdf) or poppler (pdftotext).")
        pages = pages_pdftotext(path)
    first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    last = int(sys.argv[3]) if len(sys.argv) > 3 else len(pages)
    empty = []
    for i in range(first - 1, min(last, len(pages))):
        print(f"--- p{i + 1} ---")
        print(pages[i])
        if len(pages[i]) < 40:
            empty.append(i + 1)
    if empty:
        print(f"\n[image-only? rasterize these pages: {empty}]", file=sys.stderr)


if __name__ == "__main__":
    main()
