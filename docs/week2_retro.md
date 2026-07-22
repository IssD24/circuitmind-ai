# Week 2 Retro

## What works

- Docker-backed Arduino build:
  - CircuitMind can run Arduino CLI inside Docker.
  - Broken benchmark sketches can be compiled through the CLI.

- Diagnostic parser:
  - Arduino compiler output can be parsed into structured diagnostics.
  - Diagnostics include file, line, column, severity, message, and raw output.

- Static analysis:
  - CircuitMind can run cppcheck through the analysis pipeline.
  - The analyze command combines compiler diagnostics and static-analysis style output.

- LLM diagnosis stage:
  - diagnose.py builds a prompt using source code and diagnostics.
  - The CLI diagnose command is connected.
  - The live Anthropic API call reaches the API, but it is currently blocked by low API credits.

- Validation and guardrails:
  - CircuitMind validates diagnosis output.
  - It checks confidence range, malformed patches, oversized patches, and patches referencing files not included in the prompt.

- Failure handling:
  - Arduino builds now have a timeout.
  - Clean projects are handled without calling the LLM.
  - LLM/API failures return a clean DiagnosisResult instead of crashing.

## What does not work yet

- Live LLM diagnosis cannot be fully tested until Anthropic API credits are added.
- Patch application has not been implemented yet.
- CircuitMind does not yet automatically apply a patch, rebuild, and retry.
- Validation exists, but patch validation is still basic.

## Biggest technical issue

The biggest issue this week was connecting the AI diagnosis stage safely. The code was able to reach Anthropic, but the request failed because the API account had insufficient credits. This showed that the API wiring was likely correct, but live testing is currently blocked by billing.

## What I learned

- How to run Arduino CLI through Docker.
- How to parse compiler errors into structured diagnostics.
- How to design an LLM prompt contract.
- Why LLM output needs validation before trusting patches.
- How to handle failure cases instead of letting the program crash.

## What I will fix in Week 3

1. Add API credits and test live diagnosis on all broken benchmarks.
2. Improve validation for patch format and edited files.
3. Start implementing patch application.
4. Add rebuild-after-patch behavior.
5. Track which benchmarks pass from diagnosis to repaired build.