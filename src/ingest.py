"""Steps 2 & 3 of the pipeline.

Step 2: load documents and split them into chunks.
Step 3: embed every chunk and store the vectors in Chroma.

    python -m src.ingest --preview   # Step 2 only: show chunking statistics
    python -m src.ingest             # Steps 2 + 3: build the vector database
"""
import argparse
import re
import time
from pathlib import Path

from langchain_core.documents import Document
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import config

SUPPORTED = {".md", ".txt", ".pdf"}


# ---------------------------------------------------------------- loading
def _extract_metadata(text: str) -> dict:
    """Pull the title and document ID out of the first lines of a document."""
    first_line = next((l for l in text.splitlines() if l.strip()), "")
    title = first_line.lstrip("# ").strip()
    match = re.search(r"Document ID:\s*([A-Z]+-[A-Z]+-\d+)", text)
    return {"title": title, "doc_id": match.group(1) if match else "unknown"}


def load_documents(data_dir: Path = config.DATA_DIR) -> list[Document]:
    """Load every .md / .txt / .pdf file into one LangChain Document per file.

    We read files directly (pypdf for PDFs) instead of using the loaders in
    langchain-community, because that package is being sunset by LangChain.
    """
    documents = []
    for path in sorted(data_dir.iterdir()):
        if path.suffix.lower() not in SUPPORTED:
            continue
        if path.suffix.lower() == ".pdf":
            # pypdf extracts the text layer page by page
            text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
        else:
            text = path.read_text(encoding="utf-8")

        metadata = {"source": path.name, "file_type": path.suffix.lstrip("."),
                    **_extract_metadata(text)}
        documents.append(Document(page_content=text, metadata=metadata))
    return documents


# --------------------------------------------------------------- chunking
def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into overlapping chunks.

    Separators are tried in order: markdown section headings first, then
    paragraphs, lines, sentences and finally words, so chunks break at the
    most natural boundary that keeps them under CHUNK_SIZE characters.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n\n", "\n", ". ", " ", ""],
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)

    # Contextual header: prefix every chunk with its document title so a chunk
    # like "Customers must raise a dispute within 60 days" still says WHICH
    # policy it belongs to. This improves both retrieval and answer citations.
    for i, chunk in enumerate(chunks):
        header = f"[{chunk.metadata['title']} | {chunk.metadata['doc_id']}]\n"
        chunk.page_content = header + chunk.page_content
        chunk.metadata["chunk_id"] = i
    return chunks


# --------------------------------------------------------------- indexing
def build_index(chunks: list[Document]) -> None:
    """Embed all chunks and write them to a fresh Chroma collection."""
    from src.vectorstore import get_embeddings, get_vectorstore

    print("\nLoading embedding model (first run downloads ~90 MB)...")
    embeddings = get_embeddings()
    store = get_vectorstore(embeddings)

    # Start clean so re-running never creates duplicate chunks.
    store.reset_collection()

    start = time.perf_counter()
    store.add_documents(chunks, ids=[f"chunk-{c.metadata['chunk_id']}" for c in chunks])
    elapsed = time.perf_counter() - start

    dimension = len(embeddings.embed_query("test"))
    print(f"Embedded and stored {store._collection.count()} chunks in {elapsed:.1f} s")
    print(f"Each chunk is now a vector of {dimension} numbers")
    print(f"Vector database saved to: {config.CHROMA_DIR}")


# ---------------------------------------------------------------- preview
def preview(chunks: list[Document], documents: list[Document]) -> None:
    sizes = [len(c.page_content) for c in chunks]
    print(f"\nLoaded {len(documents)} documents "
          f"({sum(d.metadata['file_type'] == 'pdf' for d in documents)} PDF, "
          f"{sum(d.metadata['file_type'] != 'pdf' for d in documents)} Markdown)")
    print(f"Created {len(chunks)} chunks "
          f"(size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP})")
    print(f"Chunk length: min {min(sizes)}, avg {sum(sizes)//len(sizes)}, max {max(sizes)} characters\n")

    print("Chunks per document:")
    for d in documents:
        n = sum(c.metadata["source"] == d.metadata["source"] for c in chunks)
        print(f"  {n:>2}  {d.metadata['source']}")

    sample = next(c for c in chunks if c.metadata["source"].startswith("09_"))
    print("\n--- Example chunk ---")
    print(sample.page_content)
    print("--- Metadata ---")
    print(sample.metadata)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load, chunk and index the FinPay documents.")
    parser.add_argument("--preview", action="store_true", help="show chunking statistics only")
    args = parser.parse_args()

    documents = load_documents()
    chunks = split_documents(documents)
    if args.preview:
        preview(chunks, documents)
    else:
        print(f"Loaded {len(documents)} documents -> {len(chunks)} chunks")
        build_index(chunks)


if __name__ == "__main__":
    main()
