
# gguf-converter-huggingface

A Python package and CLI tool for building, converting, quantizing, and uploading [LLaMA](https://ai.meta.com/llama/) models using [`llama.cpp`](https://github.com/ggerganov/llama.cpp). Ideal for efficient local inference, edge deployment, and privacy-preserving LLM applications.

---

## What It Does

`llama-tools-aisee` automates the full pipeline for preparing Hugging Face LLaMA models for `llama.cpp`. It helps you:

* Clone and build `llama.cpp`
* Convert HF models to GGUF format
* Quantize with precision options like `Q4_0`, `Q5_1`, `TQ1_0`, etc.
* Upload `.gguf` models to Hugging Face Hub
* Set up a Python virtual environment
* Run everything via CLI or Python API

---

## Installation

Install from PyPI:

```bash
pip install llama-tools-aisee
```

---

## CLI Usage

```bash
llama-tools-aisee <command> [options]
```

---

## Commands Overview

| Command      | Description                           | Python Function         |
| ------------ | ------------------------------------- | ----------------------- |
| `clone`      | Clone `llama.cpp` repo                | `clone_llama_cpp()`     |
| `setup`      | Build `llama.cpp` (CMake + Ninja)     | `setup_llama()`         |
| `venv`       | Create a Python virtual environment   | `create_virtualenv()`   |
| `convert`    | Convert HF model to GGUF and quantize | `convert_model(...)`    |
| `upload`     | Upload `.gguf` to Hugging Face        | `push_gguf(...)`        |
| `run-server` | Start local inference server          | `run_llama_server(...)` |
| `clean`      | Remove build and model folders        | `clean_build_dirs()`    |
| `status`     | Show build and env status             | `show_status()`         |

---

## Commands

### Clone `llama.cpp`

```bash
llama-tools-aisee clone
```

---

### Build with CMake + Ninja

```bash
llama-tools-aisee setup -j 8 --create-venv
```

> **Windows Users:** Install CMake, Ninja, Visual Studio Build Tools with C++ components. Use PowerShell or Git Bash.

---

### Create Virtual Environment

```bash
llama-tools-aisee venv
```

Once created, activate the virtual environment:

**Linux / macOS (bash/zsh):**

```bash
source ~/llama-cpp-venv/bin/activate
```

**Windows (PowerShell):**

```powershell
~\llama-cpp-venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
%USERPROFILE%\llama-cpp-venv\Scripts\activate.bat
```

To deactivate the environment, simply run:

```bash
deactivate
```

---


### Convert & Quantize HF Model

```bash
llama-tools-aisee convert \
  --hf_model meta-llama/Llama-2-7b-hf \
  --gguf_output models/Llama-2-7b.gguf \
  --quantized_output models/Llama-2-7b-q4.gguf \
  --quant_type Q4_0 \
  --quant_algo 8
```

---

### Upload to Hugging Face

```bash
llama-tools-aisee upload \
  --repo_id username/model-name \
  --gguf_path models/Llama-2-7b-q4.gguf
```

---

### Run Server

```bash
llama-tools-aisee run-server --gguf_model models/Llama-2-7b-q4.gguf
```

---

### Clean Builds

```bash
llama-tools-aisee clean
```

---

### Status Report

```bash
llama-tools-aisee status
```

---

##  Supported Quantization Types

| Type     | Size / Description         |
| -------- | -------------------------- |
| `Q4_0`   | 4.34G, basic 4-bit         |
| `Q4_1`   | 4.78G, improved 4-bit      |
| `Q5_1`   | 5.65G, high-quality 5-bit  |
| `Q8_0`   | 7.96G, near full precision |
| `Q3_K_M` | 3.74G, 3-bit mixed         |
| `IQ2_XS` | 2.31 bpw                   |
| `TQ1_0`  | 1.69 bpw, ternary          |

See full list: [llama.cpp#quantization](https://github.com/ggerganov/llama.cpp#quantization)

---

##  Python API Usage

Import and use core functions programmatically:

```python
from llama_tools_aisee import (
    setup_llama,
    convert_model,
    push_gguf,
    run_llama_server,
    clean_build_dirs,
    show_status
)
```

---

### `setup_llama(jobs=4, create_venv=False)`

Builds `llama.cpp`.

```python
setup_llama(jobs=8, create_venv=True)
```

---

### `convert_model(hf_model, gguf_output, quantized_output=None, quant_type=None, quant_algo="8")`

Converts a HF model to `.gguf` and applies quantization.

```python
convert_model(
    hf_model="meta-llama/Llama-2-7b-hf",
    gguf_output="models/7b.gguf",
    quantized_output="models/7b-q4.gguf",
    quant_type="Q4_0"
)
```

---

### `push_gguf(repo_id, gguf_path, local_repo_dir="./hf_tmp_repo")`

Uploads the quantized model.

```python
push_gguf("your-username/llama-7b-q4", "models/7b-q4.gguf")
```

---

### `run_llama_server(gguf_model)`

Launches a local server using a `.gguf` model.

```python
run_llama_server("models/7b-q4.gguf")
```

---

## 📁 Package Structure

```
llama_tools_aisee/
├── __main__.py                  # CLI Entrypoint
├── setup_llama_cpp.py           # llama.cpp build logic
├── venv.py                      # Virtualenv setup
├── convert_and_quantize.py      # HF → GGUF conversion
├── push_gguf.py                 # Upload to Hugging Face
├── server.py                    # Run llama-server
├── utils.py                     # Clean, status reporting
```

---

## 🧪 Testing

The package includes comprehensive unit tests with high coverage:

```bash
# Run all tests
pytest tests/

# Run tests with coverage report
pytest tests/ --cov=llama_tools_aisee --cov-report=term-missing

# Run specific test files
pytest tests/test_convert.py -v
pytest tests/test_setup.py -v
pytest tests/test_main.py -v
```

### Test Coverage

- **Main CLI (`__main__.py`)**: Comprehensive argument parsing and command dispatch testing
- **Model Conversion (`convert_and_quantize.py`)**: Testing conversion, quantization, and error handling
- **Setup & Build (`setup_llama_cpp.py`)**: Repository cloning, building, and error scenarios
- **File Upload (`push_gguf.py`)**: Hugging Face Hub upload functionality
- **Utilities (`utils.py`, `venv.py`, `server.py`)**: Supporting functions and utilities

### Recent Test Improvements

✅ **All Tests Passing**: 29+ unit tests covering core functionality  
✅ **High Coverage**: 80%+ code coverage across all modules  
✅ **Error Handling**: Comprehensive testing of error scenarios and edge cases  
✅ **CLI Testing**: Full command-line interface argument validation  
✅ **Mocking**: Proper isolation of external dependencies (git, subprocess, file system)  

---

##  Development

### Build & Publish

```bash
rm -rf dist/ build/ *.egg-info
python -m build
twine upload dist/*
```

### Run Tests

```bash
pytest tests/
```

---

## 📄 License

MIT License

---

## 👤 Author

**Jaliya Nimantha**
[jaliya@ahlab.org](mailto:jaliya@ahlab.org)
[ahlab.org](https://ahlab.org)

