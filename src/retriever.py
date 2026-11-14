"""Step 4 of the pipeline: the retriever.

Turns the user's question into a vector with the SAME embedding model used
for the documents, then asks Chroma for the TOP_K closest chunks.

Try it on its own:
    python -m src.retriever "How long do I have to dispute a card payment?"
    python -m src.retriever            # interactive mode
"""
import sys
from dataclasses import dataclass

from langchain_core.documents import Document

from src import config
from src.vectorstore import get_default_store


@dataclass
class RetrievedChunk:
    document: Document
    similarity: float  # cosine similarity: higher = more relevant

    @property
    def source(self) -> str:
        return f"{self.document.metadata['title']} ({self.document.metadata['doc_id']})"


def normalise_query(query: str) -> str:
    """Light query transformation: trim spaces and collapse whitespace.

    (Advanced systems rewrite the query with an LLM here; see the report,
    Section 5.3. We keep it simple and cheap.)
    """
    return " ".join(query.split())


def retrieve(query: str, k: int = config.TOP_K) -> list[RetrievedChunk]:
    """Return the k most similar chunks, best first."""
    store = get_default_store()
    # With the cosine setting, Chroma returns a DISTANCE (0 = identical).
    # similarity = 1 - distance makes the numbers easier to read.
    results = store.similarity_search_with_score(normalise_query(query), k=k)
    return [RetrievedChunk(doc, round(1 - distance, 3)) for doc, distance in results]


def is_relevant(chunks: list[RetrievedChunk]) -> bool:
    """Quality gate: is the best match similar enough to trust?"""
    return bool(chunks) and chunks[0].similarity >= config.MIN_SIMILARITY


def print_results(query: str, chunks: list[RetrievedChunk]) -> None:
    print(f'\nQuestion: "{query}"')
    print(f"Top {len(chunks)} chunks (minimum similarity to answer: {config.MIN_SIMILARITY}):\n")
    for rank, c in enumerate(chunks, 1):
        body = c.document.page_content.split("\n", 1)[-1]          # drop our header line
        preview = " ".join(body.split())[:220]
        print(f"#{rank}  similarity {c.similarity:.3f}  |  {c.source}")
        print(f"    {preview}...\n")
    if not is_relevant(chunks):
        print(">> Best match is below the threshold: this question is probably NOT covered by the documents.")


def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print_results(query, retrieve(query))
        return
    print("Retriever test mode. Type a question (or 'exit').")
    while (query := input("\n> ").strip()).lower() not in {"exit", "quit", ""}:
        print_results(query, retrieve(query))


if __name__ == "__main__":
    main()
