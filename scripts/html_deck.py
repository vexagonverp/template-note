#!/usr/bin/env python3
"""HTML stop-motion decks (templates/html_deck/).

  html_deck.py new <out.html> "Course Name" [design]   new deck from the template
  html_deck.py design <deck.html> <design>              swap the design language
  html_deck.py upgrade <deck.html>                      take the latest engine from the template,
                                                        keep the deck's design, slides and code
  html_deck.py artifact <deck.html> [out.html]          the part to publish as a claude.ai artifact
                                                        (lists local images to publish as files)
  html_deck.py designs                                  list design languages
  html_deck.py bundle <deck.html> [out.html]            one self-contained file to send: every local
                                                        image embedded, opens offline with a double-click
  html_deck.py pdf <deck.html> [out.pdf] [--last]       PDF for phones (iOS previews do not run the
                                                        deck's JavaScript): one page per press, so
                                                        swiping plays the animation; --last = one
                                                        page per slide
  html_deck.py shots <deck.html> [out_dir] [slide:step ...]
                                                        headless-Chrome PNG of every slide at its
                                                        last step, plus any slide:step you name
                                                        (step 0 = first), and contact sheets

A deck has five regions between markers: DESIGN and DESIGN-PARTS (filled from
docs/design/<name>/style.css, split at its /* @@PARTS */ line), DECK-CSS,
SLIDES and DECK-JS (yours).
Everything else is the shared engine and comes from the template.
"""
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "templates/html_deck/deck_template.html"
DESIGNS = ROOT / "docs/design"   # one folder per design style: README.md, style.css, preview.html
REGIONS = ["DESIGN", "DESIGN-PARTS", "DECK-CSS", "SLIDES", "DECK-JS"]
DEFAULT_DESIGN = "paper-stage"


def pat(name):
    return re.compile(r"((?:/\*|<!--) @@%s-START (?:\*/|-->))(.*?)((?:/\*|<!--) @@%s-END (?:\*/|-->))"
                      % (re.escape(name), re.escape(name)), re.S)


def get(text, name, default=None):
    m = pat(name).search(text)
    if not m:
        if default is not None:
            return default
        sys.exit(f"marker @@{name} not found")
    return m.group(2)


def put(text, name, body):
    if not pat(name).search(text):
        sys.exit(f"marker @@{name} not found")
    return pat(name).sub(lambda m: m.group(1) + body + m.group(3), text, count=1)


def design_css(name):
    """(tokens, parts): the design file is split at its /* @@PARTS */ line."""
    f = DESIGNS / name / "style.css"
    if not f.exists():
        sys.exit(f"no design '{name}'. Have: {', '.join(names())}")
    tokens, _, parts = f.read_text().partition("/* @@PARTS */")
    return "\n" + tokens.strip() + "\n", "\n" + parts.strip() + "\n" if parts.strip() else "\n"


def names():
    return [p.parent.name for p in sorted(DESIGNS.glob("*/style.css"))]


def apply_design(text, name):
    tokens, parts = design_css(name)
    return put(put(text, "DESIGN", tokens), "DESIGN-PARTS", parts)


def upgraded(old):
    """The template's engine with this deck's regions and title."""
    title = re.search(r"<title>(.*?)</title>", old, re.S).group(1)
    new = TPL.read_text()
    for r in REGIONS:
        new = put(new, r, get(old, r, default="\n" if r == "DESIGN-PARTS" else None))
    return set_title(new, title)


def set_title(text, title):
    return re.sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", text, count=1)


CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "google-chrome", "chromium", "chromium-browser", "chrome"]
# appended to a copy of the deck: ?s=<slide>&k=<step|last> jumps there and hides the key hint
JUMP = """<script>(()=>{const q=new URLSearchParams(location.search);if(q.has('s')){
document.getElementById('hint').style.display='none';
setTimeout(()=>Deck.go(+q.get('s')-1,q.get('k')==='last'?'last':+q.get('k')),50);}})();</script>"""


