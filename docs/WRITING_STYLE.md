# Writing style

The reader is a student under exam stress. Write so they can follow it in a hurry.

## Do

- **Short sentences, plain words.** "The price goes up" beats "the dual variable increases
  monotonically".
- **Numbers before symbols.** Show `(2,1) + (-1.2,-1) = (0.8, 0)` before writing
  `x + Δx`.
- **Quote the lecturer** for definitions and named lists. That wording is what gets
  marked. Then explain it in one or two plain sentences and give a tiny example.
- **Keep every item.** If a slide lists 5 things, the sheet lists 5 things.
- **Say why** each step is done, in one line ("we flip it because the multiplier must be
  ≥ 0 for a ≤ constraint").
- **"Row 1 in words"** under every iteration table: walk through the first row slowly.
- **Name the trap** where people usually go wrong, and give a quick check that catches it.

## Don't

- Filler: "it's important to note that", "it is worth mentioning".
- Puffed-up words: "leverage", "crucial", "robust", "delve", "comprehensive".
- Rule-of-three padding and slogan endings.
- Lots of em dashes. Use a full stop or a comma.
- "Checked with a solver" as the method. The method must work by hand.

## Register by document type

| Document | Register |
|----------|----------|
| Exam sheet, theory notes, question bank | plain, spoken, "you"; numbers before symbols |
| Lab report | plain "we"; say what was run and what came out, with the number |
| Presentation script | spoken: short sentences, "we" / "you", pauses marked as tips |
| Slides | short phrases; no em dashes, no contractions |
| Report, proposal, essay, paper | academic third person; plain words, no "I" |
| Vietnamese tiểu luận | formal written Vietnamese, the faculty's thesis conventions |

## Graded reports (not exam sheets)

- Third person only, no "I".
- Match the author's own voice (look at their earlier work if the repo has it).
- Do not "fix" small imperfections the author added by hand on purpose. Flag them and ask.
- Report the word count after each build if there is a target.

## Example: before and after

> **Before:** It is important to note that Newton's method leverages second-order curvature
> information, which crucially enables significantly faster convergence.
>
> **After:** Newton's method uses the curvature (the Hessian). Near the answer this makes
> the error roughly square itself each step: 0.2, then 0.024, then 0.0003.
