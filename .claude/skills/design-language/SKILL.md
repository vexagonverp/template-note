---
name: design-language
description: Create or change a named visual design language (palette, role tokens, type, layout habits, rules) for HTML decks and other visuals, save it as a folder in docs/design/, check its contrast, and restyle decks with it. Use when the user describes a look, a vibe, a brand, a website or a screenshot they want slides to follow, or says "make a design", "design language", "restyle" or "make it look like".
argument-hint: <name> [description, brand colors, reference image or URL]
---

# Design language

**Input:** `$ARGUMENTS` is the name and a description of the look. If it is empty, or shows
up literally as a placeholder, take these from the user's message, or ask for a name and a
reference (a vibe in words, colors, a site, a screenshot, a poster).

Read `docs/design/README.md` (section 10 says what a design language must contain), one
existing style folder such as `docs/design/block-shapes/` as a model, and
`templates/html_deck/DESIGN.md` (tokens and shared parts).

## Steps

1. **Read the reference.** If it is an image, look at it; if it is a site, describe its
   palette, faces and layout. Write the concept and mood in one or two sentences.
2. **Map the palette to roles.** Raw colors first (`--violet: #5E3F8F`), then every role
   token the engine uses: `--chrome --paper --card --ink --muted --line --accent --on-accent
   --tint --go --on-go --stop --on-stop --pop --display --body --mono --radius --radius-sm
   --stage-radius --title-weight --title-tracking`. `--accent` must be readable as text on
   `--card`; `--tint` is a fill that carries `--ink` text.
3. **Make the folder `docs/design/<name>/`** with `README.md` (the brief word for word if
   the user gave one, then concept, palette and roles, allowed pairings, type, layout, rules,
   contrast table, how to use) and `style.css`. **`style.css`:** a header comment (first line
   `Design language: <Name>`, then concept, allowed tile/shape pairings, and the contrast
   numbers), the Google Fonts `@import`, the `:root` tokens, then a `/* @@PARTS */` line
   followed by part overrides (headline case and size, body weight, cards, tables, code).
   Overrides use tokens only, never raw colors. A style must work with the shared,
   style-free elements in `assets/media/` (objects in original colors, icons, shapes,
   textures): adapt them in CSS (e.g. `filter: grayscale(1)`), never by adding restyled
   copies there.
4. **Check contrast:** `python3 scripts/contrast.py <name>`. Fix any FAIL; any "large text
   only" pair must not be used for body text (change the token or the part).
5. **Preview:** `python3 scripts/html_deck.py new docs/design/<name>/preview.html "Design preview" <name>`,
   then one headless Chrome screenshot of slides 1 and 3 (title and text-beside-tiles):
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1640,940 --virtual-time-budget=4000 --screenshot=<png> "file://<preview>#slide-1"`.
   Fix what looks wrong, once.
6. **Register it:** add a row to the table in `docs/design/README.md` section 10. If the user wants it as the default, change
   `DEFAULT_DESIGN` in `scripts/html_deck.py` (the only place it is set).
7. **Apply** when asked: `python3 scripts/html_deck.py design <deck.html> <name>`. If the
   deck has its own parts (DECK-CSS), check they use tokens only and still read well;
   re-screenshot one animated slide, then open the local deck (`open <deck.html>`).

Report: the concept in one line, the contrast table result, what changed in decks, and the
preview path. Do not commit unless asked.
