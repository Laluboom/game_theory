import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from HPC.config import MODEL_NAME, LOCAL_MODEL_PATH, DEVICE, NUM_GPUS

# Load model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    cache_dir=LOCAL_MODEL_PATH
)

if NUM_GPUS > 1:
    model = torch.nn.DataParallel(model)

model.to(DEVICE)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=LOCAL_MODEL_PATH)
