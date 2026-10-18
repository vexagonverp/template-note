#!/usr/bin/env python3
"""Print the text of a .pptx deck slide by slide, with speaker notes.

Usage:
    python3 scripts/pptx_text.py "Chapter 04 - Quality Attributes.pptx" > .temp/ch04.txt

Needs nothing but the Python standard library (python-pptx / LibreOffice are not
required). Slides with almost no text are flagged: they are diagrams. To see them,
export the deck to PDF (Keynote / PowerPoint: File > Export > PDF) and run
scripts/pdf_pages.sh on that PDF.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def paragraphs(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for p in root.iter(f"{A}p"):
        text = "".join(t.text or "" for t in p.iter(f"{A}t")).strip()
        if text:
            out.append(text)
    return out


def num(name):
    return int(re.search(r"(\d+)\.xml$", name).group(1))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    z = zipfile.ZipFile(sys.argv[1])
    names = z.namelist()
    slides = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=num)
    notes = {num(n): n for n in names if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)}
    media = [n for n in names if n.startswith("ppt/media/")]
    empty = []
    for s in slides:
        i = num(s)
        lines = paragraphs(z.read(s))
        print(f"--- slide {i} ---")
        print("\n".join(lines))
        if i in notes:
            note = [l for l in paragraphs(z.read(notes[i])) if not l.isdigit()]
            if note:
                print("[notes] " + " ".join(note))
        if sum(len(l) for l in lines) < 40:
            empty.append(i)
    print(f"\n[{len(slides)} slides, {len(media)} embedded media files]", file=sys.stderr)
    if empty:
        print(f"[mostly images, export to PDF and look at slides: {empty}]", file=sys.stderr)


if __name__ == "__main__":
    main()
