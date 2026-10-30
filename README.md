# template-note

A starter repo for university study notes and graded work in LaTeX, mostly written with an
AI agent's help. It turns lecture slides, question pools, the teacher's hints and lecture
transcripts into printable open-book exam sheets. It also has templates for lab reports,
assignments, proposals, essays (English and Vietnamese), slides, presentation scripts and
papers.

Exam sheets for computational courses use the same four parts for every question:

| Box | What it holds |
|-----|---------------|
| 🟦 **Question** | the question exactly as printed, with its source (`Pool §2.1, p. 1`) |
| 🟥 **Step-by-step guideline** | numbered `STEP` badges with letters instead of numbers, so it still works when the teacher changes the numbers |
| ⬜ **Worked example** | the same steps with real numbers, every line shown, iteration tables |
| 🟩 **Answer** | what to write on the exam paper, final results boxed |

Theory courses use a definition → explanation → example → trap pattern instead, with a
glossary, compare tables, situational questions and a question bank.

## Quick start

```bash
# 1. once: your name and ID into the rules and every template (+ optional Python env)
scripts/setup.sh "Jane Doe" "S1234567" --venv

# 2. a course folder + a document (run new_note.sh with no arguments for every kind)
scripts/new_note.sh Calculus final "Calculus I"      # -> Calculus/notes/JaneDoe_S1234567_Final_ExamSheet.tex

# 3. put files in Calculus/slides, materials, hints, transcripts; fill in Calculus/COURSE.md;
#    or just let the agent do it: /new-course Calculus "Calculus I" <folder of files>
#    then: /exam-final Calculus   (or /exam-midterm, /theory-notes, /graded-report, ...)

# 4. build, and render the pages to .temp/preview/ to look at them
scripts/build.sh --preview Calculus/notes/JaneDoe_S1234567_Final_ExamSheet.tex
```

## Templates

| `new_note.sh` kind | Template | For |
|--------------------|----------|-----|
| `midterm` | `midterm_template.tex` | announced question types, proof questions |
| `final` | `final_template.tex` | question pool with the numbers changed |
| `theory` | `theory_template.tex` | definitions, lists, compare tables, situational questions |
| `qbank` | `question_bank_template.tex` | tagged self-test questions, past exams, mock exams |
| `cheatsheet` | `cheatsheet_template.tex` | dense 2-column sheet when notes are page-limited |
| `lab` | `lab_report_template.tex` + `lab_template.ipynb` | lab report with its notebook |
| `report` | `report_template.tex` | assignment / technical report |
| `proposal` | `proposal_template.tex` | research proposal |
| `exercise` | `exercise_template.tex` | homework answer sheet |
| `essay-en` | `essay_en_template.tex` | English essay / critical analysis |
| `essay-vi` | `essay_vi_template.tex` | Vietnamese tiểu luận (13pt, VN margins, MỤC LỤC) |
| `slides` | `slides_template.tex` | Beamer 16:9 slides with presenter notes |
| `script` | `presentation_script_template.tex` | what to say, slide by slide |
| `asset` | `slide_asset_template.tex` | a slide-sized math image for Canva / PowerPoint |
| `deck` | `html_deck/deck_template.html` | HTML slide deck with step-by-step animated diagrams (`DECK_DESIGN=<style>`) |
| `paper` | `paper_llncs/` | Springer LNCS paper folder |

Each template has a built PDF next to it, so you can see what it looks like. Title pages show
`assets/logo.png` through `\UniLogo[height]`; replace that file to change university, or delete it
to drop the logo everywhere (nothing breaks). The LNCS paper and the slide asset leave it out on
purpose: Springer does not allow logos, and assets are pasted into someone else's slide. The exam
templates share `templates/_exam_preamble.tex`; the graded ones share
`templates/_report_preamble.tex`. Edit a shared preamble there and run
`python3 scripts/sync_preamble.py`.

## Requirements

