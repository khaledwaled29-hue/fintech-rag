"""Step 7: evaluation of the RAG system against a labelled test set.

    python -m src.evaluate --retrieval-only   # no API calls, seconds to run
    python -m src.evaluate                    # full: retrieval + answers
    python -m src.evaluate --judge            # + LLM-as-judge faithfulness check
    python -m src.evaluate --chunk-experiment # compare chunk sizes (no API calls)

Metrics
- Retrieval (answerable questions): Hit@1, Hit@K and MRR -- is a chunk from
  the correct document found, and how high is it ranked?
- Answer correctness: the answer contains the expected key facts.
- Refusal accuracy: unanswerable / off-topic questions get "I don't know".
- Faithfulness (--judge): a second LLM call checks that every claim in the
  answer is supported by the retrieved context.

Results are written to eval/results.csv and eval/summary.md.
"""
import argparse
import csv
import json
import time
import warnings
from statistics import mean

warnings.filterwarnings("ignore", category=UserWarning)

from src import config  # noqa: E402
from src.retriever import retrieve  # noqa: E402

EVAL_DIR = config.PROJECT_ROOT / "eval"
DELAY_SECONDS = 4          # pause between LLM calls to respect free-tier limits


def load_tests() -> list[dict]:
    return json.loads((EVAL_DIR / "test_set.json").read_text(encoding="utf-8"))


def normalise(text: str) -> str:
    return text.lower().replace(",", "").replace("**", "")


def contains_facts(answer: str, must_contain: list[list[str]]) -> bool:
    """Every group must match; within a group any alternative is enough."""
    a = normalise(answer)
    return all(any(normalise(alt) in a for alt in group) for group in must_contain)


def is_refusal(answer: str) -> bool:
    return "don't know" in answer.lower() or "do not know" in answer.lower()


def rank_of_expected(chunks, expected_docs) -> int | None:
    for rank, c in enumerate(chunks, 1):
        if c.document.metadata["doc_id"] in expected_docs:
            return rank
    return None


def retrieval_metrics(ranks: list) -> dict:
    return {
        "hit@1": mean(r == 1 for r in ranks),
        f"hit@{config.TOP_K}": mean(r is not None for r in ranks),
        "mrr": mean(1 / r if r else 0 for r in ranks),
    }


# ------------------------------------------------------------- LLM judge
JUDGE_PROMPT = """You are checking a RAG system for hallucinations.
Context:
{context}

Answer to check:
{answer}

Is EVERY factual claim in the answer supported by the context?
Reply with exactly one word: YES or NO."""


def judge_faithfulness(answer: str, chunks) -> bool:
    from src.generator import call_llm, format_context
    from langchain_core.messages import HumanMessage

    prompt = JUDGE_PROMPT.format(context=format_context(chunks), answer=answer)
    verdict, _ = call_llm([HumanMessage(content=prompt)])
    return verdict.strip().upper().startswith("YES")


# ---------------------------------------------------------------- runs
def run(retrieval_only: bool, judge: bool) -> None:
    from src.generator import answer as rag_answer

    tests = load_tests()
    rows = []
    for i, t in enumerate(tests, 1):
        chunks = retrieve(t["question"])
        rank = rank_of_expected(chunks, t["expected_docs"]) if t["expected_docs"] else None
        row = {"id": t["id"], "type": t["type"], "question": t["question"],
               "best_similarity": chunks[0].similarity, "rank": rank or ""}

        if not retrieval_only:
            result = rag_answer(t["question"])
            ans = result["answer"]
            row.update({"answer": " ".join(ans.split()), "model": result["model"],
                        "generation_s": result["generation_s"]})
            if t["type"] == "answerable":
                row["correct"] = contains_facts(ans, t["must_contain"])
            else:
                row["correct"] = is_refusal(ans)
            if judge and t["type"] == "answerable" and not is_refusal(ans):
                time.sleep(DELAY_SECONDS)
                row["faithful"] = judge_faithfulness(ans, result["chunks"])
            mark = "PASS" if row["correct"] else "FAIL"
            print(f"[{i:>2}/{len(tests)}] {t['id']} {mark}  {t['question']}")
            if result["model"] != "none (quality gate)":
                time.sleep(DELAY_SECONDS)
        else:
            print(f"[{i:>2}/{len(tests)}] {t['id']} rank={rank}  best={chunks[0].similarity:.3f}  {t['question']}")
        rows.append(row)

    write_outputs(rows, retrieval_only, judge)


