import subprocess

commands = [
    ["python", "eval_runner.py", "--cases", "datasets/sample_cases.jsonl", "--outputs", "datasets/sample_outputs.txt", "--pretty"],
    ["python", "eval_runner.py", "--cases", "datasets/sample_cases_1000.jsonl", "--outputs", "datasets/sample_outputs_1000.txt", "--pretty"],
]

for cmd in commands:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
