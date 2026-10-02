# game_theory — Reference

## What this is

Two unrelated things in one folder:

1. **A research question** (`main_question.md`) — how should an agent decide under
   asymmetric knowledge: hidden types, private payoffs, uncertain intentions?
   71 lines, specific, with its own experiment list. Genuinely worth pursuing.
2. **Finished coursework** (`GameTheoryIMATMT/`, root `*.py`) — Iterated Prisoner's
   Dilemma experiments on the [Axelrod](https://github.com/Axelrod-Python/Axelrod)
   library, written against a City, University of London HPC account (`adgz422`).
   One commit, 2026-05-30. No source change since.

They overlap in exactly one file: `GameTheoryIMATMT/Bayes_Player.py`, a player that
keeps a prior over opponent "strategy categories" and updates it each round. That is
the research question in code. Everything else is scaffolding or dead weight.

## Current state: nothing here runs

Unchanged since the 2026-09-21 review:

- No `requirements.txt`, no README, no venv. `axelrod` is not installed; the ambient
  `python3` is 3.14.4 with no `pip`. Every file fails at `import axelrod`.
- `.gitignore` excludes `GameTheoryIMATMT/results/`, so every CSV, JSON and plot the
  code reads or writes is absent. `Strat_per_strat.py:29` opens
  `results/Strategy_Guide_results.json`, which does not exist.
- `GameTheoryIMATMT/.python-version` says `AIRun`; `.3.11.11` and `.python3.11.11`
  both say `myenv`. All three name virtualenvs that only existed on the cluster.

## Layout

| Path | What it does | Works? |
|---|---|---|
| `GameTheoryIMATMT/Bayes_Player.py` | Bayesian opponent-type inference, 10 turns vs ~240 strategies | the core idea; belief update reads its own history, and `:34` is off by one |
| `GameTheoryIMATMT/Initial_match.py` | Hand-rolled round-robin, CSV + batched bar charts | `NameError: i` at `:81` after all 57,600 matches; `:25-26` double-counts every pair. `axl.Tournament` already does this, in parallel |
| `GameTheoryIMATMT/HPC/` | Llama-3-8B "AI player" + tournament runner | needs cluster GPUs, a City proxy, a local model path; output columns mislabelled at source |
| `GameTheoryIMATMT/Strat_per_strat.py` | LLM critiques strategy descriptions | `while True` at `:70` whose exit can never fire |
| `GameTheoryIMATMT/*.sh` | SLURM batch scripts | all four copy-pasted from an ANSYS Fluent CFD template; hardcoded to `/users/adgz422` |
| `Game_theory.py` | Full tournament + slider bar chart | runs (slowly); `CustomStrategy` is defined but never entered |
| `Input_match.py` | Human vs TitForTat, 3 turns | 5 lines, fine — the fastest install sanity check |
| `Plot_Basic.py`, `trial.py` | Matplotlib slider experiments on random data | both crash |
| `trial_copy.py`, `Horizontal_Bar_Plot.py` | Generic slider / PyQt5 scroll demos on random data | no game theory in either |

## How to run it (after the quick win in `todo.md`)

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install axelrod matplotlib numpy && pip freeze > requirements.txt
cd GameTheoryIMATMT && python Bayes_Player.py
```

`Bayes_Player.py` writes to `results/` relative to the working directory, so it must
be run from inside `GameTheoryIMATMT/`.

## Direction

Keep the Bayesian line, archive the LLM/HPC line — it cannot run anywhere you have
access to and its results are mislabelled before they are even saved. One readable
CSV of inferred-vs-true opponent category is the next milestone. See `todo.md`,
including the PARK deadline.
