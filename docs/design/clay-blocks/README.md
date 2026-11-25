# Clay Blocks

Earth and houses, cut from paper. Three flat colors and nothing else, with pictures and lists
set in a few big hand-cut blocks that do not quite line up. Calm, warm and solid; made for
university talks, with houses and land as its picture language.

| File | What it is |
|------|------------|
| `starter.html` | **start here**: one slide per part, with its limits in the comment above it (12 KB, no drawings inside). Every new clay-blocks deck begins with these slides |
| `preview.html` | the same slides, rendered (look at it in a browser; do not read its source). Sample advice and numbers, not facts |
| `style.css` | tokens + parts; decks load it through `scripts/html_deck.py` |
| `make_shapes.py` | draws the block outlines, motifs and scenes; same output every run |
| `refs/` | six of the pins it came from. Look, never ship |

Use it: `DECK_DESIGN=clay-blocks scripts/new_note.sh <Course> deck "Course"`, or
`python3 scripts/html_deck.py design <deck.html> clay-blocks`.

## The brief (the user's words, in order)

> - "the color distribution will be raw clay iron brown turquoise. In 60/30/10"
> - "just 3 color"
> - "D0BCAC 461C0C 269991"
> - "I dont like any of the cutaaway"
> - "i know we are doing 3 color but maybe we can have it turquoius be the highlight bit ?"
> - "i dont like the random quite spot in the image. so no litho ? the image outline is nice and
>   i like the slide five thing to check the blocky bit that is not even with each other"
> - "when the block is big it nice but when it small it just look confusing"
> - "maybe some slide i need to have photo of my project this is mostly for uni presentation"

## Palette and roles

| Color | Hex | Share | Role tokens | Used for |
|-------|-----|-------|-------------|----------|
| Raw clay | `#D0BCAC` | about 60 | `--card --paper --stop` | slide surface, empty space, text on brown |
| Iron brown | `#461C0C` | about 30 | `--ink --muted --line --accent --chrome` | text, blocks, outlines, code, brown slides |
| Turquoise | `#269991` | 10 at most | `--hi --tint --go --pop` | the one thing to look at |

The split is for the whole deck, not each slide. Turquoise usually lands near 5%; do not pad
it to reach 10. A slide with class `stage` is a brown slide: the roles flip. Highlight fills
use `--hi` with `--on-hi` text, which is the same on both.

## Contrast (`python3 scripts/contrast.py clay-blocks`; stage pairs are the same two colors)

| Text on background | Ratio | Rule |
|--------------------|-------|------|
| brown on clay, clay on brown | 8.0 | any text |
| brown on turquoise, turquoise on brown | 4.2 | **large text only**: 24px+, or 19px+ bold |
| turquoise on clay | 1.9 | **shapes only, never text**. Small shapes get a brown outline or sit on brown |

Status without more colors: found = solid turquoise with a brown outline, looking = solid
brown, rejected = dashed and struck through, ruled out = dashed.

## Type

**Archivo** for everything: 900 and tight (-0.04em) for titles, 500-700 for text. Code in
JetBrains Mono with ligatures off, so `===` stays three signs. Slide titles 78px, poster
title 174px capitals, brown-slide question 200px capitals. It covers Vietnamese.

## What to say, which slide

Markup for every row is in `starter.html`. Write `{{scene ...}}` where a drawing goes; `shots`,
`pdf`, `bundle` and `fill` draw it.

| You want to show | Slide (`data-id` in the starter) | Limits |
|------------------|----------------------------------|--------|
| the title | Poster (`poster`) | 2 lines of 11 capitals, or `h1.long` 3 lines of 16; 3-5 section tiles |
| a hook, a section opener | Question (`question`) | 3 lines of 10 capitals, one `<em>` |
| a list, parts, reasons, roles | Tiles (`tiles`) | 2-6 tiles, caption up to 2 short lines |
| points with a drawing | Text and drawing (`text`) | 2-4 points, headline 3 lines of 17 letters |
| amounts to compare | Blocks to size (`amounts`) | 2-5 values, none under 2% of the total; only `--total` and `--v` to set |
| an algorithm, a list, a table in memory | Street (`street`) | 2-8 houses of 1-4 floors, labels of 6 letters |
| someone sends something to someone | Send (`send`) | 2-4 parties, the item moves one step per press |
| code | Code (`code`) | 9 lines of 42 letters |
| exact numbers, more than 6 items | Table (`table`) | 3-5 rows |
| a landscape photo / two / three | `photo`, `photos` (`.pics.three`) | `--x --y` pick the part, `--zoom` crops in |
| a portrait phone photo | `tall` | beside text, never full width |
| a screenshot, figure or chart image | `shot` | if its text is small, crop the file to the part that matters, or redraw the key numbers as `amounts` |
| the things to remember | Summary (`summary`) | 3 tiles on brown |
| the end | `end` | |

Full-width headlines: 32 letters per line, 2 lines. `.sect` (bottom left) says which section a
slide belongs to; leave it off the question, summary and end slides.

**Topic not about property?** Pick motifs that fit: house tower door key pin sun hill tree flower
sprig person paper search chart network screen phone check cross question box letter arrow list
clock bulb lock unlock book code cart campus. `{{scene ground box letter house}}` puts them on the title
hills, `{{scene pic lock}}` makes a picture block, `{{scene row person paper search}}` a row for
the bottom of a brown slide. Houses also work as a picture of memory: a house is a place, its
number the address, a floor one more item in the same place. A motif that is missing: add it to
`MOTIFS` in `make_shapes.py` and run `css`, or put `.motif.x { --m: url("data:image/svg+xml,...") }`
in the deck's DECK-CSS (a black shape on 100 x 100).

## Motion

Slides pan sideways like walking past. Parts slide into place. Nothing fades, because a fade
passes through colors outside the palette.

## Rules

- **Three flat colors for everything drawn or typed.** The exception is project pictures (`.photo`,
  `.shot`) and logos, which keep their own colors. One or two pictures on a slide, nothing on top of
  them except markers. No texture, speckle, grain, tints, transparency, gradients, glow or shadow.
- **Few and big.** About six blocks on a slide at most (a street may have eight houses), never a grid of small ones. A block gets
  a picture only if it reads from the back of the room; otherwise just a number. More items:
  group them or use a plain table. Only the progress tile and the windows of drawn houses are small.
- **Blocks are uneven, text is straight.** Titles, lists, tables and code keep a straight left edge.
- **One idea in turquoise per slide**, shown at most twice (the block and the words about it), plus
  the progress tile. Numbered spots and their list count as one.
- No cutaway, underground or soil-layer pictures. No tape, pins or thin sky lines.
- **Pictures from `assets/media/`** are shown as they are filed, and `style.css` turns them into
  clay and brown (an SVG filter; in a browser without it they keep their own colors). Put them on
  a brown block (`.cutout` has one). Solid flat objects work; halftone and engraved ones turn
  spotty, so avoid them here.
- Decks from Paper & Stage: its labels, arcs and halftone are hidden, pinned cards become blocks.
  Colors written by hand in a deck's `DECK-CSS` must be changed to tokens.
