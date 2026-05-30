import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Generate 240 strategies
all_strategies = axl.strategies
chosen_strategies = [s() for s in all_strategies[:240]]

# Dummy scores for demonstration
scores = np.random.randint(0, 100, 240)

def plot_scores(num_strategies):
    fig, ax = plt.subplots(figsize=(8, 10))  # Adjust figure size for better visibility

    # Plot the bars for each strategy
    for i in range(num_strategies):
        ax.barh(i, scores[i], color='skyblue')
        ax.text(scores[i] + 1, i, str(chosen_strategies[i]), verticalalignment='center')

    # Set y-axis ticks and labels
    ax.set_yticks(np.arange(num_strategies))
    ax.set_yticklabels(str(strategy) for strategy in chosen_strategies[:num_strategies])

    # Set labels and title
    ax.set_xlabel('Scores', fontsize=14)
    ax.set_ylabel('Strategies', fontsize=14)
    ax.set_title("Prisoner's Dilemma - Strategies", fontsize=16)

    # Invert y-axis to have the strategies listed from top to bottom
    ax.invert_yaxis()

num_strategies_slider = Slider(chosen_strategies, valmin=1, valmax=len(chosen_strategies), label='Number of Strategies:')
num_strategies_slider.on_changed(plot_scores)

plt.show()