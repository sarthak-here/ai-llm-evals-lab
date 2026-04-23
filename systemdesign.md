# AI LLM Evals Lab - System Design

## What It Does
A structured evaluation framework for Large Language Models. Given a JSONL dataset of
test cases and a rubrics module, it runs models against the cases, scores outputs using
automated rubric checkers and an LLM-as-judge, and produces a detailed evaluation report.

---

## Architecture

```
Input
  datasets/sample_cases.jsonl   (test cases)
  rubrics.py                    (scoring criteria)
        |
        v
+--------------------------------------------------+
|            eval_runner.py                        |
|  - Load test cases (JSONL, streaming)            |
|  - For each case:                                |
|    1. Build prompt from case template            |
|    2. Call LLM (configurable: OpenAI / Anthropic)|
|    3. Capture output + latency + token count     |
|    4. Score against rubrics.py                   |
|  - Aggregate: pass_rate, avg_score, failures     |
|  - Write evaluation report                       |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|            rubrics.py                            |
|  Scoring dimensions:                             |
|  - exact_match   (string equality)               |
|  - fuzzy_match   (token overlap ratio)           |
|  - json_valid    (output parses as JSON)         |
|  - length_check  (within [min, max] chars)       |
|  - llm_as_judge  (GPT scores open-ended answers) |
|  - safety        (no harmful content patterns)   |
+--------------------------------------------------+
        |
        v
  Console summary table
  datasets/sample_outputs.txt  (raw LLM outputs)
  Full per-case report (input, output, scores)
```

---

## Input Format

```
// datasets/sample_cases.jsonl  (one JSON object per line)
{"id":"001","input":"Summarize: ...","expected":"...","rubrics":["correctness","length"]}
{"id":"002","input":"Translate to French: Hello","expected":"Bonjour","rubrics":["exact_match"]}
```

---

## Data Flow

```
sample_cases.jsonl
        |
  eval_runner.py loads line by line (streaming, memory-efficient)
        |
  For each test case:
    Build prompt from case["input"]
    Call LLM API -> capture raw_output, latency_ms, token_count
        |
  Score with rubrics.py:
    exact_match:    output.strip() == expected.strip()
    fuzzy_match:    token overlap ratio >= threshold
    json_valid:     json.loads(output) succeeds
    length_check:   len(output) within [min, max]
    llm_as_judge:   send (question, answer, criteria) to judge LLM
                    -> score 1-5 + reasoning
    safety:         check for harmful content patterns
        |
  Aggregate per rubric:
    pass_rate = passed_count / total_count
    avg_score = mean(scores where applicable)
    failures  = cases where any rubric failed
        |
  Output report + raw responses saved
```

---

## Key Design Decisions

| Decision                       | Reason                                           |
|--------------------------------|--------------------------------------------------|
| JSONL format                   | Streaming-friendly; matches OpenAI Evals standard|
| Rubrics separate from runner   | Rubrics can be updated without touching eval logic|
| LLM-as-judge for open-ended    | Human-equivalent scoring for no-single-answer Qs |
| Latency + token count tracking | Eval is not just accuracy; cost and speed matter  |
| CI integration (GitHub Actions)| Eval suite runs on every PR; catches regressions  |

---

## Interview Conclusion

This framework addresses the fundamental LLM development problem: how do you know if a
model change made things better or worse? Traditional unit tests fail because LLM outputs
are non-deterministic and open-ended. The layered scoring approach solves this: cheap
automated checks (exact match, JSON validity) catch clear failures instantly, while
LLM-as-judge handles nuanced cases where a paraphrase of the correct answer should still
pass. The JSONL format matches the industry standard used by OpenAI Evals, Anthropic's
evaluation suite, and the Eleuther AI Harness. CI integration elevates this from a
script to a real eval system: every code change triggers the suite and regressions are
caught before merge. Scaling: add confidence intervals around pass rates, a side-by-side
model comparison view, and a human annotation workflow for disputed cases.
