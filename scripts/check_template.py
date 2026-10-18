#!/usr/bin/env python3
"""Starter for verifying every number in a sheet before it goes in.

Copy to .temp/<course>_check.py (or <Course>/notes/checks/ to keep it), edit, run:
    python3 .temp/algo_check.py

Rules:
  - One function per question. Print the same table the sheet shows.
  - Use Fraction when the sheet shows exact fractions (4/3, -29/3).
  - After it agrees, still check by hand that the steps in the sheet produce it.
"""
from fractions import Fraction as F

import numpy as np

np.set_printoptions(precision=6, suppress=True)


def table(title, rows, header):
    print(f"\n== {title}")
    print(" | ".join(header))
    for r in rows:
        print(" | ".join(str(np.round(v, 6)) if isinstance(v, (float, np.ndarray)) else str(v) for v in r))


def q_newton():
    """Example: 2 Newton iterations on f = 0.5 x1^2 + 2 x2^2 - ln x1 from (2, 1)."""
    x = np.array([2.0, 1.0])
    rows = []
    for k in range(2):
        g = np.array([x[0] - 1 / x[0], 4 * x[1]])
        H = np.diag([1 + 1 / x[0] ** 2, 4.0])
        dx = -np.linalg.solve(H, g)
        rows.append((k, x.copy(), g, np.diag(H), dx, x + dx))
        x = x + dx
    table("Newton", rows, ["k", "x", "grad", "diag H", "dx", "x+"])


def q_exact():
    """Example: exact fractions for a small linear system."""
    w = F(2) / F(3, 2)
    print("\n== exact w =", w, "=", float(w))


if __name__ == "__main__":
    q_newton()
    q_exact()
