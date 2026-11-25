#!/usr/bin/env python3
"""Draws the hand-cut shapes of the Clay Blocks style. Same output every run (fixed seeds).

  python3 docs/design/clay-blocks/make_shapes.py css            # block outlines + motif masks (the GENERATED part of style.css)
  python3 docs/design/clay-blocks/make_shapes.py scene <scene>  # one inline <svg>; in a deck write {{scene <scene>}} instead

Poster (title) scenes:   poster                    hills, trees, one house
                         campus                    hills, trees, a university building
                         ground <motif> [motif..]  1-5 big motifs standing on the hills, the last one turquoise
Picture-block scenes:    house                     house, trees, sun
                         pic <motif> [motif]       one or two big motifs on the ground
Brown-slide bottoms:     street [lit]              row of houses (lit = one turquoise window)
                         row <motif> [motif..]     a row of 3-6 motifs
Motifs: run `make_shapes.py motifs`. Scenes use var(--clay), var(--iron), var(--turq).
"""
import math
import random
import sys
from urllib.parse import quote

AREA = .92   # every block outline keeps exactly 92% of its box, so block areas stay comparable
C, I, T = "var(--clay)", "var(--iron)", "var(--turq)"


def shoelace(p):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(p, p[1:] + p[:1]))) / 2


def cut(p, j, step, rnd):
    """Polygon with slightly wobbly edges, like scissors or a knife."""
    out = []
    for a, b in zip(p, p[1:] + p[:1]):
        m = max(1, round(math.dist(a, b) / step))
        for q in range(m):
            out.append((a[0] + (b[0] - a[0]) * q / m + (rnd.random() - .5) * 2 * j,
                        a[1] + (b[1] - a[1]) * q / m + (rnd.random() - .5) * 2 * j))
    return out


def path(p):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in p) + "Z"


def outline(seed):
    """Uneven block outline in percent of its box, area exactly AREA."""
    r = random.Random(seed)
    u = lambda: r.random() * 8
    p = [(u(), u()), (50 + r.uniform(-8, 8), u() * .5), (100 - u(), u()), (100 - u() * .4, 52 + r.uniform(-8, 8)),
         (100 - u(), 100 - u()), (46 + r.uniform(-8, 8), 100 - u() * .4), (u(), 100 - u()), (u() * .4, 50 + r.uniform(-8, 8))]
    k = math.sqrt(AREA * 1e4 / shoelace(p))
    cx, cy = sum(x for x, _ in p) / 8, sum(y for _, y in p) / 8
    p = [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in p]
    return p if all(-.01 <= v <= 100.01 for q in p for v in q) else None


def ring(cx, cy, r, m=14):
    return [(cx + r * math.cos(i * 2 * math.pi / m), cy + r * math.sin(i * 2 * math.pi / m)) for i in range(m)]


def star(cx, cy, a, b, m):
    return [(cx + (b if i % 2 else a) * math.cos(i * math.pi / m - .2), cy + (b if i % 2 else a) * math.sin(i * math.pi / m - .2)) for i in range(2 * m)]


def leaf(x, y, L, a, w):
    return [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a))
            for px, py in [(0, 0), (L * .35, -w), (L * .7, -w * .8), (L, 0), (L * .65, w * .75), (L * .3, w * .8)]]