def shots(deck, out, extra):
    """Screenshot slides with headless Chrome. The copy gets a <base> pointing at the deck's
    folder, so relative images (../../assets/media/...) still load from out/."""
    chrome = next((c for c in CHROME if os.path.exists(c) or shutil.which(c)), None)
    if not chrome:
        sys.exit("no Chrome/Chromium found")
    text = deck.read_text()
    n = len(re.findall(r'<section class="slide[\s"]', text))
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    copy = out / "_shot.html"
    base = f'<base href="{deck.parent.resolve().as_uri()}/">'
    copy.write_text(text.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + base, 1) + JUMP)
    jobs = [(f"s{i:02d}_last", i, "last") for i in range(1, n + 1)]
    for x in extra:
        sl, st = x.split(":")
        jobs.append((f"s{int(sl):02d}_k{st}", int(sl), st))

    def one(job):
        name, sl, st = job
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1600,940", "--virtual-time-budget=4000",
                        f"--screenshot={out / (name + '.png')}", f"{copy.as_uri()}?s={sl}&k={st}"],
                       capture_output=True, timeout=60)
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(one, jobs))
    copy.unlink()
    pngs = sorted(str(p) for p in out.glob("s*.png"))
    subprocess.run([sys.executable, str(ROOT / "scripts/contact_sheet.py"), "--cols", "3", "--per", "12",
                    "--out", str(out / "grids"), *pngs], capture_output=True)
    print(f"{n} slides, {len(jobs)} shots in {out}/ ; contact sheets in {out}/grids/")
    print("check: nothing clipped or overlapping (corner objects vs long titles), text at least 16px")


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".svg": "image/svg+xml"}


def bundle(deck, out):
    """Embed every local image (src, data-*, CSS url()) as a data: URI, so the deck is one file."""
    import base64
    text = deck.read_text()
    done, missing = {}, set()

    def embed(m):
        ref = m.group(2)
        f = (deck.parent / ref).resolve()
        if not f.is_file():
            if not (ref.startswith("...") or "<" in ref):   # example paths in comments
                missing.add(ref)
            return m.group(0)
        if ref not in done:
            done[ref] = f"data:{MIME[f.suffix.lower()]};base64," + base64.b64encode(f.read_bytes()).decode()
        return m.group(1) + done[ref] + m.group(3)
    pat = r'((?:src|href|data-[\w-]+)=["\']|url\(["\']?)([^"\'()\s:]+\.(?:png|jpe?g|gif|webp|svg))(["\')])'
    text = re.sub(pat, embed, text, flags=re.I)
    out.write_text(text)
    mb = out.stat().st_size / 1e6
    print(f"{out}  ({mb:.1f} MB, {len(done)} images embedded)")
    for m in sorted(missing):
        print(f"  not found, left as is: {m}")
    print("fonts still load from Google Fonts when online; offline the deck falls back to system fonts")


# PDF copy: no panel button or key hint, and the step count of every slide written into the page
PDF_JS = """<style>#panel-btn,#hint{display:none!important}</style><script>(()=>{
const q=new URLSearchParams(location.search);
if(q.has('count')){setTimeout(()=>{const n=document.querySelectorAll('#stage > .slide').length,c=[];
for(let i=0;i<n;i++){Deck.go(i,0);c.push(Math.max(1,document.querySelectorAll('#dots i').length));}
document.body.setAttribute('data-steps',c.join(','));},50);}
else if(q.has('s')){setTimeout(()=>Deck.go(+q.get('s')-1,+q.get('k')),50);}})();</script>"""


