import subprocess
import logging
from typing import Optional

# Get logger for this module
logger = logging.getLogger(__name__)

def convert_model(
    hf_model: str,
    gguf_output: str,
    quantized_output: Optional[str] = None,
    quant_type: Optional[str] = None,
    quant_algo: str = "8"
):
    convert_command = [
        "python",
        "llama.cpp/convert_hf_to_gguf.py",
        hf_model,
        "--outfile",
        gguf_output
    ]

    try:
        print("Converting HuggingFace model to GGUF...")
        subprocess.run(convert_command, check=True)

        if quant_type and quantized_output:
            quantize_command = [
                "llama.cpp/build/bin/llama-quantize",
                gguf_output,
                quantized_output,
                quant_type,
                quant_algo
            ]
            print(f"Quantizing GGUF using {quant_type}...")
            subprocess.run(quantize_command, check=True)
        else:
            print("Quantization skipped — raw GGUF saved.")

        print("Conversion completed successfully.")

    except subprocess.CalledProcessError as e:
        logger.error("Model conversion failed!")
        print(f"Command: {' '.join(convert_command)}")
        print(f"Exit Code: {e.returncode}")

        # Helpful guidance for users
        print("\nIt looks like the model path or ID may be missing or incorrect.")
        print("1. Make sure you have downloaded the model locally from Hugging Face.")
        print("2. Pass the correct local folder path to --hf_model (not just the model name).")
        print("   Example: --hf_model /path/to/meta-llama/Llama-2-7b-hf")
        print("3. If you don't have the model, download it first using:")
        print("   from huggingface_hub import snapshot_download")
        print("   snapshot_download(repo_id='meta-llama/Llama-2-7b-hf', local_dir='models/Llama-2-7b-hf')")


