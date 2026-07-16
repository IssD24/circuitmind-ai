from pathlib import Path

from circuitmind.build import build_project
from circuitmind.parse import parse_arduino_cli_errors

result = build_project(Path("benchmarks/broken_01_missing_semicolon"))

combined_output = result.stderr + "\n" + result.stdout
diagnostics = parse_arduino_cli_errors(combined_output)

for diagnostic in diagnostics:
    print(diagnostic)