---
name: presentation
description: Prepare a presentation, either Beamer slides or assets for Canva/PowerPoint slides, plus a slide-by-slide speaking script with timings, study notes and backup answers to likely questions. Use when the user has to present a paper, project or proposal.
argument-hint: <CourseFolder> <minutes> [paper.pdf] [beamer|canva]
---

# Presentation: slides and script

**Input:** `$ARGUMENTS` is the course folder, the talk length in minutes, the paper or
topic, and whether the slides are Beamer or made in Canva / PowerPoint. If it is empty, or
shows up literally as a placeholder, take these from the user's message, or ask.

## 1. Read

- The paper or topic sources, and the brief plus marking criteria in `<Course>/COURSE.md`.
- Note every number you will put on a slide, and where it comes from (figure or table).

## 2. Create

```bash
scripts/new_note.sh <Course> script "<Course display name>"     # always
scripts/new_note.sh <Course> slides "<Course display name>"     # if Beamer
scripts/new_note.sh <Course> asset  "<Course display name>"     # per math image, if Canva / PowerPoint
```

- Charts for Canva come from `scripts/figstyle.py`: `use("slides")`, then `save(fig, name, folder="<Course>/presentation/assets")`.
- Keep asset sources in `<Course>/presentation/assets/`. Never put them in `.temp/`.

## 3. Content

- **Frame arc:** hook, then a roadmap with 3 points, then problem → method → one worked
  example → results → limits → summary.
- One idea per slide, at most 5–7 bullets.
- Beamer:
  - `darkframe` for the title, the hook and the summary
  - `\analogy{}` once per hard idea
  - a `% SAY:` note under every frame
  - `% REPLACE` on every placeholder until it is replaced
- **Script:** one `\slide{n}{title}{m:ss}` per slide with `\onscreen{}`, `\say` and, where
  useful, a `\tip{}`. The times must add up to the talk length.
- The script's "How to use" box gives the slide count, the total time, a one-sentence
  fallback, and where the worked example is.
- After the slides: "Study notes" (what the speaker must understand to answer questions)
  and "Backup: answers for likely questions" (5–8 questions, short answers).
- Every number on a slide comes from the source, with its figure or table cited. Mark
  values read off a chart as approximate.
- **Register:** spoken, short sentences for the script; no em dashes or contractions on slides.

## 4. Build and check

- Build every file with `scripts/build.sh --preview` and look at every slide.
- For assets, convert with `pdftoppm -r 200 -png -singlefile <asset>.pdf <asset>`.
- Report the total script time and the slide count. Do not commit unless asked.
