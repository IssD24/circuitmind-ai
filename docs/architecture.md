# CircuitMind Architecture

## Overview

CircuitMind AI is an agentic firmware debugging system for Arduino-style embedded C/C++ projects. It compiles firmware in Docker, parses diagnostics, asks an LLM for a root-cause diagnosis and patch, validates the patch, applies it to a copied workspace, rebuilds the firmware, and generates a report.

## Pipeline

```text
Firmware project
→ Dockerized build
→ Compiler diagnostics
→ Diagnostic parser
→ Prompt builder
→ LLM diagnosis
→ Patch validation
→ Copied workspace
→ Patch application
→ Rebuild
→ Report generation
→ Optional Arduino upload