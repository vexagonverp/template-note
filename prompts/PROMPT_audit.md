# Prompt: adversarial audit of a finished sheet

Run this in a **separate, fresh session** after a sheet is built. The auditor should not be
the agent that wrote the sheet.

---

You are auditing the study documents `<file1.tex>` (and `<file2.tex>`) for **<Course>**.
Find everything that is wrong, missing, or weak, and report it. **Be adversarial:** assume
the files contain errors and that lists have been silently truncated or padded. Do **not**
trust the documents' own summaries or the generator's claims. Verify every factual claim
against the original sources and re-derive every computation yourself.

## Ground truth (read ALL of it before judging anything)

1. **The spec:** `<the prompt the sheet was built from>`. Its outline, fidelity rules,
   "cover at least" list and "definition of done" are the acceptance criteria.
2. **The sources** (the only authority on wording and list contents): `<Course>/slides/*`,
   `<Course>/materials/*`, `<Course>/transcripts/*`, hint photos in `<Course>/hints/`.
   **Re-extract the text yourself** (`scripts/pdf_text.py`, `scripts/pptx_text.py`); do not
   rely on any earlier extraction.
3. **House style:** `AGENTS.md`, `docs/SHEET_ANATOMY.md`, `docs/WRITING_STYLE.md`.

## What to check (and how)

**A. Build and artifacts.** Build every file from scratch with `scripts/build.sh`. Report any
error and list every Overfull/Underfull box with its line number. Report page counts. Run
`python3 scripts/sync_preamble.py --check <files>`: the shared preamble must be identical to
the template's. Flag any silent deviation.

**B. Source fidelity (most important).** For every definition, named principle and numbered
list, check it against the source and cite the slide/page:
- Wording: the exact phrasing is quoted where the spec asks for it. Flag paraphrases where a
  quote is required, and any misquote.
- List completeness: **if a slide has N items, the notes must have N, not N−1, not N+2.**
  Confirm the count and contents of each list. Report short, padded, or reordered lists.
- Look-alike traps: lists that are easy to mix up (e.g. "conditions" vs "components") are
  kept distinct and both correct.

**C. Coverage vs the spec.** Walk the spec's outline and "cover at least" list. Report
anything not covered. Confirm the required scaffolding exists (title block, overview box,
decoder/glossary, question layout, summary, section exam labels, hints on page 1).

**D. Recompute every number.** Do not trust the worked answers. Recompute every iteration,
table cell and boxed answer independently (show your work or your script). Check that the
steps shown on the page actually produce the number.

**E. Cross-file consistency.** Shared facts must match between the files.

**F. Correctness of the added explanations.** Plain-English extensions, examples, mnemonics
and "traps" must not introduce errors or contradict the source. **Treat a confidently-wrong
extension as a Major defect.**

**G. Typography.** Special characters escaped; tables wrap; no URL or formula past the
margin; no broken references; no duplicated or skipped question numbers; no question box
split across pages.

## Output (print it; do not edit the .tex files unless explicitly asked)

1. **Verdict:** PASS / PASS-WITH-FIXES / FAIL, plus build status and page counts.
2. **Findings table:** `Severity | File:line | Issue | Evidence (source page or recomputation) | Suggested fix`.
   Severity: **Critical** (wrong fact, wrong computation, fails to build, required topic
   missing) · **Major** (truncated list, misquote where a quote is required, cross-file
   contradiction, confidently-wrong extension) · **Minor** (overfull box, typo, weak example,
   style drift).
3. **Coverage checklist:** each required list/topic with ✓/✗ and a source citation for each ✓.
4. **Recomputation log:** your independent work for every number, agree/disagree.

Cite evidence for **every** finding. "Looks fine" is not an audit: show the check you ran.
If a category has no problems, say what you verified and how, so the PASS is trustworthy.
