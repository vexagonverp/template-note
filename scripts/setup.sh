#!/usr/bin/env bash
# One-time setup: put your name and student ID into the rules and every template.
# Usage: scripts/setup.sh "Jane Doe" "S1234567" [--venv]
#   --venv  also create .venv and install requirements.txt
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "Usage: $0 \"Your Full Name\" \"YOUR-ID\" [--venv]" >&2
  exit 1
fi
name="$1"; id="$2"
root="$(cd "$(dirname "$0")/.." && pwd)"
shopt -s nullglob
files=(
  "$root/AGENTS.md"
  "$root"/templates/*.tex
  "$root"/templates/*.ipynb
  "$root"/templates/paper_llncs/*.tex
  "$root"/templates/paper_llncs/sections/*.tex
  "$root/_course_template/COURSE.md"
)
for f in "${files[@]}"; do
  grep -q -e "Your Name" -e "YOUR-ID" "$f" || continue
  # perl handles any characters in the name (accents, slashes) safely
  NAME="$name" ID="$id" perl -pi -e 's/Your Name/$ENV{NAME}/g; s/YOUR-ID/$ENV{ID}/g' "$f"
  echo "updated ${f#$root/}"
done
echo "Author is now: $name ($id)"

if [ "${3:-}" = "--venv" ]; then
  python3 -m venv "$root/.venv"
  "$root/.venv/bin/pip" install -q -r "$root/requirements.txt"
  echo "created .venv (use .venv/bin/python for nb_run.py, contact_sheet.py, checks)"
fi
