# Anatomy of an exam sheet

There are five exam templates. They all share `templates/_exam_preamble.tex`, so every box
works in every one of them and you can mix them. Pick by **what the exam is like**, not
by its name:

| Template | Use when | Organised by |
|----------|----------|--------------|
| `midterm_template.tex` | the teacher announces question *types* ("Q1 formulate an LP, Q2 prove convexity") and some are proofs | announced question type, then practice, then theory |
| `final_template.tex` | the teacher gives a question pool and changes the numbers | pool question, in pool order |
| `theory_template.tex` | the course tests definitions, lists, comparisons, short essays | topic, each concept in a fixed pattern |
| `question_bank_template.tex` | self-test questions next to a theory sheet | past exams, topic groups, twists, mock exams |
| `cheatsheet_template.tex` | the notes are limited to N sides | topic, 2 dense columns |

## Midterm layout (announced question types)

1. **Title block** and **exam playbook**: exam conditions, the announced questions word
   for word in a table (Q, what she asks, computation or **proof**, page), habits that
   save marks, hand-calculation helpers.
2. **One "Playbook Qn" part per announced question:**
   - question box with the announcement (source: `Announcement, <date>`)
   - "what a full-mark answer contains" checklist
   - guideline box with `\step` badges
   - for proof types: a method-choice table ("if you see … use …"), a `proofbox`
     template (Claim → Method → Steps with reasons → Conclusion □), and filled-in proofs
   - worked example, answer box, trap box
3. **Practice questions**: the review sheet / exercises in original order, each heading
   tagged `(trains Qn)`, each in the 4-part layout below.
4. **Theory reference** by lecture, each section tagged `(Exam Qn, Lecture m)`. Start
   with a symbol dictionary. Lecturer's definitions go in `defbox` word for word, then a
   plain explanation and a number example.
5. **Appendix**: derivative and formula tables, slide index (topic → lecture, slide).

## Theory layout (definitions, lists, essays)

1. **Title block** with the rules line and the companion file (the question bank).
2. **Overview box** (`notebox`): format, grading split, what the lecturer said will appear
   (quoted, with `\sref{transcript L5, seg. 2}`), **Not expected**, **the numbers you must
   memorise** (every list count on one line), and the answer template
   *Definition → How it works (full list) → Tiny example → Why it matters / trap*.
3. **Jargon decoder**: a numbered glossary with `\label{term:...}`. Later uses write
   `Term\gl{term:...}`, which prints a superscript link back to the entry.
4. **One section per topic**, heading tagged `\exam{Midterm}` / `\exam{Final}` /
   `\exam{Midterm + Final}`, starting with a `Source:` line and `\examcue{}` quotes.
   Each concept:
   - `defbox{Lecture 1, slide 5}` with the lecturer's exact words, defined term in bold
   - `\lbl{What it is:}` `\lbl{How it works:}` `\lbl{Tiny example:}` `\lbl{Why it matters / trap:}`
   - `memobox[Memorise this chain (5 items)]` for ordered lists, with a memory hook
   - compare tables for look-alikes (Term | slide wording | plain English + example)
   - for patterns / frameworks: `\lbl{Context:} \lbl{Solution:} \lbl{Weaknesses:} \lbl{Example:}`
5. **Situational questions**: an answer-skeleton `notebox`, then one `scenariobox` per
   scenario (Scenario / Stakeholders / Concepts / Verdict). Phenomenon → Solution banks use
   three bullets (Phenomenon / Solution / Examples).
6. **Where to look if a question goes past the slides**: topic → textbook section → page.
7. **`pitfallbox`** (exam-day pitfalls, numbered) and **`summarybox`** (last-minute checklist).

## Question bank layout

- "How to use this bank" box with the tag legend (`\qtag{past exam A}`, `\qtag{likely}`,
  `\qtag{compute}`, `\qtag{practice}`, `\qtag{twist}`, plus any graded-component tag).
- **Past exams transcribed** word for word with marks per part, and a "which topics come up
  most" table (topic × year).
- Each question: `\Q{Q12}{\qtag{likely} Title}` → the question alone in a `qbankbox` (so the
  answer can be covered) → `\lbl{Answer:}` → `\lbl{Why, step by step:}` → `\lbl{Trap to avoid:}`
  → `\lbl{Also asked as:}` (2–3 rephrasings). Families of similar questions get a
  `\lbl{Recipe for any question like this:}`.
