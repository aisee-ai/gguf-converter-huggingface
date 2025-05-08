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




## Usage

```bash
llama-tools-jaliya <command> [options]
```

---

## Commands & Functions

### `clone`

**Clones the `llama.cpp` repository and initializes submodules.**

```bash
llama-tools-jaliya clone
```

**Function:** `clone_llama_cpp()`

---

### `setup`

**Builds `llama.cpp` using CMake + Ninja.**

```bash
llama-tools-jaliya setup -j 8 --create-venv
```

* `-j`: Number of build threads
* `--create-venv`: Also creates a virtual environment and installs Python dependencies

**Function:** `setup_llama(...)`

#### ⚠️ Windows Users

To build on Windows, ensure you have:

* [CMake](https://cmake.org/download/)
* [Ninja](https://ninja-build.org/)
* [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with:

  * C++ build tools
  * Windows SDK
  * MSVC compiler

All tools must be available in your system `PATH`. Then run the same `setup` command in PowerShell or Git Bash.

---

### `venv`

**Creates a Python virtual environment and installs dependencies.**

```bash
llama-tools-jaliya venv
```

**Function:** `create_virtualenv()`

---

### `convert`

**Converts Hugging Face model to GGUF and optionally quantizes it.**

```bash
llama-tools-jaliya convert \
  --hf_model meta-llama/Llama-2-7b-hf \
  --gguf_output models/Llama-2-7b.gguf \
  --quantized_output models/Llama-2-7b-q4.gguf \
  --quant_type Q4_0 \
  --quant_algo 8
```

* Supported quant types: `Q4_0`, `Q5_1`, `Q8_0`, `TQ1_0`, etc.

**Function:** `convert_model(...)`

---

### `upload`

**Uploads a `.gguf` model to Hugging Face Hub.**

```bash
llama-tools-jaliya upload \
  --repo_id username/model-name \
  --gguf_path models/Llama-2-7b-q4.gguf
```

**Function:** `push_gguf(...)`

---

### `run-server`

**Runs `llama-server` using a `.gguf` model.**

```bash
llama-tools-jaliya run-server --gguf_model models/Llama-2-7b-q4.gguf
```

**Function:** `run_llama_server(...)`

---

### `clean`

**Removes build and model folders.**

```bash
llama-tools-jaliya clean
```

**Function:** `clean_build_dirs()`

---

### `status`

**Displays current environment and build status.**

```bash
llama-tools-jaliya status
```

**Function:** `show_status()`

---

##  Supported Quantization Types

```text
  Q4_0    : 4.34G, basic 4-bit
  Q4_1    : 4.78G, better 4-bit
  Q5_1    : 5.65G, high-quality 5-bit
  Q8_0    : 7.96G, near full precision
  Q3_K_M  : 3.74G, 3-bit mixed
  IQ2_XS  : 2.31 bpw
  TQ1_0   : 1.69 bpw, ternary
```

See: [https://github.com/ggerganov/llama.cpp#quantization](https://github.com/ggerganov/llama.cpp#quantization)

---

##  Development

To rebuild and publish:

```bash
rm -rf dist/ build/ *.egg-info
python -m build
twine upload dist/*
```

Run tests:

```bash
pytest tests/
```

---

## 📄 License

MIT License

---

## 👤 Author

**Jaliya Nimantha**
[jaliya@ahlab.org](mailto:jaliya@ahlab.org) | [ahlab.org](https://ahlab.org)

```
