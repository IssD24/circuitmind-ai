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

## Understanding Benchmark Results

The benchmark runner reports two main stages:

- **Before**: whether the original benchmark produced compiler diagnostics.
- **Fix Result**: whether CircuitMind's fix loop ended in a compiling state.

Some benchmarks are compiler-error benchmarks. These should fail before repair because Arduino CLI can detect the issue.

Other benchmarks are logic/static-analysis benchmarks. These may compile successfully even though the firmware still contains a bug. For those cases, a `pass` result means only that the compiler accepted the code. It does not mean the program is logically correct.

Examples:

- `broken_01_missing_semicolon` fails before repair because the compiler detects the syntax error.
- `broken_07_incorrect_pin` may compile because the compiler does not know that `-1` is not a valid practical output pin.
- `broken_10_forgotten_serial_begin` may compile because using `Serial.println` without `Serial.begin` is a runtime/logic issue, not a syntax error.

Future benchmark scoring should use `benchmark.json` metadata so CircuitMind can evaluate both compiler failures and logic-level firmware issues.

## Project description
## Features
## Architecture
## Usage commands

## Current limitations
## Next steps

### Running the Benchmark Suite

Run all firmware benchmarks with:

```powershell
python benchmarks/run_all.py
benchmark_results/scoreboard.md


## Step 3: Add/adjust limitations

Make sure your limitations include this:

```markdown
## Current Limitations

- Live LLM repair requires a valid Anthropic API key and available credits.
- Some benchmarks compile successfully even though they contain logic bugs.
- The current benchmark runner treats a compiling final state as fixed.
- Logic/static benchmarks require metadata-aware scoring instead of compiler-only scoring.
- Third-party library failures may require Docker image updates or dependency installation rather than source-code patches.
- Hardware upload support is not implemented yet.