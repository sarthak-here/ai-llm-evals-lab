from dataclasses import dataclass
from typing import List


@dataclass
class EvalCase:
    prompt: str
    expected: str


def exact_match_score(pred: str, expected: str) -> float:
    return 1.0 if pred.strip() == expected.strip() else 0.0


def run_eval(cases: List[EvalCase], model_outputs: List[str]) -> dict:
    if len(cases) != len(model_outputs):
        raise ValueError("cases and outputs length mismatch")

    scores = [exact_match_score(out, case.expected) for case, out in zip(cases, model_outputs)]
    avg = sum(scores) / len(scores) if scores else 0.0
    return {"cases": len(cases), "exact_match": round(avg, 4)}
