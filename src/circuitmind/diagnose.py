import json
import os
from pathlib import Path

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


def parse_llm_json(raw_text: str) -> DiagnosisResult:
    data = json.loads(raw_text)

    return DiagnosisResult(
        diagnosis=data["diagnosis"],
        root_cause=data["root_cause"],
        confidence=float(data["confidence"]),
        patch=data.get("patch", ""),
        raw_response=raw_text,
    )


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
            model="claude-3-5-sonnet-latest",
            max_tokens=2000,
            temperature=0,
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

    raw_text = response.content[0].text.strip()
    return parse_llm_json(raw_text)