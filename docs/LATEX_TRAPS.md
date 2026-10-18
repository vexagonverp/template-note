# LaTeX traps (read before debugging a slow or broken build)

## 1. `hyperref` + math in a heading = compile hangs forever

**Symptom:** the build never finishes. One CPU core sits at 100% and no PDF appears. On
Overleaf's free tier it shows up as "compile timed out".

**Cause:** `hyperref` turns every section title into a PDF bookmark string. A heading
with a heavy math expression (e.g. `\subsection{The experiment $\PrivK^{\mathrm{eav}}_{A,\Pi}(n)$}`)
sends the bookmark builder into an infinite loop. Plain text and simple math (`$x^2$`)
are fine.

**Fix used here** (already in the template): turn bookmarks off. A printed sheet does
not need them.

```latex
\usepackage[hidelinks,bookmarks=false]{hyperref}
```

If you do need bookmarks, wrap the math in each heading instead:

```latex
\subsection{The experiment \texorpdfstring{$\PrivK^{\mathrm{eav}}_{A,\Pi}(n)$}{(IND-EAV)}}
```

**How to find it:** bisect the body section by section. The hang starts at the first
heading with heavy math.

## 2. Missing characters in bold fonts

`Missing character: There is no – in font ec-lmbx10!` means a Unicode character (here an
en dash) was typed straight into bold text. Use `--`, `---`, `\textendash`, or math.

## 2b. Accented names (Vietnamese etc.) print as missing glyphs

Tectonic runs XeTeX. There, `\usepackage[T1]{fontenc}` + `lmodern` has no glyphs for
characters like `ầ`, `ả`, and switching font encodings does nothing. The template
uses `fontspec` (OpenType Latin Modern, which covers them) when the engine is XeTeX/LuaTeX,
and the classic `fontenc`/`lmodern` setup only under pdflatex. Keep file names ASCII anyway:
`scripts/new_note.sh` strips accents (`Trần Bảo Thành` → `TranBaoThanh`).

## 3. Overfull boxes

Long inline formulas run past the margin. Fixes, in order of preference:

1. Move it to display math (`\[ ... \]`).
2. Split with `aligned` or a line break `\\`.
3. Shorten words in the same line.

`scripts/build.sh` prints every Overfull warning with its line number. Treat each one as a
bug: on a printed sheet the overflow gets cut off.

## 4. `tcolorbox` vs `mdframed`

`tcolorbox` (especially `breakable`) loads all of TikZ and is slower per box. It is
fine at this size (a 40-page sheet builds in about 5 s). For lots of plain framed boxes,
`mdframed` with `framemethod=default` looks the same and builds faster.

A non-breakable box taller than a page will overflow. Only the question box is
non-breakable, so keep questions shorter than a page.

## 5. Figure paths break when files move

A lab report did `\includegraphics{lab1_figs/fig1.pdf}` and its notebook saved to
`Path("lab1_figs")`. Then the `.tex` and `.ipynb` were moved into `lab/` and the figures
stayed behind: the report no longer built, and re-running the notebook made a new, empty
folder. Fix used in the templates: figures live in `figs/` **next to** the `.tex`, the
notebook saves there, and `\graphicspath{{figs/}{../figs/}}` finds them. Move the `.tex`,
the notebook and `figs/` together.

## 6. Invalid class options are ignored silently

`\documentclass[13pt]{report}` does not fail: `report` only knows 10/11/12pt, so it quietly
uses 10pt. Vietnamese university rules usually ask for 13pt. Use KOMA:
`\documentclass[fontsize=13pt]{scrreprt}` (the `essay_vi` template does this). Check the
real size with `pdffonts` or by measuring the text.

## 7. A TikZ library without TikZ

`\usetikzlibrary{arrows.meta}` with no `\usepackage{tikz}` works only because `tcolorbox`
skins happens to load TikZ. Remove the boxes and the build breaks. Load `tikz` explicitly
(both shared preambles do).

## 8. Renaming the PDF instead of the .tex

A proposal's PDF was renamed to `Name_ID_Proposal.pdf` but the `.tex` kept its old name.
The next build wrote a fresh `proposal_report.pdf` and the submitted file went stale. Name
the `.tex` with the submission name from the start (`new_note.sh` does).

## 9. Sources kept only in `.temp/`

`.temp/` is ignored by git. A presentation's slide-asset sources and chart script lived
there and are not versioned. Keep anything you need to rebuild next to the document
(`presentation/assets/`, `notes/checks/`).

## 10. pdflatex-only sources

Some sources (an LNCS paper from a co-author, an old template) assume pdflatex. Under
tectonic/XeTeX, `\usepackage[T1]{fontenc}` + Unicode dashes in the text gives missing
glyphs. Either build those with `latexmk -pdf`, or use the `\ifTUTeX` font switch the
templates use. Also: in LaTeX `~` is a non-breaking space, so `~1.8 KB` prints "1.8 KB"
and loses "about". Write `$\sim$1.8` or "about 1.8".

## 11. Fonts by name vs by file

Under tectonic, `\setmainfont{TeX Gyre Termes}` (by family name) may not be found, but the
file form works: `\setmainfont{texgyretermes}[Extension=.otf, UprightFont=*-regular, ...]`.
Lato is `\setsansfont{Lato}[Extension=.ttf, UprightFont=*-Regular, ...]`. If a font is
"cannot be found", look for the file name in `~/Library/Caches/Tectonic`.

## 12. General

- The first tectonic build downloads packages and fonts, so it is slow. Later builds use
  the cache.
- Drop packages you don't use.
- A few-page document should build in seconds. If not, suspect a hang (trap 1), not
  "too many packages".
