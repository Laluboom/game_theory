import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

class CustomStrategy(axl.Player):
    name = "Custom Strategy"
    classifier = {
        "memory_depth": 1,
        "stochastic": False, 
        "makes_use_of": set(),
    }

    def strategy(self, opponent: axl.Player) -> axl.Action:
        if len(self.history) >= 2 and len(opponent.history) >= 2:
            if self.history[0] == opponent.history[0]:
                return axl.Action.C
            elif self.history[0] == opponent.history[1]:
                return axl.Action.C
            elif self.history[1] == opponent.history[1]:
                return axl.Action.D
            else:
                return axl.Action.C

# Tournament setup
repetitions = 1
custom_game = axl.Game(r=3, s=0, t=5, p=1)
all_strategies = [s() for s in axl.strategies]
First_game_strategies = [s() for s in axl.axelrod_first_strategies]
tournament = axl.Tournament(all_strategies, turns=10, game=custom_game, repetitions=repetitions)
results = tournament.play()

# Extract scores and strategy names
total_points = results.scores
sorted_indices = np.argsort([sum(scores) for scores in total_points])[::-1]
sorted_scores = [sum(total_points[i]) for i in sorted_indices]
sorted_strategies = [str(all_strategies[i]) for i in sorted_indices]

# Visualization
fig, ax = plt.subplots(figsize=(12, 6.5))

def plot_scores(start_index):
    """Update the bar chart based on the current slider value."""
    ax.clear()  # Clear the previous plot

    # Calculate the ending index
    end_index = min(start_index + 20, len(sorted_scores))

    # Plot the strategies and scores
    y_positions = np.arange(end_index - start_index)
    ax.barh(y_positions, sorted_scores[start_index:end_index], color='skyblue')
    for i, strategy_name in enumerate(sorted_strategies[start_index:end_index]):
        ax.text(sorted_scores[start_index + i] + 1, i, strategy_name, va='center')

    # Set axis labels, title, and ticks
    ax.set_yticks(y_positions)
    ax.set_yticklabels(sorted_strategies[start_index:end_index])
    ax.set_xlabel('Scores', fontsize=12)
    ax.set_ylabel('Strategies', fontsize=12)
    ax.set_title("Prisoner's Dilemma - Strategies", fontsize=14)
    ax.invert_yaxis()

    # Update the figure
    plt.draw()

# Initial plot
plot_scores(0)

# Add slider
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
num_strategies_slider = Slider(slider_ax, 'Start Index', 0, len(sorted_scores) - 20, valinit=0, valstep=1)

# Update function for slider
def update(val):
    start_index = int(num_strategies_slider.val)
    plot_scores(start_index)

num_strategies_slider.on_changed(update)

# Display the plot
plt.show()