- [tectonic](https://tectonic-typesetting.github.io/) for LaTeX (`brew install tectonic`).
  The first build fetches packages and fonts, so it is slow.
- poppler (`pdftotext`, `pdftoppm`, `pdfinfo`, `pdffonts`): `brew install poppler`.
- Python 3. `requirements.txt` lists the optional packages (pypdf, pillow, numpy, scipy,
  matplotlib, nbformat/nbclient for notebooks). `scripts/setup.sh ... --venv` installs them
  into `.venv`.
- macOS `sips` (built in) or ImageMagick to convert phone photos. No LibreOffice needed:
  PPTX text is read with the standard library.

## Layout

```
AGENTS.md                     rules every agent follows
assets/logo.png               university logo on every title page (swap or delete it)
assets/media/                 style-free images, icons, shapes, textures for decks (README lists sources)
.claude/skills/               one skill per task, used by Claude Code and Copilot (see below)
CLAUDE.md                     Claude Code entry point: @AGENTS.md
.claude/settings.json         Claude Code: allowlist for the build/read commands (no rm)
.github/copilot-instructions.md   Copilot: short form of the rules
.github/agents/notes.agent.md     Copilot custom agent: edit notes / answer math
.vscode/                      LaTeX Workshop builds with tectonic; recommended extensions
.editorconfig  .gitignore  requirements.txt
templates/                    every template + shared preambles + lab notebook + paper folder
  html_deck/                  HTML stop-motion deck template + DESIGN.md
_course_template/             copied for each new course (COURSE.md + folders)
scripts/
  setup.sh                    your name and ID everywhere; --venv for Python packages
  new_note.sh                 new course folder + a document of any kind
  build.sh                    tectonic build, warnings, hang timeout, --preview pages
  build_sections.py           build one section at a time to find a hang or bad section
  sync_preamble.py            stamp the shared preambles into templates / notes
  pdf_text.py  pptx_text.py  mhtml_text.py  nb_text.py   read sources as text
  pdf_pages.sh  contact_sheet.py  photos_to_jpg.sh        see pages and photos
  nb_run.py                   run a notebook, save it, print outputs and errors
  check_template.py           starter for verifying every number in a sheet
  apply_patches.py            many exact replacements, each must match once, dry run first
  figstyle.py                 shared matplotlib style + save() for report/slide figures
  package_submission.sh       hand-in folder + zip in <Course>/submit/
  html_deck.py                new deck, switch its design style, screenshots, bundle to send, artifact copy
  contrast.py  cutout.py      check a style's color contrast; cut an object out of its background

docs/
  SHEET_ANATOMY.md   page order and boxes for every exam template
  WRITING_STYLE.md   how the prose should read, register per document type
  LATEX_TRAPS.md     hangs, missing glyphs, broken figure paths, ignored options, ...
  WORKFLOWS.md       recipes: reading sources, transcripts, checks, labs, hangs, patches
  LOCAL_LLM.md       running the agent rules with a local model
  design/            visual rules (README.md) + one folder per deck style (paper-stage, block-shapes)
```

## Skills

The repo is meant to be driven by Claude Code or GitHub Copilot. Both read
`.claude/skills/`, so every task is a slash command (or loads by itself when you ask for it):

| Skill | Use it to |
|-------|-----------|
| `/new-course <Course> ["Name"] [files]` | set up a course: folders, sort files, fill in COURSE.md |
| `/read-sources <Course>` | extract and inventory every slide, page, photo, notebook |
| `/transcript <file> [L05]` | turn a lecture transcript into an exam-alert outline |
| `/exam-final <Course>` | final sheet from a question pool, numbers will change |
| `/exam-midterm <Course>` | sheet for announced question types, with proof templates |
| `/theory-notes <Course> [midterm\|final\|both]` | theory sheet + question bank with mock exams |
| `/audit-sheet <file.tex>` | adversarial audit in a fresh context; prints a findings table |
| `/graded-report <Course> <kind> [Descriptor]` | lab (+ notebook), report, proposal, exercise, essay |
| `/presentation <Course> <minutes> [paper]` | HTML deck, Beamer slides or Canva assets + speaking script |
| `/design-language <name> <look>` | create or apply a visual style for decks (`docs/design/`) |
| `/tutor <question>` | one question solved by hand in chat, nothing written to disk |

A typical exam: `/new-course` → `/read-sources` → `/transcript` (if you have recordings) →
`/exam-final` → `/audit-sheet`.

## Using it with an agent

The rules live in one place: `AGENTS.md`; the task steps live in `.claude/skills/`. Claude
Code loads the rules through `CLAUDE.md` (`@AGENTS.md`); Copilot reads
`.github/copilot-instructions.md`, can use the `notes` agent, and picks up the same skills.

The main points:

1. Read everything first: hints and transcripts outrank the pool, which outranks the slides.
2. Pick the template by what the exam is like; never edit a template for one course.
3. Copy questions exactly, with their source. Cover what the hints say, and their variants.
4. Answers must work with pen and paper. Check every number with a script.
5. Build with tectonic, fix every warning, look at the pages. Audit big sheets in a fresh session.
6. Plain, short sentences. Explain like the reader is new to it. No page limit unless told.

## Workflow in one picture

```
slides / pool / past exams / hints / transcripts
        │  /read-sources · /transcript
        ▼
   COURSE.md (/new-course) ──► /exam-final · /exam-midterm · /theory-notes · /graded-report
        │                                                     │
        │                       check_template.py (numbers) ◄─┤
        ▼                                                     ▼
   build.sh --preview ──► fix warnings, look at pages ──► /audit-sheet (fresh context)
```
