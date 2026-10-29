---
name: presentation
description: Prepare a presentation, either an HTML stop-motion deck (default for algorithm and data-structure talks), Beamer slides, or assets for Canva/PowerPoint slides, plus a slide-by-slide speaking script with timings, study notes and backup answers to likely questions. Use when the user has to present a paper, project or proposal.
argument-hint: <CourseFolder> <minutes> [paper.pdf] [deck|beamer|canva]
---

# Presentation: slides and script

**Input:** `$ARGUMENTS` is the course folder, the talk length in minutes, the paper or
topic, and whether the slides are Beamer or made in Canva / PowerPoint. If it is empty, or
shows up literally as a placeholder, take these from the user's message, or ask.

## 1. Read

- The paper or topic sources, and the brief plus marking criteria in `<Course>/COURSE.md`.
- Note every number you will put on a slide, and where it comes from (figure or table).

## 2. Create

**HTML deck (default when the talk explains an algorithm or data structure):**
`[DECK_DESIGN=<name>] scripts/new_note.sh <Course> deck "<Course display name>" <Descriptor>`
(styles in `docs/design/`, default `paper-stage`; a new look via `/design-language`).
Read `docs/design/README.md` first (audience, hierarchy, color, diagrams, examples), then follow
`templates/html_deck/DESIGN.md`: one everyday running example, every operation
animated one step per press with a caption and a counter, every state checked by a script
in `<Course>/presentation/checks/`. Look at it once in headless Chrome, then open the local file
for the user (`open <deck.html>`). Do not publish it as a claude.ai artifact unless the user
asks for a link. Do not generate the deck with
Canva's AI; it invents vague content and wrong diagrams.

**Beamer or Canva:**

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
