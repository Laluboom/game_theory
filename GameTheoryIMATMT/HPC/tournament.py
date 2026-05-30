import axelrod as axl
from HPC.ai_player import AIPlayer
from HPC.results import save_results
from HPC.config import PLAYS

def run_tournament():
    strategies = [*axl.strategies, AIPlayer ]  # Get all available Axelrod strategies
    results = []
    for opponent_class in strategies:
        for strategy_class in strategies:
            strategy = strategy_class()  # Instantiate strategy
            opponent = opponent_class()  # Instantiate opponent

            match = axl.Match([strategy, opponent], turns=PLAYS)
            history = match.play()  # Play the match and get history

            # Track moves for each turn
            match_history = [(turn + 1, move[0], move[1]) for turn, move in enumerate(history)]

            scores = list(map(int, match.final_score()))  # Get scores
            results.append({
                "Strategy": opponent.name, 
                "Opponent": scores[0], 
                "Match History": match_history
            })
    # Save results to CSV
    save_results(results)

    return results