def rect(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


# motif -> (solid parts, holes), on a 100 x 100 box
MOTIFS = {
    "house": ([[(8, 50), (50, 12), (92, 50), (84, 50), (84, 90), (16, 90), (16, 50)]], [rect(43, 62, 16, 28), rect(24, 56, 11, 12), rect(67, 56, 10, 12)]),
    "tower": ([rect(26, 6, 48, 90)], [rect(x, y, 11, 12) for x in (35, 54) for y in (18, 42, 66)]),
    "door": ([[(24, 96), (24, 34), (34, 14), (50, 6), (66, 14), (76, 34), (76, 96)]], [rect(34, 40, 13, 24), rect(53, 40, 13, 24), ring(65, 76, 4, 7)]),
    "key": ([ring(27, 50, 23), [(44, 43), (96, 43), (96, 66), (86, 66), (86, 56), (78, 56), (78, 64), (69, 64), (69, 56), (44, 56)]], [ring(25, 50, 9)]),
    "pin": ([[(50, 96), (24, 56), (18, 36), (26, 16), (44, 6), (60, 6), (76, 17), (82, 36), (76, 56)]], [ring(50, 37, 14)]),
    "sun": ([star(50, 50, 46, 27, 9)], [ring(50, 50, 13)]),
    "hill": ([[(2, 86), (26, 38), (42, 60), (66, 18), (98, 86)]], [[(66, 18), (78, 44), (70, 40), (64, 52), (60, 34)]]),
    "tree": ([[(50, 4), (66, 18), (76, 42), (72, 64), (55, 74), (55, 96), (45, 96), (45, 74), (28, 64), (24, 42), (34, 18)]], [[(48, 30), (52, 30), (51, 70), (49, 70)]]),
    "flower": ([ring(50, 24, 20, 9), ring(76, 50, 20, 9), ring(50, 76, 20, 9), ring(24, 50, 20, 9), ring(50, 50, 20, 9)], [ring(50, 50, 12, 8)]),
    "person": ([ring(50, 27, 19, 12), [(14, 94), (18, 68), (34, 54), (66, 54), (82, 68), (86, 94)]], []),
    "paper": ([[(20, 6), (64, 6), (82, 24), (82, 94), (20, 94)]], [rect(32, 32, 38, 7), rect(32, 50, 38, 7), rect(32, 68, 24, 7)]),
    "search": ([ring(40, 40, 33, 14), [(58, 66), (66, 58), (96, 86), (86, 96)]], [ring(40, 40, 20, 12)]),
    "chart": ([rect(8, 58, 20, 34), rect(40, 36, 20, 56), rect(72, 10, 20, 82)], []),
    "network": ([ring(50, 20, 16, 10), ring(18, 78, 16, 10), ring(82, 78, 16, 10), [(46, 24), (54, 24), (26, 80), (16, 76)], [(46, 24), (54, 24), (84, 76), (74, 80)], rect(18, 74, 64, 8)], []),
    "screen": ([rect(6, 12, 88, 60), [(40, 72), (60, 72), (64, 88), (36, 88)], rect(26, 86, 48, 7)], [rect(15, 21, 70, 42)]),
    "phone": ([rect(26, 4, 48, 92)], [rect(34, 14, 32, 62), ring(50, 86, 5, 8)]),
    "check": ([[(8, 54), (24, 38), (42, 56), (78, 14), (94, 30), (44, 88)]], []),
    "cross": ([[(14, 26), (26, 14), (50, 38), (74, 14), (86, 26), (62, 50), (86, 74), (74, 86), (50, 62), (26, 86), (14, 74), (38, 50)]], []),
    "question": ([[(22, 34), (26, 16), (42, 6), (62, 8), (76, 20), (78, 38), (68, 52), (58, 60), (58, 70), (42, 70), (42, 54), (56, 44), (60, 34), (56, 25), (46, 23), (40, 34)], rect(42, 79, 16, 15)], []),
    "box": ([[(8, 30), (50, 8), (92, 30), (92, 74), (50, 95), (8, 74)]], [[(47, 52), (53, 52), (53, 86), (47, 86)], [(15, 35), (19, 32), (50, 47), (81, 32), (85, 35), (50, 53)]]),
    "letter": ([rect(6, 20, 88, 62)], [[(12, 26), (20, 25), (50, 51), (80, 25), (88, 26), (50, 60)]]),
    "arrow": ([[(6, 40), (54, 40), (54, 18), (94, 50), (54, 82), (54, 60), (6, 60)]], []),
    "list": ([rect(8, 12, 18, 18), rect(8, 41, 18, 18), rect(8, 70, 18, 18), rect(36, 15, 56, 12), rect(36, 44, 56, 12), rect(36, 73, 56, 12)], []),
    "clock": ([ring(50, 50, 44, 16)], [[(46, 20), (54, 20), (54, 47), (76, 58), (72, 66), (46, 53)]]),
    "bulb": ([[(50, 4), (72, 10), (84, 30), (80, 48), (66, 62), (64, 74), (36, 74), (34, 62), (20, 48), (16, 30), (28, 10)], rect(37, 78, 26, 7), rect(41, 88, 18, 7)], []),
    "lock": ([rect(16, 44, 68, 50), [(26, 46), (26, 24), (38, 8), (62, 8), (74, 24), (74, 46), (62, 46), (62, 28), (56, 20), (44, 20), (38, 28), (38, 46)]], [ring(50, 65, 8, 8), rect(47, 68, 6, 14)]),
    "unlock": ([rect(16, 46, 68, 48), [(26, 48), (26, 22), (38, 6), (62, 6), (74, 22), (74, 32), (62, 32), (62, 26), (56, 18), (44, 18), (38, 26), (38, 48)]], [ring(50, 65, 8, 8), rect(47, 68, 6, 14)]),
    "book": ([[(4, 18), (28, 12), (48, 20), (48, 90), (28, 82), (4, 88)], [(52, 20), (72, 12), (96, 18), (96, 88), (72, 82), (52, 90)]], [rect(14, 34, 24, 6), rect(14, 50, 24, 6), rect(62, 34, 24, 6), rect(62, 50, 24, 6)]),
    "code": ([[(30, 22), (40, 32), (22, 50), (40, 68), (30, 78), (2, 50)], [(70, 22), (98, 50), (70, 78), (60, 68), (78, 50), (60, 32)], [(54, 14), (63, 17), (46, 86), (37, 83)]], []),
    "cart": ([[(2, 14), (20, 14), (25, 30), (94, 30), (84, 64), (32, 64), (14, 24), (2, 24)], ring(38, 80, 10, 10), ring(74, 80, 10, 10)], []),
    "campus": ([[(4, 36), (50, 8), (96, 36), (96, 44), (4, 44)], rect(12, 48, 12, 36), rect(34, 48, 12, 36), rect(54, 48, 12, 36), rect(76, 48, 12, 36), rect(4, 86, 92, 9)], [ring(50, 28, 6, 8)]),
    "sprig": ([rect(48, 4, 4, 92)] + [leaf(50, y, L, a, w) for y, L, w in ((84, 38, 9), (60, 36, 9), (36, 32, 8)) for a in (-.6, -2.54)], []),
}


def motif_uri(name):
    r = random.Random(name)
    solid, holes = MOTIFS[name]
    d = lambda ps: " ".join(path(cut(p, .8, 18, r)) for p in ps)
    body = f"<mask id='m'><path d='{d(solid)}' fill='#fff'/><path d='{d(holes)}' fill='#000'/></mask><path d='M0 0H100V100H0Z' mask='url(#m)'/>"
    return "url(\"data:image/svg+xml," + quote(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>{body}</svg>", safe="/:=' ,()") + "\")"


def css():
    n, seed = 0, 1
    print("/* GENERATED by make_shapes.py css: block outlines (each keeps 92% of its box) and motif masks */")
    print(":root {")
    while n < 6:
        p = outline(seed)
        seed += 1
        if not p:
            continue
        n += 1
        print(f"  --cut-{n}: polygon({', '.join(f'{x:.2f}% {y:.2f}%' for x, y in p)});")
    for m in MOTIFS:
        print(f"  --m-{m}: {motif_uri(m)};")
    print("}")
    for m in MOTIFS:
        print(f".motif.{m} {{ --m: var(--m-{m}); }}")


P = lambda p, f, x="": f'<path d="{path(p)}" fill="{f}"{" " + x if x else ""}/>'


def tree(x, y, w, h, f, r):
    s = [(0, -1), (.34, -.82), (.5, -.5), (.42, -.22), (.1, -.1), (.07, 0)]
    return P(cut([(x + a * w, y + b * h) for a, b in s] + [(x - a * w, y + b * h) for a, b in s[:0:-1]], 1.4, 24, r), f)


def cottage(x, y, s, roof, halo, hw, r):
    pt = lambda a: [(x + u * s, y + v * s) for u, v in a]
    g, side = cut(pt([(0, 42), (20, 0), (42, 42), (42, 100), (0, 100)]), 1, 30, r), cut(pt([(42, 42), (130, 42), (130, 96), (42, 100)]), 1, 30, r)
    rf = cut(pt([(20, 0), (112, 0), (134, 44), (42, 44)]), 1.2, 30, r)
    o = f'<path d="{path(g)}{path(side)}{path(rf)}" fill="{halo}" stroke="{halo}" stroke-width="{hw}" stroke-linejoin="round"/>'
    o += P(g, C) + P(side, C) + P(rf, roof) + P(pt(rect(42, 42, 2.5, 58)), I)
    return o + P(ring(x + 21 * s, y + 38 * s, 7 * s, 8), I) + P(cut(pt(rect(58, 58, 16, 16)), .6, 20, r), I) + P(cut(pt(rect(96, 58, 17, 39)), .6, 20, r), I)


def big(name, x, y, s, f, hole, halo, r):
    """A motif drawn with size s and its foot at (x, y); halo = outline color, so it reads on any ground."""
    solid, holes = MOTIFS[name]
    foot = max(q[1] for p in solid for q in p)
    pt = lambda p: [(x + (a - 50) * s / 100, y + (b - foot) * s / 100) for a, b in p]
    parts = [cut(pt(p), .9 * s / 100, 18 * s / 100, r) for p in solid]
    o = f'<path d="{"".join(map(path, parts))}" fill="{halo}" stroke="{halo}" stroke-width="14" stroke-linejoin="round"/>' if halo else ""
    return o + "".join(P(p, f) for p in parts) + "".join(P(cut(pt(p), .8 * s / 100, 18 * s / 100, r), hole) for p in holes)


def row(pts, f, w):
    d = f"M{pts[0][0]} {pts[0][1]}"
    for k in range(len(pts) - 1):
        a, b, c = pts[max(k - 1, 0)], pts[k], pts[k + 1]
        e = pts[min(k + 2, len(pts) - 1)]
        d += f"C{b[0] + (c[0] - a[0]) / 6:.1f} {b[1] + (c[1] - a[1]) / 6:.1f} {c[0] - (e[0] - b[0]) / 6:.1f} {c[1] - (e[1] - b[1]) / 6:.1f} {c[0]} {c[1]}"
    return f'<path d="{d}" fill="none" stroke="{f}" stroke-width="{w}" stroke-linecap="round"/>'


def scene(name, *what):
    r = random.Random(7)
    bad = [m for m in what if m not in MOTIFS and m != "lit"]
    if bad:
        sys.exit(f"unknown motif {', '.join(bad)}. Have: {' '.join(MOTIFS)}")
    if name in ("poster", "campus", "ground"):   # box 1472 x 636, the ground fills the bottom third; the title goes above
        w, h = 1472, 636
        far = cut([(496, 670), (696, 466), (836, 386), (946, 346), (1036, 382), (1166, 416), (1296, 364), (1396, 338), (1540, 416), (1540, 670)], 2, 60, r)
        near = cut([(-44, 506), (66, 416), (186, 344), (266, 398), (346, 446), (436, 398), (516, 370), (626, 446), (756, 536), (836, 586), (836, 670), (-44, 670)], 2, 60, r)
        o = "".join(f'<path d="{path(p)}" fill="{C}" stroke="{I}" stroke-width="14" stroke-linejoin="round"/>' for p in (far, near))
        o += "".join(tree(*a, I, r) for a in ((914, 498, 56, 96), (1228, 486, 62, 82), (1288, 492, 50, 70), (1360, 498, 64, 118), (366, 558, 58, 120), (422, 556, 46, 92)) if name != "ground")
        o += P([(-24, 586), (196, 536), (456, 550), (696, 512), (936, 476), (1176, 466), (1500, 506), (1500, 670), (-24, 670)], I)
        if name == "poster":
            o += cottage(946, 378, 1.22, T, I, 10, r)
        elif name == "campus":
            o += big("campus", 1060, 514, 176, C, I, I, r) + P([(979, 423), (1060, 372), (1141, 423), (1141, 437), (979, 437)], T)
        else:
            k = len(what)
            for i, m in enumerate(what[:5]):
                x = 700 + (i - (k - 1) / 2) * min(250, 1100 / max(k, 1)) + (120 if k < 4 else 0)
                o += big(m, x, 566 - (x - 300) * .03, 176 if k < 4 else 148, T if i == k - 1 else C, I, I, r)
        front = cut([(-24, 544), (116, 552), (316, 580), (536, 618), (700, 650), (700, 690), (-24, 690)], 1.2, 60, r)
        o += f'<path d="{path(front)}" fill="{C}" stroke="{I}" stroke-width="10"/>'
        o += "".join(row([(6, 580 + q * 24), (136, 590 + q * 24), (316, 618 + q * 24), (496, 652 + q * 24)], I, 5) for q in range(3))
    elif name == "house":  # box 560 x 700
        w, h = 560, 700
        o = P(cut(star(424, 170, 104, 70, 11), 2, 40, r), C) + tree(470, 566, 84, 250, C, r) + tree(400, 558, 60, 150, C, r)
        o += cottage(46, 340, 2.25, I, C, 20, r)
        o += "".join(row([(36, 580 + q * 40), (188, 570 + q * 40), (308, 567 + q * 40), (448, 572 + q * 40), (528, 580 + q * 40)], C, 5 if q else 9) for q in range(3))
    elif name == "pic":    # box 560 x 700, one big motif
        w, h = 560, 700
        size = 400 if len(what) == 1 else 250
        pts = [q for m in what[:2] for p in MOTIFS[m][0] for q in p]
        up = max(0, (size - (max(q[1] for q in pts) - min(q[1] for q in pts)) * size / 100) * .55)   # flat motifs (a key) sit higher
        o = "".join(big(m, 280 + (i - (len(what[:2]) - 1) / 2) * 260, 560 - up, size, C, I, None, r) for i, m in enumerate(what[:2]))
        o += "".join(row([(36, 580 - up + q * 40), (188, 570 - up + q * 40), (308, 567 - up + q * 40), (448, 572 - up + q * 40), (528, 580 - up + q * 40)], C, 5 if q else 9) for q in range(3 + int(up // 40)))
    elif name == "row":    # box 1600 x 230
        w, h, k = 1600, 230, len(what)
        o = "".join(big(m, 1600 * (i + .5) / k, 232, 190 + 16 * (i % 2), C, I, None, r) for i, m in enumerate(what))
        o += P(rect(0, 222, 1600, 8), C)
    elif name == "street":  # box 1600 x 230, sits on the bottom edge
        w, h, x, o, lit = 1600, 230, -30, "", 0
        for k, (bw, bh) in enumerate(zip([170, 130, 210, 150, 180, 140, 220, 160, 270], [118, 172, 100, 210, 132, 92, 156, 112, 78])):
            top, flat = h - bh, k % 3 == 1
            o += P(cut(rect(x, top, bw, bh + 12) if flat else [(x, top + 56), (x + bw / 2, top), (x + bw, top + 56), (x + bw, h + 12), (x, h + 12)], 1.8, 50, r), C)
            y = top + (26 if flat else 76)
            while y < h - 46:
                wx = x + 26
                while wx < x + bw - 44:
                    on = "lit" in what and k == 6 and (lit := lit + 1) == 2
                    o += P(cut(rect(wx, y, 26, 34), .9, 20, r), T if on else I)
                    wx += 50
                y += 58
            x += bw + 6
    else:
        sys.exit(__doc__)
    print(f'<svg viewBox="0 0 {w} {h}" aria-hidden="true">{o}</svg>')


if __name__ == "__main__":
    if sys.argv[1:] == ["css"]:
        css()
    elif sys.argv[1:] == ["motifs"]:
        print(" ".join(MOTIFS))
    elif len(sys.argv) >= 3 and sys.argv[1] == "scene":
        scene(*sys.argv[2:])
    else:
        sys.exit(__doc__.strip())
