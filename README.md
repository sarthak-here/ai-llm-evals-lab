# ai-llm-evals-lab

Lightweight evaluation starter for prompt/model experiments with reproducible local runs.

## What it does
- Computes **exact-match** score over evaluation cases
- Supports file-based runs via CLI
- Includes sample dataset + outputs
- Includes CI + tests

## Project structure
- `eval_runner.py` — core eval logic + CLI
- `rubrics.py` — qualitative rubric prompts
- `datasets/sample_cases.jsonl` — sample eval cases
- `datasets/sample_outputs.txt` — sample model outputs
- `tests/test_eval_runner.py` — unit tests

## Setup
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
pytest -q
```

## Run sample eval
```bash
python eval_runner.py --cases datasets/sample_cases.jsonl --outputs datasets/sample_outputs.txt --pretty
```

Expected output:
```json
{
  "cases": 3,
  "exact_match": 0.6667
}
```

## Data format
### Cases (`.jsonl`)
One JSON object per line with:
- `prompt` (string)
- `expected` (string)

Example line:
```json
{"prompt":"Capital of France?","expected":"Paris"}
```

### Outputs (`.txt`)
One model output per line, same order as cases.
