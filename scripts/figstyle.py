"""Shared matplotlib style for figures in reports, notebooks and slides.

    import sys; sys.path.insert(0, "scripts")   # or copy this file next to the notebook
    from figstyle import use, save, PALETTE
    use()                                       # "report" (default) or "slides"
    fig, ax = plt.subplots(figsize=WIDE)
    ...
    save(fig, "fig3_gd_convergence", folder="lab1_figs")   # -> lab1_figs/fig3_gd_convergence.pdf

Conventions:
  - Report figures are vector PDF, named figN_<short_desc>.pdf, in <deliverable>_figs/,
    and the report \\includegraphics the same files the notebook made.
  - One panel: ONE = (6.5, 4). Two panels side by side: WIDE = (11, 4).
  - Slides: PNG at 150 dpi, big font, no top/right spines, legend above the plot.
"""
from pathlib import Path

import matplotlib.pyplot as plt

PALETTE = {"accent": "#F28C45", "navy": "#0E3A6B", "grey": "#9AA3AE",
           "green": "#2E8B57", "red": "#C0392B", "bg": "#F7F9FC"}
ONE, WIDE, SLIDE = (6.5, 4), (11, 4), (12.3, 6.5)


def use(kind="report"):
    plt.rcParams.update({
        "figure.dpi": 110, "savefig.bbox": "tight",
        "axes.grid": True, "grid.alpha": 0.3,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": plt.cycler(color=[PALETTE[k] for k in ("navy", "accent", "green", "red", "grey")]),
        "font.size": 10, "legend.frameon": False,
    })
    if kind == "slides":
        plt.rcParams.update({"font.size": 15, "figure.facecolor": PALETTE["bg"],
                             "axes.facecolor": PALETTE["bg"], "axes.grid.axis": "y"})


def save(fig, name, folder="figs", fmt=None):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    fmt = fmt or ("png" if plt.rcParams["font.size"] >= 15 else "pdf")
    path = folder / f"{name}.{fmt}"
    fig.savefig(path, dpi=150 if fmt == "png" else None)
    plt.close(fig)
    return path
