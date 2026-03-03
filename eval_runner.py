from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class EvalCase:
    prompt: str
    expected: str


def exact_match_score(pred: str, expected: str) -> float:
    return 1.0 if pred.strip() == expected.strip() else 0.0


def run_eval(cases: List[EvalCase], model_outputs: List[str]) -> Dict[str, float]:
    if len(cases) != len(model_outputs):
        raise ValueError("cases and outputs length mismatch")

    scores = [exact_match_score(out, case.expected) for case, out in zip(cases, model_outputs)]
    avg = sum(scores) / len(scores) if scores else 0.0
    return {"cases": len(cases), "exact_match": round(avg, 4)}


def load_cases_jsonl(path: str | Path) -> List[EvalCase]:
    cases: List[EvalCase] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if "prompt" not in record or "expected" not in record:
                raise ValueError(f"Invalid case on line {line_no}: expected keys 'prompt' and 'expected'")
            cases.append(EvalCase(prompt=str(record["prompt"]), expected=str(record["expected"])))
    return cases


def load_outputs_txt(path: str | Path) -> List[str]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run exact-match LLM evals from local files.")
    parser.add_argument("--cases", required=True, help="Path to JSONL with fields: prompt, expected")
    parser.add_argument("--outputs", required=True, help="Path to TXT with one model output per line")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    args = parser.parse_args()

    cases = load_cases_jsonl(args.cases)
    outputs = load_outputs_txt(args.outputs)
    result = run_eval(cases, outputs)

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
