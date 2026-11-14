"""Step 3 building blocks: the embedding model and the Chroma vector store.

Both ingest.py (writing) and retriever.py (reading) use these functions,
so the same embedding model is ALWAYS used for documents and questions.
"""
from functools import lru_cache

from langchain_chroma import Chroma

from src import config


@lru_cache(maxsize=1)
def get_embeddings():
    """Load the local SentenceTransformers model (downloaded once, ~90 MB).

    all-MiniLM-L6-v2 maps any text to a 384-number vector. Vectors are
    normalised to length 1, so cosine similarity is a simple dot product.
    """
    from langchain_huggingface import HuggingFaceEmbeddings  # heavy import, load lazily

    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vectorstore(embeddings=None) -> Chroma:
    """Open (or create) the persistent Chroma collection on disk."""
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings or get_embeddings(),
        persist_directory=str(config.CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},  # compare vectors by angle
    )


@lru_cache(maxsize=1)
def get_default_store() -> Chroma:
    """Open the store once and reuse it (used by the retriever / app)."""
    return get_vectorstore()
