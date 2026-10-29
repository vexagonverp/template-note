# Paper & Stage

Punchy kinetic-typography slides for normal 16:9 decks. Slides alternate between a warm
off-white **paper** world and a pitch-black **stage** world, with a hard cut between them.
Short phrases build word by word on their own (one press per slide, not per word); exactly
one key word per phrase is red. Paper cut-out
objects, a pinned grey card, big soft grey arcs and halftone figures carry the visuals.

| File | What it is |
|------|------------|
| `style.css` | tokens + parts (worlds, phrases, labels, arcs, halftone, pinned card, cut-outs, emoji, phone mock-up) |
| `preview.html` | six sample slides, three paper and three stage |
| `refs/` | inspiration only (posters, screenshots), indexed in `refs/README.md`. Usable objects go to `assets/media/inbox/` |

Use it: `DECK_DESIGN=paper-stage scripts/new_note.sh <Course> deck "Course"`, or
`python3 scripts/html_deck.py design <deck.html> paper-stage`.

## Palette and roles

Nothing is colored except the one red key word (and the push-pin). Shared objects from
`assets/media/` keep their own colors there; this style turns every slide image grey
(`filter: grayscale(1)` in `style.css`), so any object can be used as is. A school or client logo
(`<img class="logo">`) keeps its real colors.

| Color | Hex | Role | Used for |
|-------|-----|------|----------|
| Paper | `#F6F2EA` | `--card` (paper slides) | slide surface |
| Darker paper | `#E9E3D8` | `--paper`, `--tint` | quiet fills, counter chip, table header |
| Ink | `#1F1F1F` | `--ink` (paper) | all text on paper |
| Warm grey | `#66625B` | `--muted` (paper) | labels, small text |
| Stage black | `#050505` | `--card` (stage slides), `--chrome` | stage surface, around the slide |
| White | `#FFFFFF` | `--ink` (stage) | all text on stage |
| Grey | `#A8A8A8` | `--muted` (stage) | labels on stage |
| Red, flat | `#E8505B` | `--accent` (paper) | the key word on paper |
| Red, glow | `#E8202A` | `--accent` (stage) | the key word on stage, with a red outer glow |
| Card grey | `#9A9A9A` | `--pop` | pinned card, cut-out props |
| Arc grey | `#BDBAB4` | `--line` | arcs, grid, resting lines |

A slide with class `stage` redefines the tokens for that slide, so every shared part
(tables, code, diagrams, captions) flips to the black world automatically.

## Contrast (checked with `python3 scripts/contrast.py paper-stage`)

| Text on background | Ratio | Rule |
|--------------------|-------|------|
| ink on paper | 14.8 | ok |
| warm grey on paper | 5.4 | ok |
| **red `#E8505B` on paper** | **3.3** | **large text only**: key words and headlines, never small text |
| red `#E8202A` on black | 4.5 | ok |
| white on black | 20.4 | ok |
| grey `#A8A8A8` on black | 8.6 | ok |
| ink on card grey | 5.9 | ok |

## Type

One family: **Inter Tight** (fallback Manrope), tight tracking (-0.03em), tight leading,
centered. Phrases are 800 weight, about 112px (96px beside an object). The key word is
larger (1.22em), 900 weight and red; on stage it glows and pulses once when it appears.
Small technical labels (corner marks, a code like `03 · LEVELS`, a barcode) use the same
family at 15px.

## Parts

| Part | Markup |
|------|--------|
| Stage slide | `<section class="slide stage">` |
| Phrase (builds itself) | `<p class="phrase"><span class="w">Each</span><span class="w">lane</span><span class="w key">skips</span></p>` (one `.key` only, up to 7 words). `style="--d:.5s"` delays the start; `data-step="1"` on the phrase makes it wait for a press |
| Corner labels | `<div class="hud"><i></i><i></i><i></i><i></i><span class="code">03 · LEVELS</span><span class="code2">...</span><span class="barcode"></span></div>` |
| Faint square grid | `<div class="grid-bg"></div>` |
| Big soft arcs | `<div class="arcs"></div>` |
| Halftone figure (stage) | `<div class="halftone"></div>` |
| Pinned card (drops in) | `<div class="pin-card"><h3>Title</h3><ul><li><svg>…</svg>Item</li> ×3</ul></div>` |
| Cut-out object | `<div class="cutout"><img src="..."></div>` (shared engine part): drops in with a bounce and a soft contact shadow; `.corner-object` pins a small one top-right and hides the corner label |
| Emoji punchline | `<div class="emoji-pop">🚀</div>` |
| Phone mock-up (stage) | `<div class="mock-phone"><div class="scr"><div class="bar"></div><div class="row hit">…</div></div></div>` |

