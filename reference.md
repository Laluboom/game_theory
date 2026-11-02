# game_theory — Reference

**Status 2026-11-02: PARKED.** Not retired — see "Why parked" below. The idea is sound;
the machine cannot run Python packages.

## What this is

Two unrelated things in one folder:

1. **A research question** (`main_question.md`) — how should an agent decide under
   asymmetric knowledge: hidden types, private payoffs, uncertain intentions? 72 lines,
   specific, with its own experiment list. Genuinely worth pursuing.
2. **Finished coursework** (`GameTheoryIMATMT/`, root `*.py`) — Iterated Prisoner's
   Dilemma experiments on the [Axelrod](https://github.com/Axelrod-Python/Axelrod)
   library, written against a City, University of London HPC account (`adgz422`).
   One commit, 2026-05-30. **No source change since** — the two commits after it are
   review notes, and the third deleted three dead pyenv marker files.

They overlap in exactly one file: `GameTheoryIMATMT/Bayes_Player.py`, a player holding a
prior over opponent "strategy categories" and updating it each round. That is the
research question in code, about 80% written. Everything else is scaffolding or dead
weight.

## Why parked: nothing here can run, and not for a repo-local reason

Verified this review, not inferred:

```
python3 --version                → Python 3.14.4
python3 -c "import ensurepip"    → ModuleNotFoundError
python3 -c "import axelrod"      → ModuleNotFoundError
```

No `ensurepip` in the stdlib means `python3 -m venv` **cannot bootstrap pip**. There is
no `requirements.txt` and no venv, so every `.py` here dies on line 1 at
`import axelrod`. Three consecutive reviews proposed "create a venv, pip install
axelrod" as a 15-minute quick win; the 2026-10-02 doer run burned a session proving it
impossible. Also note the ambient Python is **3.14** while this repo's own deleted pyenv
markers named `3.11.11` — axelrod may well have no 3.14 wheels.

`.gitignore` excludes `GameTheoryIMATMT/results/`, so every CSV, JSON and plot the code
reads or writes is absent from the repo too.

## Layout

| Path | What it does | Works? |
|---|---|---|
| `GameTheoryIMATMT/Bayes_Player.py` | Bayesian opponent-type inference, 10 turns vs ~240 strategies | the core idea; belief update reads its own history (`:30`, `:46`), `:34` off by one, `strategy_categories` never read |
| `GameTheoryIMATMT/Initial_match.py` | Hand-rolled round-robin, CSV + batched bar charts | `NameError: i` at `:81` after all ~57,600 matches; `:25-26` double-counts every pair. `axl.Tournament` already does this, in parallel |
| `GameTheoryIMATMT/HPC/` | Llama-3-8B "AI player" + tournament runner | needs cluster GPUs, City proxy, local model path; moves parsed as raw characters (`ai_player.py:48`), columns mislabelled at source |
| `GameTheoryIMATMT/Strat_per_strat.py` | LLM critiques strategy descriptions | `while True` at `:70` whose exit can never fire |
| `GameTheoryIMATMT/*.sh` | SLURM batch scripts | all four copy-pasted from an ANSYS Fluent CFD template; hardcoded to `/users/adgz422` |
| `GameTheoryIMATMT/trial/trial.py` | — | one line, `print("Hello World!")` |
| `Game_theory.py` | Full tournament + slider bar chart | would run (slowly); `CustomStrategy` returns `None` for rounds 1–2 and is never entered |
| `Input_match.py` | Human vs TitForTat, 3 turns | 5 lines, fine — the fastest install sanity check |
| `Plot_Basic.py`, `trial.py` | Matplotlib slider experiments on random data | both crash |
| `trial_copy.py`, `Horizontal_Bar_Plot.py` | Generic slider / PyQt5 scroll demos on random data | no game theory in either |

## How to run it

You cannot, yet. Once a working toolchain exists (`todo.md` task 1):

```sh
uv venv --python 3.11 && uv pip install axelrod matplotlib numpy
cd GameTheoryIMATMT && python Bayes_Player.py      # ~240 matches, 10 turns each
```

`Bayes_Player.py` writes to `results/` **relative to the working directory**, so it must
be run from inside `GameTheoryIMATMT/`.

## Direction

Keep the Bayesian line, archive the LLM/HPC line — it cannot run anywhere you have
access to and its results are mislabelled before they are even saved. One readable CSV of
inferred-vs-true opponent category is still the next milestone. **Unpark condition: `pip
install axelrod` succeeds on this machine.** Nothing else is in the way.
