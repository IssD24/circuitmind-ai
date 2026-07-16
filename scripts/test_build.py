from pathlib import Path
from circuitmind.build import build_project

result = build_project(Path("benchmarks/broken_01_missing_semicolon"))

print("Exit code:", result.exit_code)
print("STDOUT:")
print(result.stdout)
print("STDERR:")
print(result.stderr)