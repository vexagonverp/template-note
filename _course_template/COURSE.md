# <Course name>

Student: Your Name (YOUR-ID)
Lecturer: <name>
Course code: <code>

## Exam

- **Date / time:** <e.g. Monday 19 Oct, 6:30>
- **Format:** <open book / closed book, printed material only?, calculator?, solver allowed?>
- **Length / number of questions / marks split:** <e.g. 5 questions: 3 theory 50%, 2 computation 50%>
- **Page limit for notes:** <none / 2 sides (use the cheatsheet template)>
- **Announced topics** (copy the teacher's message word for word):
  1. ...
  2. ...
- **Not expected** (what the lecturer ruled out): ...

## Hints and transcripts

Photos of the board / slides shown in class go in `hints/`. Lecture transcripts or
recording summaries go in `transcripts/` (make them with `prompts/PROMPT_transcript.md`).
One line per file, so an agent knows what each one is without guessing.

| File | What it shows |
|------|---------------|
| `hints/IMG_0001.jpg` | board: "Q1: find the dual problem, solve with dual-based method" |
| `hints/IMG_0002.jpg` | slide shown in class: Lecture 6, slide 29 (KKT system) |
| `transcripts/L05.md` | lecture 5 summary, 3 [EXAM ALERT]s on hash functions |

## Assignments

Paste each brief **word for word** (any language), with its deadline and marking criteria.

| Item | Brief | Deadline | Weight | Length | Submit as |
|------|-------|----------|--------|--------|-----------|
| Lab 1 | below | <date> | 10% | -- | notebook + report PDF in a zip |
| Essay | below | <date> | 30% | 15–30 pages | PDF |

<details><summary>Lab 1 brief</summary>

<paste the brief here>

</details>

## Where things are

- `slides/` lecture slides (PDF, PPTX)
- `materials/` question pools, past exams, exercise sheets, lab handouts, textbook, assigned papers
- `hints/` photos of hints, `transcripts/` lecture transcripts
- `notes/` exam sheets, `labs/` lab notebooks + reports (+ `figs/`), `assignments/` reports,
  essays, proposals, `presentation/` slides, script, `assets/`
- `submit/` packaged hand-ins (made by `scripts/package_submission.sh`)

## Notes for the agent

Course-specific things: notation the lecturer uses, a past exam that shows the style,
preferences ("do 2 iterations, not 1"), things that went wrong last time.
