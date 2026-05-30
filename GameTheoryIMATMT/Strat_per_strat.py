
import json
import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ['https_proxy'] = "http://hpc-proxy00.city.ac.uk:3128" 

# Device Setup
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "NousResearch/DeepHermes-3-Llama-3-8B-Preview"
LOCAL_MODEL_PATH = "../archive/Llama3-8B"
RESULTS_FILE = "results/Strategy_Guide_results.json"

# Load Model & Tokenizer
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16, 
    device_map="none",
    cache_dir=LOCAL_MODEL_PATH
).to(DEVICE)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    cache_dir=LOCAL_MODEL_PATH
)

# Load strategies
with open(RESULTS_FILE, "r") as file:
    strategies = json.load(file)

def evaluate_strategy(strategy_name, strategy_description):
    """AI evaluates the strategy and suggests changes if necessary."""
    
    prompt = f"""
    You are evaluating a strategy for an Iterated Prisoner's Dilemma tournament.
    
    **Strategy Name:** {strategy_name}
    **Strategy Description:** {strategy_description}

    Analyze the strategy to determine if it is logically sound and optimal.

    - If the strategy is valid, return only this exact character: Y✅  
    - If the strategy is flawed, return a revised strategy with an explanation.
    """

    model_input = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(
            **model_input,
            max_new_tokens=300,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9
        )

    response = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    
    return response

# Process strategies
for strategy in strategies:
    strategy_name = strategy["Opponent Strategy"]
    strategy_description = strategy["AI Response"]
    
    # Keep evaluating until it gets a green tick ✅
    while True:
        ai_response = evaluate_strategy(strategy_name, strategy_description)

        if ai_response == "✅":
            strategies[strategy_name]["evaluation"] = "Y"
            break  # Stop evaluating this strategy

        strategy_description = ai_response  # Update strategy with AI's response

    # Save results after each update
    with open(RESULTS_FILE, "w") as file:
        json.dump(strategies, file, indent=4)

print(f"All strategies evaluated and saved to {RESULTS_FILE}")

