---
name: new-course
description: Set up a new course folder from the course template, sort the user's files (slides, pools, past papers, photos, transcripts, notebooks) into the right subfolders, and fill in COURSE.md from the teacher's announcement and assignment briefs. Use when the user starts a new course, drops a pile of course files, or pastes an exam announcement.
argument-hint: <CourseFolder> ["Course display name"] [folder with files to sort]
---

# New course setup

**Input:** `$ARGUMENTS` is the course folder name (CamelCase, no spaces, e.g.
`SoftwareArchitect`), an optional display name, and an optional folder of files to sort.
If it is empty, or shows up literally as a placeholder, take these from the user's message,
or ask.

## Steps

1. **Create the folder** if it doesn't exist: `cp -R _course_template <Course>`. An
   existing course keeps its files; only add what's missing.
2. **Sort the files** using the table in `_course_template/README.md`. Move them, keep the
   original names, and never delete anything.

   | Files | Folder |
   |-------|--------|
   | lecture slides (pdf, pptx) | `slides/` |
   | question pools, past exams, exercise sheets, lab handouts, textbook, assigned papers, saved web pages | `materials/` |
   | board photos, screenshots of hints | `hints/` |
   | transcripts / recording notes | `transcripts/` (outline them with `/transcript`) |
   | notebooks the user wrote | `labs/` |

   If you can't tell what a file is, read it first (`scripts/pdf_text.py` with a page range,
   `scripts/pptx_text.py`, or open the image). Ask if it's still unclear.
3. **Fill in `COURSE.md`:**
   - exam date and format, and the announcement **word for word**
   - one line per hint photo saying what it shows (look at each one)
   - one line per transcript
   - each assignment brief word for word, with deadline, weight, length and submission format
   - anything the user said about the lecturer's preferences, under "Notes for the agent"

   Leave a field as `<...>` rather than guessing.
4. **Say what's next:** which skill fits the exam (`/exam-final` for a question pool,
   `/exam-midterm` for announced question types, `/theory-notes` for a theory course), plus
   `/graded-report` for any assignment, and what information is still missing.

Do not commit unless asked.
