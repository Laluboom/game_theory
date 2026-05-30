import os
import torch

# Set up proxy if needed
os.environ['https_proxy'] = "http://hpc-proxy00.city.ac.uk:3128"

# Model details
MODEL_NAME = "NousResearch/DeepHermes-3-Llama-3-8B-Preview"
LOCAL_MODEL_PATH = "../archive/Llama3-8B"

# Device settings
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
NUM_GPUS = torch.cuda.device_count()

# Game settings
PLAYS = 50
