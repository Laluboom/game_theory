# game_theory — Reference

## What this is

Two unrelated things in one repo:

1. **A research question** (`main_question.md`) — how should agents decide under
   asymmetric knowledge (hidden types, private payoffs, uncertain intentions)?
   Written recently, specific, and genuinely worth pursuing.
2. **Old coursework** (`GameTheoryIMATMT/`, root `*.py`) — Iterated Prisoner's
   Dilemma experiments built on the [Axelrod](https://github.com/Axelrod-Python/Axelrod)
   library, written for a City, University of London HPC account (`adgz422`).
   Committed once on 2026-05-30 and untouched since.

The overlap between the two is exactly one file: `GameTheoryIMATMT/Bayes_Player.py`,
a player that maintains a prior over opponent "strategy categories" and updates it
each round. That is the research question in code form. Everything else is scaffolding
around it or dead weight.

## Current state: nothing in this repo runs

- No `requirements.txt`, no `README`, no environment manifest.
- `axelrod` is not installed in the ambient Python — every file fails at `import axelrod`.
- `.gitignore` excludes `GameTheoryIMATMT/results/`, so every saved result, CSV and
  plot referenced by the code is absent. `Strat_per_strat.py:29` reads
  `results/Strategy_Guide_results.json`, which does not exist.
- `GameTheoryIMATMT/.python-version` says `AIRun` — a pyenv virtualenv name that
  only ever existed on the university cluster.

## Layout

| Path | What it does | Works? |
|---|---|---|
| `GameTheoryIMATMT/Bayes_Player.py` | Bayesian opponent-type inference vs all strategies | core idea; belief update has a real bug (see `todo.md`) |
| `GameTheoryIMATMT/Initial_match.py` | Round-robin over all strategies, CSV + batched bar charts | `NameError` at line 81; 240×240 matches |
| `GameTheoryIMATMT/HPC/` | Llama-3-8B "AI player" + tournament runner | needs cluster GPUs, a proxy, and a local model path |
| `GameTheoryIMATMT/Strat_per_strat.py` | LLM critiques strategy descriptions | infinite `while True` (line 70) — exit condition can never fire |
| `GameTheoryIMATMT/*.sh` | SLURM batch scripts | hardcoded to `/users/adgz422` |
| `Game_theory.py` | Full tournament + slider bar chart | runs (slowly); `CustomStrategy` is defined but never entered |
| `Plot_Basic.py`, `trial.py`, `trial_copy.py` | Matplotlib slider experiments on random data | `Plot_Basic.py` and `trial.py` crash |
| `Horizontal_Bar_Plot.py` | PyQt5 scrollable-plot demo on random data; no bars, no game theory | runs, if you install PyQt5 |

## How to run it (once the quick win in `todo.md` is done)

```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt          # axelrod, matplotlib, numpy — not yet written
cd GameTheoryIMATMT && python Bayes_Player.py
```

Note `Bayes_Player.py` writes to `results/` relative to the *current working
directory*, so it must be run from inside `GameTheoryIMATMT/`.

## Direction

Keep the Bayesian line, drop the LLM/HPC line. The HPC code cannot run anywhere
you currently have access to, and its results are mislabelled at the source
(`HPC/tournament.py:22-24`). See `todo.md`.
