import axelrod as axl
import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

# Get all strategies
strategies = axl.all_strategies
match_scores = []
total_scores = defaultdict(int)  # Store total accumulated scores

# Play matches and collect scores
for strategy_cls in strategies:
    for opponent_cls in strategies:
        strategy = strategy_cls()
        opponent = opponent_cls()

        match = axl.Match((strategy, opponent), turns=20)
        match.play()
        scores = match.final_score()

        match_scores.append([strategy.name, scores[0], opponent.name, scores[1]])

        # Accumulate total scores for each strategy
        total_scores[strategy.name] += scores[0]
        total_scores[opponent.name] += scores[1]

# Ensure results directory exists
os.makedirs("results/Initial", exist_ok=True)

# Sort scores by first strategy's score
sorted_scores = sorted(match_scores, key=lambda x: x[1], reverse=True)

# Sort total scores for CSV entry
sorted_total_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)

# Save results to CSV
csv_file = "results/Initial/Initial_match.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    # Write Header
    writer.writerow(["Strategy", "Score", "Opponent", "Opponent Score"])  
    
    # Write Accumulated Scores on the 3rd and 4th rows
    writer.writerow(["Total Scores"] + [""] * 3)  
    for strat, score in sorted_total_scores:
        writer.writerow([strat, score, "", ""])  

    writer.writerow(["Match Details"] + [""] * 3)  # Separate section
    writer.writerows(sorted_scores)  # Write actual match results

print(f"Results saved to {csv_file}")

# Extract strategy names and scores for plotting
strategy_names = [s[0] for s in sorted_total_scores]
scores = [s[1] for s in sorted_total_scores]

def plot_results(strategy_names, scores, batch_size=20, output_dir="results/Initial"):
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

    num_batches = (len(strategy_names) + batch_size - 1) // batch_size  # Calculate the number of batches

    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size

        plt.figure(figsize=(12, 6))
        plt.barh(strategy_names[start:end], scores[start:end], color="blue")
        plt.xlabel("Total Accumulated Score")
        plt.ylabel("Strategy")
        plt.title(f"Total Scores of Strategies (Batch {i+1})")
        plt.gca().invert_yaxis()  # Highest scores at the top

        # Save each batch separately
        plot_file = os.path.join(output_dir, f"score_plot_batch_{i+1}.png")
        plt.savefig(plot_file, bbox_inches="tight", dpi=300)
        plt.close()

plot_results(strategy_names, scores)
plot_file = os.path.join("results/Initial", f"score_plot_batch_{i+1}.png")
print(f"Score plot saved to {plot_file}")

