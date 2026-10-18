---
name: read-sources
description: Extract and read every source in a course folder (PDF and PPTX slides, scanned or image-only pages, phone photos of hints, saved web pages, notebooks, transcripts) into .temp/ text files and page images, and summarise what each contains. Use before writing any sheet or report, or when the user asks what is in the course material.
argument-hint: <CourseFolder> [subfolder or file]
---

# Read a course's sources

**Input:** `$ARGUMENTS` is the course folder, optionally narrowed to one subfolder or file.
If it is empty, or shows up literally as a placeholder, take it from the user's message, or ask.

Everything extracted goes under `.temp/<Course>/`, which git ignores. Quote file names,
since many contain spaces.

## Per file type

| Type | Command | Then |
|------|---------|------|
| PDF | `python3 scripts/pdf_text.py "<f>" > ".temp/<Course>/<name>.txt"` | it lists image-only pages on stderr |
| image-only / scanned page | `scripts/pdf_pages.sh "<f>" <first> <last> 150` | look at each PNG; never guess its content |
| whole deck at a glance | `scripts/pdf_pages.sh "<f>" 1 <N> 50` then `.venv/bin/python scripts/contact_sheet.py .temp/imgs/<name>-*.png` | look at the grids |
| PPTX | `python3 scripts/pptx_text.py "<f>" > ".temp/<Course>/<name>.txt"` | diagram slides: ask the user to export the deck to PDF, then `pdf_pages.sh` |
| photo (HEIC, JPG, PNG) | `scripts/photos_to_jpg.sh "<Course>/hints"` | look at each JPG in `.temp/photos/hints/` |
| saved web page (.mhtml) | `python3 scripts/mhtml_text.py "<f>"` | |
| notebook (.ipynb) | `python3 scripts/nb_text.py "<f>"` | |
| transcript (.md, .txt) | read it directly | |

## Report back

Give a short inventory, one line per file, covering:

- what it is (lecture N on X, question pool part 2, board photo of Q1, …)
- page or slide count
- which pages are image-only, and what you saw on them
- anything that looks like an exam hint (marked, circled or repeated content, "this will
  be on the exam")

Note anything you could not read. If `COURSE.md` lacks a line for a hint photo or
transcript, offer to add it.
