# HTML decks

An HTML deck is one `.html` file that runs in any browser, works offline (apart from web
fonts), and animates algorithms step by step ("stop motion"). Use it instead of Canva or
Beamer when a talk needs moving diagrams.

```bash
scripts/new_note.sh <Course> deck "Course Name" [Descriptor]            # default design: paper-stage
DECK_DESIGN=<name> scripts/new_note.sh <Course> deck "Course Name"     # pick a design
python3 scripts/html_deck.py designs                                   # list designs
python3 scripts/html_deck.py design <deck.html> <name>                 # restyle a deck
python3 scripts/html_deck.py upgrade <deck.html>                       # latest engine, keep slides
python3 scripts/html_deck.py artifact <deck.html>                      # copy to publish on claude.ai
```

Presenting: Right / Space = next step, Left = back, **S = slide panel** (thumbnails on the
left, click to jump), F = full screen, Home / End.

Styles (colors, fonts, extra parts) live in `docs/design/<name>/`; visual and deck rules
(one idea per slide, running example, step-by-step diagrams, contrast) are in
`docs/design/README.md`. New style: `/design-language`.

## The regions

| Region | What goes there |
|--------|-----------------|
| `DESIGN`, `DESIGN-PARTS` | the design language: tokens, then part overrides. Filled from `docs/design/<name>/style.css` (split at its `/* @@PARTS */` line); do not edit by hand in a deck. |
| `DECK-CSS` | parts only this deck needs (a diagram, a phone mock-up). Colors and fonts come from tokens only. |
| `SLIDES` | one `<section class="slide" data-id="..." data-title="...">` per slide. |
| `DECK-JS` | `Deck.register(id, { steps, init, render })` for animated slides. |

Everything else is the shared engine. Fix the engine in `deck_template.html`, then run
`html_deck.py upgrade` on each deck.

**Steps without code:** `data-step="k"` shows an element from press k on; `data-at="k"`
highlights it only on press k (code lines, rules). **Steps with code:** register the slide,
keep every state in a list, and make `render(step)` draw state `step` from scratch, so going
back works. Check every number in the states with a script (`<Course>/presentation/checks/`).

**Shared parts:** `.eyebrow`, `h2`, `.lede`, `.points` (bullets), `.cards.two|three` with
`.card` / `.card.dark` / `.n` / `.tag`, `.grid-table` (+ `.row.win`, `.mono`), `pre.code`
with `data-at` lines, `.rule`, `.split` (two columns), `.capbar` with `.cap` and `.counter`
(caption and counter under a diagram), `.big-q`, `.title-slide` with `.title-top`,
`.title-col` and a `.tile-band`, and `.cutout` (a cut-out object from `assets/media/objects/`
that drops in with a contact shadow; add `.corner-object` to pin a small one top-right).
Shared objects, icons, shapes and textures: `assets/media/` only. They are style-free (kept
in original colors); a style changes how they look in its own CSS (for example a grayscale
filter), never by adding its own copies there.

**Tiles and shapes** (every design): `.tile` with a color `.t-ink|card|accent|tint|go|stop|pop`
holding one `.shape` (`.circle .half .arch .triangle .stair .band .ellipse .eye`) colored
`.s-*`, cropped with `.crop-l|r|t|b` or enlarged with `.huge`, plus at most one `.big` number
or word. Layouts: `.tile-band` (6 across the bottom of a `.tiled-bottom` title slide) and
`.tile-col` (3 down the right edge of a `.tiled-right` slide). Shapes carry meaning: circle
= node, stair = levels, band = jump or path, triangle = pointer. Never two neighboring tiles
in one color.

## Tokens a style must set

Every color and font in the engine and shared parts comes from these, so swapping
`style.css` restyles the whole deck. A style may add its own tokens and parts after its
`/* @@PARTS */` line.

| Token | Role |
|-------|------|
| `--chrome` | around the stage (defaults to `--paper`) |
| `--paper` | quiet fills: table headers, chips |
| `--card` | slide surface |
| `--ink` | main text, dark cards, code background |
| `--muted` | secondary text |
| `--line` | rules, resting borders and arrows |
| `--accent`, `--on-accent` | the one thing to look at, and text on it |
| `--tint` | highlight fill behind `--ink` text |
| `--go`, `--on-go` / `--stop`, `--on-stop` | found or correct / rejected or too far, and text on them |
| `--pop` | an extra tile or prop color |
| `--shadow` | cut-out and card shadow color (`transparent` = flat) |
| `--display` / `--body` / `--mono` | title face / text face / numbers and code |
| `--radius`, `--radius-sm`, `--stage-radius`, `--title-weight`, `--title-tracking` | shape and title feel |
| `--stage-w`, `--stage-h` | slide size, default 1600px x 900px (a deck can override) |
