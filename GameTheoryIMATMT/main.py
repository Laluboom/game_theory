from HPC.tournament import run_tournament
from HPC.plots import generate_plots

if __name__ == "__main__":
    results = run_tournament()
    generate_plots()
