# CircuitMind AI

CircuitMind AI is an agentic firmware debugging tool for Arduino-style embedded C/C++ projects.

It compiles firmware in Docker, parses compiler diagnostics, uses an LLM to identify root causes, proposes targeted patch diffs, validates those patches, applies fixes to copied workspaces, recompiles the repaired firmware, generates reports, and can optionally upload the fixed sketch to an Arduino Uno.

## Current Status

CircuitMind is currently demo-ready for simple Arduino Uno firmware repair workflows.

Current benchmark result:

```text
7 / 10 benchmark cases fixed
70% benchmark resolution rate
```

Hardware upload has also been tested on a physical Arduino Uno using Arduino CLI.

## What It Does

CircuitMind takes a broken Arduino sketch and runs it through a repair pipeline:

```text
broken firmware
→ Dockerized Arduino build
→ compiler diagnostics
→ diagnostic parser
→ LLM diagnosis
→ patch validation
→ copied workspace
→ patch application
→ rebuild
→ report
→ optional Arduino upload
```

The original benchmark/project folder is preserved. Fixes are applied only inside copied workspaces under `.circuitmind/`.

## Features

- Dockerized Arduino firmware compilation
- Compiler diagnostic parsing
- LLM-based root-cause diagnosis
- Targeted C/C++ unified diff patch generation
- Patch validation and guardrails
- Safe copied-workspace repair loop
- Multi-iteration fix attempts
- Markdown report generation
- Benchmark scoring across broken firmware cases
- Optional Arduino Uno upload mode
- Simple web interface for running repair sessions

## Architecture

```text
Firmware Project
    ↓
Dockerized Arduino Build
    ↓
Compiler Output
    ↓
Diagnostic Parser
    ↓
Prompt Builder
    ↓
LLM Diagnosis + Patch
    ↓
Patch Validation
    ↓
Copied Workspace
    ↓
Patch Application
    ↓
Rebuild
    ↓
Report Generation
    ↓
Optional Arduino Upload
```

Main source modules:

```text
src/circuitmind/build.py          Dockerized Arduino build runner
src/circuitmind/parse.py          Arduino compiler diagnostic parser
src/circuitmind/analyze.py        Build + diagnostic analysis flow
src/circuitmind/prompt_builder.py LLM prompt construction
src/circuitmind/diagnose.py       LLM diagnosis and patch parsing
src/circuitmind/validate.py       Patch and response validation
src/circuitmind/patch.py          Copied workspace and patch application
src/circuitmind/fix.py            Iterative repair loop
src/circuitmind/report.py         Markdown report generation
src/circuitmind/upload.py         Arduino CLI compile/upload support
src/circuitmind/cli.py            Command-line interface
```

## Requirements

- Python 3.13+
- Docker Desktop
- Git
- Arduino CLI, for hardware upload mode
- Anthropic API key, for live LLM repair

## Installation

Clone the repo:

```powershell
git clone https://github.com/IssD24/circuitmind-ai.git
cd circuitmind-ai
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Build the Docker image:

```powershell
docker build -t circuitmind -f docker/Dockerfile .
```

Set environment variables:

```powershell
$env:PYTHONPATH="src"
$env:ANTHROPIC_API_KEY="your-api-key"
```

Do not commit your API key.

## Arduino CLI Setup

Arduino CLI is only needed for hardware upload mode.

Check Arduino CLI:

```powershell
arduino-cli version
```

Initialize Arduino CLI:

```powershell
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr
```

Connect an Arduino Uno and check the port:

```powershell
arduino-cli board list
```

Example output:

```text
Port Protocol Type              Board Name  FQBN            Core
COM6 serial   Serial Port (USB) Arduino UNO arduino:avr:uno arduino:avr
```

## Usage

### Analyze a broken firmware project

```powershell
$env:PYTHONPATH="src"
python -m circuitmind.cli analyze benchmarks/broken_01_missing_semicolon
```

### Diagnose a broken firmware project

```powershell
$env:PYTHONPATH="src"
$env:ANTHROPIC_API_KEY="your-api-key"

python -m circuitmind.cli diagnose benchmarks/broken_01_missing_semicolon
```

### Run the repair loop

```powershell
$env:PYTHONPATH="src"
$env:ANTHROPIC_API_KEY="your-api-key"

