# CircuitMind AI

CircuitMind AI is a human-in-the-loop developer tool that diagnoses and patches Arduino/ESP32 firmware build failures.

## Goal

The tool will:
1. Run an Arduino/ESP32 build inside Docker.
2. Capture compiler errors.
3. Parse errors into structured diagnostics.
4. Ask an LLM to explain the likely issue and propose a patch.
5. Show the patch to the user for approval.
6. Apply the patch and rebuild.
7. Generate a final Markdown report.

## Current Status

Day 1 setup:
- Repo created
- Project structure created
- Docker environment planned
- Diagnostic schema drafted