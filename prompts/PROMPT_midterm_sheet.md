# Prompt: build a midterm exam sheet (announced question types)

Use this when the teacher announced the *types* of questions instead of giving a pool.
Copy it, fill the `<...>` parts, and give it to the agent from the repo root.

---

Help me prepare an open-book exam sheet for the **<Course>** midterm. Everything is in
`<Course>/`. Use `templates/midterm_template.tex` (`scripts/new_note.sh <Course> midterm`).

- Exam conditions: <open book, printed material only, pen and paper, no solver>.
- The teacher announced these questions (word for word):
  1. <Q1 ...>
  2. <Q2 ...>
  3. <...>
  She said <which ones> are **theory questions that need proofs**.
- Practice material: `<Course>/materials/<review sheet>.pdf`, past papers in `<path>`, labs.
- Lectures covered: `<Course>/slides/` lectures <N–M>.

Follow `AGENTS.md` and `docs/SHEET_ANATOMY.md` (midterm layout):

1. Lead with the exam playbook: one part per announced question, each with what a
   full-mark answer contains, a step-by-step recipe that works for any numbers, a worked
   example, the answer box, and the usual trap.
2. For every proof question, give a method-choice table and a proof template I can copy,
   plus at least two filled-in proofs.
3. Then every practice question in its original order, tagged "trains Qn", in the
   question → steps → worked → answer layout.
4. Then theory by lecture, tagged with the exam question it feeds, quoting the lecturer's
   definitions exactly (all items of every list).
5. Appendix: symbol dictionary, derivative / formula tables, slide index.

Everything must be doable by hand. Verify every number with a script, but never use "a
solver says" as the method. No page limit: explain the math like I'm new to it. Build
with tectonic, fix all warnings, and check the rendered pages.

**Definition of done:** the sheet builds with no errors or Overfull warnings; every
announced topic, hint and transcript [EXAM ALERT] is covered and listed on page 1; every
question has all four parts (question, steps, worked example, answer); every number was
checked with a script; every slide list has its full count. State the page count. Then run
`prompts/PROMPT_audit.md` in a fresh session.

Ask me if anything is unclear before you start writing.
