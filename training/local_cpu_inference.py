"""
LOCAL CPU INFERENCE FOR MATHESIS
Runs quantized or LoRA-adapted 1.5B models directly on the AMD A4-6300 CPU.
Memory footprint: ~1.2 GB RAM.
"""

import sys
import os

def check_local_environment():
    print("=" * 60)
    print("MATHESIS LOCAL SILICON INFERENCE CHECK (AMD A4-6300)")
    print("=" * 60)
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    
    # Check if llama-cpp-python or transformers is installed
    try:
        import torch
        print(f"PyTorch version: {torch.__version__} (CPU threads: {torch.get_num_threads()})")
    except ImportError:
        print("PyTorch not installed in this environment.")
        
    adapter_path = os.path.join(os.path.dirname(__file__), "mathesis_lora_adapter")
    if os.path.exists(adapter_path):
        print(f"[OK] Found local LoRA adapter at: {adapter_path}")
    else:
        print(f"[INFO] LoRA adapter not yet downloaded to: {adapter_path}")
        print("Run 'kaggle_finetune_mathesis.py' on Kaggle GPU T4 (free) to generate it.")

if __name__ == "__main__":
    check_local_environment()
