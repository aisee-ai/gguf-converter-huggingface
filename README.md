# gguf-converter-huggingface

A Python package and CLI tool that simplifies building, converting, quantizing, and uploading [LLaMA](https://ai.meta.com/llama/) models using [`llama.cpp`](https://github.com/ggerganov/llama.cpp).

---

## What is this?

`llama-tools-jaliya` is designed to automate and streamline the full pipeline for preparing LLaMA models for local or edge-device inference. It helps developers and researchers:

- Clone and build the `llama.cpp` backend
- Convert Hugging Face transformer models into GGUF format
- Apply quantization for efficient on-device execution
- Upload GGUF models to Hugging Face Hub
- Manage environment setup with optional virtualenv support
- Use a single CLI or Python API to orchestrate everything

Ideal for on-device LLM apps, embedded AI agents, offline research tools, and performance-focused inference pipelines.

---

## Features

- Build `llama.cpp` with Ninja and CMake
- Convert Hugging Face models to GGUF
- Quantize with support for Q4_0, Q5_1, TQ1_0, and more
- Push models directly to Hugging Face
- Scriptable via CLI or Python
- Virtual environment auto-setup (optional)

---

## Installation

Install from PyPI:

```bash
pip install llama-tools-jaliya
