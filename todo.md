# TODO — game_theory

Verdict 2026-11-02: **PARK.** The 2026-10-02 review set an explicit gate — "if tasks 1
and 2 have not happened by ~2026-10-12, the honest call is PARK." It is now three weeks
past that date. Task 1 was attempted on 2026-10-02 and **failed for a reason nobody
could have fixed from inside this repo**; task 2 was never started. The gate fires.

This is not a judgment on the idea. `main_question.md` is a real research agenda and
`Bayes_Player.py` is roughly 80% of the first experiment. It is a judgment on the
*prerequisite*, which is now diagnosed precisely instead of re-proposed a fourth time:

```
$ python3 --version                      → Python 3.14.4
$ python3 -c "import ensurepip"          → ModuleNotFoundError: No module named 'ensurepip'
$ python3 -c "import axelrod"            → ModuleNotFoundError: No module named 'axelrod'
```

No `ensurepip` means `python3 -m venv` **cannot bootstrap pip at all** — it is not a
sandbox permission quirk, the stdlib module is simply absent. Three consecutive reviews
proposed "create a venv, pip install axelrod" as the 15-minute quick win. It was never a
15-minute task on this machine; it was impossible. Task 1 below is the real blocker, and
it does not belong to this repo.

**Unpark when:** `pip install axelrod` succeeds on this machine. That is the whole
condition. At that point tasks 2–4 of the 2026-10-02 list are still correct and still
worth doing — they are preserved in git history at `55cc105` and summarised in task 4.

---

## 1. [CHORE] Fix the Python toolchain — this is the actual blocker, and it is not local

**File this in `_agents/TODO.md`, not here.** It blocks every Python repo in the fleet,
not just this one: any doer run that needs a third-party package dies the same way, and
the 2026-10-02 run burned a full session discovering that.

Two things are needed, and the second is the one that gets missed:

- **A pip that exists.** Either `sudo apt-get install python3-venv` (the Debian package
  that ships `ensurepip`), or drop a `uv` binary on the box — `uv` bundles its own
  Python downloads and sidesteps the system interpreter entirely, which is the lower-risk
  fix given the next point.
- **An interpreter axelrod actually supports.** The ambient `python3` is **3.14**.
  Axelrod is a slow-moving project and this repo's own deleted pyenv markers named
  `3.11.11` — the original coursework ran on 3.11. Do not assume `pip install axelrod`
  will resolve on 3.14; verify, and if it does not, pin 3.11 or 3.12 (`uv python install
  3.11` makes this one line). **Confirming which Python versions axelrod has wheels for
  is the first five minutes of this task**, not an afterthought.

Why it matters: three reviews have now ranked a task first that could not be executed.
Until this is fixed, every future `game_theory` task list is fiction.

---

## 2. `[QUICK WIN ~15min]` [CHORE] Delete the four dead plot scratch files

Deliberately chosen because it needs **no Python at all** — it is `git rm` and nothing
else, so unlike the last three quick wins it cannot be blocked by task 1. All four are
root-level, none are imported by anything, and all four operate on random dummy data:

- `Plot_Basic.py` — `:33` passes `chosen_strategies` (a list of `Player` objects) where
  `Slider` requires an `Axes`. `TypeError` on import. Scores at `:11` are
  `np.random.randint` dummies.
- `trial.py` — `:67` calls `ax.set_size_inches(8, 6)`, a `Figure` method, on an `Axes`.
  `AttributeError` every run, before `plt.show()`. Scores at `:11` are dummies too.
- `trial_copy.py` — a generic matplotlib slider demo over `np.random.rand(37)`. Does not
  import axelrod. No game theory in it.
- `Horizontal_Bar_Plot.py` — a verbatim StackOverflow PyQt5 scroll-plot demo plotting
  `np.cumsum(np.random.randn(...))` at `:83`. Despite the filename there is no bar chart,
  and it builds a second `QApplication` at `:75` after `__init__` already made one at
  `:18-21`. Keeping it drags PyQt5 into the dependency list for nothing.

Keep `Input_match.py` — five lines, human vs TitForTat, and the fastest sanity check that
Axelrod works once task 1 lands. Keep `Game_theory.py`, with its known wart recorded in
`reference.md` rather than fixed now.

---

## 3. [DOCS] Archive the LLM/HPC half outright — the one decision that survives PARK

This was task 3 on the last two lists and it is the part that should happen *regardless*
of whether the repo ever unparks, because it is the only subtraction that makes the
remaining repo legible. `HPC/`, `Strat_per_strat.py` and the four `*.sh` runners need
cluster GPUs, a City proxy (`HPC/config.py:5`), and `../archive/Llama3-8B`. None exist
and none will. They are also broken on their own terms, so nothing is lost:

- `HPC/ai_player.py:48` takes the last 50 **characters** of decoded output as the move
  sequence — still including the echoed prompt, since the input ids are never stripped —
  and `:53` maps anything that is not literally `"C"` to Defect. The headline "LLM player"
  is a defect-heavy random player measuring parsing noise.
- `HPC/tournament.py:21-25` writes `"Strategy": opponent.name` and `"Opponent":
  scores[0]` — a score stored under a key named Opponent — and never records
  `strategy.name` or `scores[1]`. `HPC/plots.py:15` then keys a dict by that name across
  the 240×240 loop, so every chart shows only the last match per name.
- `Strat_per_strat.py:70-77` loops `while True` until `ai_response == "✅"` while the
  prompt at `:43` asks for `Y✅`; the condition can never fire. `:74` would raise
  `TypeError` anyway (`strategies` is a list, indexed there by strategy name), and `:20`
  passes `device_map="none"`, not a valid value. It dies at `:29` first regardless,
  reading a `results/` path that `.gitignore` excludes.
- All four `*.sh` are copy-pasted from an **ANSYS Fluent CFD** template — verified, every
  one carries `module load fluent` and `--licenses=anshpc:176` on a PyTorch job, plus
  `#SBATCH -D /users/adgz422`. They would queue for licenses they never use.

Move the lot to `archive/` with a three-line note saying what it was and why it stopped.
Do not fix any of it.

---

## 4. [DESIGN] Write the experiment design down, on paper, before unparking

~30 minutes, needs no interpreter, and it is the one task that makes PARK cheap to
reverse. The 2026-10-02 review worked out the full design and it is currently spread
across a TODO that this file just replaced. Capture it in `main_question.md` under a
"First experiment" heading so the next session is pure implementation:

- The CSV schema that defines "working": `opponent, true_category, inferred_category,
  bayes_score, titfortat_score` — eight rows, readable in one glance.
- The eight opponents, **by real Axelrod class name**. `Bayes_Player.py:13-22` invents
  names that do not exist in the library (`GrimTrigger`, `Forgiver`,
  `Stochastic_TitForTat`, `ForgivingTitForTat`, `FriendlyGrudger`, `RiskyCooperator`;
  `Grudger` is the real one). Resolving those names needs library docs, not a working
  install — do it now.
- The three code fixes, already located: `:30`/`:46` compute `cooperation_ratio` and
  `recent_defections` over `self.history`, the agent's **own** moves, then use them at
  `:40`/`:47` as evidence about the opponent; `:34` is off by one (a TitForTat opponent's
  move at round *t−1* copies your move at round *t−2*, so compare against
  `self.history[-2]`, guarded for `len >= 2`); `:91` `Turns = 10` gives nine updates,
  which with 0.1/0.9 likelihoods and no floor at `:53-58` locks priors near zero before
  converging — raise to 200.
- That `strategy_categories` is currently **never read** — only its keys and `len()`.
  Wiring it up as the answer key is the point of the experiment.
