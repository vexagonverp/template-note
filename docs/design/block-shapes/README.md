# Block Shapes

Bauhaus-inspired geometric modernism. Every slide is built on a strict grid of flat color
tiles, each holding one bold primitive shape, oversized and often cropped by the tile edge.
Confident, playful and graphic, like a modernist gallery poster.

| File | What it is |
|------|------------|
| `style.css` | tokens + part overrides; decks load it through `scripts/html_deck.py` |
| `preview.html` | sample slides: tiled title slide, text-beside-tiles content slide, and the shared parts |
| `refs/` | inspiration images and GIFs, indexed in `refs/README.md` |

Use it: `DECK_DESIGN=block-shapes scripts/new_note.sh <Course> deck "Course"`,
or `python3 scripts/html_deck.py design <deck.html> block-shapes`.
Example deck: `preview.html` in this folder.

## Palette and roles

Flat fills only: no tints, gradients, outlines, textures or shadows.

| Color | Hex | Role token | Used for |
|-------|-----|------------|----------|
| Paper white | `#FFFFFF` | `--card`, `--paper` | text areas, slide surface |
| Black | `#121212` | `--ink`, `--line`, `--chrome` | headlines, shapes, tiles, thin rules, around the stage |
| Marigold | `#F2B01E` | `--tint` | highlight fill behind black text (counter, winning row, current code line) |
| Violet | `#5E3F8F` | `--accent` | the current step, the search path, eyebrows, key words |
| Pink | `#EA7BAE` | `--pop` | extra tile color |
| Red-orange | `#E8492C` | `--stop` | checked and rejected ("too far") |
| Sage green | `#5E8A68` | `--go` | found, in range |
| Grey | `#4A4A4A` | `--muted` | small credits and secondary text |

**Shape on tile** (only pairs that clearly contrast): black on marigold, marigold on black,
marigold on violet, white on violet, black on pink, white or black on sage, black on
red-orange. Never two neighboring tiles in the same color.

## Contrast (checked with `python3 scripts/contrast.py block-shapes`)

| Text on background | Ratio |
|--------------------|-------|
| black on white | 18.7 |
| grey `#4A4A4A` on white | 8.9 |
| violet on white, white on violet | 8.1 |
| black on marigold | 9.8 |
| black on pink | 7.1 |
| black on red-orange | 4.8 (white is only 3.9, so text on red-orange is black) |
| black on sage | 4.7 (white is only 4.0, so text on sage is black) |
| violet on marigold | **4.3, not allowed for text** |

## Type

- **Headlines:** Anton (fallback Bebas Neue, then Impact), uppercase, huge (92px slide
  titles, 230px on the title slide), leading 0.9, flush left, two or three stacked lines.
- **Body:** Jost Light 300 (fallback Josefin Sans), around 27px, line height 1.6, in a
  narrow column under a thin black rule.
- **Credits and slide numbers:** Jost, small, grey.
- **Code and numbers in diagrams:** JetBrains Mono.
- The signature is the contrast between the giant black headline and the delicate body.

## Layout

- **Title slide** (`.title-slide.tiled-bottom`): headline top-left, a thin text column
  top-right (`.title-col`), a band of six square tiles across the bottom (`.tile-band`),
  edge to edge, no gaps.
- **Content slide** (`.tiled-right`): text on white on the left, a column of three square
  tiles down the right edge (`.tile-col`).
- **Diagram slides:** full width on white, square flat boxes, black arrows, violet for the
  moving part, a marigold counter chip, a thin rule above the caption.
- **Shapes carry meaning:** circle = node, stair = levels, diagonal band = jump or path,
  triangle = pointer, eye = "look here", arch and half-circle = decoration.

## Rules

- Flat color only. No outlines on tiles or cards, no gradients, textures, shadows or
  rounded cards (diagram boxes keep a thin black border so they read as boxes).
- One shape per tile, centered or cropped on purpose by the tile edge (`.crop-*`, `.huge`).
- Text stays off colored tiles, except one big number or word (`.big`).
- Every text color passes 4.5:1 on its background.
- Shared objects from `assets/media/objects/` are shown in their original colors and cast
  no shadow (`--shadow: transparent`), to stay flat.

## The brief this style was built from (as given)

> Create a slide design language called "Block Shapes".
>
> Concept: Bauhaus-inspired geometric modernism. Every slide is built on a strict grid of
> flat color tiles, each holding one bold primitive shape: circle, half-circle, arch,
> triangle, stepped stair, diagonal band, ellipse, eye. Shapes are flat, oversized and often
> cropped by their tile's edge. The mood is confident, playful and graphic, like a modernist
> gallery poster.
>
> Palette (flat fills only, no tints, gradients or shadows): Paper white #FFFFFF for text
> areas; Black #121212 for headlines, shapes and tiles; Marigold #F2B01E; Violet #5E3F8F;
> Pink #EA7BAE; Red-orange #E8492C; Sage green #5E8A68. Put a shape on a tile only in a
> color that clearly contrasts with it (black on marigold, violet on black, marigold on
> violet, white on violet). Never place two neighboring tiles in the same color.
>
> Typography: Headlines: a heavy, very condensed grotesque (Anton, or Bebas Neue as a
> fallback), all set huge, tight leading (0.9), flush left, two or three stacked lines.
> Body: a light geometric sans (Josefin Sans Light or Jost 300), small, with wide line
> spacing, set in a narrow column under a thin rule. Small credits and slide numbers: same
> light sans, tiny, right-aligned. The contrast between the giant black headline and the
> delicate body text is the signature of the style.
>
> Layout: Split slides into a white text band and a grid of square tiles (3×3, 3×2 or 2×2),
> edge to edge with no gaps or borders. Title slides: headline top-left, thin text column
> top-right, tile grid below. Content slides: text on white on one side, a column or block
> of 2–3 tiles on the other. Use the shapes to carry meaning in diagrams: circles as nodes,
> a diagonal band as a path or jump, a stepped stair as levels, a triangle as a pointer.
>
> Rules: Flat color only. No outlines, gradients, textures, shadows or rounded cards. One
> shape per tile, centered or cropped deliberately by the tile edge. Keep text off the
> colored tiles except for one big number or word. Every text color must pass 4.5:1
> contrast on its background. Output CSS custom properties for every token, a tile grid
> class, a class for each shape, and two sample slides: a title slide and a content slide.

**Where it differs from the brief, and why:**
- Violet shapes on black tiles are not used: violet on black is only 2.3:1 and disappears
  on a projector.
- Violet text on marigold is not allowed: it is only 4.3:1.
- Text on sage and red-orange tiles is black, not white, to pass 4.5:1.
- The title uses a 6 x 1 band of square tiles instead of a 3 x 2 grid, so the headline keeps
  room on a 16:9 slide.
