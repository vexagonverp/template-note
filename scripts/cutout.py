#!/usr/bin/env python3
"""Turn a sticker / paper cut-out image into a transparent PNG with a clean paper edge.

  python3 scripts/cutout.py in.jpg out.png [--edge 10] [--tol 28] [--close 3] [--gray] [--split]
                                            [--paper FFFFFF] [--max 900]

A PNG that already has transparency (cut out by hand) keeps its own edges: only --edge,
--gray, --split, trimming and resizing apply.

How it works on a flat image: the background is whatever touches the image border and is close to the
border colors (one color, or two for a baked-in transparency checkerboard). Everything
else is the object. Halftone gaps are closed, holes filled, specks dropped, then a uniform
paper border of --edge px is added so every cut-out in a deck matches.
--split writes one file per separate object: out_1.png, out_2.png, ... (left to right).
Check the result on a dark and a light background before using it.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def bg_colors(a):
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    lum = edge.mean(axis=1)
    if lum.std() < 12:
        return [np.median(edge, axis=0)]
    lo, hi = edge[lum < lum.mean()], edge[lum >= lum.mean()]
    return [np.median(lo, axis=0), np.median(hi, axis=0)]


def object_mask(a, tol, close):
    dist = np.min([np.linalg.norm(a - c, axis=2) for c in bg_colors(a)], axis=0)
    cand = dist < tol
    lab, _ = ndimage.label(cand)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    fg = ~np.isin(lab, border[border > 0])
    fg = ndimage.binary_opening(fg, iterations=1)
    if close:
        fg = ndimage.binary_closing(fg, structure=disk(close), iterations=1)
    fg = ndimage.binary_fill_holes(fg)
    lab, n = ndimage.label(fg)
    if n:
        sizes = ndimage.sum(fg, lab, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s >= 0.004 * fg.size]
        fg = np.isin(lab, keep)
    return fg


def render(a, fg, edge, paper, gray):
    ring = ndimage.binary_dilation(fg, structure=disk(edge)) if edge else fg
    rgb = a.copy()
    if gray:
        g = (a @ np.array([0.299, 0.587, 0.114]))[..., None]
        rgb = np.repeat(g, 3, axis=2)
    rgb[ring & ~fg] = paper
    alpha = Image.fromarray((ring * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    img = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).convert("RGBA")
    img.putalpha(alpha)
    return img, ring


def crop(img, ring, pad):
    ys, xs = np.nonzero(ring)
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad + 1, ring.shape[1]), min(ys.max() + pad + 1, ring.shape[0]))
    return img.crop(box)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--edge", type=int, default=10, help="paper border in px (0 = none)")
    ap.add_argument("--tol", type=float, default=28, help="how far from the background color still counts as background")
    ap.add_argument("--close", type=int, default=3, help="px to close halftone gaps (0 = off)")
    ap.add_argument("--paper", default="FFFFFF", help="paper edge color, hex")
    ap.add_argument("--gray", action="store_true", help="convert the object to greyscale")
    ap.add_argument("--split", action="store_true", help="one file per separate object")
    ap.add_argument("--max", type=int, default=900, help="longest side of the output in px")
    o = ap.parse_args()

    src = Image.open(o.src)
    has_alpha = src.mode in ("RGBA", "LA", "PA") and np.asarray(src.convert("RGBA"))[..., 3].min() < 250
    pad = o.edge + 2
    if has_alpha:
        # already cut out by hand: trust its transparency, only add an edge if asked
        rgba = np.pad(np.asarray(src.convert("RGBA")).astype(float), ((pad,) * 2, (pad,) * 2, (0, 0)))
        a, src_alpha = rgba[..., :3], rgba[..., 3]
        fg = src_alpha > 16
    else:
        a = np.asarray(src.convert("RGB")).astype(float)
        # leave room for the paper edge around objects that touch the frame
        a = np.pad(a, ((pad,) * 2, (pad,) * 2, (0, 0)), mode="edge")
        fg = object_mask(a, o.tol, o.close)
        src_alpha = None
    paper = np.array([int(o.paper[i:i + 2], 16) for i in (0, 2, 4)], float)
    out = Path(o.out)
    parts = [fg]
    if o.split:
        ring_all = ndimage.binary_dilation(fg, structure=disk(o.edge)) if o.edge else fg
        lab, n = ndimage.label(ring_all)
        order = sorted(range(1, n + 1), key=lambda i: np.nonzero(lab == i)[1].mean())
        parts = [fg & (lab == i) for i in order]
    for k, part in enumerate(parts, 1):
        img, ring = render(a, part, o.edge, paper, o.gray)
        if src_alpha is not None and o.edge == 0:
            # keep the hand-made soft edge instead of a hard mask
            alpha = np.where(part, src_alpha, 0).astype(np.uint8)
            img.putalpha(Image.fromarray(alpha))
        elif src_alpha is not None:
            alpha = np.maximum(np.asarray(img)[..., 3], np.where(part, src_alpha, 0)).astype(np.uint8)
            img.putalpha(Image.fromarray(alpha))
        img = crop(img, ring, 4)
        img.thumbnail((o.max, o.max), Image.LANCZOS)
        dest = out if len(parts) == 1 else out.with_name(f"{out.stem}_{k}{out.suffix}")
        img.save(dest, optimize=True)
        print(f"{dest}  {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
