#!/usr/bin/env bash
# Rasterize PDF pages to PNG so an agent (or you) can read diagrams and screenshots.
# Usage: scripts/pdf_pages.sh file.pdf [first] [last] [dpi]
#   output: .temp/imgs/<pdfname>-<page>.png
set -euo pipefail
[ $# -ge 1 ] || { echo "Usage: $0 file.pdf [first] [last] [dpi]" >&2; exit 1; }
root="$(cd "$(dirname "$0")/.." && pwd)"
pdf="$1"; first="${2:-1}"; last="${3:-$first}"; dpi="${4:-150}"
[ $# -ge 2 ] || last=$(pdfinfo "$pdf" | awk '/^Pages/{print $2}')
name="$(basename "$pdf" .pdf | tr ' ' '_')"
mkdir -p "$root/.temp/imgs"
pdftoppm -f "$first" -l "$last" -r "$dpi" -png "$pdf" "$root/.temp/imgs/$name"
echo "wrote pages $first-$last to .temp/imgs/${name}-*.png"
