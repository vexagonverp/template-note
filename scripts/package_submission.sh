#!/usr/bin/env bash
# Collect the files to hand in into one folder and a zip, outside the figures folder.
# Usage: scripts/package_submission.sh <Course> <PackageName> file [file ...]
#   e.g. scripts/package_submission.sh AlgorithmOptimization AlgorithmOptimization_Lab2 \
#          AlgorithmOptimization/labs/JaneDoe_S1_Lab2.ipynb AlgorithmOptimization/labs/JaneDoe_S1_Lab2_Report.pdf
#   -> AlgorithmOptimization/submit/<Name>_<ID>_<PackageName>/ and .zip
# Rebuild the PDF and re-run the notebook first, so the package matches the sources.
set -euo pipefail
[ $# -ge 3 ] || { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 1; }
root="$(cd "$(dirname "$0")/.." && pwd)"
course="$1"; pkg="$2"; shift 2
author=$(sed -n 's/.*\\newcommand{\\StudentName}{\(.*\)}.*/\1/p' "$root/templates/final_template.tex")
author=$(python3 -c 'import sys,unicodedata as u; s=sys.argv[1].replace("đ","d").replace("Đ","D"); print("".join(c for c in u.normalize("NFKD",s) if c.isascii() and c.isalnum()))' "$author")
sid=$(sed -n 's/.*\\newcommand{\\StudentID}{\(.*\)}.*/\1/p' "$root/templates/final_template.tex")
name="${author}_${sid}_${pkg}"
out="$root/$course/submit/$name"
mkdir -p "$out"
for f in "$@"; do
  [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
  case "$f" in *.tex) pdf="${f%.tex}.pdf"
    if [ -f "$pdf" ] && [ "$f" -nt "$pdf" ]; then echo "warning: $f is newer than its PDF, rebuild first" >&2; fi ;;
  esac
  cp "$f" "$out/"
  echo "  + $(basename "$f")"
done
(cd "$(dirname "$out")" && zip -qr "$name.zip" "$name")
echo "packaged ${out#$root/}/ and ${out#$root/}.zip"
