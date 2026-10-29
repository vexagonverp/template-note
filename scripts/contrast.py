#!/usr/bin/env python3
"""Check text contrast of a deck design language (WCAG 2.1).

  python3 scripts/contrast.py block-shapes        # docs/design/<name>/style.css
  python3 scripts/contrast.py '#5E3F8F' '#FFFFFF' # one pair

Body text needs 4.5:1. Large text (about 24px+, or 19px+ bold) may use 3:1.
"""
import re
import sys
from pathlib import Path

DESIGNS = Path(__file__).resolve().parents[1] / "docs/design"
# (text token, background token): every pairing the engine and the shared parts use
PAIRS = [("ink", "card"), ("muted", "card"), ("accent", "card"), ("ink", "paper"), ("muted", "paper"),
         ("ink", "tint"), ("on-accent", "accent"), ("on-go", "go"), ("on-stop", "stop"),
         ("card", "ink"), ("ink", "pop")]


def lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    a, b = lum(a), lum(b)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def tokens(css):
    raw = dict(re.findall(r"--([\w-]+):\s*([^;]+);", css))

    def res(v, depth=0):
        v = v.strip()
        m = re.fullmatch(r"var\(--([\w-]+)(?:,\s*(.+))?\)", v)
        if m and depth < 10:
            return res(raw[m.group(1)], depth + 1) if m.group(1) in raw else (res(m.group(2), depth + 1) if m.group(2) else None)
        return v if re.fullmatch(r"#[0-9A-Fa-f]{3,6}", v) else None
    return {k: res(v) for k, v in raw.items()}


def main(argv):
    if len(argv) == 3:
        print(f"{ratio(argv[1], argv[2]):.2f}:1"); return
    if len(argv) != 2:
        sys.exit(__doc__.strip())
    t = tokens((DESIGNS / argv[1] / "style.css").read_text().partition("/* @@PARTS */")[0])
    t.setdefault("on-accent", t.get("card")); t.setdefault("on-go", t.get("card")); t.setdefault("on-stop", t.get("card"))
    bad = 0
    for fg, bg in PAIRS:
        if not t.get(fg) or not t.get(bg):
            continue
        r = ratio(t[fg], t[bg])
        verdict = "ok" if r >= 4.5 else ("large text only" if r >= 3 else "FAIL")
        bad += r < 3
        print(f"--{fg:10} on --{bg:7} {t[fg]} on {t[bg]}  {r:5.2f}:1  {verdict}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv)
