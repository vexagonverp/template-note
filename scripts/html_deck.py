#!/usr/bin/env python3
"""HTML stop-motion decks (templates/html_deck/).

  html_deck.py new <out.html> "Course Name" [design]   new deck; starts with the design's own slides
                                                        (docs/design/<name>/starter.html) if it has them
  html_deck.py fill <deck.html>                         draw {{scene ...}} placeholders (designs with
                                                        a make_shapes.py); shots, pdf, bundle do it too
  html_deck.py put <deck.html> <slides.html> [deck.js]  replace the deck's slides (and its code) from files
  html_deck.py check <deck.html>                        measure every slide: overflow, overlaps, tiny
                                                        text, missing pictures, unfilled placeholders
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
                                                        (step 0 = first), and contact sheets;
                                                        then runs check

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


def design_of(text):
    m = re.search(r"Design language: (.+)", text)
    for n in names():
        if m and (DESIGNS / n / "style.css").read_text().splitlines()[0].strip("/* ").endswith(m.group(1).strip()):
            return n
    return None


def filled(text):
    """Draw every {{scene name ...}} placeholder with the design's make_shapes.py."""
    if "{{scene" not in text:
        return text
    tool = DESIGNS / (design_of(text) or "") / "make_shapes.py"
    if not tool.is_file():
        sys.exit("{{scene ...}} needs a design with a make_shapes.py")

    def draw(m):
        r = subprocess.run([sys.executable, str(tool), "scene", *m.group(1).split()], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"scene {m.group(1)}: {(r.stderr or r.stdout).strip()}")
        return r.stdout.strip()
    return re.sub(r"\{\{scene ([\w -]+)\}\}", draw, text)


def read_deck(deck):
    """Deck text with scenes drawn; the file is updated if it still had placeholders."""
    old = deck.read_text()
    text = filled(old)
    if text != old:
        deck.write_text(text)
    return text


def temp_name(deck):
    """Course folder + deck name, so decks with the same file name do not overwrite each other."""
    d = deck.resolve().parent
    return f"{(d.parent if d.name == 'presentation' else d).name}_{deck.stem}"


def set_title(text, title):
    return re.sub(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", text, count=1)


CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          "google-chrome", "chromium", "chromium-browser", "chrome"]
# appended to a copy of the deck: ?s=<slide>&k=<step|last> jumps there and hides the key hint
STILL = "<style>*,*::before,*::after{transition:none!important;animation:none!important}</style>"   # never catch a slide mid-move
JUMP = STILL + """<script>(()=>{const q=new URLSearchParams(location.search);if(q.has('s')){
document.getElementById('hint').style.display='none';
setTimeout(()=>Deck.go(+q.get('s')-1,q.get('k')==='last'?'last':+q.get('k')),50);}})();</script>"""


def shots(deck, out, extra):
    """Screenshot slides with headless Chrome. The copy gets a <base> pointing at the deck's
    folder, so relative images (../../assets/media/...) still load from out/."""
    chrome = next((c for c in CHROME if os.path.exists(c) or shutil.which(c)), None)
    if not chrome:
        sys.exit("no Chrome/Chromium found")
    text = read_deck(deck)
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
    pngs = sorted(str(out / f"{j[0]}.png") for j in jobs)
    subprocess.run([sys.executable, str(ROOT / "scripts/contact_sheet.py"), "--cols", "3", "--per", "12",
                    "--out", str(out / "grids"), *pngs], capture_output=True)
    print(f"{n} slides, {len(jobs)} shots in {out}/ ; contact sheets in {out}/grids/")
    check(deck)
    print("now look at every sheet, and at full size at any slide with small text or a picture")


