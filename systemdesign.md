# AI LLM Evals Lab — System Design

## What It Does
A structured evaluation framework for Large Language Models. Given a dataset of test cases and a set of rubrics, it runs models against the cases, scores the outputs using automated rubric checkers and an LLM-as-judge, and produces a detailed evaluation report with pass/fail rates and failure analysis.

---

## Architecture

```
Input
  datasets/sample_cases.jsonl    (test cases)
  rubrics.py                     (scoring criteria)
        |
        v
+--------------------------------------------------+
|            eval_runner.py                        |
|  - Load test cases from JSONL                    |
|  - For each case:                                |
|    1. Build prompt from case template            |
|    2. Call LLM (configurable model)              |
|    3. Get raw output                             |
|    4. Score against rubrics                      |
|  - Aggregate: pass rate, avg score, failures     |
|  - Write: results report                         |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|            rubrics.py                            |
|  Scoring dimensions:                             |
|  - Correctness  (exact match or fuzzy)           |
|  - Format       (JSON valid, length constraints) |
|  - Faithfulness (answer grounded in context)     |
|  - Safety       (no harmful content)             |
|  - LLM-as-judge (GPT grades open-ended answers)  |
+--------------------------------------------------+
        |
        v
  Evaluation report:
    Per-case: input, output, scores, pass/fail
    Aggregate: accuracy, rubric breakdown, failures
```

---

## Input Format

```jsonl
// datasets/sample_cases.jsonl
{"id": "001", "input": "Summarize this article: ...",
 "expected": "...", "rubrics": ["correctness", "length"]}
{"id": "002", "input": "Translate to French: Hello",
 "expected": "Bonjour", "rubrics": ["exact_match"]}
```

---

## Data Flow

```
sample_cases.jsonl
        |
  eval_runner.py loads cases (json.loads per line)
        |
  For each test case:
    Build prompt from case["input"]
    Call LLM API (OpenAI / Anthropic / local)
    Capture: raw_output, latency_ms, token_count
        |
  Score with rubrics.py:
    exact_match:    output.strip() == expected.strip()
    fuzzy_match:    token overlap ratio >= threshold
    json_valid:     json.loads(output) succeeds
    length_check:   len(output) within [min, max]
    llm_as_judge:   send (question, answer, criteria)
                    to judge model -> score 1-5 + reasoning
    safety:         check for harmful content patterns
        |
  Aggregate per rubric:
    pass_rate = passed / total
    avg_score = mean(scores)
    failures  = cases where any rubric failed
        |
  Output:
    Console: summary table
    datasets/sample_outputs.txt: raw outputs
    Structured report: per-case breakdown
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| JSONL test case format | Streaming-friendly; can add cases without parsing entire file |
| Rubric separation from runner | Rubrics can be updated without changing evaluation logic |
| LLM-as-judge for open-ended | Human-equivalent scoring for answers with no single correct answer |
| Latency + token tracking | Eval is not just about accuracy; cost and speed matter for production LLMs |
| CI integration (GitHub Actions) | Eval suite runs on every PR to catch model regressions automatically |

---

## Interview Conclusion

This project addresses a fundamental problem in LLM development: how do you know if a model change made things better or worse? Traditional unit tests fail because LLM outputs are non-deterministic and open-ended. The evaluation framework solves this with a layered scoring approach: cheap automated checks (exact match, JSON validity) catch clear failures instantly, while the LLM-as-judge handles the nuanced cases where a paraphrase of the correct answer should still pass. The JSONL format is a deliberate choice matching the industry standard used by OpenAI Evals, Anthropic's evaluation suite, and the Eleuther AI Harness. The CI integration is what elevates this from a script to a real eval system: every code change triggers the eval suite, and regressions are caught before merge. If I were scaling this, I would add confidence intervals around pass rates (since LLM outputs vary across runs), implement a baseline comparison view (model A vs model B side by side), and add human annotation workflow for disputed cases.
