# ai-llm-evals-lab

A lightweight lab for running reproducible LLM evals locally.

## Features
- Exact-match scoring (`0.0` to `1.0`)
- Simple CLI runner
- Small sample dataset (3 cases)
- Large sample dataset (1000 cases)
- Pytest test suite
- GitHub Actions CI

## Repository structure
- `eval_runner.py` — eval engine + CLI
- `rubrics.py` — qualitative rubric references
- `datasets/sample_cases.jsonl` — 3 demo cases
- `datasets/sample_outputs.txt` — outputs for 3 demo cases
- `datasets/sample_cases_1000.jsonl` — 1000 sample cases
- `datasets/sample_outputs_1000.txt` — outputs for 1000 sample cases
- `tests/test_eval_runner.py` — unit tests

## Quickstart
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

## Run tests
```bash
python -m pytest -q
```

## CLI usage
```bash
python eval_runner.py --cases <path-to-cases.jsonl> --outputs <path-to-outputs.txt> [--pretty]
```

## Example: 3-case run
```bash
python eval_runner.py --cases datasets/sample_cases.jsonl --outputs datasets/sample_outputs.txt --pretty
```

Expected:
```json
{
  "cases": 3,
  "exact_match": 0.6667
}
```

## Example: 1000-case run
```bash
python eval_runner.py --cases datasets/sample_cases_1000.jsonl --outputs datasets/sample_outputs_1000.txt --pretty
```

Expected:
```json
{
  "cases": 1000,
  "exact_match": 0.925
}
```

## Data format
### Cases file (`.jsonl`)
One JSON object per line:
- `prompt` (string)
- `expected` (string)

Example:
```json
{"prompt":"Capital of France?","expected":"Paris"}
```

### Outputs file (`.txt`)
- One model output per line
- Order must match the cases file

## Notes
- `run_eval` raises `ValueError` if case/output lengths mismatch.
- Exact match is whitespace-trimmed and case-sensitive.
