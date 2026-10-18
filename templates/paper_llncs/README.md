# Paper title

| Item | Value |
|------|-------|
| Venue | <conference / journal, year> |
| Format | Springer LNCS (`llncs`), <N> pages excluding references |
| Review | single-blind / double-blind |
| Deadlines | abstract <date>, paper <date>, camera-ready <date> |

## Build

```bash
tectonic main.tex          # fetches llncs.cls and splncs04.bst, runs BibTeX
# or, with TeX Live:  latexmk -pdf main.tex
```

## Layout

- `main.tex` front matter and `\input` of each section
- `sections/` one file per section, each starting `\section{..}\label{sec:..}`
- `figures/` images (found via `\graphicspath`)
- `references.bib` BibTeX entries

## Evidence (if the paper reports measurements)

Keep the raw results next to the paper so every number can be traced:

- `docs/EVIDENCE.md`: where each result came from (repo, commit, date), and a note that
  this copy is not a new experiment.
- `docs/evidence-sha256.txt`: checksums, verify with `shasum -a 256 -c docs/evidence-sha256.txt`.
- `docs/validation-YYYY-MM-DD/README.md`: what was checked, the exact commands to reproduce,
  environment, limitations. Keep the earlier run beside the final one and say which one the
  paper uses.
