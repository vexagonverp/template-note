#!/usr/bin/env python3
"""Tile many page images into a few grid images, so a whole deck can be scanned fast.

Usage:
    scripts/pdf_pages.sh slides.pdf 1 60 50          # small renders first
    python3 scripts/contact_sheet.py .temp/imgs/slides-*.png
    python3 scripts/contact_sheet.py --cols 4 --per 12 .temp/imgs/slides-*.png

Writes .temp/grids/grid_001.png, grid_002.png, ... each with a page label.
Needs Pillow (pip install pillow).
"""
import argparse
import pathlib
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("pip install pillow")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--per", type=int, default=16, help="pages per grid image")
    ap.add_argument("--width", type=int, default=420, help="tile width in px")
    a = ap.parse_args()
    files = sorted(a.images)
    root = pathlib.Path(__file__).resolve().parent.parent
    out = root / ".temp" / "grids"
    out.mkdir(parents=True, exist_ok=True)
    for g in range(0, len(files), a.per):
        chunk = files[g:g + a.per]
        tiles = []
        for f in chunk:
            im = Image.open(f).convert("RGB")
            im = im.resize((a.width, int(im.height * a.width / im.width)))
            tiles.append((pathlib.Path(f).stem, im))
        h = max(t.height for _, t in tiles) + 18
        rows = -(-len(tiles) // a.cols)
        sheet = Image.new("RGB", (a.cols * (a.width + 6), rows * h), "white")
        d = ImageDraw.Draw(sheet)
        for k, (name, im) in enumerate(tiles):
            x, y = (k % a.cols) * (a.width + 6), (k // a.cols) * h
            sheet.paste(im, (x, y + 16))
            d.text((x + 2, y + 2), name, fill="black")
        path = out / f"grid_{g // a.per + 1:03d}.png"
        sheet.save(path)
        print(path.relative_to(root))


if __name__ == "__main__":
    main()
