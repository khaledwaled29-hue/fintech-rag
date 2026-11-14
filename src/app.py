"""Step 6: end-to-end interactive app (command line).

    python -m src.app            # normal mode
    python -m src.app --debug    # also print the retrieved chunks

The embedding model, vector store and Gemini client are loaded ONCE at
start-up, so every question after the first is answered much faster.
"""
import argparse
import time
import warnings

warnings.filterwarnings("ignore", category=UserWarning)   # hide library noise in the demo

from src import config  # noqa: E402
from src.generator import answer  # noqa: E402
from src.retriever import retrieve  # noqa: E402

BANNER = """
==============================================================
  FinPay Knowledge Assistant  (RAG demo)
  Ask about FinPay policies, limits, fees, disputes, the API...
  Commands:  /debug  toggle showing retrieved chunks
             /help   show example questions
             exit    quit
==============================================================
"""

EXAMPLES = [
    "How long do I have to dispute a card payment?",
    "What is the daily ATM limit for a new Plus customer?",
    "What does error FP-2003 mean and should I retry?",
    "When do new merchants get their money?",
    "What is the weather in Cairo?",
]


def show(result: dict, debug: bool) -> None:
    print("\n" + result["answer"])
    if debug:
        print("\n--- Retrieved chunks ---")
        for rank, c in enumerate(result["chunks"], 1):
            body = " ".join(c.document.page_content.split("\n", 1)[-1].split())
            print(f"#{rank} [{c.similarity:.3f}] {c.source}\n    {body[:300]}...")
    if result["sources"]:
        print("\nSources: " + "; ".join(result["sources"]))
    print(f"({result['model']} | retrieval {result['retrieval_s']} s"
          f" | generation {result['generation_s']} s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="FinPay RAG assistant")
    parser.add_argument("--debug", action="store_true", help="show retrieved chunks")
    debug = parser.parse_args().debug

    config.require_api_key()
    print("Loading embedding model and vector database...")
    start = time.perf_counter()
    retrieve("warm up")                       # loads the model + store once
    print(f"Ready in {time.perf_counter() - start:.1f} s")
    print(BANNER)

    while True:
        try:
            question = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break
        if question == "/debug":
            debug = not debug
            print(f"Debug mode {'ON' if debug else 'OFF'}")
            continue
        if question == "/help":
            print("Try:\n" + "\n".join(f"  - {e}" for e in EXAMPLES))
            continue
        try:
            show(answer(question), debug)
        except Exception as error:            # keep the app alive on API errors
            print(f"\n[error] {error}")
    print("Goodbye!")


if __name__ == "__main__":
    main()
