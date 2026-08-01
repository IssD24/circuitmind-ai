# CircuitMind AI

CircuitMind AI is a human-in-the-loop developer tool that diagnoses and patches Arduino/ESP32 firmware build failures.

## Goal

The tool will:

1. Run an Arduino/ESP32 build inside Docker.
2. Capture compiler errors.
3. Parse errors into structured diagnostics.
4. Ask an LLM to explain the likely issue and propose a patch.
5. Show the patch to the user for approval.
6. Apply the patch to a copied workspace and rebuild.
7. Generate a final Markdown report.

## Current Status

CircuitMind currently supports:

- Docker-backed Arduino firmware compilation
- Compiler diagnostic parsing
- Static-analysis support with cppcheck
- LLM-based diagnosis flow
- Patch validation guardrails
- Safe copied-workspace patch application
- Multi-iteration fix loop
- Session logging with diagnosis JSON, patch diffs, build output, and Markdown reports
- Firmware benchmark suite with compiler-error and logic/static-analysis examples

Live LLM repair currently requires a valid Anthropic API key and available credits.

## Features

- Docker-backed Arduino/ESP32 firmware builds
- Structured compiler diagnostic parsing
- Static-analysis support with cppcheck
- LLM diagnosis stage for root-cause analysis
- Patch validation guardrails
- Safe copied-workspace patch application
- Multi-iteration fix loop
- Session report generation
- Benchmark suite for compiler errors, missing dependencies, and firmware logic issues

## Architecture

```text
Source firmware
→ Docker build
→ Compiler output
→ Diagnostic parser
→ LLM diagnosis
→ Patch validation
→ Copied workspace
→ Patch application
→ Rebuild
→ Session report
```

## Usage Commands

From the project root, set `PYTHONPATH`:

```powershell
$env:PYTHONPATH="src"
```

Analyze a benchmark:

```powershell
python -m circuitmind.cli analyze benchmarks/broken_01_missing_semicolon --output analysis_01.json
```

Diagnose a benchmark:

```powershell
python -m circuitmind.cli diagnose benchmarks/broken_01_missing_semicolon
```

Run the fix loop:

```powershell
python -m circuitmind.cli fix benchmarks/broken_01_missing_semicolon --max-iterations 3
```

Run all tests:

```powershell
python -m pytest
```

## Running the Benchmark Suite

Run all firmware benchmarks with:

```powershell
python benchmarks/run_all.py
```

This prints a terminal scoreboard and writes a generated Markdown scoreboard to:

```text
benchmark_results/scoreboard.md
```

The `benchmark_results/` folder is ignored by Git because it contains generated output.

## Benchmark Results

| Benchmark | Before | Fix Result | Notes |
|---|---|---|---|
| broken_01_missing_semicolon | Fail | Not fixed | LLM unavailable: API key/credits required |
| broken_02_wrong_wire_signature | Fail | Not fixed | LLM unavailable: API key/credits required |
| broken_03_missing_include | Fail | Not fixed | LLM unavailable: API key/credits required |
| broken_04_wrong_api | Fail | Not fixed | LLM unavailable: API key/credits required |
| broken_05_missing_include | Fail | Not fixed | LLM unavailable: API key/credits required |
| broken_06_missing_library | Fail | Not fixed | Missing third-party library / LLM unavailable |
| broken_07_incorrect_pin | Pass | Fixed | Logic issue; compiler does not catch |
| broken_08_wrong_function_signature | Fail | Not fixed | LLM unavailable: API key/credits required |
| broken_09_deprecated_api | Pass | Fixed | Warning/static issue; compiler does not catch |
| broken_10_forgotten_serial_begin | Pass | Fixed | Logic issue; compiler does not catch |

## Understanding Benchmark Results

The benchmark runner reports two main stages:

- **Before**: whether the original benchmark produced compiler diagnostics.
- **Fix Result**: whether CircuitMind's fix loop ended in a compiling state.

Some benchmarks are compiler-error benchmarks. These should fail before repair because Arduino CLI can detect the issue.

Other benchmarks are logic/static-analysis benchmarks. These may compile successfully even though the firmware still contains a bug. For those cases, a `Pass` result means only that the compiler accepted the code. It does not mean the program is logically correct.

Examples:

- `broken_01_missing_semicolon` fails before repair because the compiler detects the syntax error.
- `broken_07_incorrect_pin` may compile because the compiler does not know that `-1` is not a valid practical output pin.
- `broken_10_forgotten_serial_begin` may compile because using `Serial.println` without `Serial.begin` is a runtime/logic issue, not a syntax error.

Future benchmark scoring should use `benchmark.json` metadata so CircuitMind can evaluate both compiler failures and logic-level firmware issues.

## Current Limitations

- Live LLM repair requires a valid Anthropic API key and available credits.
- Some benchmarks compile successfully even though they contain logic bugs.
- The current benchmark runner treats a compiling final state as fixed.
- Logic/static benchmarks require metadata-aware scoring instead of compiler-only scoring.
- Third-party library failures may require Docker image updates or dependency installation rather than source-code patches.
- Hardware upload support is not implemented yet.
- The patch approval flow is planned but not fully built yet.

## Next Steps

- Add Anthropic API credits and test live repair on compiler-error benchmarks.
- Improve benchmark scoring so logic/static benchmarks are not marked as fixed just because they compile.
- Use `benchmark.json` metadata during benchmark evaluation.
- Add explicit user approval before applying generated patches.
- Improve before/after error-count reporting.
- Add hardware upload support later.