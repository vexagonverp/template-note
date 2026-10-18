#!/usr/bin/env bash
# Build one or more .tex files with tectonic and report problems that matter.
# Usage: scripts/build.sh path/to/file.tex [more.tex ...]
#        scripts/build.sh --preview path/to/file.tex   (also renders pages to .temp/preview/)
# A build that runs past BUILD_TIMEOUT seconds (default 120) is stopped and reported
# as a HANG: suspect math in a heading (docs/LATEX_TRAPS.md), then use
# scripts/build_sections.py to find the section.
set -euo pipefail
preview=0
if [ "${1:-}" = "--preview" ]; then preview=1; shift; fi
[ $# -ge 1 ] || { echo "Usage: $0 [--preview] file.tex ..." >&2; exit 1; }
root="$(cd "$(dirname "$0")/.." && pwd)"
limit="${BUILD_TIMEOUT:-120}"
status=0
for tex in "$@"; do
  dir="$(cd "$(dirname "$tex")" && pwd)"; base="$(basename "$tex" .tex)"
  echo "== $tex"
  set +e
  log="$(cd "$dir" && python3 - "$base.tex" "$limit" <<'PY'
import subprocess, sys
try:
    r = subprocess.run(["tectonic", sys.argv[1]], capture_output=True, text=True, timeout=int(sys.argv[2]))
    print(r.stdout + r.stderr, end=""); sys.exit(r.returncode)
except subprocess.TimeoutExpired:
    print(f"HANG: still running after {sys.argv[2]} s, stopped."); sys.exit(124)
PY
)"
  rc=$?
  set -e
  if [ $rc -ne 0 ]; then echo "$log" | grep -vE "^note: (downloading|Skipped)" ; status=1; continue; fi
  echo "$log" | grep -E "error|Overfull|Missing character|Undefined|Citation .* undefined" | sort -u || true
  pages=$(pdfinfo "$dir/$base.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
  echo "   -> $base.pdf (${pages:-?} pages)"
  if [ $preview -eq 1 ] && command -v pdftoppm >/dev/null; then
    out="$root/.temp/preview/$base"; mkdir -p "$out"
    pdftoppm -r 70 -png "$dir/$base.pdf" "$out/p"
    echo "   preview pages in ${out#$root/}/"
  fi
done
exit $status
