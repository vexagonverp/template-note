#!/usr/bin/env bash
# Convert phone photos (HEIC/JPG/PNG) in a folder to small JPGs an agent can read.
# Usage: scripts/photos_to_jpg.sh <Course>/hints [maxsize]
#   output: .temp/photos/<folder>/<name>.jpg   (originals are not touched)
set -euo pipefail
[ $# -ge 1 ] || { echo "Usage: $0 <folder> [maxsize]" >&2; exit 1; }
root="$(cd "$(dirname "$0")/.." && pwd)"
src="$1"; size="${2:-1600}"
out="$root/.temp/photos/$(basename "$src")"; mkdir -p "$out"
shopt -s nullglob nocaseglob
for f in "$src"/*.{heic,jpg,jpeg,png}; do
  base="$(basename "${f%.*}")"
  if command -v sips >/dev/null; then          # macOS
    sips -s format jpeg -Z "$size" "$f" --out "$out/$base.jpg" >/dev/null
  elif command -v magick >/dev/null; then      # ImageMagick 7
    magick "$f" -resize "${size}x${size}>" "$out/$base.jpg"
  else
    echo "need sips (macOS) or ImageMagick" >&2; exit 1
  fi
  echo "  $base.jpg"
done
echo "photos in ${out#$root/}/"
