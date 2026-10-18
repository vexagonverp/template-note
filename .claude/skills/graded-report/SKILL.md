---
name: graded-report
description: Write a graded document (lab report with its notebook, assignment or technical report, research proposal, exercise answers, English essay, or Vietnamese tiểu luận) from the assignment brief, built to a PDF whose file name is the submission name. Use when the user asks to write or finish a lab report, assignment, proposal, essay or homework.
argument-hint: <CourseFolder> <lab|report|proposal|exercise|essay-en|essay-vi> [Descriptor] [notes]
---

# Graded document

**Input:** `$ARGUMENTS` is the course folder, the kind, an optional descriptor (e.g.
`Lab2_Report`, `Assignment_Space_Based`), and any notes. If it is empty, or shows up
literally as a placeholder, take these from the user's message, or ask.

Follow `AGENTS.md` → "Workflow for graded work", and `docs/WRITING_STYLE.md` → "Register
by document type".

## 1. The brief first

- Find the brief word for word in `<Course>/COURSE.md` → Assignments. If it isn't there,
  ask the user to paste it, then save it there.
- Pull out the deliverables, the marking criteria, the length or word target, the deadline,
  and the submission format. Every criterion must be visibly answered in the document.
- Ask about anything the brief leaves open that changes the work (topic choice, data,
  language). Otherwise pick a sensible default and say so.

## 2. Create it

```bash
scripts/new_note.sh <Course> <kind> "<Course display name>" <Descriptor>
```

The `.tex` name is the submission name. Never rename the PDF afterwards.

## 3. Per kind

**lab**
- The notebook comes first. Fill in `<Course>/labs/<Name>_<ID>_LabN.ipynb` (made next to
  the report), keeping a fixed seed and the `save()` helper that writes to `figs/`.
- Run it with `.venv/bin/python scripts/nb_run.py <notebook>` and fix any errors.
- Take every number from the saved output (`python3 scripts/nb_text.py <nb> --outputs`).
- Report sections mirror the notebook's `## Step k` headings: Idea / Math / Method (short
  listing with a caption) / Results (figure + "does it reach the optimum?"), then a
  comparison table and the conclusion.
- Package with `scripts/package_submission.sh <Course> <Course>_LabN <nb> <report.pdf>`.

**report / proposal**
- Academic third person, plain words.
- Keywords and abstract, then sections in the brief's own order (the proposal template
  already follows the usual marking scheme).
- TikZ diagrams use the `container / person / extsys` styles, and tables are booktabs with
  captions and `\ref`s.

**exercise**
- Copy the problem exactly into the `notebox`, show every step, and put the answer in a
  `resultbox`.
- Check the numbers with a script.

**essay-en / essay-vi**
- One idea per paragraph, a counter-argument section, and no slogan endings.
- Vietnamese: formal written style, with the MỞ ĐẦU / chapters / KẾT LUẬN structure and
  the bibliography split into Vietnamese and English sources. Put the university logo next
  to the `.tex` as `logo.png`.

## 4. Sources and honesty

- Every reference must be real and checkable (DOI or URL). Never invent a source, a quote
  or a number. If you can't find a source for a claim, say so or drop the claim.
- Match the user's earlier writing voice if their past work is in the repo.
- Do not "fix" small imperfections the user added by hand on purpose. Flag them instead.

## 5. Build, check, hand over

1. Run `scripts/build.sh --preview <file>.tex`, fix every warning, and look at the pages.
2. Report the page count and the word count (`pdftotext <pdf> - | wc -w`) against the target.
3. List every marking criterion and where the document answers it.
4. Do not commit unless asked.
