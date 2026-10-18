---
name: transcript
description: Turn a lecture transcript, auto-captions or recording notes into an exam-alert outline (segments, [EXAM ALERT] tags, the lecturer's exact words on what will or won't be tested, and a final checklist), saved under the course's transcripts folder. Use when the user gives a transcript or recording of a lecture or review session.
argument-hint: <transcript file or CourseFolder> [lecture number / date]
---

# Transcript → exam-alert outline

**Input:** `$ARGUMENTS` is a transcript file (txt, md, srt, vtt, pdf) or a course folder,
optionally with the lecture number and date. If it is empty, or shows up literally as a
placeholder, use the transcript pasted in the user's message, or ask for it.

## Steps

1. Read the whole transcript. For a PDF, use `python3 scripts/pdf_text.py`. For srt/vtt,
   ignore the timestamps' formatting but keep the times.
2. Write the outline (format below) to `<Course>/transcripts/L<NN>.md`, using
   `L<NN>-review.md` for a review session.
3. Add one line for it to the table in `<Course>/COURSE.md` → "Hints and transcripts",
   e.g. `transcripts/L05.md | lecture 5 summary, 3 [EXAM ALERT]s on hash functions`.
4. If an exam sheet already exists for this course, list the alerts it does not cover yet,
   and offer to add them.

## Outline format

- Split it into segments by topic. For each segment:
  - `### Segment N: <title>`, with the time range if there are timestamps (e.g. `**00:00 – 05:00**`)
  - a `**Topics:**` line
  - short bullets
- Mark everything the lecturer stressed with `**[EXAM ALERT]**`: "this will be on the
  exam", "I guarantee", "remember this", points they repeated, and examples worked on the board.
- Quote the lecturer's exact words in bold quotes when they say what will or won't be
  tested: *Professor's note:* **"…"**. Write any question they asked out loud as
  *Exam question:* … .
- Put what was ruled out under **Not on the exam:**.
- Do not invent content that isn't in the transcript. Where a passage is unclear, write
  `[unclear]` instead of guessing.
- End with **Exam checklist (lecturer's "guaranteed" topics)**: a numbered list, most
  certain first. Then one line of **Teacher's tip** if they gave one.

Mixed-language transcripts (e.g. English content, Vietnamese logistics): write the outline
in English, but quote the original words as spoken.
