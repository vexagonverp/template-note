# Prompt: build a presentation (slides + script)

---

Help me prepare a <N>-minute presentation for **<Course>** on <paper / topic>.
Sources: `<paper.pdf>` and `<Course>/COURSE.md` (assignment brief, marking criteria).

- Slides: `scripts/new_note.sh <Course> slides` (Beamer), or tell me the slides are in
  <Canva / PowerPoint> and make only the assets: math images from
  `scripts/new_note.sh <Course> asset`, charts with `scripts/figstyle.py` (`use("slides")`).
  Keep asset sources in `<Course>/presentation/assets/`, not in `.temp/`.
- Script: `scripts/new_note.sh <Course> script`. One `\slide{n}{title}{m:ss}` per slide with
  `\onscreen{}`, `\say`, and a `\tip{}` where useful. The times must add up to <N> minutes.
- Frame arc: hook → roadmap (3 points) → problem → method → one worked example → results →
  limits → summary. One idea per slide, at most 5–7 bullets.
- After the slides: "Study notes" (what I must understand to answer questions) and
  "Backup: answers for likely questions" (5–8 questions, short answers).
- Every number on a slide must come from the paper; cite the figure/table it came from.
  Mark approximate values read off a chart as approximate.
- Register: spoken, short sentences on the script; no em dashes or contractions on slides.

Build both, fix all warnings, and check the rendered pages.
