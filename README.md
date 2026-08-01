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

## Benchmark Results

| Benchmark | Before | Fix Result | Notes |
|---|---|---|---|
| broken_01_missing_semicolon | Fail | Not fixed | LLM credits blocked |
| broken_02_wrong_wire_signature | Fail | Not fixed | LLM credits blocked |
| broken_03_missing_include | Fail | Not fixed | LLM credits blocked |
| broken_04_wrong_api | Fail | Not fixed | LLM credits blocked |
| broken_05_missing_include | Fail | Not fixed | LLM credits blocked |
| broken_06_missing_library | Fail | Not fixed | Missing third-party library |
| broken_07_incorrect_pin | Pass | Fixed | Logic issue; compiler does not catch |
| broken_08_wrong_function_signature | Fail | Not fixed | LLM credits blocked |
| broken_09_deprecated_api | Pass | Fixed | Warning/static issue; compiler does not catch |
| broken_10_forgotten_serial_begin | Pass | Fixed | Logic issue; compiler does not catch |

## Project description
## Features
## Architecture
## Usage commands

## Current limitations
## Next steps