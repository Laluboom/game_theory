import axelrod as axl
import torch
from transformers import AutoTokenizer
from HPC.config import DEVICE, PLAYS, NUM_GPUS
from HPC.model import model, tokenizer

class AIPlayer(axl.Player):
    """AI-based player for Axelrod's tournament using a transformer model."""
    name = "AIPlayer"

    def __init__(self):
        super().__init__()
        self.generated_moves = []  # Store AI-generated moves

    def strategy(self, opponent: axl.Player) -> axl.Action:
        """Decide next move using a deep learning model based on opponent's past moves."""
        if not self.generated_moves:
            opponent_strategy = opponent.__class__.__name__
            prompt = f"""
            You are playing an iterated prisoner's dilemma tournament where the goal is to win every match you play.
            The match consists of {PLAYS} rounds.
            Your opponent has the strategy of {opponent_strategy}.

            Take the following logical conclusions into account:
            - If your opponent mostly cooperates, continue cooperating to build trust.
            - If your opponent defects occasionally, analyze whether it’s strategic or random. Generate a sequence of moves for the next {PLAYS} rounds using logical strategies.
            - If your opponent always defects, retaliate by defecting to avoid exploitation.
            - If the opponent mimics your previous move, exploit this pattern in the last few moves.
            - Use your knowledge of the opponent’s strategy to maximize your score.
            Output should end with your planned moves.
            """

            model_input = tokenizer(prompt, return_tensors="pt").to(DEVICE)

            with torch.no_grad():
                generate_func = model.module.generate if NUM_GPUS > 1 else model.generate
                output_ids = generate_func(
                    **model_input,
                    max_new_tokens=PLAYS,
                    eos_token_id=tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7,
                    top_k=50,
                    top_p=0.9
                )

            response = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip().upper()
            self.generated_moves = list(response[-PLAYS:])  # Store sequence of moves
            print(f"Opponent: {opponent_strategy} || Generated move sequence: {self.generated_moves}")

        # Play the next move in the sequence
        ai_move = self.generated_moves.pop(0)
        return axl.Action.C if ai_move == "C" else axl.Action.D
