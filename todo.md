# TODO — game_theory

Verdict 2026-10-02: **REVIVE, with a deadline.** Second review in a row with this
verdict. The 2026-09-21 TODO was accurate and nothing was done — the only commit
since is the review commit itself. So this list is deliberately shorter: two tasks
produce a result, and everything else is deleted from the plan.

**The gate:** if tasks 1 and 2 have not happened by the next review (~2026-10-12),
the honest call is **PARK**. Not because the idea is bad — `main_question.md` is a
real research agenda — but because a third unactioned REVIVE is just bookkeeping.

---

## 1. `[DONE 2026-10-02]` Make one file run

Still true, 11 days later: `axelrod` is not installed, there is no `requirements.txt`,
no venv, and the system `python3` (3.14.4) has no `pip`. Every `.py` in this repo
dies on line 1. This is the entire reason nothing above it got done.

```sh
cd /home/laluboom/repos/04_early_stage_and_ideas/game_theory
python3 -m venv .venv && . .venv/bin/activate
pip install axelrod matplotlib numpy && pip freeze > requirements.txt
cd GameTheoryIMATMT && python Bayes_Player.py      # ~240 matches, 10 turns each
```

Then delete the three dead pyenv markers — `.python-version` (`AIRun`),
`.3.11.11` and `.python3.11.11` (both `myenv`). They name virtualenvs that only
existed on the City cluster account and actively mislead any tool that reads them.

Why it matters: you cannot form an opinion about the Bayesian player until you have
watched it play once. Everything below assumes this is done.

---

## 2. [DESIGN] One session, one result — then stop

This is the whole repo. Do not touch tasks 3–4 until this CSV exists.

`Bayes_Player.py` scores itself but never records **whether it identified the
opponent**, which is the only question `main_question.md` actually asks. Fix that
and the belief bug together, because the result is worthless without both:

- **`:30`, `:46`** — `cooperation_ratio` and `recent_defections` are computed over
  `self.history`, the agent's *own* moves, then used at `:40`/`:47` as evidence about
  the *opponent's* type. Pass `opponent` into `update_beliefs` and read
  `opponent.history`. (`:46` also guards `len(self.history) > 5` around a `[-5:]`
  slice, so it reports `0` for the first six turns.)
- **`:34`** — off-by-one, and the prior review got this one wrong by calling it
  correct. A TitForTat opponent's move at round *t−1* copies your move at round
  *t−2*, so this must compare `opponent_move` against `self.history[-2]`, not
  `[-1]`. As written it tests whether you both happened to play the same thing in
  the same round — which is near-50/50 noise, so the TitForTat hypothesis never
  gets real evidence. Guard for `len(self.history) >= 2`.
- **`:91`** — `Turns = 10` gives nine belief updates. With likelihoods pinned at
  0.1/0.9 and no floor (`:53-58`), that is not enough to converge and more than
  enough to lock a prior near zero permanently. Raise to 200.
- **`:94`** — cut `axl.all_strategies` (~240) to the ~8 opponents you have real
  categories for, chosen from `axl.strategies` by their actual class names. The
  names in `self.strategy_categories` (`:13-22`) are invented — `GrimTrigger`,
  `Forgiver`, `Stochastic_TitForTat` do not exist in Axelrod (`Grudger` does) — and
  that dict is **never read anywhere in the file**. Wire it up as the answer key.
- Add `axl.TitForTat()` playing the same opponents, so "Bayesian scored 31" becomes
  "Bayesian scored 31 where TitForTat scored 34".

**Working means:** one CSV, `opponent, true_category, inferred_category,
bayes_score, titfortat_score`, eight rows you can read in one glance. If the
inferred column is mostly wrong, that is still a result — write it down.

---

## 3. [CHORE] Archive the LLM/HPC half, do not fix it

`HPC/`, `Strat_per_strat.py` and the four `*.sh` runners need cluster GPUs, a City
proxy (`HPC/config.py:5`), and `../archive/Llama3-8B`. None exist. They are also
broken on their own terms, so there is nothing to preserve by keeping them live:

- `HPC/ai_player.py:48` takes the last 50 **characters** of decoded output as the
  move sequence — including the echoed prompt, since nothing strips the input ids —
  and `:53` maps anything that isn't `"C"` to defect. The "LLM player" is a
  defect-heavy random player. The repo's headline comparison measures parsing noise.
- `HPC/tournament.py:22-24` writes `"Strategy": opponent.name` and
  `"Opponent": scores[0]` — a score under a key named Opponent — and never records
  `strategy.name` or `scores[1]`. `HPC/plots.py:15` then keys a dict by that name
  across a 240×240 loop, so each chart shows only the last match per name.
- `Strat_per_strat.py:70-77` loops `while True` until `ai_response == "✅"` while the
  prompt asks for `Y✅`; the condition can never fire. `:19` also passes
  `device_map="none"`, which is not a valid value. It dies at `:29` first anyway,
  reading a `results/` file that `.gitignore` excludes.
- All four `*.sh` are copy-pasted from an **ANSYS Fluent CFD** template: every one
  carries `module load fluent` and `--licenses=anshpc:176` on a PyTorch job, plus
  `#SBATCH -D /users/adgz422`. They would queue for licenses they never use.

Move all of it to `archive/` with a short note on what it was for.

---

## 4. [CHORE] Delete the four root-level plot scratch files

`Plot_Basic.py` (`:33` passes a list of Players where `Slider` needs an Axes —
crashes), `trial.py` (`:67` calls `ax.set_size_inches`, a Figure method — crashes),
`trial_copy.py` (generic slider demo, no axelrod), `Horizontal_Bar_Plot.py` (a
verbatim StackOverflow PyQt5 scroll-plot demo over `np.cumsum(np.random.randn(...))`
at `:83` — no bars, no game theory, and it drags PyQt5 into your deps).

Keep `Game_theory.py`, but note `CustomStrategy` (`:14-23`) falls off the end and
returns `None` for the first two rounds and is never entered into the tournament
(`:28` uses `axl.strategies`; `First_game_strategies` at `:29` is unused). Either
give it a `return axl.Action.C` default and add it to the player list, or delete it.

`Input_match.py` is five lines and fine — it is the human-vs-TitForTat REPL and the
fastest way to sanity-check that Axelrod works after task 1.
