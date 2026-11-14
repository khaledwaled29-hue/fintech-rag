"""Step 1 sanity check: run `python check_setup.py` after installing."""
import importlib
import sys

print(f"Python {sys.version.split()[0]}", "OK" if sys.version_info >= (3, 10) else "-> need 3.10+")

for pkg in ["langchain_core", "langchain_text_splitters",
            "langchain_google_genai", "langchain_chroma", "langchain_huggingface",
            "chromadb", "sentence_transformers", "pypdf", "dotenv"]:
    try:
        importlib.import_module(pkg)
        print(f"  [OK]      {pkg}")
    except ImportError as e:
        print(f"  [MISSING] {pkg}: {e}")

from src import config
try:
    config.require_api_key()
    print("GOOGLE_API_KEY found in .env")
except RuntimeError as e:
    print(f"[WARNING] {e}")