- **Twist questions** (a lecture example with one detail changed), with a "read this first" box.
- **Mock exams**, graded Easy / Medium / Hard, with question ids `M1-Q1`.
- A **model deliverable** (e.g. a full proposal) with a marking checklist when the exam asks
  you to produce an artefact.

## Cheat-sheet layout

10pt, 0.8–0.9 cm margins, `\footnotesize` body, two columns (`multicols`) with a rule.
Tables instead of prose, one formula `notebox` per topic, no worked examples (point to the
full sheet), `\columnbreak` to balance. Black and white so it photocopies.

## Final layout (question pool)

### Page order

1. **Title block.** Course, exam, date, `Student: Name (ID)`.
2. **Exam playbook.** What the teacher announced (topics, format, allowed material), every
   hint (board photos, slides shown in class), and a table: question type → what can change
   → page. Then "habits that save marks" and a box of hand-calculation helpers.
3. **Part 0: the math from zero.** Every tool used later (derivatives, matrix inverse,
   Lagrangian, sign/clip, ...), explained with a number example before the symbols.
4. **One part per topic**, each question in the 4-part layout below.

## The 4-part layout (per question, both templates)

| # | Box | Colour | LaTeX | What goes in it |
|---|-----|--------|-------|-----------------|
| 1 | Question | blue bar | `\begin{origbox}{Title}{Source}` | The question exactly as printed, same equation numbers, source on the right. Hint overrides noted in italics. |
| 2 | Guideline | red bar | `\begin{guidebox}` + `\step{n}{Name}` | The recipe, written with letters, so it works for any numbers. Shortcut formulas. Sign traps. |
| 3 | Worked example | plain | `\step{n}{Name}`, `\iterhead{k}{...}` | Same step names as the guideline, real numbers, every line. Iteration tables with a "Row 1 in words" sentence. |
| 4 | Answer | green bar | `\begin{examsolbox}{Question X}` | What to write on the paper: parts (a)(b)(c), short working, final results in `\boxed{}`. |

Optional boxes:

- `resultbox`: formulas and facts to quote.
- `qbox`: a small problem statement (for variants).
- `algobox{Title}`: numbered pseudocode, with *(inner max)* / *(outer min)* style labels.
- `trapbox`: the mistake most people make here and how to catch it.
- `defbox{Lecture 2, slide 7}`: the lecturer's exact definition or named list.
- `proofbox{Title}`: a proof laid out Claim → Method → Steps (with reasons) → Conclusion □.
- `notebox`, `memobox`, `scenariobox`, `pitfallbox`, `summarybox`, `qbankbox`: see the theory and
  question bank layouts above.
- Inline: `\sref{L1 p46}` source tag, `\gl{term:x}` glossary link, `\qtag{likely}` tag badge,
  `\exam{Final}` exam label, `\lbl{Label:}` run-in label, `\examcue{"quote"}`.
- Code: `\begin{lstlisting}[style=pyStyle]` (or `cppStyle`). Diagrams: TikZ styles
  `blk`, `enc`, `xr`, `kb`, `lb`, `ar` for redrawing exam figures (block ciphers, pipelines).

## Rules of thumb

- Question boxes never break across pages. Guideline and answer boxes may.
- Iterations always go in a table: one row per iteration, one column per quantity.
- Every iteration also gets a sanity check line ("did f go down? still feasible?").
- Add 1–2 variants the teacher could plausibly give (flip ≤ to ≥, active vs inactive
  constraint, non-diagonal Hessian, 2 iterations instead of 1).
- If a step is not given (step size, start point), the sheet picks one and says so,
  because that is what the student should do on the paper too.

## Minimal example

```latex
\begin{origbox}{2.1 \ Newton's Method}{Pool \S2.1, p.~1}
Consider $\min f(\mathbf{x})=\tfrac12x_1^2+2x_2^2-\ln x_1$ ... \tag{1}
\begin{enumerate}[label=(\alph*)] \item ... \end{enumerate}
\end{origbox}

\begin{guidebox}
\step{1}{Gradient and Hessian} Take $\partial f/\partial x_i$ ...
\step{2}{Newton direction} $\Delta x=-(\nabla^2f)^{-1}\nabla f$ ...
\end{guidebox}

\iterhead{1}{at $x^{(0)}=(2,1)$:}
...

\begin{examsolbox}{Question 2.1}
\begin{enumerate}[label=\textbf{(\alph*)}]
  \item ... $\boxed{x^{(1)}=(0.8,\ 0)}$
\end{enumerate}
\end{examsolbox}
```
