# Shared media

One library for every design style and every course. **Rule: everything here is
style-free**: each object is kept once, in its original colors, with no style's palette,
fonts or logos applied. Each design style decides how to show them (Paper & Stage turns
every image grey in its `style.css`; Block Shapes shows them as they are). Decks take
shared elements from here and only here; style-only inspiration goes in
`docs/design/<style>/refs/`.

Folders are by kind, not by style:

| Folder | What goes there |
|--------|-----------------|
| `objects/` | cut-out objects with transparent background (any style; most are halftone with a paper edge). In a deck: `<div class="cutout">` or `<div class="cutout corner-object">` |
| `icons/` | line icons (SVG, 24x24, stroke 2): search, insert, delete, alert, levels, speed, check, cross, arrow-right |
| `shapes/` | the eight geometric primitives (SVG, 100x100, filled): circle, half, arch, triangle, stair, band, ellipse, eye |
| `textures/` | repeating tiles for backgrounds: `halftone-dots.svg` (16px), `square-grid.svg` (64px) |
| `inbox/` | new files waiting to be processed |

Icons and shapes use `currentColor`: pasted inline as `<svg>` they take the surrounding text
color, so one file works in every design (as an `<img>` they stay black). Textures are black
tiles meant for `background: url(...)` at low opacity.

Add a folder when a new kind appears (`photos/`, `clips/`) and list it here.

**New files: remove the background yourself, then drop them in `inbox/`** (any name) and ask
Claude to process the inbox; they get checked, trimmed, named and filed into the folders below.

Images, GIFs and short clips that any deck or document may reuse. Course-specific media
goes in `<Course>/presentation/assets/`; style inspiration goes in `docs/design/<style>/refs/`.

## Naming

`<topic>_<what>[_<variant>].<ext>`, lowercase, no spaces: `shopping_price-slider.gif`,
`metro_express-local.png`, `logo_iu_white.png`. Add a line to the list below with the
source (URL or "own photo") and the license, so we know it can be used.

## Formats

- Photos: JPG or WebP. Flat graphics, screenshots, logos: PNG or SVG.
- GIFs: keep under about 5 MB. For slides prefer a short MP4/WebM loop (`<video autoplay
  muted loop playsinline>`), which is 5-10x smaller.
- Files over 50 MB stay out of git (note where to get them here).

## Tools (installed)

- `ffmpeg`: cut a clip, GIF to MP4, pull frames (`ffmpeg -i in.gif .temp/frames/f_%03d.png`).
- `gifsicle`: crop, resize, trim or shrink a GIF (`gifsicle --crop 0,0+800x450 -O3 in.gif > out.gif`).
- `cwebp`: shrink a photo for slides (`cwebp -q 80 in.jpg -o out.webp`).

## Files

| File | Source | License | Notes |
|------|--------|---------|-------|
| `objects/*.png` (19 files) | Pinterest pins; sources and pin IDs below | unknown | transparent PNGs, backgrounds removed by hand, trimmed and split with `scripts/cutout.py`. Fine for class slides; check licences before publishing anything public |

## Objects

`objects/`: cut-out objects (arrows, hands, dice, coins, light bulb, price tag, train,
magnifying glass, pencil, push-pin, phone, exclamation mark, retro computer, sold-out stamp).
Seven more (alarm clock, balance scale, brain, camera, keys, ladder, laptop hands) moved to
`docs/design/paper-stage/refs/` on 30 Oct 2026: reference only, not for slides. Most are black-and-white
halftone with a white paper edge; `retro-computer.png` (yellow), `train.png` (photo) and
`sold-out-stamp.png` (red) keep their colors. File names say what each shows. Use in a deck:
`<div class="cutout"><img src="<relative path>/arrow-up-right.png" alt="arrow"></div>`.

Backgrounds are removed by hand before files reach the inbox. Processing a transparent PNG:
`python3 scripts/cutout.py <in.png> <out.png> --edge 0` trims it and keeps its own edges;
add `--split` for one file per object, `--edge 10` to add a white paper edge. (`--gray`
exists, but media keeps original colors; a style greys images in its CSS.) (For a flat image with a plain background the same script can also
remove the background; tune `--tol` and `--close`.)

### Where the objects came from

Downloaded from Pinterest on 29 Oct 2026, background removed by hand, then trimmed and
split with `scripts/cutout.py`. The hand-cut sources were deleted after
processing; the cut-outs keep their full resolution.

| Source (deleted) | What it shows | Pin / origin | Cut-out(s) |
|------------------|---------------|--------------|------------|
| `pencil_src.png` | halftone pencil, torn paper edge | pin 1067845761667422696 | `pencil.png` |
| `retro-computer_src.png` (no paper edge; yellow kept) | halftone desktop computer with yellow paper flashes | pin 1081145454315262360 | `retro-computer.png` (original colors, 10px paper edge added) |
| `dice_src.png` | halftone die showing five, paper edge | added 29 Oct (source not recorded) | `dice.png`; good for randomness / coin flips |
| `magnifying-glass_src.png` | halftone magnifying glass, paper edge | added 29 Oct (source not recorded) | `magnifying-glass.png`; good for search |
| `push-pin_src.png` | halftone push-pin on beige paper | pin 1141944049324791239 | `push-pin.png` |
| `brain_src.png` | halftone brain | pin 734649758007848254 | `brain.png` (now in paper-stage `refs/`) |
| `arrows-three_src.png` | three hand-drawn arrows on beige paper | pin 857232110368480380 | `arrow-right.png`, `arrow-down-right.png`, `arrow-up-right.png` |
| `camera-rangefinder_src.png` | halftone rangefinder camera | pin 883268545692559022 | `camera-rangefinder.png` (now in paper-stage `refs/`) |
| `phone-hands_src.png` | halftone hands holding a phone (blank screen) | pin 947163365478021277 | `phone-hands.png` |
| `arrow-curved_src.png` | hand-drawn curved arrow on beige paper | pin 948500371540596813 | `arrow-curved.png` |
| `exclamation-big_src.png` | double exclamation mark, halftone | Pinterest (no pin ID) | `exclamation-big.png` |
| `laptop-hands_src.png` | halftone hands typing on a laptop (checkerboard baked in) | Pinterest (no pin ID) | `laptop-hands.png` (now in paper-stage `refs/`) |
| `hands-two_src.png` | two halftone hands, open palm and pinch | Pinterest (no pin ID) | `hand-open-palm.png`, `hand-pinch.png` |

### Added 29 Oct 2026 (inbox, background removed by hand; source not recorded)

(`alarm-clock`, `balance-scale`, `keys` and `ladder` were added here too; they moved to
paper-stage `refs/` on 30 Oct.)

| Cut-out | What it shows | Notes |
|---------|---------------|-------|
| `coin-heads.png`, `coin-tails.png` | both sides of a 1945 US dime (smooth drawing, not halftone) | coin flips; real currency design, public domain |
| `light-bulb.png` | halftone light bulb with paper edge | an idea |
| `price-tag.png` | blank hand-drawn price tag | inside made solid white so it reads on black |
| `sold-out-stamp.png` | red "SOLD OUT" stamp | letters filled white so they read on black |
| `train.png` | metro train photo, in color | express trains analogy |

