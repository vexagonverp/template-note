# Prompt: turn a lecture recording / transcript into an exam-alert outline

Give the agent (or any LLM) the raw transcript or auto-captions of one lecture. Save the
result as `<Course>/transcripts/L<NN>.md` and add a line for it in `COURSE.md`.

---

Below is the transcript of a <Course> lecture (<date>, topic: <topic>). Turn it into an
outline a student can use to prepare for the exam.

Rules:
- Split it into segments by topic. For each: `### Segment N: <title>` (add the time range
  if the transcript has timestamps, e.g. `**00:00 – 05:00**`), then a `**Topics:**` line,
  then short bullets.
- Mark everything the lecturer stressed with `**[EXAM ALERT]**`: "this will be on the exam",
  "I guarantee", "remember this", repeated points, worked examples done on the board.
- Quote the lecturer's exact words in bold quotes when they say what will or will not be
  tested: *Professor's note:* **"…"**. Write any question they asked out loud as
  *Exam question:* … .
- Write what was ruled out under **Not on the exam:**.
- Do not invent content that is not in the transcript. If a passage is unclear, write
  `[unclear]` instead of guessing.
- End with **Exam checklist (lecturer's "guaranteed" topics)**: a numbered list, most
  certain first, then one line of **Teacher's tip** if they gave one.

<paste transcript here>
