#!/usr/bin/env python3
"""Print a Jupyter notebook as plain text: markdown, code, and text outputs.

Usage:
    python3 scripts/nb_text.py Lab1.ipynb            # everything
    python3 scripts/nb_text.py Lab1.ipynb --outputs  # only outputs (numbers to cite)

Standard library only. Use it to read a notebook or to copy exact numbers into a report.
"""
import json
import sys


def text(x):
    return "".join(x) if isinstance(x, list) else (x or "")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    only_out = "--outputs" in sys.argv
    nb = json.load(open(sys.argv[1], encoding="utf-8"))
    for i, c in enumerate(nb.get("cells", []), 1):
        kind = c["cell_type"]
        if not only_out:
            print(f"--- cell {i} [{kind}] ---")
            print(text(c.get("source")))
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream":
                body = text(o.get("text"))
            elif o.get("output_type") == "error":
                body = f"ERROR {o.get('ename')}: {o.get('evalue')}"
            else:
                data = o.get("data", {})
                body = text(data.get("text/plain")) if "text/plain" in data else ""
                if "image/png" in data:
                    body += "\n[image output]"
            if body.strip():
                print(f"[out {i}] {body.rstrip()}")


if __name__ == "__main__":
    main()