Object beside a phrase: wrap both in `<div class="split">`; the phrase then aligns left.

## Motion

- **One press per slide.** When a slide (or a phrase with `data-step`) appears, its words pop
  in by themselves, 0.12 s apart, with a quick scale-up and a slight overshoot. Objects
  (cut-out, pinned card, emoji) animate in on their own too. Put `data-step` on a single
  word or object only if you really want a click before it.
- Hard cut between slides (no sideways slide); a slow, gentle push-in (2.5%) while a slide
  is on screen.
- The red glow pulses once when the key word lands on a stage slide.
- Cut-outs drop in with a small bounce and settle their shadow.

## Rules

- One idea per slide. Phrases of 2-5 words.
- Exactly one red word per phrase. No other accent colors, gradients or decorative shapes.
- Red never on small text.
- Only original logos and UI; no real brand marks or real app screens.
- Cut-out objects come from `assets/media/objects/` (21 ready PNGs: arrows, hands, dice, magnifying glass,
  cameras, brain, pencil, push-pin, laptop, phone, exclamation marks). New ones: drop them
  in `assets/media/inbox/` and ask Claude to process the inbox.

<details><summary>Original brief (written for short vertical video; the video-only parts are not used)</summary>

> Create a motion design language called "Paper & Stage".
>
> Concept: a fast, punchy kinetic-typography explainer for short-form video. Scenes
> alternate between two worlds: a warm off-white "paper" world and a pitch-black "stage"
> world. Each switch lands on a beat, like a cut in a reel.
>
> Palette: Paper #F6F2EA, stage black #050505; Ink #1F1F1F on paper, white #FFFFFF on stage;
> One red accent: #E8202A with a soft glow on black, #E8505B flat on paper; Greys for props:
> card #9A9A9A, arcs #BDBAB4. Red marks exactly one key word per phrase. Nothing else is
> colored.
>
> Typography: One bold geometric sans (Inter Tight 800 or Manrope 800), tight tracking
> (-0.03em), tight leading, centered. Short phrases of 2–5 words, revealed word by word. The
> key word is larger, heavier and red. On black it gets a red outer glow. Tiny technical
> labels (6–8% of headline size) in the same font: a barcode, a frame code, corner marks, a
> thin grid.
>
> Visual elements: 1. Realistic cut-out objects with soft contact shadows, floating over a
> faint square grid (a lightbulb for an idea, a key for access, a ladder for levels).
> 2. Halftone dot texture for figures and silhouettes on black, fading to black. 3. A grey
> paper card pinned with a glossy red push-pin, holding a short title and a list of 3 items
> with simple line icons. 4. Large soft grey arcs sweeping through the frame as background
> structure. 5. Glossy 3D emoji for the punchline beat. 6. Clean phone or app UI mockups on
> black for "real world" moments.
>
> Motion: Words pop in one at a time with a quick scale-up and slight overshoot. Slow camera
> push-in during each scene; hard cut between paper and stage. Red glow pulses once when the
> key word lands. Objects slide or drop in with a small bounce and settle their shadow.
> 9:16 vertical, 1–2 seconds per beat, never more than one idea on screen.
>
> Rules: No other accent colors, gradients or decorative shapes. Never more than one red
> word per phrase. Use only original logos and UI; no real brand marks or app interfaces.

Not used for decks: 9:16 vertical, 1–2 seconds per beat, cuts timed to music beats. Labels
are 15px instead of 6–8% of the headline so they stay readable on a projector.
</details>
