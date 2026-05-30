import csv
import os

RESULTS_DIR = "results/Fourth results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "tournament_results.csv")

# Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)
    
def save_results(results):
    with open(RESULTS_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Correct CSV header
        writer.writerow(["Strategy", "Opponent", "Match History"])
        
        # Write each result entry correctly
        for result in results:
            strategy_name = result["Strategy"]
            opponent_name = result["Opponent"]
            match_history = "; ".join(f"Turn {turn}: {p1} vs {p2}" for turn, p1, p2 in result["Match History"])
            
            writer.writerow([strategy_name, opponent_name, match_history])
