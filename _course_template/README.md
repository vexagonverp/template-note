# Course folder

Copied from `_course_template/`. Fill in `COURSE.md` first: exam format, the teacher's
announcement word for word, assignment briefs, and one line per hint photo or transcript.

## What goes where

| You have | Put it in | Read it with |
|----------|-----------|--------------|
| Lecture slides (PDF) | `slides/` | `python3 scripts/pdf_text.py`, `scripts/pdf_pages.sh` for diagrams |
| Lecture slides (PPTX) | `slides/` | `python3 scripts/pptx_text.py` (export to PDF to see diagrams) |
| Question pool, past exam, exercise sheet | `materials/` | `pdf_text.py`; scanned pages: `pdf_pages.sh` |
| Textbook, assigned papers | `materials/` | `pdf_text.py` |
| Saved web page (.mhtml) | `materials/` | `python3 scripts/mhtml_text.py` |
| Board photo, screenshot (HEIC/JPG/PNG) | `hints/` | `scripts/photos_to_jpg.sh` |
| Lecture transcript / recording summary | `transcripts/` | plain markdown (`prompts/PROMPT_transcript.md`) |
| Lab notebook (.ipynb) | `labs/` | `python3 scripts/nb_text.py`, run with `scripts/nb_run.py` |

File names with spaces are fine; quote them in the shell.

## Start a document

```bash
scripts/new_note.sh <ThisFolder> final "Course Name"      # or midterm, theory, qbank, cheatsheet
scripts/new_note.sh <ThisFolder> lab "Course Name" Lab2_Report
scripts/new_note.sh <ThisFolder> report "Course Name" Assignment_Topic
```

Run `scripts/new_note.sh` with no arguments for the full list.
