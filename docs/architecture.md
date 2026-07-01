# CircuitMind AI Architecture

## Problem

Arduino and ESP32 firmware errors are often difficult for beginners to understand because compiler output can be long, noisy, and spread across multiple files.

CircuitMind AI will help by running the build, extracting the important errors, asking an LLM for a grounded diagnosis, and proposing a patch that the user can approve.

## Pipeline

```text
User project
   ↓
Docker build environment
   ↓
arduino-cli compile
   ↓
Raw compiler output
   ↓
Diagnostic parser
   ↓
Structured diagnostics JSON
   ↓
LLM diagnosis and patch proposal
   ↓
Human approval
   ↓
Patch applied to copied workspace
   ↓
Rebuild
   ↓
Final report