# game_theory — review brief, 2026-09-21

## What I looked at

One commit, "Initial commit", 2026-05-30, 1069 lines, untouched since. I read all
24 source files: the root plotting scripts, everything in `GameTheoryIMATMT/`
including the `HPC/` package, the SLURM runners, and `main_question.md`. Not a
web project, so no browser check.

## What's actually here

Two things that arrived from different places. `main_question.md` is a recent,
well-shaped research question about decision-making under asymmetric knowledge —
hidden types, private payoffs, deceptive signalling. The rest is old City,
University of London coursework: Axelrod-library Prisoner's Dilemma experiments
written to run on a cluster account (`adgz422`) against a locally-cached
Llama-3-8B, with a hardcoded `city.ac.uk` proxy.

They touch in exactly one file. `GameTheoryIMATMT/Bayes_Player.py` maintains a
prior over opponent "strategy categories" and updates it each round — that is the
research question in code. It is 124 lines and most of the way there.

## What I found

The headline bug is in that one file. The belief update reads `self.history`
where it means `opponent.history`: `:30` computes the cooperation ratio over the
agent's **own** moves and then uses it at `:40` as evidence about the opponent;
`:46` counts the agent's own defections as evidence for `ThresholdBased`; `:80`
and `:86` branch on own history too. So the posterior is substantially a function
of what the agent already decided to do. Any number this produces is not
measuring what the file says it measures.

Second: the experiment can't answer its own question. `:99-104` saves only
scores, never the inferred category, and `strategy_categories` at `:13-22` — the
natural answer key — is populated and then never read anywhere in the file. Its
names (`GrimTrigger`, `Forgiver`, `Stochastic_TitForTat`) don't match real
Axelrod classes either.

The LLM/HPC half is broken beyond the missing cluster. `Strat_per_strat.py:70`
loops `while True` waiting for a response equal to `"✅"`, but the prompt asks for
`Y✅` and the response is the full decoded prompt+completion — the exit condition
can never fire; `:74` would raise `TypeError` anyway. `HPC/tournament.py:22-24`
files a numeric score under the key `"Opponent"` and never records the strategy
name, and `HPC/plots.py:15` then keys a dict by opponent name across a 240×240
loop, so every chart shows only the last match per name. `HPC/ai_player.py:48`
slices the last 50 *characters* of model output as moves and `:53` maps anything
that isn't `"C"` to defect, which makes the "LLM player" a defect-heavy random
player. `Initial_match.py:81` is a plain `NameError`.

And nothing runs: no `requirements.txt`, no README, `axelrod` not installed,
`.python-version` containing `AIRun`.

## Verdict: REVIVE, narrowly

The idea is real and the first step is small. But revive one line and retire the
other. Tasks 1–3 in `todo.md` are a single session that ends with a CSV reading
`opponent, true_category, inferred_category, bayes_score, titfortat_score` and one
chart — that is the definition of "working" for this project, and it is the first
thing that would be worth putting in the empty `wiki/`. Task 4 moves `HPC/`,
`Strat_per_strat.py` and the SLURM scripts to `archive/`: they cannot run anywhere
you have access to, and fixing their result-labelling would be work spent on an
experiment you can't execute. Task 5 clears four root-level plot demos on random
data, one of which drags in PyQt5.

There was no previous `todo.md` or `reference.md`; both are new. If tasks 1–3
haven't been touched by the next review, that's the signal to downgrade this to
PARK or RETIRE — the Bayesian experiment is the only thing keeping it alive.
