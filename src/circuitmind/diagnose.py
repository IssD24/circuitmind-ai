import json
import os
from pathlib import Path
import re

from anthropic import Anthropic

from circuitmind.analyze import analyze_project
from circuitmind.models import DiagnosisResult, Diagnostic
from circuitmind.build import build_project


def add_line_numbers(source: str) -> str:
    lines = source.splitlines()
    return "\n".join(
        f"{index:4} | {line}"
        for index, line in enumerate(lines, start=1)
    )


def collect_source_files(project_path: Path) -> str:
    sections: list[str] = []

    for path in project_path.rglob("*"):
        if path.suffix not in {".ino", ".cpp", ".h", ".hpp", ".c"}:
            continue

        source = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(project_path)

        sections.append(
            f"File: {relative}\n\n{add_line_numbers(source)}"
        )

    return "\n\n---\n\n".join(sections)


def diagnostics_to_json(diagnostics: list[Diagnostic]) -> str:
    data = [
        {
            "file": d.file,
            "line": d.line,
            "column": d.column,
            "severity": d.severity,
            "message": d.message,
            "raw": d.raw,
        }
        for d in diagnostics
    ]

    return json.dumps(data, indent=2)


def build_diagnosis_prompt(project_path: Path, diagnostics: list[Diagnostic]) -> str:
    source_text = collect_source_files(project_path)
    diagnostics_json = diagnostics_to_json(diagnostics)

    return f"""
You are CircuitMind, a firmware build-failure assistant.

You diagnose Arduino and ESP32 compilation errors using only:
1. The source files provided.
2. The compiler diagnostics provided.
3. The static-analysis diagnostics provided.

You must not assume files, libraries, APIs, or hardware that are not shown in the input.

Return only raw JSON. Do not wrap it in markdown fences.

Return strict JSON with exactly these fields:
- diagnosis
- root_cause
- confidence
- patch

The patch must be a unified diff beginning with "--- a/" and "+++ b/".
The patch must only edit files included in the source section.
The patch should be minimal.
Do not rewrite unrelated code.

Project path:
{project_path}

Diagnostics JSON:
{diagnostics_json}

Source with line numbers:
{source_text}
"""


def extract_json_object(raw_text: str) -> str:
    text = raw_text.strip()

    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)

    first_brace = text.find("{")
    last_brace = text.rfind("}")

    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return text[first_brace : last_brace + 1]

    return text

def normalize_confidence(value) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))

    if isinstance(value, str):
        cleaned = value.strip().lower()

        confidence_map = {
            "low": 0.3,
            "medium": 0.6,
            "moderate": 0.6,
            "high": 0.9,
            "very high": 0.95,
        }

        if cleaned in confidence_map:
            return confidence_map[cleaned]

        try:
            return max(0.0, min(1.0, float(cleaned)))
        except ValueError:
            return 0.0

    return 0.0

def parse_llm_json(raw_text: str) -> DiagnosisResult:
    json_text = extract_json_object(raw_text)
    data = json.loads(json_text)

    return DiagnosisResult(
        diagnosis=str(data.get("diagnosis", "")).strip(),
        root_cause=str(data.get("root_cause", "")).strip(),
        confidence=normalize_confidence(data.get("confidence", 0.0)),
        patch=str(data.get("patch", "")),
        raw_response=raw_text,
    )
def extract_response_text(response) -> str:
    text_parts = []

    for block in response.content:
        text = getattr(block, "text", None)

        if text:
            text_parts.append(text)

    return "\n".join(text_parts).strip()

def diagnose_project(project_path: Path) -> DiagnosisResult:
    project_path = project_path.resolve()

    build_result = build_project(project_path)

    if build_result.exit_code == 0:
        return DiagnosisResult(
            diagnosis="Project already compiles.",
            root_cause="No compiler error was found.",
            confidence=1.0,
            patch="",
            raw_response=None,
        )

    if build_result.exit_code == -1:
        return DiagnosisResult(
            diagnosis="Build timed out.",
            root_cause=build_result.stderr,
            confidence=0.0,
            patch="",
            raw_response=None,
        )

    diagnostics = analyze_project(project_path)

    prompt = build_diagnosis_prompt(project_path, diagnostics)

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    try:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
    except Exception as exc:
        return DiagnosisResult(
            diagnosis="LLM request failed.",
            root_cause=str(exc),
            confidence=0.0,
            patch="",
            raw_response=None,
        )

    raw_text = extract_response_text(response)

    if not raw_text:
        return DiagnosisResult(
        diagnosis="LLM response did not contain text output.",
        root_cause=f"Response contained no text block.\n\nRaw response:\n{response}",
        confidence=0.0,
        patch="",
        raw_response=str(response),
    )

    try:
        return parse_llm_json(raw_text)
    except Exception as exc:
        return DiagnosisResult(
        diagnosis="LLM response was not valid JSON.",
        root_cause=f"{exc}\n\nRaw response:\n{raw_text}",
        confidence=0.0,
        patch="",
        raw_response=raw_text,
    )