def write_outputs(rows: list[dict], retrieval_only: bool, judge: bool) -> None:
    ans = [r for r in rows if r["type"] == "answerable"]
    neg = [r for r in rows if r["type"] != "answerable"]
    ret = retrieval_metrics([r["rank"] or None for r in ans])

    lines = ["# Evaluation summary", "",
             f"Test set: {len(rows)} questions ({len(ans)} answerable, "
             f"{sum(r['type'] == 'unanswerable' for r in rows)} unanswerable, "
             f"{sum(r['type'] == 'off_topic' for r in rows)} off-topic)",
             f"Settings: chunk {config.CHUNK_SIZE}/{config.CHUNK_OVERLAP}, top-k {config.TOP_K}, "
             f"threshold {config.MIN_SIMILARITY}, model {config.GEMINI_MODEL}", "",
             "## Retrieval (answerable questions)", "",
             "| Metric | Value |", "|---|---|"]
    lines += [f"| {k} | {v:.2f} |" for k, v in ret.items()]

    if not retrieval_only:
        lines += ["", "## Answers", "", "| Metric | Value |", "|---|---|",
                  f"| Answer correctness (answerable) | {sum(r['correct'] for r in ans)}/{len(ans)} |",
                  f"| Correct refusals (unanswerable + off-topic) | {sum(r['correct'] for r in neg)}/{len(neg)} |"]
        judged = [r for r in ans if "faithful" in r]
        if judge and judged:
            lines.append(f"| Faithfulness (LLM judge) | {sum(r['faithful'] for r in judged)}/{len(judged)} |")
        gen = [r["generation_s"] for r in rows if r.get("generation_s")]
        if gen:
            lines.append(f"| Avg generation time | {mean(gen):.2f} s |")

    lines += ["", "## Quality-gate threshold check (best similarity per question)", "",
              "| Group | Min | Max |", "|---|---|---|"]
    for label, group in [("answerable", ans),
                         ("unanswerable", [r for r in rows if r["type"] == "unanswerable"]),
                         ("off-topic", [r for r in rows if r["type"] == "off_topic"])]:
        sims = [r["best_similarity"] for r in group]
        lines.append(f"| {label} | {min(sims):.3f} | {max(sims):.3f} |")

    failures = [r for r in rows if r.get("correct") is False or (r["type"] == "answerable" and not r["rank"])]
    if failures:
        lines += ["", "## Failures to analyse", ""]
        lines += [f"- {r['id']}: {r['question']} (rank {r['rank'] or 'not found'})"
                  + (f" -> {r.get('answer', '')[:150]}" if "answer" in r else "") for r in failures]

    summary = "\n".join(lines) + "\n"
    (EVAL_DIR / "summary.md").write_text(summary, encoding="utf-8")
    with open(EVAL_DIR / "results.csv", "w", newline="", encoding="utf-8") as f:
        fields = list(dict.fromkeys(k for r in rows for k in r))
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("\n" + summary)
    print(f"Saved: {EVAL_DIR / 'summary.md'} and {EVAL_DIR / 'results.csv'}")


# --------------------------------------------------- chunk-size experiment
def chunk_experiment() -> None:
    """Rebuild a temporary in-memory index for several chunk sizes and
    compare retrieval quality. No API calls, nothing on disk is changed."""
    from langchain_chroma import Chroma
    from src import ingest
    from src.vectorstore import get_embeddings

    tests = [t for t in load_tests() if t["type"] == "answerable"]
    documents = ingest.load_documents()
    embeddings = get_embeddings()
    original = (config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    lines = ["| Chunk size / overlap | Chunks | Hit@1 | Hit@4 | MRR |", "|---|---|---|---|---|"]
    for size, overlap in [(300, 50), (500, 100), (800, 150), (1200, 200), (2000, 300)]:
        config.CHUNK_SIZE, config.CHUNK_OVERLAP = size, overlap
        chunks = ingest.split_documents(documents)
        store = Chroma(collection_name=f"exp_{size}", embedding_function=embeddings,
                       collection_metadata={"hnsw:space": "cosine"})
        store.add_documents(chunks)
        ranks = []
        for t in tests:
            docs = store.similarity_search(t["question"], k=config.TOP_K)
            ranks.append(next((i for i, d in enumerate(docs, 1)
                               if d.metadata["doc_id"] in t["expected_docs"]), None))
        m = retrieval_metrics(ranks)
        lines.append(f"| {size} / {overlap} | {len(chunks)} | {m['hit@1']:.2f} | "
                     f"{m[f'hit@{config.TOP_K}']:.2f} | {m['mrr']:.2f} |")
        print(lines[-1])
        store.delete_collection()
    config.CHUNK_SIZE, config.CHUNK_OVERLAP = original

    text = "# Chunk-size experiment (retrieval only)\n\n" + "\n".join(lines) + "\n"
    (EVAL_DIR / "chunk_experiment.md").write_text(text, encoding="utf-8")
    print(f"\nSaved: {EVAL_DIR / 'chunk_experiment.md'}")


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate the FinPay RAG system")
    p.add_argument("--retrieval-only", action="store_true", help="skip the LLM (no API calls)")
    p.add_argument("--judge", action="store_true", help="add LLM-as-judge faithfulness check")
    p.add_argument("--chunk-experiment", action="store_true", help="compare chunk sizes")
    a = p.parse_args()
    if a.chunk_experiment:
        chunk_experiment()
    else:
        run(a.retrieval_only, a.judge)


if __name__ == "__main__":
    main()