# measures every slide at every step; one line per problem goes to <pre id="lint">
LINT = STILL + r"""<script>setTimeout(()=>{const out=[],st=document.getElementById('stage');
const secs=[...document.querySelectorAll('#stage > .slide')];
const vis=e=>{const c=getComputedStyle(e);return c.visibility!=='hidden'&&c.display!=='none'&&+c.opacity>0};
if(document.title==='Deck Title')out.push('deck: <title> is still "Deck Title" (shown in the footer)');
if(/\{\{[^}]*\}\}/.test(st.innerHTML))out.push('deck: unfilled {{placeholder}}');
secs.forEach((s,i)=>{const got={};Deck.go(i,'last');const last=document.querySelectorAll('#dots i').length||1;for(let st0=0;st0<last;st0++){Deck.go(i,st0);const fin=st0===last-1,sr=s.getBoundingClientRect(),k=sr.width/s.offsetWidth||1,say=m=>{const kind=m.split(':')[0];(got[kind]=got[kind]||new Set()).add(m)};
const box=e=>{const r=e.getBoundingClientRect();return{l:(r.left-sr.left)/k,t:(r.top-sr.top)/k,r:(r.right-sr.left)/k,b:(r.bottom-sr.top)/k,w:r.width/k,h:r.height/k}};
const W=s.offsetWidth,H=s.offsetHeight,sect=s.querySelector('.sect'),sb=sect&&box(sect);let bottom=0;const seen=new Set();
const tw=document.createTreeWalker(s,NodeFilter.SHOW_TEXT);let n;
while(n=tw.nextNode()){const e=n.parentElement;if(!n.data.trim()||!vis(e)||e.closest('.hud,script,style'))continue;
const g=document.createRange();g.selectNodeContents(n);const r0=g.getBoundingClientRect();if(!r0.width)continue;
const r={l:(r0.left-sr.left)/k,t:(r0.top-sr.top)/k,r:(r0.right-sr.left)/k,b:(r0.bottom-sr.top)/k},c=getComputedStyle(e),t=n.data.trim().slice(0,30);
let fs=parseFloat(c.fontSize);const own=e.ownerSVGElement;if(own){const m=e.getScreenCTM();if(m)fs*=m.a/k}
if(fs<15&&!seen.has(fs)){seen.add(fs);say(`text ${fs.toFixed(0)}px is too small: "${t}"`)}
if(r.r>W-30||r.l<6||r.b>H-12||r.t<0)say(`text runs off or touches the edge: "${t}"`);
const clip=e.closest('.block,.card,.cutout,.pin-card');if(clip&&!own&&getComputedStyle(clip).clipPath!=='none'){const q=box(clip);if(r.r>q.r-6||r.l<q.l+4||r.b>q.b-2)say(`text does not fit its block: "${t}"`)}
if(sect&&!e.closest('.sect')&&!(r.r<sb.l||r.l>sb.r||r.b<sb.t+4||r.t>sb.b))say(`text sits on the progress tile: "${t}"`);
if(!e.closest('.sect'))bottom=Math.max(bottom,r.b)}
s.querySelectorAll('img').forEach(m=>{if(m.complete&&!m.naturalWidth)say('picture not found: '+m.getAttribute('src').slice(-60));
else{const b=box(m);if(!m.closest('.photo')&&(b.b>H||b.r>W+1))say('picture runs off the slide: '+m.getAttribute('src').slice(-40));
if(b.w>1.6*m.naturalWidth)say('picture is stretched and will look blurry: '+m.getAttribute('src').slice(-40));if(m.closest('.shot')){const d=box(m.closest('.shot').firstElementChild);if(b.w*b.h<.3*d.w*d.h)say('picture fills under half of its block: '+m.getAttribute('src').slice(-40))}}});
s.querySelectorAll('.motif').forEach(m=>{if(!getComputedStyle(m).getPropertyValue('--m').trim())say('unknown motif: '+m.className)});
s.querySelectorAll('.block,.photo,.shot,.plots,.pics,.grid-table,.cards,pre.code,.cutout,svg').forEach(e=>{if(!e.closest('.sect'))bottom=Math.max(bottom,box(e).b)});
s.querySelectorAll('.block:not(.frame),.grid-table,.cards,.plots,.pics,.shot,.photo,pre.code').forEach(e=>{const b=box(e);
if(b.b>H+1||b.r>W+1)say(`"${e.className}" runs off the slide`);else if(sect&&!e.closest('.sect')&&b.b>sb.t+8&&b.l<sb.r&&b.r>sb.l)say(`"${e.className}" runs into the progress tile`)});
const h1=s.classList.contains('poster')&&s.querySelector('h1'),f=s.querySelector('.frame');if(h1&&f){const g=document.createRange();g.selectNodeContents(h1);const r=g.getBoundingClientRect(),q=box(f);
if((r.right-sr.left)/k>q.r-40)say('poster title is too wide: shorten it or use <h1 class="long">');if((r.bottom-sr.top)/k>q.t+430)say('poster title goes behind the picture: use 2 lines, or <h1 class="long"> for 3')}
if(fin&&bottom<H*.66)say(`lower ${Math.round(100-100*bottom/H)}% of the slide is empty`);
const hi=[...s.querySelectorAll('.block.hi,.mark,.lot.hit,.card.dark,.row.win,.big-q em,h2 em')].filter(e=>!e.closest('.sect')&&vis(e));if(document.querySelector('.poster,.lot,.bk')&&hi.length>2)say(`${hi.length} turquoise things at once (aim for one idea, shown at most twice)`);
}for(const g of Object.values(got)){const a=[...g];out.push(`slide ${i+1} (${s.dataset.id}): ${a[0]}${a.length>1?`  (+${a.length-1} more like this)`:''}`)}});const p=document.createElement('pre');p.id='lint';p.textContent='LINT['+[...new Set(out)].join('\n')+']TNIL';document.body.appendChild(p)},900)</script>"""


