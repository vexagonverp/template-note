# Workflows

Short recipes for the jobs that keep coming back. Every command runs from the repo root.

## Read a new course's material

```bash
python3 scripts/pdf_text.py "Course/slides/Lecture 1.pdf" > .temp/L1.txt   # flags image-only pages
python3 scripts/pptx_text.py "Course/slides/Chapter 04.pptx" > .temp/ch04.txt
python3 scripts/mhtml_text.py "Course/materials/Saved page.mhtml"
python3 scripts/nb_text.py Course/labs/Lab1.ipynb
scripts/photos_to_jpg.sh Course/hints                 # -> .temp/photos/hints/*.jpg
scripts/pdf_pages.sh "Course/slides/Lecture 1.pdf" 12 12   # one page as PNG
scripts/pdf_pages.sh "Course/slides/Lecture 1.pdf" 1 60 50 && \
  .venv/bin/python scripts/contact_sheet.py .temp/imgs/Lecture_1-*.png   # scan a deck fast
```

PPTX diagrams: export the deck to PDF (Keynote / PowerPoint), then `pdf_pages.sh`.

## Turn a lecture recording into exam alerts

1. Get the transcript (auto-captions, a recording tool, or notes).
2. Run `/transcript <file> L05`: it writes `Course/transcripts/L05.md` and adds the line to `COURSE.md`.
4. When building the sheet, every `[EXAM ALERT]` goes on page 1 and must be covered; cite it
   as `\sref{transcript L5, seg. 2}`.

## Check the numbers

```bash
cp scripts/check_template.py Course/notes/checks/final_check.py   # kept with the sheet
python3 Course/notes/checks/final_check.py
```

One function per question, printing the same table the sheet shows. Use `Fraction` when
the sheet shows exact fractions. After it agrees, check by hand that the steps on the page
produce the number. Keep the check script (in `notes/checks/`) so the sheet can be re-checked
after edits.

## Find a hang or a broken section

```bash
scripts/build.sh Course/notes/Sheet.tex                 # stops after 120 s: HANG
python3 scripts/build_sections.py Course/notes/Sheet.tex --at examPart --timeout 60
```

Each piece builds alone; the one that says HANG or FAIL holds the problem (usually math in
a heading, see `docs/LATEX_TRAPS.md`).

## A wording pass over a big file

1. Copy first: `cp Sheet.tex .temp/Sheet_before_wording.tex` (or commit).
2. Write the pairs to `.temp/patches.py` as `R = [(old, new), ...]`.
3. `python3 scripts/apply_patches.py Sheet.tex .temp/patches.py` (dry run, shows the diff).
4. Add `--write`, rebuild, look at the pages.

## Lab report from a notebook

```bash
scripts/new_note.sh Course lab "Course Name" Lab2_Report    # makes the .tex, the .ipynb and figs/
.venv/bin/python scripts/nb_run.py Course/labs/Name_ID_Lab2.ipynb
python3 scripts/nb_text.py Course/labs/Name_ID_Lab2.ipynb --outputs   # numbers for the report
scripts/build.sh Course/labs/Name_ID_Lab2_Report.tex
scripts/package_submission.sh Course Course_Lab2 Course/labs/Name_ID_Lab2.ipynb Course/labs/Name_ID_Lab2_Report.pdf
```

## Keep the shared preambles in sync

Edit `templates/_exam_preamble.tex` or `templates/_report_preamble.tex`, then:

```bash
python3 scripts/sync_preamble.py           # update every template
python3 scripts/sync_preamble.py Course/notes/Sheet.tex   # also update an existing note
python3 scripts/sync_preamble.py --check   # before committing
```

## Evidence for reports with measurements

For a report or paper with experiments, keep a `docs/` folder next to it:
`EVIDENCE.md` (where each result came from: repo, commit, date), a `sha256` manifest checked
with `shasum -a 256 -c`, and a dated `validation-YYYY-MM-DD/README.md` (what was checked, the
exact commands, environment, limits). Keep an earlier run beside the final one and say which
one the report uses.
