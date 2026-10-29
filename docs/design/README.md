# Design reference

This folder holds the general rules (this file) and one folder per design style:

```
docs/design/
  README.md            general rules for anything visual (this file)
  <style>/README.md    the style's spec: brief, palette and roles, pairings, type, layout, rules, contrast
  <style>/style.css    tokens + part overrides that decks load (via scripts/html_deck.py)
  <style>/preview.html sample slides in that style
  <style>/refs/        inspiration: posters, screenshots, GIFs of motion. Look, never ship.
```

Media that goes on slides: shared by every style in `assets/media/` (objects, icons, shapes,
textures; see its README). Everything there is style-free (original colors, no style
applied), and each style decides how to show it (Paper & Stage turns images grey). Style-only
inspiration stays in the style's `refs/`. Per-talk media goes in
`<Course>/presentation/assets/`. Cut and resize with `ffmpeg`, `gifsicle`, `cwebp`; GIFs
are read by extracting frames into `.temp/` first.

How anything visual in this repo should look and read: HTML decks, slide assets, figures,
posters, claude.ai artifacts. Writing rules live in `WRITING_STYLE.md`; deck mechanics in
`templates/html_deck/DESIGN.md`. This file is the "why" behind both.

Precedence: the user's own words, then the design language picked for the piece, then
this file.

## 1. Start from the audience and the one job

Before drawing anything, write down three things: who looks at it (classmates who have
never seen the topic, a lecturer marking criteria, a supervisor), where (projector in a
bright room, phone, printed A4), and the single job of the piece (understand one algorithm,
compare four options, remember three takeaways). Every later choice should serve that job.

## 2. Hierarchy

- **One idea per slide or panel.** If it needs two headlines, it is two slides.
- **Three levels of text at most:** headline, body, small label. Make each level clearly
  different in size (at least 1.5x apart), not just in weight.
- **The headline says the point**, not the topic: "Find the 70k item in 4 steps" beats
  "Search".
- **Read order is top-left to bottom-right.** Put the thing to look at first there, or make
  it the only colored thing on the slide.

## 3. Type

- Pair a characterful display face (titles only) with a quiet body face; add a monospace
  for numbers, prices, complexity and code.
- Slide sizes on the 1600x900 stage: body 26-34px, labels 16-20px (uppercase, tracked
  +0.12em or more), headlines 60px and up. Nothing under 16px.
- Line length about 45-75 characters; line height 1.3-1.6 for body, 0.9-1.05 for big titles.
- Use `tabular-nums` where digits line up. Use real units (`70k`, `O(log n)`, `20 ms`).

## 4. Color

- Define colors once as **role tokens** (`--ink`, `--accent`, `--go`, `--stop`, ...) and use
  only those. A role says what a color means, so it stays consistent across slides.
- **One accent** for "look here / current step". Keep status colors separate: one for
  found / correct, one for rejected / too far.
- **Contrast:** body text at least 4.5:1, large text (24px+ or 19px+ bold) at least 3:1.
  Check with `python3 scripts/contrast.py <design>`.
- Never carry meaning by hue alone (about 1 in 12 men is red-green color blind): pair color
  with shape, a label, a dashed border or a position.
- Projectors wash colors out. Avoid thin light-grey text and pale tints for anything that
  must be read.

## 5. Layout

- Work on a grid. Align edges; give repeated items the same size and the same inner spacing.
- Leave space. A half-empty slide reads faster than a full one.
- Keep a safe margin (about 70-100px on the 1600x900 stage) for text; only full-bleed tiles,
  images or bands may touch the edge.
- Put a caption bar in the same place on every animated slide so eyes know where to look.

## 6. Diagrams and stop-motion

- **Draw the real mechanism**, not a decoration: the actual boxes, pointers and values.
- **One press = one change** (one comparison, one pointer move, one coin flip). Say what
  happened in a caption, in plain words, and keep a counter (boxes looked at, comparisons).
- Keep everything else still while one thing moves. Use the accent for the moving part,
  the "found" color for the answer, the "rejected" color (dashed) for what was checked and
  skipped.
- Show the same small example (6-10 items) across search, insert and delete, so the
  audience learns the picture once.
- **Every number on a diagram is checked by a script** before it goes on a slide
  (`<Course>/presentation/checks/`). Going backwards must redraw the exact earlier state.

## 7. Examples

- One running example from everyday life, introduced early and reused (the shop's price
  filter, a queue at the clinic, contacts sorted by name).
- Abstract numbers get a label the audience recognizes (`70k Mouse pad`, not `70`).
- Avoid examples that need explaining before they help. Never claim a real company uses a
  technique unless a source says so.

## 8. Motion

- Motion explains change; it is not decoration. Slide transitions are short (0.3-0.5 s);
  diagram moves 0.4-0.5 s with ease-out.
- Respect `prefers-reduced-motion`.

## 9. Words on visuals

- Plain words, short sentences, no em dashes, no slogans, no "not X but Y".
- At most 5 bullets, each one line if possible.
- Numbers before symbols: show `4 boxes instead of 7` before `O(log n)`.

## 10. Design languages

A design language is a named, reusable look: a token file plus a few part overrides in
`docs/design/<name>/` (spec in `README.md`, tokens in `style.css`, `preview.html`). Make one
with `/design-language`. Each must say:

1. **Concept and mood** in one or two sentences (what world it borrows from).
2. **Palette** as raw colors, then **role tokens** mapped onto them, with the allowed
   pairings (which shape or text color may sit on which fill).
3. **Type**: display, body and mono faces with fallbacks, and how they contrast.
4. **Layout** habits (where text sits, how images or tiles are used).
5. **Rules** (what is never done: shadows, gradients, rounded cards, text on tiles ...).
   Include how the style shows the shared, style-free elements in `assets/media/` (as is,
   greyed with a CSS filter, with or without `--shadow`); never add restyled copies there.
6. **Checks**: contrast table from `scripts/contrast.py`, and a preview file.

| Name | Mood | Use for |
|------|------|---------|
| [`block-shapes`](block-shapes/README.md) | Bauhaus geometric: flat color tiles with big cropped shapes, giant condensed headlines, light body text | seminars, algorithm talks, anything that should look bold and graphic |
| [`paper-stage`](paper-stage/README.md) (default) | kinetic typography: warm paper slides and black stage slides, one red key word per phrase revealed word by word, paper cut-outs, pinned card, arcs | punchy explainers, hooks, short talks with few words per slide |

## 11. Final check (any visual piece)

- [ ] The one job is clear from the first view.
- [ ] Every text color passes contrast; nothing important under 16px.
- [ ] Every color comes from a token; status is never shown by hue alone.
- [ ] Every number is checked; every animated step can be reversed.
- [ ] Looked at it once rendered (headless Chrome screenshot or the build preview) at the
      real size, and fixed what was clipped, overlapping or too small.
