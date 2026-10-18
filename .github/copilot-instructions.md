Follow the rules in `AGENTS.md` at the repo root. Short version:

- New documents come from `scripts/new_note.sh <Course> <kind>` (midterm, final, theory, qbank,
  cheatsheet, lab, report, proposal, exercise, essay-en, essay-vi, slides, script, asset, paper).
  Never edit a file in `templates/` for one course.
- Read everything first. Trust hints and transcripts over the question pool, the pool over slides.
- Computational questions: question box (exact text + source) → step-by-step guideline →
  worked example → answer box. Theory: lecturer's definition → what it is / how it works /
  tiny example / why it matters.
- Answers must be doable by pen and paper. Verify numbers with a script, never cite a solver as the method.
- Graded work: the file name is the submission name; lab numbers come from the saved notebook output.
- Build with `scripts/build.sh` (tectonic), fix every Overfull warning, look at the rendered pages.
- Read a file before editing; make small edits; scratch goes in `.temp/`; never `rm` with globs.
- Plain, short sentences. Explain like the reader is new to the topic.
- Don't commit or push unless asked.
