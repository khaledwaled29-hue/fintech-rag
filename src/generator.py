"""Step 5 of the pipeline: prompt engineering and generation.

Builds the augmented prompt (instructions + retrieved chunks + question),
sends it to Gemini, and returns the answer with its sources.

Try it on its own:
    python -m src.generator "How long do I have to dispute a card payment?"
"""
import sys
import time
from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate

from src import config
from src.retriever import RetrievedChunk, is_relevant, retrieve

NOT_FOUND_ANSWER = "I don't know based on the FinPay documents."

# ------------------------------------------------------------ prompt template
SYSTEM_PROMPT = """You are FinPay's internal knowledge assistant. You answer questions \
from FinPay employees using ONLY the context documents provided below.

Rules:
1. Use only facts stated in the context. Never use outside knowledge, and never guess.
2. If the context does not contain the answer, reply exactly: "{not_found}"
3. If the context answers only part of the question, answer that part and say \
which part is not covered.
4. Cite the document ID in square brackets after each fact, e.g. [FP-DSP-009].
5. Keep numbers, time limits and amounts exactly as written in the context.
6. Be concise: a short direct answer first, then details as bullet points if needed.

Context documents:
{context}"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Question: {question}"),
])


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Number each chunk and label it with its source so the LLM can cite it."""
    blocks = []
    for i, c in enumerate(chunks, 1):
        body = c.document.page_content.split("\n", 1)[-1].strip()   # drop our header line
        blocks.append(f"--- Document {i}: {c.source} ---\n{body}")
    return "\n\n".join(blocks)


# ------------------------------------------------------------------ the LLM
@lru_cache(maxsize=4)
def get_llm(model_name: str):
    """Create the Gemini client once per model and reuse it."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    config.require_api_key()
    if model_name.startswith("gemini-3"):
        # Gemini 3 models use fixed sampling settings and ignore temperature.
        return ChatGoogleGenerativeAI(model=model_name)
    return ChatGoogleGenerativeAI(model=model_name, temperature=config.TEMPERATURE)


def _is_temporary(error: Exception) -> bool:
    text = str(error)
    return any(code in text for code in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500"))


def _is_model_missing(error: Exception) -> bool:
    return "404" in str(error) or "NOT_FOUND" in str(error)


def call_llm(messages) -> tuple[str, str]:
    """Call Gemini with retries and a fallback model. Returns (text, model_used).

    - Temporary errors (overloaded / rate limited): wait 2s, 4s, 8s... and retry.
    - Model retired (404) or still failing: switch to the fallback model.
    - Other errors (e.g. invalid API key): raise immediately, retrying won't help.
    """
    last_error = None
    for model_name in dict.fromkeys([config.GEMINI_MODEL, config.GEMINI_FALLBACK_MODEL]):
        llm = get_llm(model_name)
        for attempt in range(1, config.MAX_RETRIES + 1):
            try:
                return llm.invoke(messages).text, model_name
            except Exception as error:  # the SDK raises several error types
                last_error = error
                if _is_model_missing(error):
                    print(f"[warning] model '{model_name}' not available, trying fallback...")
                    break
                if not _is_temporary(error):
                    raise
                if attempt == config.MAX_RETRIES:
                    print(f"[warning] {model_name} still busy, switching to fallback model...")
                    break
                wait = 2 ** attempt
                print(f"[warning] {model_name} busy (attempt {attempt}/{config.MAX_RETRIES}), retrying in {wait}s...")
                time.sleep(wait)
    raise RuntimeError(f"All models failed. Last error: {last_error}")


# --------------------------------------------------------------- pipeline
def answer(question: str) -> dict:
    """Full RAG answer: retrieve -> (quality gate) -> augment -> generate."""
    t0 = time.perf_counter()
    chunks = retrieve(question)
    t1 = time.perf_counter()

    if not is_relevant(chunks):
        # Nothing similar enough in the knowledge base: don't let the LLM guess.
        return {"answer": NOT_FOUND_ANSWER, "sources": [], "chunks": chunks,
                "model": "none (quality gate)",
                "retrieval_s": round(t1 - t0, 2), "generation_s": 0.0}

    messages = PROMPT.format_messages(
        not_found=NOT_FOUND_ANSWER, context=format_context(chunks), question=question)
    text, model_used = call_llm(messages)
    t2 = time.perf_counter()

    return {
        "answer": text.strip(),
        "sources": list(dict.fromkeys(c.source for c in chunks)),   # unique, in rank order
        "chunks": chunks,
        "model": model_used,
        "retrieval_s": round(t1 - t0, 2),
        "generation_s": round(t2 - t1, 2),
    }


def print_answer(question: str, result: dict) -> None:
    print(f"\nQuestion: {question}\n")
    print(result["answer"])
    print("\nRetrieved from:")
    for c in result["chunks"]:
        print(f"  - {c.source}  (similarity {c.similarity:.3f})")
    print(f"\nModel: {result['model']} | Retrieval: {result['retrieval_s']} s"
          f" | Generation: {result['generation_s']} s")


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "How long do I have to dispute a card payment?"
    print_answer(q, answer(q))
