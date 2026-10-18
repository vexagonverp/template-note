# Prompt: write a graded report (lab, assignment, proposal, essay)

---

Write my **<lab report / assignment / proposal / essay>** for **<Course>**.

- Assignment brief (word for word): `<Course>/COURSE.md` → "Assignments", or paste it here.
- Template: `scripts/new_note.sh <Course> <lab|report|proposal|essay-en|essay-vi> "<Course>" <Descriptor>`.
  The file name is the submission name; never rename the PDF afterwards.
- Length / word target: <N words or pages>. Report the word count after each build.
- Sources to use: <papers, slides, data>. References in <IEEE / author-year> style, and
  every reference must be real and checkable (give DOI or URL). Do not invent sources.

For a **lab**: run the notebook first (`scripts/nb_run.py`), take every number from its
saved output (`scripts/nb_text.py --outputs`), use the same figures (`figs/`), and mirror
the notebook's "Step k" sections. Package with `scripts/package_submission.sh`.

Writing: follow `docs/WRITING_STYLE.md` for this document type (academic third person for
reports, proposals and essays; plain "we" for lab reports). Match my earlier writing voice
in `<path to earlier work>` if given. Do not change small things I edited by hand on
purpose; flag them instead.

Build, fix every warning, check the pages, and tell me the page and word count.
