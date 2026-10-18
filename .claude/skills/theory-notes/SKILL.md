---
name: theory-notes
description: Build open-book notes for a theory course (definitions, named lists, comparisons, situational or essay questions) as two files, a theory sheet and a question bank with model answers and mock exams. Use for courses like research methods, ethics, software architecture, or the theory half of security, or when the user asks for theory notes, a question bank, or a glossary-style sheet.
argument-hint: <CourseFolder> [midterm|final|both] [extra instructions]
---

# Theory notes + question bank

**Input:** `$ARGUMENTS` is the course folder, which exam (midterm / final / both), and any
extra instructions. If it is empty (or shows up literally as a placeholder), take these
from the user's message, or ask.

This is a long job: no page limit, so more complete is better. Follow `AGENTS.md`. Layout
reference: `docs/SHEET_ANATOMY.md` → "Theory layout" and "Question bank layout".

## 1. Read ALL the sources first

- Slides: `python3 scripts/pdf_text.py` / `python3 scripts/pptx_text.py` for every deck.
  Image-only slides: `scripts/pdf_pages.sh`, then look. To scan a whole deck,
  `scripts/contact_sheet.py`.
- `<Course>/COURSE.md`: announcement, grading split, what each exam covers.
- `<Course>/transcripts/`: every `[EXAM ALERT]` and "guaranteed" item goes in the overview
  box and must be covered. Note anything the lecturer ruled out.
- Past papers and assigned readings in `<Course>/materials/`, and the textbook (for the
  "where to look" index).
- A finished sheet the user liked, if one exists, as the reference for tone and density.

## 2. Create both files

```bash
scripts/new_note.sh <Course> theory "<Course display name>"
scripts/new_note.sh <Course> qbank  "<Course display name>"
```

Each file builds on its own, and each names the other in its title block.

## 3. Fidelity rules (most important)

- **Keep the slides' exact wording** for definitions, named principles and lists, in a
  `defbox{Lecture n, slide m}`, with the **defined term in bold**.
- **Then extend the meaning:** after each quoted point, write `\lbl{What it is:}`,
  `\lbl{How it works:}`, `\lbl{Tiny example:}` and `\lbl{Why it matters / trap:}`. That is
  1–3 plain sentences each, with a concrete example.
- **If a slide has N items, the note has N.** Ordered lists go in a `memobox` with a memory hook.
- Look-alike terms get a compare table (Term | slide wording | plain English + example).
- Label every top-level section `\exam{Midterm}`, `\exam{Final}` or `\exam{Midterm + Final}`,
  start it with a `Source:` line, and quote what the lecturer stressed with `\examcue{}`.

## 4. Theory file contents

- Title block with the rules line ("Open Book · Open Notes (paper only) · No electronics").
- Overview `notebox` containing:
  - format and grading split
  - what the lecturer said will appear, quoted, with `\sref{}`
  - **Not expected** (what was ruled out)
  - **the numbers you must memorise** (every list count on one line)
  - the answer template: Definition → How it works (full list) → Tiny example → Why/trap
- Jargon decoder: a numbered glossary with `\label{term:..}`, referenced later with `\gl{}`.
- One section per topic.
- Situational questions: an answer-skeleton `notebox`, then `scenariobox`es with Scenario /
  Stakeholders / Concepts / Verdict. Phenomenon → Solution banks where the course asks "why
  does X happen".
- "Where to look if a question goes past the slides" (topic → textbook section → page).
- `pitfallbox` and `summarybox` at the end.

## 5. Question bank contents

- "How to use this bank" box and the tag legend: `\qtag{likely}`, `\qtag{past exam A}`,
  `\qtag{compute}`, `\qtag{practice}`, `\qtag{twist}`, plus a tag for any graded component.
- Past papers transcribed word for word with marks, plus a "which topics come up most" table.
- About 6–12 questions per topic group. Each one goes: `\Q{}` header → the question alone
  in a `qbankbox` → Answer → Why, step by step → Trap to avoid → Also asked as (2–3
  rephrasings).
- Every [COMPUTE] item: the formula first, then a worked example, then a sanity check.
  Verify the numbers with a script.
- Twist questions, and mock exams graded Easy / Medium / Hard.
- A model deliverable with a marking checklist, if the exam asks you to produce an artefact.

## 6. Definition of done

- Both files build with no errors or Overfull warnings (`scripts/build.sh --preview`), and
  you have looked at the pages.
- Every slide topic is covered in the slide's own words plus the extension. Every section
  is labelled, and every list has its full count.
- The bank has worked answers for every topic, with verified numbers.

Report the page counts and the number of questions, then offer `/audit-sheet` on both
files. Do not commit unless asked.
