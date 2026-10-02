# game_theory — daily brief, 2026-10-02

## What I looked at

All 1,069 lines of source: the six root-level scripts, `GameTheoryIMATMT/` and its
`HPC/` package, all four SLURM runners, and `main_question.md`. Also re-read the
2026-09-21 review's `todo.md` and `last_run.json` to check them against the code.
Not a web project, so no browser check.

## The finding that matters most

**The last review was right about everything and nothing was done.** `git log` shows
two commits total: the 2026-05-30 initial commit and `5ce0c23`, the review commit
itself. Eleven days, zero source changes. The previous TODO was accurate, specific
and anchored to line numbers — and it still didn't move. That is the actual signal
here, more than any individual bug.

The reason is probably task ordering. Last time the quick win was "write
requirements.txt" and the real experiment was task 3 of 5. Nobody reaches task 3 of
5 in a 40-repo rotation. So this list is four tasks, two of them deletions, and the
experiment is task 2.

## What I found that the last review missed

`Bayes_Player.py:34` is an **off-by-one**, and the previous review explicitly called
it one of the two correct lines. It isn't. In Axelrod both histories are the same
length when `strategy()` is called, so a TitForTat opponent's move at round *t−1*
copies your move at round *t−2* — `self.history[-2]`, not `[-1]`. As written the line
tests whether both players happened to play the same action in the same round, which
is close to a coin flip, so the TitForTat hypothesis never accumulates real evidence.
That matters because TitForTat-detection is the single thing this player most needs
to get right.

Two more: the likelihoods at `:53-58` are pinned at 0.1/0.9 with no floor, so priors
decay geometrically and lock near zero permanently — and `Turns = 10` at `:91` gives
only nine updates, so the posterior cannot converge either way. The experiment's
horizon is too short to test its own hypothesis. And all four `*.sh` runners turn out
to be copy-pasted from an **ANSYS Fluent CFD** job template: every one carries
`module load fluent` and `--licenses=anshpc:176` on a PyTorch job, so they would
queue for ANSYS licenses they never use.

## What I'm proposing, and the verdict

**REVIVE, with a deadline.** `main_question.md` is a genuine research agenda — 71
specific lines on asymmetric information, clearly written by hand — and
`Bayes_Player.py` is that agenda roughly 80% implemented. That is more than most
repos in this tier have, and it's why this isn't PARK today.

But I've written the gate into `todo.md`: if the first two tasks haven't happened by
~2026-10-12, the honest call is PARK. A third consecutive unactioned REVIVE would be
bookkeeping rather than a plan.

Task 1 is unavoidable and genuinely 15 minutes — `axelrod` is still not installed,
there's no venv, and the system `python3` has no `pip`, so every file in the repo
dies on line 1. Task 2 collapses last review's bug fix and experiment redesign into
one session with a concrete finish line: one CSV, eight rows, columns `opponent,
true_category, inferred_category, bayes_score, titfortat_score`. If the inferred
column comes out mostly wrong, that is still a result worth writing down.

Tasks 3 and 4 are both deletions. The LLM/HPC half is retired outright, not fixed —
`HPC/ai_player.py:48` slices the last 50 *characters* of decoded output (prompt
included, since the input ids are never stripped) and `:53` maps anything that isn't
`"C"` to Defect, so the "LLM player" is a defect-heavy random player. The repo's
headline comparison was measuring parsing noise. `HPC/tournament.py:22-24` then
stores a score under a key named `Opponent` and never records `strategy.name` at all,
so the saved results were unusable before the charts ever got them.
