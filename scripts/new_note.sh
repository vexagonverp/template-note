#!/usr/bin/env bash
# Start a new course folder (if needed) and a new document from a template.
# Usage: scripts/new_note.sh <CourseFolder> <kind> ["Course Display Name"] [Descriptor]
#
#   kind        template                         default file name (after Name_ID_)
#   midterm     midterm_template.tex             Midterm_ExamSheet      notes/
#   final       final_template.tex               Final_ExamSheet        notes/
#   theory      theory_template.tex              Theory_Notes           notes/
#   qbank       question_bank_template.tex       Question_Bank          notes/
#   cheatsheet  cheatsheet_template.tex          Cheat_Sheet            notes/
#   lab         lab_report_template.tex (+ .ipynb) Lab1_Report          labs/
#   report      report_template.tex              Assignment             assignments/
#   proposal    proposal_template.tex            Proposal               assignments/
#   exercise    exercise_template.tex            Exercise               assignments/
#   essay-en    essay_en_template.tex            Essay                  assignments/
#   essay-vi    essay_vi_template.tex            TieuLuan               assignments/
#   slides      slides_template.tex              Slides                 presentation/
#   script      presentation_script_template.tex Presentation_Script    presentation/
#   asset       slide_asset_template.tex         Slide_Asset            presentation/assets/
#   paper       paper_llncs/ (folder)            Paper                  paper/
#
#   e.g. scripts/new_note.sh AlgorithmOptimization final "Algorithm Optimization"
#        scripts/new_note.sh AlgorithmOptimization lab "Algorithm Optimization" Lab2_Report
set -euo pipefail
if [ $# -lt 2 ]; then
  sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 1
fi
root="$(cd "$(dirname "$0")/.." && pwd)"
course="$1"; kind="$2"; display="${3:-$1}"
T="$root/templates"
case "$kind" in
  midterm)    tpl=midterm_template.tex;             desc=Midterm_ExamSheet;   sub=notes ;;
  final)      tpl=final_template.tex;               desc=Final_ExamSheet;     sub=notes ;;
  theory)     tpl=theory_template.tex;              desc=Theory_Notes;        sub=notes ;;
  qbank)      tpl=question_bank_template.tex;       desc=Question_Bank;       sub=notes ;;
  cheatsheet) tpl=cheatsheet_template.tex;          desc=Cheat_Sheet;         sub=notes ;;
  lab)        tpl=lab_report_template.tex;          desc=Lab1_Report;         sub=labs ;;
  report)     tpl=report_template.tex;              desc=Assignment;          sub=assignments ;;
  proposal)   tpl=proposal_template.tex;            desc=Proposal;            sub=assignments ;;
  exercise)   tpl=exercise_template.tex;            desc=Exercise;            sub=assignments ;;
  essay-en)   tpl=essay_en_template.tex;            desc=Essay;               sub=assignments ;;
  essay-vi)   tpl=essay_vi_template.tex;            desc=TieuLuan;            sub=assignments ;;
  slides)     tpl=slides_template.tex;              desc=Slides;              sub=presentation ;;
  script)     tpl=presentation_script_template.tex; desc=Presentation_Script; sub=presentation ;;
  asset)      tpl=slide_asset_template.tex;         desc=Slide_Asset;         sub=presentation/assets ;;
  paper)      tpl=paper_llncs;                      desc=Paper;               sub=paper ;;
  *) echo "unknown kind '$kind' (run without arguments to see the list)" >&2; exit 1 ;;
esac
desc="${4:-$desc}"
dir="$root/$course"

if [ ! -d "$dir" ]; then
  cp -R "$root/_course_template" "$dir"
  echo "created course folder $course/"
fi
mkdir -p "$dir/$sub"

# Name_ID prefix from the exam template (after scripts/setup.sh); ASCII only
author=$(sed -n 's/.*\\newcommand{\\StudentName}{\(.*\)}.*/\1/p' "$T/final_template.tex")
author=$(python3 -c 'import sys,unicodedata as u; s=sys.argv[1].replace("đ","d").replace("Đ","D"); print("".join(c for c in u.normalize("NFKD",s) if c.isascii() and c.isalnum()))' "$author")
sid=$(sed -n 's/.*\\newcommand{\\StudentID}{\(.*\)}.*/\1/p' "$T/final_template.tex")
name="${author}_${sid}_${desc}"

if [ "$kind" = paper ]; then
  out="$dir/$sub/$name"
  [ -e "$out" ] && { echo "refusing to overwrite existing $out" >&2; exit 1; }
  cp -R "$T/paper_llncs" "$out"
  echo "created ${out#$root/}/ (build with: cd ${out#$root/} && tectonic main.tex)"
  exit 0
fi

out="$dir/$sub/$name.tex"
[ -e "$out" ] && { echo "refusing to overwrite existing $out" >&2; exit 1; }
DISPLAY_NAME="$display" perl -pe 's/\\newcommand\{\\CourseName\}\{(Course Name|Tên môn học)\}/\\newcommand{\\CourseName}{$ENV{DISPLAY_NAME}}/' "$T/$tpl" > "$out"
echo "created ${out#$root/} (from $tpl)"

if [ "$kind" = lab ]; then
  nb="$dir/$sub/${author}_${sid}_${desc%_Report}.ipynb"
  if [ ! -e "$nb" ]; then
    NAME="$author" ID="$sid" COURSE="$display" perl -pe 's/Your Name/$ENV{NAME}/; s/YOUR-ID/$ENV{ID}/; s/Course Name/$ENV{COURSE}/' "$T/lab_template.ipynb" > "$nb"
    mkdir -p "$dir/$sub/figs"
    echo "created ${nb#$root/} (figures go to ${sub}/figs/, shared with the report)"
  fi
fi
echo "build with: scripts/build.sh ${out#$root/}"
