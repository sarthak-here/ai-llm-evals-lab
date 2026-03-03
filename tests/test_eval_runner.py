import json
from pathlib import Path

import pytest

from eval_runner import EvalCase, exact_match_score, load_cases_jsonl, load_outputs_txt, run_eval


def test_exact_match_score_trimmed_match():
    assert exact_match_score(" Paris ", "Paris") == 1.0


def test_exact_match_score_mismatch():
    assert exact_match_score("blue", "Blue") == 0.0


def test_run_eval_basic():
    cases = [EvalCase(prompt="p1", expected="a"), EvalCase(prompt="p2", expected="b")]
    outputs = ["a", "x"]
    result = run_eval(cases, outputs)
    assert result == {"cases": 2, "exact_match": 0.5}


def test_run_eval_length_mismatch_raises():
    with pytest.raises(ValueError):
        run_eval([EvalCase(prompt="p1", expected="a")], ["a", "b"])


def test_load_cases_and_outputs(tmp_path: Path):
    cases_file = tmp_path / "cases.jsonl"
    outputs_file = tmp_path / "outputs.txt"

    cases_file.write_text(
        "\n".join([
            json.dumps({"prompt": "p1", "expected": "e1"}),
            json.dumps({"prompt": "p2", "expected": "e2"}),
        ])
        + "\n",
        encoding="utf-8",
    )
    outputs_file.write_text("e1\nwrong\n", encoding="utf-8")

    cases = load_cases_jsonl(cases_file)
    outputs = load_outputs_txt(outputs_file)

    assert len(cases) == 2
    assert outputs == ["e1", "wrong"]
