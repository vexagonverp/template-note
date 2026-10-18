#!/usr/bin/env python3
"""Run a notebook top to bottom, save the executed copy, print outputs and errors.

Usage:
    python3 scripts/nb_run.py Course/lab/Lab1.ipynb               # overwrite in place
    python3 scripts/nb_run.py Course/lab/Lab1.ipynb .temp/run.ipynb  # write elsewhere

Needs: pip install nbformat nbclient ipykernel  (see requirements.txt)
The notebook runs with its own folder as the working directory, so relative paths
like "lab1_figs/fig1.pdf" land next to it. Exit code 1 if any cell raised an error.
"""
import pathlib
import sys

try:
    import nbformat
    from nbclient import NotebookClient
except ImportError:
    sys.exit("pip install nbformat nbclient ipykernel  (or use .venv/bin/python)")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1]).resolve()
    dst = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else src
    nb = nbformat.read(src, as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name="python3",
                            allow_errors=True,
                            resources={"metadata": {"path": str(src.parent)}})
    client.execute()
    nbformat.write(nb, dst)
    errors = 0
    for i, c in enumerate(nb.cells, 1):
        for o in c.get("outputs", []):
            if o.get("text"):
                print(o["text"], end="")
            if o.output_type == "error":
                errors += 1
                print(f"ERROR in cell {i}: {o.ename}: {o.evalue}")
    print(f"\n[saved {dst}; {errors} error(s)]", file=sys.stderr)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
