---
name: exam-final
description: Build an open-book FINAL exam sheet from a question pool where the teacher changes the numbers. Every question gets the exact question box, a step-by-step guideline that works for any numbers, a worked example, and a "what to write on the paper" answer box. Use when the user asks for a final exam sheet, exam notes from a question pool, or says the questions will come from a pool with different numbers.
argument-hint: <CourseFolder> [extra instructions]
---

# Final exam sheet (question pool)

**Input:** `$ARGUMENTS` is the course folder, optionally followed by extra instructions.
If it is empty (or shows up literally as a placeholder), take the course from the user's
message, or ask which folder.

Follow `AGENTS.md` throughout. Layout reference: `docs/SHEET_ANATOMY.md` → "Final layout"
and "The 4-part layout". Template: `templates/final_template.tex`.

## 1. Read everything first

Nothing gets written before this step is done.

1. `<Course>/COURSE.md`: exam date, format, allowed material, the announcement word for word.
2. Every file in `<Course>/hints/` (convert photos with `scripts/photos_to_jpg.sh`, then look
   at each image) and `<Course>/transcripts/`. These outrank everything else: each hint and
   each `[EXAM ALERT]` must be listed on page 1 and covered.
3. The question pool and past exams in `<Course>/materials/` (`python3 scripts/pdf_text.py`).
   Past exams show the question style and the answer format.
4. The slides for every topic in the pool (`pdf_text.py` / `pptx_text.py`; image-only pages
   → `scripts/pdf_pages.sh`, then look).

If the exam format, the allowed material, or the meaning of a hint is unclear, ask now.
Otherwise pick a sensible default and say so.

## 2. Create the sheet

```bash
scripts/new_note.sh <Course> final "<Course display name>"
```

## 3. Write it

- **Page 1: exam playbook.** The announcement, every hint (with source: `board, 16 Oct`,
  `Lecture 6, slide 29`), what each hint means for the exam, a table "question type → what
  she can change → page", habits that save marks, and hand-calculation helpers.
- **Part 0: the math from zero.** Every tool used later, explained with numbers before
  symbols, as if the reader is new to it. No page limit.
- **One part per topic.** For every pool question, in pool order:
  1. `origbox{<number + title as printed>}{Pool \S<n>, p.~<p>}`: the question **exactly**
     as printed, same equation numbers. If a hint changes it (e.g. "do 2 iterations, not
     1"), say so in italics inside the box. If the pool text is cut, keep it and add a note.
  2. `guidebox` with named `\step{n}{Name}` badges, written with letters so it works for
     any numbers. Add shortcut formulas and the sign traps.
  3. Worked example with the same step names, every line shown. Iterations go in a table
     (one row per iteration) followed by "Row 1 in words", and `\iterhead{k}{...}` badges.
     After each step, a sanity check (did f go down? still feasible?).
  4. One or two variants she could plausibly give (flipped inequality, active vs inactive
     constraint, non-diagonal matrix, two iterations).
  5. `examsolbox{Question <n>}`: what to write on the paper, parts (a)(b)(c), short
     working, final results in `\boxed{}`, pseudocode as numbered lines.
- Pen and paper only: every answer must be reproducible by hand. Never use "a solver says"
  as the method.

## 4. Check the numbers

Copy `scripts/check_template.py` to `<Course>/notes/checks/final_check.py`. Put in one
function per question that prints the same table the sheet shows. Fix the sheet until they
agree. Then check by hand that the steps written on the page produce those numbers.

## 5. Build and look

```bash
scripts/build.sh --preview <Course>/notes/<file>.tex
```

Fix every error and Overfull warning. Then look at the rendered pages. A question box split
across pages, a formula past the margin, or a missing glyph is a bug. If the build hangs,
use `python3 scripts/build_sections.py <file> --at examPart`.

## 6. Hand over

Report the page count and anything you assumed. Offer `/audit-sheet <file>` for an
independent check. Leave the PDF next to the `.tex`. Do not commit unless asked.

## Follow-up requests that worked before

- "Format the questions like the actual paper": blue `origbox` with exact wording,
  equation numbers, and source on the right.
- "Make the steps easy to follow": named `\step` badges, with the same names in the
  guideline and in the worked example.
- "Answers in the same style": green `examsolbox` with (a)(b)(c), boxed results, and
  numbered pseudocode.
- "These photos are hints": list them on page 1, cover each one, and follow the hint where
  it differs from the pool.
- "Explain like I'm stupid, no page limit": a bigger Part 0, slower calculations, and
  "Row 1 in words" under every table.
- "What does <symbol> mean?": answer, and add the plain explanation in the sheet at that
  spot, then rebuild.
