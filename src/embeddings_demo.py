"""Small experiment that shows what embeddings do.

    python -m src.embeddings_demo

It embeds a few sentences and prints how similar each one is to a
question (cosine similarity: 1.0 = same meaning, around 0 = unrelated),
sorted from most to least similar.
"""
from src.vectorstore import get_embeddings

QUESTION = "How long do I have to dispute a card payment?"
SENTENCES = [
    "Customers must raise a chargeback within 60 days of the transaction.",
    "My card was stolen, what should I do?",
    "How do I reset my password?",
    "Merchants are paid on the next business day.",
]


def cosine(a, b):
    # vectors are normalised to length 1, so the dot product IS the cosine similarity
    return sum(x * y for x, y in zip(a, b))


def main():
    emb = get_embeddings()
    q_vec = emb.embed_query(QUESTION)
    vectors = emb.embed_documents(SENTENCES)
    print(f"Each sentence -> vector of {len(q_vec)} numbers")
    print(f"First 5 numbers of the question vector: {[round(v, 3) for v in q_vec[:5]]}\n")

    scored = sorted(((cosine(q_vec, v), s) for s, v in zip(SENTENCES, vectors)), reverse=True)
    print(f'Similarity to: "{QUESTION}"')
    for score, text in scored:
        print(f"  {score:.3f}  {text}")


if __name__ == "__main__":
    main()
