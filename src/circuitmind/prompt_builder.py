from pathlib import Path

from circuitmind.models import Diagnostic


def add_line_numbers(source: str) -> str:
    lines = source.splitlines()
    numbered = []

    for index, line in enumerate(lines, start=1):
        numbered.append(f"{index:4} | {line}")

    return "\n".join(numbered)


def build_prompt(project_path: Path, diagnostics: list[Diagnostic]) -> str:
    project_path = project_path.resolve()

    source_sections = []

    for path in project_path.glob("*.ino"):
        source = path.read_text()
        source_sections.append(
            f"File: {path.name}\n\n{add_line_numbers(source)}"
        )

    diagnostics_text = "\n".join(
        f"- {d.file}:{d.line}:{d.column} {d.severity}: {d.message}"
        for d in diagnostics
    )

    return f"""
You are CircuitMind, a firmware build-failure assistant.

Use only the provided diagnostics and source files.

Return strict JSON with:
- diagnosis
- root_cause
- confidence
- patch

Diagnostics:
{diagnostics_text}

Source:
{chr(10).join(source_sections)}
"""