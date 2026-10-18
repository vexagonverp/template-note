# Prompt: build a theory-course exam sheet + question bank

For courses tested on definitions, lists, comparisons and short essays (research methods,
ethics, software architecture, the theory half of security). Paste it into a **fresh
agent session opened at the repo root**, so it is never length-limited.

---

You are building an open-book reference for **<Course>** (<university>), covering
**<midterm / final / both>**. It has two files that each build on their own and point at
each other:

1. `<Course>/notes/<Name>_<ID>_Theory_Notes.tex` from `scripts/new_note.sh <Course> theory`
2. `<Course>/notes/<Name>_<ID>_Question_Bank.tex` from `scripts/new_note.sh <Course> qbank`

## Sources (read ALL of it first)

- Slides: `<Course>/slides/*` (PDF: `python3 scripts/pdf_text.py`, PPTX:
  `python3 scripts/pptx_text.py`). Image-only pages: `scripts/pdf_pages.sh`, then look.
- Announcement and grading split: `<Course>/COURSE.md`.
- Transcripts / review-session notes: `<Course>/transcripts/` (every [EXAM ALERT] and
  "guaranteed" item goes in the overview box and must be covered).
- Past papers: `<Course>/materials/`. Textbook (for the "where to look" index): `<path>`.
- Gold standard for tone and density: `<path to a finished sheet you liked>`.

## Fidelity rules (most important)

- **Keep the slides' exact wording** for definitions, named principles and lists, in a
  `defbox` citing the slide. **Bold the exact term being defined.**
- **Then extend the meaning:** after each quoted point add 1–3 sentences of plain English,
  why it matters, a tiny concrete example, and any exam trap. Use the fixed labels
  `\lbl{What it is:} / \lbl{How it works:} / \lbl{Tiny example:} / \lbl{Why it matters / trap:}`.
- **If a slide has N items, the note has N.** Ordered lists go in a `memobox` with a memory hook.
- Look-alike terms get a compare table (Term | slide wording | plain English + example).
- Label every top-level section `\exam{Midterm}`, `\exam{Final}` or `\exam{Midterm + Final}`,
  and start it with a `Source:` line.

## Theory file must have

- Title block with the rules line ("Open Book · Open Notes (paper only) · No electronics").
- Overview box: format, grading split, what the lecturer said will appear (quoted, with
  `\sref{}`), what is **not** expected, **the numbers you must memorise**, the answer template.
- Jargon decoder (glossary) with `\label`s, referenced later with `\gl{}`.
- One section per topic in this order: <outline / table of contents>.
- Situational questions (`scenariobox` + the answer skeleton) if the course has them.
- "Where to look if a question goes past the slides" (topic → textbook section → page).
- Exam-day pitfalls box and the quick-reference summary at the end.

## Question bank must have

- "How to use this bank" box and the tag legend: `\qtag{likely}` `\qtag{past exam A}`
  `\qtag{compute}` `\qtag{practice}` `\qtag{twist}` (+ any graded-component tag).
- Past papers transcribed word for word with marks, and a "which topics come up most" table.
- ~6–12 questions per topic group, each: `\Q{}` header → question alone in `qbankbox` →
  Answer → Why, step by step → Trap to avoid → Also asked as (2–3 rephrasings).
- Every [COMPUTE] item: formula first, a worked example, a sanity check. Verify the numbers
  with a script (`scripts/check_template.py`).
- Cover at least: <list of must-have questions>.
- Twist questions, and <N> mock exams graded Easy / Medium / Hard.

## Definition of done

Both files build with no errors or Overfull warnings (`scripts/build.sh`); every slide topic
is covered in the slide's own words plus the extension; every section is labelled; every
list has its full count; the bank has worked answers for every topic with verified
numbers. State the page counts and the number of questions. Err on the side of
completeness: there is no length limit. Then run `prompts/PROMPT_audit.md` on the result.
