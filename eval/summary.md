# Evaluation summary

Test set: 22 questions (17 answerable, 3 unanswerable, 2 off-topic)
Settings: chunk 800/150, top-k 4, threshold 0.25, model gemini-3.5-flash-lite

## Retrieval (answerable questions)

| Metric | Value |
|---|---|
| hit@1 | 0.94 |
| hit@4 | 1.00 |
| mrr | 0.97 |

## Answers

| Metric | Value |
|---|---|
| Answer correctness (answerable) | 17/17 |
| Correct refusals (unanswerable + off-topic) | 5/5 |
| Faithfulness (LLM judge) | 17/17 |
| Avg generation time | 0.96 s |

## Quality-gate threshold check (best similarity per question)

| Group | Min | Max |
|---|---|---|
| answerable | 0.404 | 0.748 |
| unanswerable | 0.513 | 0.567 |
| off-topic | 0.067 | 0.086 |
