# TODO — game_theory

Verdict from the 2026-09-21 review: **REVIVE, narrowly.** The Bayesian
opponent-type player is a real experiment that is ~80% written. The LLM/HPC half
is dead and should be retired rather than maintained. These tasks are ordered so
that finishing 1–3 gives you one result you could actually write down.

---

## 1. [QUICK WIN ~15min] Make the repo runnable at all

Nothing here runs. There is no `requirements.txt`, no README, and `axelrod` is not
installed anywhere on this machine — every single `.py` file dies on line 1.
`GameTheoryIMATMT/.python-version` contains `AIRun`, a pyenv virtualenv that only
existed on the City HPC cluster.

Write `requirements.txt` with pinned `axelrod`, `matplotlib`, `numpy`. Delete the
three stale pyenv markers (`.python-version`, `.3.11.11`, `.python3.11.11`).
Confirm with:

```sh
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -c "import axelrod as axl; print(len(axl.strategies), 'strategies')"
```

Why it matters: this is the only thing standing between "a folder of files" and
"a thing I can poke at". Everything below assumes it is done.

---

## 2. [BUG] The Bayesian player infers the opponent's type from its own moves

`GameTheoryIMATMT/Bayes_Player.py` is the whole point of the repo, and its belief
update reads `self.history` where it means `opponent.history`:

- `:30` — `cooperation_ratio` is computed over **the agent's own** actions, then
  used at `:40` as evidence for `MajorityBased`.
- `:46` — `recent_defections` counts the agent's own defections as evidence for
  `ThresholdBased`. It also uses `self.history[-5:]` but guards with
  `len(self.history) > 5`, so it silently reports `0` for the first six turns.
- `:80`, `:86` — the action choice branches on the agent's own history too.

`:34` and `:42` are the only lines where `self.history` is correct (they are
checking whether the opponent mirrors *you*). `update_beliefs` receives
`opponent_move` but never sees the opponent's full history — pass the opponent in.

Why it matters: right now the posterior is mostly a function of what the agent
already decided to do, which makes it self-confirming. Any result you get from
this file before fixing it is meaningless.

---

## 3. [DESIGN] Make the experiment answer its own question

`Bayes_Player.py:99-104` records only scores. So you can run it and still not know
the one thing you care about: **did it identify the opponent correctly?**

In one session:

- Record `max(self.priors, key=self.priors.get)` per match alongside the score.
- Add a ground-truth column. `self.strategy_categories` (`:13-22`) already lists
  opponent names per category but is **never read anywhere in the file** — wire it
  up as the answer key. Note its names are invented (`"GrimTrigger"`,
  `"Forgiver"`, `"Stochastic_TitForTat"`) and do not match real Axelrod class
  names; reconcile them against `axl.strategies`.
- Add a TitForTat baseline playing the same opponents, so "Bayesian scored 31"
  becomes "Bayesian scored 31 where TitForTat scored 34".
- Cut `:94` from `axl.all_strategies` (~240) down to the ~20 named opponents you
  actually have categories for. Faster loop, interpretable table.

Working means: one CSV with columns `opponent, true_category, inferred_category,
bayes_score, titfortat_score`, and one chart. That is a result.

---

## 4. [CHORE] Retire the LLM / HPC branch instead of maintaining it

`GameTheoryIMATMT/HPC/` and `Strat_per_strat.py` cannot run anywhere you have
access to, and are broken independently of that:

- `HPC/tournament.py:22-24` stores `"Strategy": opponent.name` but
  `"Opponent": scores[0]` — a *score* under a key named Opponent, and
  `strategy.name` is never recorded. `HPC/plots.py:15` then does
  `results[row[0]] = int(row[1])`, keying a dict by opponent name across a
  240×240 loop, so every chart plots only the last match per name.
- `HPC/ai_player.py:48` takes the last 50 **characters** of decoded model output
  as the move sequence; `:53` maps anything that isn't `"C"` to defect, so
  whitespace and punctuation become defections. The "LLM player" is a defect-heavy
  random player.
- `Strat_per_strat.py:70-77` loops `while True` until `ai_response == "✅"`, but
  the prompt asks for `Y✅` and the response is the full decoded prompt+completion.
  The condition can never be true. `:74` would then raise `TypeError` anyway —
  `strategies` is a list being indexed by strategy name.
- `config.py:5` hardcodes `hpc-proxy00.city.ac.uk`; `*.sh` hardcode
  `/users/adgz422`.

Move `HPC/`, `Strat_per_strat.py` and the `*.sh` runners into `archive/` with a
one-paragraph note on what they were for. Keep the SLURM scripts as templates if
you ever get cluster access again — just stop pretending they are live code.

---

## 5. [BUG] Clear out the crashing root-level plot scripts

Five files at the repo root, four of which are slider/scroll plot demos over
random data and contain no game theory at all:

- `Plot_Basic.py:33` — `Slider(chosen_strategies, ...)` passes a list where an
  Axes is required. Crashes. `plot_scores` at `:13` also creates a new figure per
  slider callback.
- `trial.py:67` — `ax.set_size_inches(8, 6)`; that is a `Figure` method, not an
  `Axes` method. `AttributeError` every run.
- `trial_copy.py` — a generic matplotlib slider demo, 35 lines, random data.
- `Horizontal_Bar_Plot.py` — a PyQt5 scrollable-plot widget plotting
  `np.cumsum(np.random.randn(...))` at `:83`. No bars, horizontal or otherwise,
  and it drags `PyQt5` into the dependency list for a demo. It also builds a
  second `QApplication` at `:75` after `__init__` already made one at `:18-21`.
- `Game_theory.py:14-23` — `CustomStrategy.strategy` falls off the end and returns
  `None` for the first two rounds, and the class is never added to the tournament
  (`:28` uses `axl.strategies`; `First_game_strategies` at `:29` is unused).

Keep `Game_theory.py`, delete the other four, and either fix `CustomStrategy`
(return `C` when history is short) and enter it into the tournament, or delete it
too. This also keeps `PyQt5` out of the `requirements.txt` you write in task 1.
