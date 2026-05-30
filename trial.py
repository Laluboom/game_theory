import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Generate 240 strategies
all_strategies = axl.strategies
chosen_strategies = [s() for s in all_strategies[:240]]

# Dummy scores for demonstration
scores = np.random.randint(0, 100, 240)

# Initialize global figure and axes with a larger figure size
fig, ax = plt.subplots(figsize=(8, 6))  # Adjust width and height for the initial figure size

# Define the plot function to display scores based on the starting index of strategies
def plot_scores(start_index):
    ax.clear()  # Clear previous plot

    # Calculate the ending index based on the starting index and number of strategies to display
    end_index = start_index + 20

    # Sort the strategies and scores based on scores in descending order
    sorted_indices = np.argsort(scores)[::-1]  # Get indices to sort scores in descending order
    sorted_strategies = [chosen_strategies[i] for i in sorted_indices]
    sorted_scores = scores[sorted_indices]

    # Plot the bars for each strategy within the specified range
    for i in range(start_index, end_index):
        ax.barh(i - start_index, sorted_scores[i], color='skyblue')
        ax.text(sorted_scores[i] + 1, i - start_index, str(sorted_strategies[i]), verticalalignment='center')

    # Set y-axis ticks and labels for the displayed strategies
    ax.set_yticks(np.arange(20))
    ax.set_yticklabels(str(strategy) for strategy in sorted_strategies[start_index:end_index])

    # Set labels and title
    ax.set_xlabel('Scores', fontsize=12)  # Adjust font size for axis labels
    ax.set_ylabel('Strategies', fontsize=12)  # Adjust font size for axis labels
    ax.set_title("Prisoner's Dilemma - Strategies", fontsize=14)  # Adjust font size for title

    # Invert y-axis to have the strategies listed from top to bottom
    ax.invert_yaxis()
    
    # Adjust subplot parameters to shift the graph upwards
    # ax.subplots_adjust(top=0.95)  # Increase top margin

    # Update the plot
    plt.draw()

# Create initial plot with the first 20 strategies sorted by scores
plot_scores(0)

# Create a slider for shifting the displayed strategies
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
num_strategies_slider = Slider(slider_ax, 'Shift Strategies', 0, len(chosen_strategies) - 20, valinit=0, valstep=1)

# Define the update function for the slider
def update(val):
    start_index = int(val)
    plot_scores(start_index)

# Connect the slider to the update function
num_strategies_slider.on_changed(update)

# Set the figure size (in inches) independent of the window size
ax.set_size_inches(8, 6)  # Set the figure size to 10x12 inches

# Display the plot
plt.show()
