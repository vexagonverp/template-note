---
name: exam-midterm
description: Build an open-book exam sheet when the teacher has announced the TYPES of questions (e.g. "Q1 formulate an LP and its dual, Q2 prove convexity") and some are proof questions. Produces a playbook per announced question (recipe, proof template, worked example, answer), practice questions tagged by type, theory by lecture, and appendix tables. Use for a midterm, or any exam announced as question types rather than a pool.
argument-hint: <CourseFolder> [extra instructions]
---

# Midterm-style exam sheet (announced question types)

**Input:** `$ARGUMENTS` is the course folder, optionally followed by extra instructions.
If it is empty (or shows up literally as a placeholder), take the course from the user's
message, or ask.

Follow `AGENTS.md`. Layout reference: `docs/SHEET_ANATOMY.md` → "Midterm layout".
Template: `templates/midterm_template.tex`.

## 1. Read everything first

- `<Course>/COURSE.md`: exam conditions (solver allowed? calculator?) and the announced
  questions **word for word**. Note which ones the teacher called theory or proof questions.
- `<Course>/hints/`, `<Course>/transcripts/`: these outrank everything else.
- The practice material in `<Course>/materials/`: review sheets, past papers, labs.
- The slides for the lectures covered (`scripts/pdf_text.py`, `scripts/pptx_text.py`).

If an announced question is ambiguous, ask before writing.

## 2. Create the sheet

```bash
scripts/new_note.sh <Course> midterm "<Course display name>"
```

## 3. Write it

1. **Exam playbook:** exam conditions; a table of the announced questions (Q, what she
   will ask, computation or **proof**, page); habits that save marks; hand-calculation
   helpers.
2. **One "Playbook Qn" part per announced question:**
   - `origbox` with the announcement (source `Announcement, <date>`)
   - "what a full-mark answer contains" checklist
   - `guidebox` with named `\step` badges that work for any problem of this type
   - worked example(s) from the review sheet / past papers, using the same step names
   - `examsolbox`, then a `trapbox` with the usual mistake and a quick check that catches it
   - **proof questions** also get a method-choice table ("if you see … use …"), a
     `proofbox` template (Claim → Method → Steps with reasons → Conclusion □), and at least
     two filled-in proofs
3. **Practice questions:** every review / exercise question in its original order, each
   heading tagged `(trains Qn)`, each in the 4-part layout (question → steps → worked →
   answer).
4. **Theory reference** by lecture, each section tagged `(Exam Qn, Lecture m)`. Start with
   a symbol dictionary. Quote the lecturer's definitions exactly in `defbox`, and include
   every item of every list.
5. **Appendix:** derivative / formula tables and a slide index (topic → lecture, slide).

Everything must be doable by hand: corner method for 2-variable LPs; guess the tight
constraints and certify with complementary slackness; solve KKT by trying cases. Never
use "a solver says" as the method.

## 4. Check, build, look

- Verify every number with a script (copy `scripts/check_template.py` to
  `<Course>/notes/checks/`).
- `scripts/build.sh --preview <file>.tex`: fix every warning, then look at the pages.
- Report the page count and your assumptions. Offer `/audit-sheet <file>`. Do not commit
  unless asked.