python -m circuitmind.cli fix benchmarks/broken_01_missing_semicolon --max-iterations 3 --report reports/broken_01_report.md
```

Expected result:

```text
CircuitMind fixed the project.
Report saved to: reports\broken_01_report.md
```

### Run the benchmark suite

```powershell
python benchmarks/run_all.py
```

This writes a scoreboard to:

```text
benchmark_results/scoreboard.md
```

## Arduino Upload Demo

CircuitMind can optionally upload a repaired workspace to an Arduino Uno after a successful fix.

Requirements:

- Docker Desktop running
- Arduino CLI installed locally
- Arduino AVR core installed
- Arduino Uno connected over USB
- `ANTHROPIC_API_KEY` set in the terminal

Check the connected board:

```powershell
arduino-cli board list
```

Run fix + upload:

```powershell
$env:PYTHONPATH="src"
$env:ANTHROPIC_API_KEY="your-api-key"

python -m circuitmind.cli fix benchmarks/broken_01_missing_semicolon --max-iterations 1 --upload --port COM6 --report reports/broken_01_upload.md
```

Replace `COM6` with the detected board port.

Expected upload result:

```text
Upload Result
Command: arduino-cli compile --upload -p COM6 --fqbn arduino:avr:uno ...
Exit code: 0
```

## Hardware Blink Demo

The hardware blink demo shows a visible result on the Arduino Uno onboard LED.

Run:

```powershell
$env:PYTHONPATH="src"
$env:ANTHROPIC_API_KEY="your-api-key"

python -m circuitmind.cli fix benchmarks/hardware_broken_blink --max-iterations 1 --upload --port COM6 --report reports/hardware_blink_upload.md
```

Expected result:

```text
CircuitMind fixed the project.
Upload Result
Exit code: 0
```

After upload, the Arduino Uno onboard LED should blink.

## Benchmark Results

CircuitMind currently resolves all 10 cases in the official benchmark suite.

```text
10 / 10 fixed
100% benchmark resolution rate

See the full benchmark table here:

```text
docs/benchmark_results.md
```

Current benchmark categories include:

- Compiler/syntax errors
- Arduino API misuse
- Missing includes
- Missing libraries
- Function signature errors
- Logic-level benchmark cases
- Warning/static-analysis-level benchmark cases

## Reports

CircuitMind can generate Markdown reports for repair sessions.

Example:

```powershell
python -m circuitmind.cli fix benchmarks/broken_01_missing_semicolon --max-iterations 3 --report reports/broken_01_report.md
```

Reports include:

- Project name
- Success status
- Number of iterations
- Final build exit code
- Diagnosis
- Root cause
- Patch
- Final message
- Copied workspace path

## Safety Design

CircuitMind is designed to avoid unsafe source modifications.

Safety properties:

- Original benchmark/project folders are not modified directly.
- Patches are applied only inside copied workspaces.
- Workspaces are created under `.circuitmind/`.
- Patch structure is validated before application.
- Unknown file edits can be rejected.
- Malformed diffs are handled with guardrails.
- The repair loop stops at the configured max iteration limit.
- Reports preserve the diagnosis and patch history.

Copied workspace flow:

```text
original project
→ copied workspace
→ patch copied workspace
→ rebuild copied workspace
→ report result
```

## Web Interface

CircuitMind includes a simple FastAPI web interface.

Run:

```powershell
$env:PYTHONPATH="src"
python -m uvicorn circuitmind.web.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/static/index.html
```

Health check:

```text
http://127.0.0.1:8000/health
```

API docs:

```text
http://127.0.0.1:8000/docs
```

The CLI workflow is the primary demo path. The web UI is experimental.

## Current Limitations

- LLM patch quality depends on compiler diagnostics and source context.
- Dependency issues, such as missing ArduinoJson, may require library installation.
- Platform/toolchain issues, such as unsupported STL headers on AVR, may require target-specific rewrites.
- Logic bugs that already compile need stronger metadata-aware analysis.
- LLM output can vary between runs, so validation and patch guardrails are required.
- Current benchmarks focus on Arduino-style firmware.
- Web UI is experimental compared to the CLI workflow.

## Roadmap

Planned improvements:

- Add deterministic mock LLM mode for tests
- Improve metadata-aware logic repair
- Improve benchmark scoring beyond compiler pass/fail
- Expand benchmark suite
- Improve web UI polish
- Add more embedded targets beyond Arduino Uno

## Resume Summary

CircuitMind AI demonstrates an agentic firmware debugging workflow:

```text
Python + Docker + Arduino CLI + Embedded C/C++ + LLM Agents
```

Current resume-ready result:

```text
Resolved 70% of 10 benchmark firmware cases through live end-to-end repair, with Arduino Uno upload support validating repaired firmware on hardware.
```