def check(deck):
    chrome = next((c for c in CHROME if os.path.exists(c) or shutil.which(c)), None)
    if not chrome:
        sys.exit("no Chrome/Chromium found")
    text = read_deck(deck)
    copy = ROOT / ".temp" / f"_check_{temp_name(deck)}.html"
    copy.parent.mkdir(exist_ok=True)
    base = f'<base href="{deck.parent.resolve().as_uri()}/">'
    copy.write_text(text.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + base, 1) + LINT)
    dom = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--window-size=1600,940", "--virtual-time-budget=6000",
                          "--dump-dom", copy.as_uri()], capture_output=True, text=True, timeout=120).stdout
    copy.unlink()
    m = re.search(r'<pre id="lint">LINT\[(.*?)\]TNIL', dom, re.S)
    if not m:
        print("check: could not run (is the deck's JavaScript broken?)")
        return
    lines = [x for x in m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").splitlines() if x]
    print(f"check: {len(lines)} thing(s) to look at" if lines else "check: nothing found (it measures boxes; it does not judge looks)")
    for x in lines:
        print("  " + x)


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".svg": "image/svg+xml"}


def bundle(deck, out):
    """Embed every local image (src, data-*, CSS url()) as a data: URI, so the deck is one file."""
    import base64
    text = read_deck(deck)
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
PDF_JS = STILL + """<style>#panel-btn,#hint{display:none!important}</style><script>(()=>{
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
    work = (ROOT / ".temp" / "pdf" / temp_name(deck)).resolve()
    work.mkdir(parents=True, exist_ok=True)
    copy = work / "_pdf.html"
    base = f'<base href="{deck.parent.resolve().as_uri()}/">'
    copy.write_text(read_deck(deck).replace('<meta charset="utf-8">', '<meta charset="utf-8">' + base, 1) + PDF_JS)
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
        start = DESIGNS / design / "starter.html"
        if start.is_file():   # the design's own sample slides instead of the generic ones
            st = start.read_text()
            t = put(t, "DECK-CSS", "\n")
            for r in ("SLIDES", "DECK-JS"):
                t = put(t, r, get(st, r))
            who = re.search(r"\*\*(.+?) — ([\w-]+)\.\*\*", (ROOT / "AGENTS.md").read_text())
            if who:
                t = t.replace(">Presenter name<", f">{who.group(1)}, {who.group(2)}<")
            t = filled(t)
        t = set_title(t.replace("Course Name · Presentation", f"{course} · Presentation"), course)
        out.write_text(t)
        print(f"created {out} (design: {design})")
    elif cmd == "fill":
        read_deck(Path(argv[2]))
        print(f"{argv[2]}: scenes drawn")
    elif cmd == "put":
        deck = Path(argv[2])
        t = put(deck.read_text(), "SLIDES", "\n" + Path(argv[3]).read_text().strip() + "\n")
        if len(argv) > 4:
            t = put(t, "DECK-JS", "\n" + Path(argv[4]).read_text().strip() + "\n")
        deck.write_text(filled(t))
        print(f"{deck}: slides replaced")
    elif cmd == "check":
        check(Path(argv[2]))
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
        out = Path(argv[3]) if len(argv) > 3 else ROOT / ".temp" / "share" / f"{temp_name(deck)}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        bundle(deck, out)
    elif cmd == "pdf":
        deck = Path(argv[2])
        rest = [a for a in argv[3:] if a != "--last"]
        out = Path(rest[0]) if rest else ROOT / ".temp" / "share" / f"{temp_name(deck)}.pdf"
        out.parent.mkdir(parents=True, exist_ok=True)
        pdf(deck, out, "--last" in argv)
    elif cmd == "shots":
        deck = Path(argv[2])
        rest = argv[3:]
        out = Path(rest.pop(0)) if rest and ":" not in rest[0] else ROOT / ".temp" / "shots" / temp_name(deck)
        shots(deck, out, rest)
    else:
        sys.exit(__doc__.strip())


if __name__ == "__main__":
    try:
        main(sys.argv)
    except IndexError:
        sys.exit(__doc__.strip())
