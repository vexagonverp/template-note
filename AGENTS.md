# AGENTS.md

Rules for any AI agent (Claude Code, Copilot, Codex, Gemini, a local model, ...) working in
this repo. Read this before you build or edit anything. `CLAUDE.md` imports this file and
`.github/copilot-instructions.md` points to it, so there is one source of truth.

## Author

**Your Name — YOUR-ID.** Use this name and ID wherever a document asks for one (title
blocks, graded file names). Run `scripts/setup.sh "Name" "ID"` once to fill these in
across the repo.

## What this repo is

Study material and graded work for university courses, written in LaTeX and built to PDF.
Each course is a folder with its sources (slides, past papers, question pools, hint photos,
lecture transcripts), the documents built from them, and their compiled PDFs. Most exam
notes end up as one open-book reference sheet the student prints and brings to the exam.

## Layout

```
templates/          one template per document type (see "Pick the template" below)
  _exam_preamble.tex    shared preamble of every exam template
  _report_preamble.tex  shared preamble of every graded-document template
_course_template/   copied for each new course (folders + COURSE.md)
assets/logo.png     university logo; templates show it with \UniLogo[height], found from any depth
scripts/            setup, new document, build, read sources, notebooks, checks, packaging
.claude/skills/     task skills (/exam-final, /theory-notes, /audit-sheet, ...), read by Claude and Copilot
docs/               sheet anatomy, writing style, LaTeX traps, workflows
<Course>/           one folder per course (see _course_template/README.md)
```

## Skills (start here)

Each task has a skill in `.claude/skills/<name>/SKILL.md`. Claude Code and Copilot both load
them: as `/name <args>`, or on their own when the request matches. A skill holds the steps
for one task; this file holds the rules that apply to all of them.

| Skill | Does |
|-------|------|
| `/new-course <Course>` | create the folder, sort the files, fill in COURSE.md |
| `/read-sources <Course>` | extract every slide, photo, page, notebook into `.temp/` and inventory it |
| `/transcript <file>` | lecture transcript → exam-alert outline in `transcripts/` |
| `/exam-final <Course>` | final sheet from a question pool (4-part layout) |
| `/exam-midterm <Course>` | sheet for announced question types + proofs |
| `/theory-notes <Course>` | theory sheet + question bank for a theory course |
| `/audit-sheet <file.tex>` | independent adversarial audit, fresh context, no edits |
| `/graded-report <Course> <kind>` | lab report + notebook, report, proposal, exercise, essay |
| `/presentation <Course> <min>` | slides or slide assets + speaking script |
| `/tutor <question>` | solve one question by hand in chat, no files |

When you add a skill: one folder per skill, lowercase-hyphen name matching the folder,
a `description` that says what it does **and when to use it**, steps that point to
`AGENTS.md` / `docs/` instead of repeating them, and `$ARGUMENTS` handled with a fallback
("if empty, take it from the user's message") so it also works where arguments are not
substituted.

## Pick the template

`scripts/new_note.sh <Course> <kind> "Course Name" [Descriptor]`. Never edit a file in
`templates/` for one course. Pick by **what the exam or task is like**, not by its name.

| kind | Use when |
|------|----------|
| `midterm` | the teacher announces question *types* ("Q1 formulate an LP, Q2 prove convexity") and some are proofs |
| `final` | the teacher gives a question pool and changes the numbers |
| `theory` | the course tests definitions, lists, comparisons, short essays, situational questions |
| `qbank` | a self-test question bank (past exams, tagged questions, mock exams) next to a theory sheet |
| `cheatsheet` | the exam limits the notes to N sides: dense, 2 columns, black and white |
| `lab` | a lab report with its Jupyter notebook (both are created) |
| `report` | an assignment or technical report |
| `proposal` | a research proposal |
| `exercise` | a short homework / exercise answer sheet |
| `essay-en` / `essay-vi` | an English essay / a Vietnamese tiểu luận (13pt, VN margins) |
| `slides` / `script` / `asset` | Beamer slides / a presentation script / a slide-sized image for Canva |
| `paper` | a Springer LNCS paper (folder with sections/, figures/, references.bib) |

