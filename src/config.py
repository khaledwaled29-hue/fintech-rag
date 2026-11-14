"""Central configuration for the FinPay RAG system.

All tunable settings live here so experiments (e.g. chunk size)
only need one change, and secrets are read from .env, never hard-coded.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "finpay_docs"

# --- Chunking ---
CHUNK_SIZE = 800       # characters per chunk
CHUNK_OVERLAP = 150    # characters shared between neighbouring chunks

# --- Embeddings (runs locally, no API key needed) ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- Retrieval ---
TOP_K = 4              # number of chunks passed to the LLM

# --- Generation (Google Gemini, free tier) ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
TEMPERATURE = 0.0      # deterministic, factual answers


def require_api_key() -> str:
    """Fail early with a clear message if the key is missing."""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_gemini_api_key_here":
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env "
            "and paste your key from https://aistudio.google.com/apikey"
        )
    return GOOGLE_API_KEY

# --- Retrieval quality gate ---
# If even the best chunk is less similar than this, the question is probably
# outside the knowledge base. Tuned later in the evaluation step.
MIN_SIMILARITY = 0.25

# --- Resilience ---
# Used automatically if the main model is overloaded (503), rate-limited (429)
# or retired (404). Both can be changed in .env without touching code.
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.8-flash")
MAX_RETRIES = 3          # attempts per model before moving on
