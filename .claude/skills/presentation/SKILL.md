---
name: presentation
description: Prepare a presentation, either an HTML stop-motion deck (default for algorithm and data-structure talks), Beamer slides, or assets for Canva/PowerPoint slides, plus a slide-by-slide speaking script with timings, study notes and backup answers to likely questions. Use when the user has to present a paper, project or proposal.
argument-hint: <CourseFolder> <minutes> [paper.pdf] [deck|beamer|canva]
---

# Presentation: slides and script

**Input:** `$ARGUMENTS` is the course folder, the talk length in minutes, the paper or
topic, and whether the slides are Beamer or made in Canva / PowerPoint. If it is empty, or
shows up literally as a placeholder, take these from the user's message, or ask.

**Talk or study deck?** If the user will present it, follow every step. If the deck is for the
user's own study (explain a paper or concept to them), there is no talk length and no script:
skip the script, timings and backup answers, and say so in the reply.

## 1. Read

- The paper or topic sources, and the brief plus marking criteria in `<Course>/COURSE.md`.
- Note every number you will put on a slide, and where it comes from (figure or table).

## 2. Create

**HTML deck (default when the talk explains an algorithm, data structure or protocol):**

- Create: `[DECK_DESIGN=<name>] scripts/new_note.sh <Course> deck "<Course display name>" <Descriptor>`
  (styles in `docs/design/`, default `paper-stage`; a new look via `/design-language`).
- Read `docs/design/README.md` (audience, hierarchy, color, diagrams, examples), then follow
  `templates/html_deck/DESIGN.md`: one everyday running example, every operation animated one
  step per press with a caption and a counter, every state checked by a script in
  `<Course>/presentation/checks/`.
- **Media:** before writing slides, list `assets/media/` (objects, icons, shapes, textures; see
  its README) and look at the chosen style's `refs/` for the look to aim for (refs never go on
  slides). Use a cut-out (`.cutout`, `.corner-object`, or beside a phrase in a `.split`) only
  where the object carries the idea: keys for a private key, a magnifying glass for the checker,
  a coin for a fee. Roughly one per section, on hooks, section slides and analogy slides; never
  as decoration on diagram slides. Check any words printed on an object (the stamp says
  "SOLD OUT", so it cannot mean "revoked"). If nothing fits, put a new object in
  `assets/media/inbox/` and say so.
- **A series of decks** (one per paper or chapter): keep one running example across all of
  them, write the deck CSS once and splice the same file into each, and add an overview deck
  that compares them. Give deck-only CSS classes names that cannot clash with the engine's or
  the diagram's state classes (a `.calc` layout class broke tree nodes that used `calc` as a state).
- Never generate the deck with Canva's AI; it invents vague content and wrong diagrams.

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
- Anything that is not in the source (our own arithmetic, an inference, a weakness we spotted)
  is labelled on the slide: "(our calculation)", "(our reading)". Never put words in the
  authors' mouths.
- **No code for newcomers.** If the audience is new to the topic, do not show code or
  pseudo-code. Show what it does: a table of parts (what it stores, what each button does, who
  may press it, what it costs) with the real names only as small grey labels, and actions as
  plain sentences ("IU presses Cancel on Binh's diploma"). Formulas become worked numbers with
  labels ("value there: 10² − 10 + 3 = 93").
  **Exception:** code is fine when the audience already programs (a data structures or
  algorithms class). Keep it short, put it next to the diagram it drives, and put the real
  numbers from the running example in the comments (`update[lane] = x  # 20k, 40k, 50k`).
- **Register:** spoken, short sentences for the script; no em dashes or contractions on slides.

## 4. Build and check

- **HTML deck:** `python3 scripts/html_deck.py shots <deck.html> [slide:step ...]` screenshots
  every slide at its last step (plus any middle steps you name) into `.temp/shots/<deck>/`, with
  contact sheets in `grids/`. Look at every sheet and the middle steps of each animation. Fix
  anything clipped, overflowing the bottom, or overlapping (a corner object against a long title
  is the usual one), then shoot again. Then open the local file for the user
  (`open <deck.html>`). Do not publish it as a claude.ai artifact unless the user asks for a link.
- **Beamer / script / assets:** build every file with `scripts/build.sh --preview` and look at
  every slide. Convert assets with `pdftoppm -r 200 -png -singlefile <asset>.pdf <asset>`.
- **Independent review** for a big deck or a series: start a fresh-context agent with the deck
  paths, the source papers and the audience, and ask it (no edits) for jargon used before it is
  explained, jumps between slides, anything that still reads like code, and every claim or
  number that the source does not support. Apply the fixes and shoot again.
- **Sending a deck to someone:** `python3 scripts/html_deck.py bundle <deck.html>` writes one
  self-contained file to `.temp/share/` with every local image embedded, so it opens offline with
  a double-click (fonts fall back to system fonts when offline). Check it with `shots` on the
  bundled file, then `open -R` it so the user can send it. Re-bundle after every change.
- Report the slide count (and the total script time if there is a script). Do not commit unless asked.
