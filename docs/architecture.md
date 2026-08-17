# CircuitMind Architecture

## Overview

CircuitMind AI is an agentic firmware debugging system for Arduino-style embedded C/C++ projects. It compiles firmware, parses compiler diagnostics, asks an LLM for a diagnosis and patch, validates the patch, applies it to a copied workspace, rebuilds the firmware, generates a report, and can optionally upload the repaired firmware to an Arduino Uno.

## Pipeline

```text
Firmware source
→ Dockerized compiler
→ Compiler diagnostics
→ Diagnostic parser
→ Prompt builder
→ LLM diagnosis
→ Patch validation
→ Copied workspace
→ Patch application
→ Rebuild
→ Report
→ Optional Arduino upload