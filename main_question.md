# Main Question

How can intelligent agents make strong decisions in games and real-world systems where players have asymmetric knowledge, hidden information, uncertain intentions, private strategies, or unequal access to evidence?

## Reference Sub-Questions

### Background: What Is Asymmetric Knowledge?

- What is the difference between asymmetric information, incomplete information, imperfect information, hidden types, hidden actions, and hidden payoffs?
- How do classic examples such as poker, auctions, markets, negotiations, insurance, security games, and repeated prisoner's dilemma expose asymmetric knowledge?
- When does asymmetric knowledge create advantage, mistrust, exploitation, signaling, bluffing, adverse selection, moral hazard, or coordination failure?
- How does a player reason when they know that the opponent may know something they do not?
- What changes when the hidden information is about the opponent's type, goal, resources, payoff function, available moves, or future plan?
- How can repeated interaction reduce uncertainty through observation, reputation, punishment, and learning?

### Tackling Asymmetric Problems

- How should an agent act when it has incomplete knowledge but must still choose a move now?
- What information should the agent try to infer first: opponent type, likely next move, payoff incentives, hidden constraints, or long-term strategy?
- How can an agent decide whether to cooperate, probe, signal, bluff, punish, delay, reveal information, or hide information?
- When is it better to gather more information, and when is it better to exploit the best current belief?
- How can an agent avoid being manipulated by misleading signals or strategic deception?
- How should decisions change when the opponent is rational, boundedly rational, random, adversarial, or learning too?
- What strategies are robust when the agent's model of the opponent is probably wrong?
- How can an agent balance short-term payoff against long-term information gain?
- What should the agent do when multiple explanations fit the same observed behavior?
- How can the agent detect whether the opponent is adapting to its own strategy?

### Existing Methods and What Has Been Done

- How do Bayesian games model players with hidden types and private information?
- How do perfect Bayesian equilibrium, sequential equilibrium, and signaling games handle belief updates after observed actions?
- How do auctions, mechanism design, and contract theory solve problems where participants privately know values, costs, effort, or risk?
- How do repeated games use reputation and history to reduce asymmetric knowledge over time?
- How do partially observable Markov decision processes model hidden state and uncertain observations?
- How do opponent modeling and belief-state tracking help agents act under uncertainty?
- How do poker AI systems handle hidden cards, bluffing, ranges, counterfactual reasoning, and imperfect information?
- How do multi-agent reinforcement learning systems handle non-stationary opponents and private observations?
- How do Axelrod-style tournaments reveal strengths and weaknesses of simple strategies under limited knowledge?
- How can Bayesian AI and LLM-based players be compared against classic strategies in asymmetric-information settings?

### Gaps and Areas to Explore

- How can we build agents that reason well when the opponent is intentionally hiding or distorting information?
- How can an agent learn which information is worth revealing, hiding, or requesting?
- How can strategies stay reliable when opponent behavior changes after the opponent learns about the agent?
- How can an agent distinguish noise, mistakes, deception, and genuine strategy shifts?
- How can belief updates remain useful when the prior categories are incomplete or wrong?
- How can language models be used for strategic reasoning without trusting unsupported explanations?
- Can an LLM help generate hypotheses about hidden opponent goals, while a formal model checks the decisions?
- What experiments would show that an agent handles asymmetric knowledge better than a simple reactive strategy?
- How can asymmetric-knowledge methods transfer from games to real systems such as negotiation, markets, cybersecurity, misinformation, finance, or political strategy?
- What ethical limits are needed when studying bluffing, persuasion, manipulation, and strategic information control?

### Experiment Ideas

- Modify iterated prisoner's dilemma tournaments so players have unequal knowledge about opponent identity, payoff matrix, round count, or past behavior.
- Compare classic Axelrod strategies against Bayesian players that infer hidden opponent types from early moves.
- Test whether an agent should spend early turns probing the opponent or immediately maximize payoff.
- Add noisy observations where players sometimes misread cooperation and defection.
- Test signaling strategies where an agent intentionally cooperates, defects, or randomizes to shape the opponent's beliefs.
- Compare a hand-written Bayesian strategy, a classic strategy, and an LLM-generated strategy under the same asymmetric-information rules.
- Build plots showing belief updates, opponent-type estimates, action choices, payoff, and cooperation rate over time.
- Identify cases where extra information helps, hurts, or causes overconfidence.

## Current Project Materials

- Axelrod library references and guide links.
- Classic plotting and tournament scripts.
- `GameTheoryIMATMT/`: tournament code, Bayesian player experiments, LLM/HPC player code, shell runners, and saved results.
- `GameTheoryIMATMT/HPC/`: transformer-based AI player, tournament runner, config, model loading, plotting, and results utilities.
