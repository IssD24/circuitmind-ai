# CircuitMind Demo Script

## Goal

Show CircuitMind repairing broken Arduino firmware end-to-end, generating a report, and optionally uploading the repaired firmware to a physical Arduino Uno.

This demo focuses on the CLI workflow because it is the most stable and reproducible path.

## Demo Setup

Requirements:

- Docker Desktop running
- Python dependencies installed
- Arduino CLI installed, for hardware upload demo
- Arduino Uno connected over USB, for hardware upload demo
- Anthropic API key set in the terminal

Set environment variables:

```powershell
$env:PYTHONPATH="src"
$env:ANTHROPIC_API_KEY="your-api-key"