def pdf(deck, out, last_only):
    """One page per press (or per slide), screenshotted at 1920x1080 and stitched with Pillow."""
    from PIL import Image
    chrome = next((c for c in CHROME if os.path.exists(c) or shutil.which(c)), None)
    if not chrome:
        sys.exit("no Chrome/Chromium found")
    work = (ROOT / ".temp" / "pdf" / deck.stem).resolve()
    work.mkdir(parents=True, exist_ok=True)
    copy = work / "_pdf.html"
    base = f'<base href="{deck.parent.resolve().as_uri()}/">'
    copy.write_text(deck.read_text().replace('<meta charset="utf-8">', '<meta charset="utf-8">' + base, 1) + PDF_JS)
    dom = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--virtual-time-budget=4000",
                          "--dump-dom", f"{copy.as_uri()}?count=1"], capture_output=True, text=True, timeout=120).stdout
    m = re.search(r'data-steps="([\d,]+)"', dom)
    if not m:
        sys.exit("could not read the step counts from the deck")
    counts = [int(x) for x in m.group(1).split(",")]
    jobs = [(i, (n - 1) if last_only else k) for i, n in enumerate(counts, 1) for k in ([0] if last_only else range(n))]

    def one(job):
        sl, st = job
        png = work / f"p{sl:02d}_{st:02d}.png"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1920,1080",
                        "--virtual-time-budget=4000", f"--screenshot={png}", f"{copy.as_uri()}?s={sl}&k={st}"],
                       capture_output=True, timeout=60)
        return png
    with ThreadPoolExecutor(6) as ex:
        pngs = list(ex.map(one, jobs))
    copy.unlink()
    pages = [Image.open(p).convert("RGB") for p in pngs]
    pages[0].save(out, save_all=True, append_images=pages[1:], resolution=144, quality=85)
    print(f"{out}  ({out.stat().st_size / 1e6:.1f} MB, {len(pages)} pages from {len(counts)} slides)")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip()); return
    cmd = argv[1]
    if cmd == "designs":
        for n in names():
            first = (DESIGNS / n / "style.css").read_text().splitlines()[0]
            print(f"{n:16} {first.strip('/* ')}   docs/design/{n}/")
    elif cmd == "new":
        out, course = Path(argv[2]), argv[3]
        design = argv[4] if len(argv) > 4 else DEFAULT_DESIGN
        if out.exists():
            sys.exit(f"refusing to overwrite {out}")
        t = apply_design(TPL.read_text(), design)
        t = t.replace("Course Name · Presentation", f"{course} · Presentation")
        out.write_text(t)
        print(f"created {out} (design: {design})")
    elif cmd == "design":
        deck, design = Path(argv[2]), argv[3]
        text = deck.read_text()
        if not pat("DESIGN-PARTS").search(text):
            text = upgraded(text)
            print(f"{deck}: engine updated from template first (older deck)")
        deck.write_text(apply_design(text, design))
        print(f"{deck}: design set to {design}")
    elif cmd == "upgrade":
        deck = Path(argv[2])
        deck.write_text(upgraded(deck.read_text()))
        print(f"{deck}: engine updated from template")
    elif cmd == "artifact":
        deck = Path(argv[2])
        m = re.search(r"<!-- @@ARTIFACT-START -->\n(.*)<!-- @@ARTIFACT-END -->", deck.read_text(), re.S)
        out = Path(argv[3]) if len(argv) > 3 else ROOT / ".temp" / (deck.stem + ".artifact.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        page, files = m.group(1), {}

        def local(mt):
            src = mt.group(2)
            if re.match(r"(https?:|data:|//)", src):
                return mt.group(0)
            f = (deck.parent / src).resolve()
            files[f"media/{f.name}"] = str(f)
            return f'{mt.group(1)}media/{f.name}"'
        # local images move to media/ next to the page; publish them with the page as `files`
        page = re.sub(r'((?:src|data-[\w-]+)=")([^"]+\.(?:png|jpe?g|gif|webp|svg))"', local, page)
        out.write_text(page)
        print(out)
        for k, v in files.items():
            print(f"  file {k} <- {v}")
    elif cmd == "bundle":
        deck = Path(argv[2])
        out = Path(argv[3]) if len(argv) > 3 else ROOT / ".temp" / "share" / f"{deck.stem}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        bundle(deck, out)
    elif cmd == "pdf":
        deck = Path(argv[2])
        rest = [a for a in argv[3:] if a != "--last"]
        out = Path(rest[0]) if rest else ROOT / ".temp" / "share" / f"{deck.stem}.pdf"
        out.parent.mkdir(parents=True, exist_ok=True)
        pdf(deck, out, "--last" in argv)
    elif cmd == "shots":
        deck = Path(argv[2])
        rest = argv[3:]
        out = Path(rest.pop(0)) if rest and ":" not in rest[0] else ROOT / ".temp" / "shots" / deck.stem
        shots(deck, out, rest)
    else:
        sys.exit(__doc__.strip())


if __name__ == "__main__":
    main(sys.argv)
