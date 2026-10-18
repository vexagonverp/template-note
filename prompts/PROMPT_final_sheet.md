# Prompt: build a final exam sheet (question pool)

Copy this, fill the `<...>` parts, and give it to the agent from the repo root.

---

Help me prepare an open-book exam sheet for **<Course>**. Everything is in `<Course>/`.

- Teacher's announcement (exam date, format, topics): see `<Course>/COURSE.md`
  (or paste it here).
- The questions will most likely come from `<Course>/materials/<question pool>.pdf`.
  The teacher will **substitute the numbers**, so for each question I need a step-by-step
  guideline that works for any numbers, a worked example, and a box with what to write on
  the exam paper.
- Every photo in `<Course>/hints/` is a hint the teacher gave about the exam. Put them
  on page 1 and make sure each is covered.
- A past exam to show the question style: `<path>`.
- Exam conditions: <pen and paper, no solver / calculator allowed / ...>.

Follow `AGENTS.md` and `docs/SHEET_ANATOMY.md`. The sheet has no page limit: be verbose
and explain the math like I'm new to it (start with a "math from zero" part). Copy each
question exactly as printed, with its source. Verify every number with a script before
writing it. Build with tectonic, fix all warnings, and check the rendered pages.

**Definition of done:** the sheet builds with no errors or Overfull warnings; every
announced topic, hint and transcript [EXAM ALERT] is covered and listed on page 1; every
question has all four parts (question, steps, worked example, answer); every number was
checked with a script; every slide list has its full count. State the page count. Then run
`prompts/PROMPT_audit.md` in a fresh session.

Ask me if anything is unclear before you start writing.