The exam templates share `_exam_preamble.tex` and the graded templates share
`_report_preamble.tex`. Change a shared preamble only there, then run
`python3 scripts/sync_preamble.py` (and `--check` before committing).

## Source priority

When sources disagree, trust them in this order:

1. **Hints** the teacher gave about this exam (board photos, slides shown in class, what
   was said in a review session). They say what will be on the exam.
2. **Transcripts** of lectures: every `[EXAM ALERT]`, quoted "guaranteed" question and
   "not on the exam" line.
3. **The question pool / announced question types**, then **past exams** (for style).
4. **Slides** (the authority on wording and list contents), then the **textbook**.

If a hint differs from the pool (e.g. the pool says 1 iteration, the board says 2), do
what the hint says and note it where the question is copied.

## Workflow for an exam sheet

1. **Read everything first:** `COURSE.md`, every file in `hints/` and `transcripts/`, the
   question pool, past exams, and the slides. Do not start writing before this.
2. **Extract text:** `scripts/pdf_text.py` (PDF), `scripts/pptx_text.py` (PPTX),
   `scripts/mhtml_text.py` (saved web pages), `scripts/nb_text.py` (notebooks). A page
   with no text is an image: render it with `scripts/pdf_pages.sh` and look at it. To scan
   a whole deck quickly, tile the renders with `scripts/contact_sheet.py`. Convert phone
   photos with `scripts/photos_to_jpg.sh` (HEIC can't be read directly). The `pdf` skill
   also works if you'd rather read a PDF that way.
3. **Ask only what you can't find.** If the exam format, allowed material, or the meaning of
   a hint is unclear, ask. Otherwise pick a sensible default and say so.
4. **Start from the right template** (table above).
5. **Lead with the exam playbook:** what was announced, every hint and transcript alert,
   and a table from question type to page. Organise by exam question type, not by lecture.
6. **Every computational question uses the 4-part layout** (`docs/SHEET_ANATOMY.md`):
   question box → step-by-step guideline → worked example → answer box. Theory questions use
   the theory layout (defbox → What it is / How it works / Tiny example / Why it matters).
7. **Check every number with a script** before it goes in (start from
   `scripts/check_template.py`). Then check by hand that the steps shown produce it.
8. **Build and look at it:** `scripts/build.sh --preview <file>.tex`, fix every Overfull
   warning, and look at the pages. A box split across pages or a formula past the margin
   is a bug. For a hang or a broken section, use `scripts/build_sections.py`.
9. **Audit:** for a big sheet, run `/audit-sheet <file>` (it runs in a fresh context).
10. Leave the compiled PDF next to the `.tex`. Commit only when the user asks.

## Workflow for graded work

- **The file name is the submission name:** `<NameNoSpaces>_<ID>_<Descriptor>.tex` builds
  `<...>.pdf`. Never rename the PDF by hand; rename the `.tex` and rebuild.
- **Paste the brief word for word** into `COURSE.md` → Assignments before writing, and
  check the result against its marking criteria.
- **Labs:** the notebook comes first. Run it (`scripts/nb_run.py`), take every number from
  its saved output (`scripts/nb_text.py --outputs`), and keep figures in `figs/` next to the
  report so the notebook and report use the same files. Report sections mirror the notebook's
  `## Step k` headings. Package with `scripts/package_submission.sh` (writes `submit/`).
- **Figures:** vector PDF, named `figN_<short_desc>.pdf`, made with `scripts/figstyle.py`.
- **References** must be real and checkable (DOI or URL). Never invent a source.
- **Reports and essays:** report the word count after each build if there is a target.

## Content rules (learned the hard way)

- **The teacher changes the numbers.** Every computational question needs a guideline
  written with letters that works for any numbers, plus a worked example, plus the answer box.
- **Pen and paper unless told otherwise.** Every answer must be reproducible by hand. Never
  write "checked with a solver" as the method. Use the script only to verify.
- **Copy the question exactly as printed**, same wording, same equation numbers, and its
  source (`Pool §2.1, p. 1`, `Lecture 6, slide 29`, `board, 16 Oct`). If the source text is
  cut or wrong, keep it and add a short note.
- **Cover variations:** one or two variants the teacher could plausibly give (flipped
  inequality, active vs inactive constraint, non-diagonal matrix, 2 iterations).
- **Open-book means more is better.** No page limit unless the user says so (then use the
  cheatsheet template). If a slide list has N items, the note has all N.
- **Quote the lecturer** for definitions and named lists (that wording gets marked), then
  explain it in plain words with a tiny example and the trap.
- **Explain like the reader is new to it.** Start sheets with a "math from zero" part (or a
  jargon decoder for theory courses). Numbers before symbols.
- **Fold clarifications into the document.** When the user asks what a symbol or line in
  the sheet means, answer and also add the plain explanation at that spot, then rebuild.
  Meta questions (formatting, process) stay in chat.
- **When the user asks for "the prompt"**, give them the prompt text and stop. Don't start
  running it until they say go.

## Editing

- Read a file before you edit it. Make small, targeted edits; don't rewrite whole files.
- Many notes are too big to read whole. Search for the section first, then read only those lines.
- For many exact replacements at once (a wording pass), use `scripts/apply_patches.py`: every
  old string must match exactly once, and it shows a diff before writing.
- Before a big restructure, copy the file to `.temp/<name>_before_<step>.tex` (or commit).
- If you don't know which file or section the user means, ask.

## Math questions in chat

Answer step by step so it can be checked by hand. Run big arithmetic with `python3 -c`.
Check the final answer (substitute it back) and say whether the check passes. End with the
answer on its own line: `Answer: ...`.

## Writing style

Write like a person explaining it to a classmate, not like a textbook or a bot. Plain
words, short sentences, no filler, few em dashes. Register depends on the document:
spoken and plain for exam sheets, lab reports and scripts; academic third person for
reports, proposals, essays and papers. If a draft reads like AI output, run a humanizer
pass over the prose. Do not "fix" small imperfections the user added by hand on purpose;
flag them instead. Details: `docs/WRITING_STYLE.md`.

## Building

Use **tectonic**, not pdflatex: `scripts/build.sh file.tex` (or `tectonic file.tex`). The
first build downloads packages and fonts and is slow; after that a 40-page sheet builds in
seconds. `build.sh` stops a build after 120 s and calls it a HANG. Ignore any old prompt
that says "run pdflatex twice".

Known traps (full list in `docs/LATEX_TRAPS.md`):

- `hyperref` + heavy math in a heading hangs forever. The templates set `bookmarks=false`.
- Unicode dashes/symbols (`–`, `—`) can be missing from the font. Type `--` and `---`.
- Moving a `.tex` or notebook away from its `figs/` breaks figure paths. Keep them together.
- `report` / `article` silently ignore `13pt`. Use KOMA (`fontsize=13pt`), as `essay_vi` does.
- Names with accents: the templates use fontspec under XeTeX, so they print; file names
  stay ASCII (`new_note.sh` strips accents).

## Files, git and safety

- Scratch work (extracted text, rendered pages, section builds) goes in `.temp/`, which is
  ignored. Anything you need to keep (check scripts behind a sheet, slide-asset sources) goes
  next to the document, e.g. `<Course>/notes/checks/`, `<Course>/presentation/assets/`.
- Never `rm` with globs or variables. Overwrite files instead of deleting them.
- PDFs are tracked on purpose, and so are hint photos (they are the evidence of what was
  announced). Very large reference books (> 50 MB) are better kept out of git; note in
  `COURSE.md` where to get them.
- Commit the `.tex` and its rebuilt `.pdf` together. Message format: `<Course>: <what changed>`
  (e.g. `AlgorithmOptimization: final sheet, answer boxes restyled`). Commit and push only
  when the user asks.
