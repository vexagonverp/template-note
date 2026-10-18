#!/usr/bin/env python3
"""Unpack a saved web page (.mhtml / .mht) and print its readable text.

Usage:
    python3 scripts/mhtml_text.py "Machine Learning_ Lasso Regression -.mhtml"

Writes the HTML and images to .temp/web/<name>/ (open index.html in a browser)
and prints the page text, with code blocks kept on their own lines.
Standard library only.
"""
import email
import html
import pathlib
import re
import sys
from email import policy


def to_text(markup):
    markup = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", "", markup)
    markup = re.sub(r"(?i)<br\s*/?>|</(p|div|h\d|li|tr|pre)>", "\n", markup)
    text = html.unescape(re.sub(r"<[^>]+>", "", markup))
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    root = pathlib.Path(__file__).resolve().parent.parent
    out = root / ".temp" / "web" / re.sub(r"\W+", "_", src.stem)
    out.mkdir(parents=True, exist_ok=True)
    msg = email.message_from_bytes(src.read_bytes(), policy=policy.default)
    page = None
    for k, part in enumerate(msg.walk()):
        if part.is_multipart():
            continue
        ctype = part.get_content_type()
        data = part.get_payload(decode=True) or b""
        if ctype == "text/html" and page is None:
            page = data.decode(part.get_content_charset() or "utf-8", "replace")
            (out / "index.html").write_text(page)
        elif ctype.startswith("image/"):
            (out / f"img{k}.{ctype.split('/')[1].split('+')[0]}").write_bytes(data)
    if page is None:
        sys.exit("no HTML part found")
    print(to_text(page))
    print(f"\n[unpacked to {out.relative_to(root)}/]", file=sys.stderr)


if __name__ == "__main__":
    main()
