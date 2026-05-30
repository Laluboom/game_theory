import axelrod as axl
import numpy as np
import os
import json
import csv

class BayesianAI(axl.Player):
    """AI Player using Bayesian updates & Perfect Bayesian Equilibrium strategies"""
    name = "Bayesian Equilibrium AI"

    def __init__(self):
        super().__init__()
        self.strategy_categories = {
            "TitForTat": ["TitForTat", "AdaptiveTitForTat", "AntiTitForTat", "SpitefulTitForTat"],
            "DefectionBased": ["AlwaysDefect", "Grudger", "HardMajority", "BackStabber"],
            "CooperationBased": ["AlwaysCooperate", "SoftMajority", "Forgiver"],
            "Randomized": ["Random", "Stochastic_TitForTat"],
            "MajorityBased": ["HardMajority", "SoftMajority", "WinStayLoseShift"],
            "PunishmentBased": ["GrimTrigger", "Joss", "TrickyDefector"],
            "Forgiving": ["ForgivingTitForTat", "ContriteTitForTat", "FriendlyGrudger"],
            "ThresholdBased": ["WorseAndWorse", "FoolMeOnce", "RiskyCooperator"]
        }

        self.priors = {category: 1 / len(self.strategy_categories) for category in self.strategy_categories}
        self.turn = 0

    def update_beliefs(self, opponent_move):
        """Bayesian belief update based on observed opponent move."""
        likelihoods = {}
        cooperation_ratio = sum(1 for action in self.history if action == axl.Action.C) / len(self.history) if self.history else 0.5

        for category in self.strategy_categories:
            if category == "TitForTat":
                likelihoods[category] = 0.9 if (self.history and self.history[-1] == opponent_move) else 0.1
            elif category == "DefectionBased":
                likelihoods[category] = 0.1 if opponent_move == axl.Action.C else 0.9
            elif category == "CooperationBased":
                likelihoods[category] = 0.9 if opponent_move == axl.Action.C else 0.1
            elif category == "MajorityBased":
                likelihoods[category] = 0.8 if cooperation_ratio > 0.5 else 0.2
            elif category == "PunishmentBased":
                likelihoods[category] = 0.9 if opponent_move == axl.Action.D and self.history and self.history[-1] == axl.Action.D else 0.1
            elif category == "Forgiving":
                likelihoods[category] = 0.8 if opponent_move == axl.Action.C else 0.2
            elif category == "ThresholdBased":
                recent_defections = sum(1 for action in self.history[-5:] if action == axl.Action.D) if len(self.history) > 5 else 0
                likelihoods[category] = 0.7 if recent_defections > 2 else 0.3
            elif category == "Randomized":
                likelihoods[category] = 0.5
            else:
                likelihoods[category] = 0.5

        total_prob = sum(self.priors[cat] * likelihoods[cat] for cat in self.priors)
        if total_prob == 0:  
            self.priors = {category: 1 / len(self.strategy_categories) for category in self.strategy_categories}  # Reset priors
        else:
            for category in self.priors:
                self.priors[category] = (self.priors[category] * likelihoods[category]) / total_prob

    def strategy(self, opponent):
        """Decide move using Bayesian Equilibrium logic."""
        self.turn += 1
        if not opponent.history:
            return axl.Action.C  # Cooperate initially

        opponent_move = opponent.history[-1]
        self.update_beliefs(opponent_move)

        predicted_category = max(self.priors, key=self.priors.get)

        if predicted_category == "DefectionBased":
            return axl.Action.D
        elif predicted_category == "TitForTat":
            return opponent_move
        elif predicted_category == "PunishmentBased":
            return axl.Action.D
        elif predicted_category == "Forgiving":
            return axl.Action.C
        elif predicted_category == "ThresholdBased":
            return axl.Action.D if sum(1 for action in self.history if action == axl.Action.D) > 2 else axl.Action.C
        elif predicted_category == "Randomized":
            return np.random.choice([axl.Action.C, axl.Action.D])
        elif predicted_category == "CooperationBased":
            return axl.Action.C
        elif predicted_category == "MajorityBased":
            return axl.Action.C if sum(1 for action in self.history if action == axl.Action.C) >= sum(1 for action in self.history if action == axl.Action.D) else axl.Action.D
        else:
            return axl.Action.D

# Run Bayesian AI against all strategies
Turns = 10
results = []

for opponent_strategy in axl.all_strategies:
    players = [opponent_strategy(), BayesianAI()]
    match = axl.Match(players, turns=Turns)
    match.play()
    scores = match.final_score()
    results.append({
        "opponent": opponent_strategy.__name__,
        "description": opponent_strategy.__doc__,
        "BayesianAI_score": int(scores[1]),  # BayesianAI is player 2
        "Opponent_score": int(scores[0])    # Opponent is player 1
    })

# Function to save results
def save_results(results):
    os.makedirs("results/Initial", exist_ok=True)
    with open("results/Initial/BayesPlayer.json", 'w') as file:
        json.dump(results, file, indent=4)

def save_results_csv(results):
    os.makedirs("results/Initial", exist_ok=True)
    file_path = "results/Initial/BayesPlayer.csv"
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Opponent", "BayesianAI Score", "Opponent Score"])
        for row in results:
            writer.writerow([row["opponent"], row["BayesianAI_score"], row["Opponent_score"]])

save_results_csv(results)
save_results(results)

