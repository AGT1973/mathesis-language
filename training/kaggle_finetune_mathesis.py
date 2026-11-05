# %% [markdown]
# # 🌌 MATHESIS Fine-Tuning Pipeline (Kaggle / Colab Free Tier)
# ## SFT Training for DeepSeek-R1-Distill-Qwen-1.5B and Qwen-2.5-Coder-1.5B
# **Project:** POLYDIM / MATHESIS (Ariel García Traba)
# **Target:** Train a local 1.5B model to natively compile and reason in 64-byte MATHESIS binary tuples.
# **Hardware Requirement:** 1x NVIDIA T4 (16GB VRAM) — 100% Free on Kaggle (30h/week) or Google Colab.
# **Training Time:** ~35-45 minutes. Output LoRA adapter: ~15 MB.

# %%
# 1. Install dependencies
!pip install -q -U torch transformers datasets peft bitsandbytes trl accelerate

# %%
import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# %%
# 2. Select SOTA Base Model
# Option A (Recommended for logic & math): "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
# Option B (Recommended for pure code/assembler): "Qwen/Qwen2.5-Coder-1.5B-Instruct"
MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
OUTPUT_DIR = "./mathesis_lora_adapter"

print(f"Loading Base Model: {MODEL_ID}")

# %%
# 3. 4-bit Quantization Configuration (Fits in 4GB of T4 VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
model = prepare_model_for_kbit_training(model)

# %%
# 4. LoRA Configuration (Rank 16, Alpha 32 — Target Attention Projections)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# %%
# 5. Load Verified MATHESIS Dataset
# Upload 'mathesis_train_dataset.jsonl' to Kaggle working directory or dataset input
dataset_file = "mathesis_train_dataset.jsonl"
if not os.path.exists(dataset_file):
    print(f"Please upload {dataset_file}!")
else:
    dataset = load_dataset("json", data_files=dataset_file, split="train")
    print(f"Loaded {len(dataset)} verified MATHESIS training samples.")

# %%
# 6. Formatting Function
def format_prompts(batch):
    texts = []
    for i in range(len(batch["instruction"])):
        sys = batch["system"][i]
        inst = batch["instruction"][i]
        resp = batch["response"][i]
        # ChatML / Qwen format
        text = f"<|im_start|>system\n{sys}<|im_end|>\n<|im_start|>user\n{inst}<|im_end|>\n<|im_start|>assistant\n{resp}<|im_end|>"
        texts.append(text)
    return {"text": texts}

formatted_dataset = dataset.map(format_prompts, batched=True)

# %%
# 7. Training Arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_ratio=0.05,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    optim="paged_adamw_8bit",
    save_strategy="epoch",
    report_to="none"
)

# %%
# 8. Train with SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=formatted_dataset,
    dataset_text_field="text",
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=training_args
)

print("Starting SFT QLoRA Training...")
trainer.train()

# %%
# 9. Save LoRA Adapter
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"Adapter successfully saved to {OUTPUT_DIR}!")
print("Zip this directory and download it to run locally on AMD A4-6300 CPU.")
!zip -r mathesis_lora_adapter.zip {OUTPUT_DIR}
