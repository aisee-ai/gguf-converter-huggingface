# llama_tools/setup_llama.py

import subprocess
import os
from pathlib import Path
import shutil
import sys

from llama_tools_aisee.venv import create_virtualenv


def clone_llama_cpp(
    repo_url: str = "https://github.com/ggerganov/llama.cpp.git",
    repo_dir: Path = None,
) -> Path:
    """Clone llama.cpp repo into repo_dir if missing and return the resolved path."""
    if repo_dir is None:
        repo_dir = Path.home() / ".cache" / "llama-tools-aisee" / "llama.cpp"
    else:
        repo_dir = Path(repo_dir)

    repo_dir.parent.mkdir(parents=True, exist_ok=True)

    if not (repo_dir / ".git").exists():
        subprocess.run(["git", "clone", repo_url, str(repo_dir)], check=True)
        print(f"Cloned llama.cpp to {repo_dir}")
    else:
        print(f"Repository already exists at {repo_dir}, pulling latest changes...")
        subprocess.run(["git", "-C", str(repo_dir), "fetch", "--all", "--tags"], check=False)
        subprocess.run(["git", "-C", str(repo_dir), "reset", "--hard", "origin/master"], check=False)

    gm = repo_dir / ".gitmodules"
    if gm.exists():
        subprocess.run(
            ["git", "-C", str(repo_dir), "submodule", "update", "--init", "--recursive"],
            check=True,
        )
        print("Submodules initialized.")
    else:
        print("No submodules found — skipping.")

    return repo_dir


def setup_llama(jobs: int = 4, create_venv: bool = False, repo_dir: str = "llama.cpp"):
    """
    Configures and builds llama.cpp using CMake & Ninja, optionally sets up a Python venv.
    """
    repo_path = clone_llama_cpp(repo_dir=repo_dir)

    if not (repo_path / "CMakeLists.txt").exists():
        sys.exit(f"Error: No CMakeLists.txt found in {repo_path}. Clone may have failed.")

    # Ensure cmake & ninja exist
    for tool in ["cmake", "ninja"]:
        if shutil.which(tool) is None:
            sys.exit(f"Error: {tool} not found. Install it via `conda install -c conda-forge cmake ninja`")

    cmake_config_cmd = [
        "cmake", "-S", ".", "-B", "build",
        "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DLLAMA_BUILD_TESTS=OFF",
        "-DLLAMA_BUILD_EXAMPLES=ON",
        "-DLLAMA_BUILD_SERVER=ON",
        "-DLLAMA_CURL=OFF"
    ]

    subprocess.run(cmake_config_cmd, cwd=repo_path, check=True)
    print("CMake configuration completed.")

    subprocess.run(["cmake", "--build", "build", "--config", "Release", f"-j{jobs}"], cwd=repo_path, check=True)
    print(f"Build completed with -j{jobs}.")

    if create_venv:
        create_virtualenv()
        print("Virtual environment created. Run `source ~/llama-cpp-venv/bin/activate` to activate.")
