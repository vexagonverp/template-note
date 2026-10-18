---
name: audit-sheet
description: Adversarial, independent audit of a finished exam sheet, theory notes or question bank. Re-extracts the sources, checks wording and list counts against the slides, recomputes every number, rebuilds the PDF, and prints a findings table with a verdict. Does not edit files. Use after a sheet is built, or when the user asks to check, verify, audit or review notes.
argument-hint: <file.tex> [second.tex] [spec or extra focus]
context: fork
agent: general-purpose
background: false
---

# Adversarial audit

You are auditing `$ARGUMENTS` (one or two `.tex` files, plus an optional note on what to
focus on). If that is empty, or shows up literally as a placeholder, take the files from
the user's message, or audit the most recently changed `*.tex` under `*/notes/`.

You have **no context from whoever wrote these files**, and that is intended. Find
everything that is wrong, missing or weak, and report it.

**Be adversarial.** Assume the files contain errors and that lists were silently truncated
or padded. Do **not** trust the documents' own summaries. Verify every factual claim
against the original sources, and re-derive every computation yourself.

**Do not edit any file.** Print the report only.

## Ground truth (read ALL of it before judging anything)

1. **The spec.** The skill or brief the sheet was built from: `.claude/skills/exam-final`,
   `exam-midterm` or `theory-notes` (match the file's template), plus `<Course>/COURSE.md`.
   Its outline, fidelity rules and "definition of done" are your acceptance criteria.
2. **The sources.** These are the only authority on wording and list contents:
   `<Course>/slides/*`, `<Course>/materials/*`, `<Course>/transcripts/*`, and the photos in
   `<Course>/hints/`. **Re-extract the text yourself** with `python3 scripts/pdf_text.py`,
   `python3 scripts/pptx_text.py` and `scripts/photos_to_jpg.sh`. Do not reuse anything
   extracted earlier.
3. **House style.** `AGENTS.md`, `docs/SHEET_ANATOMY.md`, `docs/WRITING_STYLE.md`.

## What to check, and how

**A. Build and artifacts.**
- Run `scripts/build.sh <file>` from scratch. Report every error, and every Overfull or
  Underfull box with its line number. Report page counts.
- Run `python3 scripts/sync_preamble.py --check <file>`. The shared preamble must match the
  template's; flag any silent deviation.

**B. Source fidelity (most important).** For every definition, named principle and
numbered list, check it against the source and cite the slide or page:
- Wording: exact phrasing is quoted where the spec asks for it. Flag a paraphrase where a
  quote is required, and every misquote.
- List completeness: **if a slide has N items, the notes must have N, not N−1 and not N+2.**
  Confirm the count and the contents of each list.
- Look-alike traps: lists that are easy to mix up are kept distinct, and both are correct.
- Hints and transcript alerts: every one is listed on page 1 and covered in the body.

**C. Coverage against the spec.**
- Walk through the spec's outline and report anything it requires that is not covered.
- Confirm the required scaffolding is there: title block, overview or playbook, decoder or
  Part 0, the per-question layout, the summary, and the section exam labels.

**D. Recompute every number.**
- Do not trust the worked answers. Recompute every iteration, table cell and boxed answer
  independently, in a script under `.temp/audit/`.
- Check that the steps shown on the page actually produce the number.

**E. Cross-file consistency.** Facts shared by the two files must match.

**F. Correctness of the added explanations.** Plain-English extensions, examples,
mnemonics and "traps" must not introduce errors or contradict the source. **Treat a
confidently-wrong extension as a Major defect.**

**G. Typography.** Check for:
- unescaped special characters, tables that don't wrap, URLs or formulas past the margin
- broken references, duplicated or skipped question numbers
- a question box split across pages (render with `scripts/pdf_pages.sh` and look)

## Output

1. **Verdict:** PASS, PASS-WITH-FIXES or FAIL, plus build status and page counts.
2. **Findings table:** `Severity | File:line | Issue | Evidence (source page or recomputation) | Suggested fix`.
   - **Critical:** wrong fact, wrong computation, fails to build, or a required topic is missing.
   - **Major:** truncated list, misquote where a quote is required, cross-file
     contradiction, or a confidently-wrong extension.
   - **Minor:** overfull box, typo, weak example, or style drift.
3. **Coverage checklist:** each required list and topic marked ✓ or ✗, with a source
   citation for every ✓.
4. **Recomputation log:** your own independent work for every number, marked agree or disagree.

Cite evidence for **every** finding. "Looks fine" is not an audit: show the check you ran.
If a category has no problems, say what you verified and how, so the PASS can be trusted.
