import matplotlib.pyplot as plt
import csv

RESULTS_FILE = "results/Fourth results/tournament_results.csv"

def generate_plots():
    """Generate bar charts and save as PNGs, with 20 games per image."""
    results = {}

    # Read CSV results
    with open(RESULTS_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            results[row[0]] = int(row[1])

    # Sort results in descending order
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    # Split into chunks of 20
    chunk_size = 20
    chunks = [list(sorted_results.items())[i:i + chunk_size] for i in range(0, len(sorted_results), chunk_size)]

    # Generate plots
    for idx, chunk in enumerate(chunks):
        plt.figure(figsize=(12, 6))
        
        opponents = [x[0] for x in chunk]
        scores = [x[1] for x in chunk]

        plt.barh(opponents, scores, color='skyblue')
        plt.xlabel("Scores")
        plt.ylabel("Opponent Strategies")
        plt.title(f"Axelrod Tournament Results (Games {idx * chunk_size + 1}-{(idx + 1) * chunk_size})")
        plt.gca().invert_yaxis()

        filename = f"results/Fourth results/GameTheoryPlay_{idx+1}.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close()

    print("✅ PNGs saved successfully!")
