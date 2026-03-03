.PHONY: test sample sample1000

test:
	python -m pytest

sample:
	python eval_runner.py --cases datasets/sample_cases.jsonl --outputs datasets/sample_outputs.txt --pretty

sample1000:
	python eval_runner.py --cases datasets/sample_cases_1000.jsonl --outputs datasets/sample_outputs_1000.txt --pretty
