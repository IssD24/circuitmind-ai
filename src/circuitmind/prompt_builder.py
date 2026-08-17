from pathlib import Path
from typing import Iterable

from circuitmind.models import Diagnostic


SOURCE_SUFFIXES = {".ino", ".cpp", ".h", ".hpp", ".c"}


def add_line_numbers(content: str) -> str:
    lines = content.splitlines()

    numbered_lines = []
    for index, line in enumerate(lines, start=1):
        numbered_lines.append(f"{index}: {line}")

    return "\n".join(numbered_lines)


def collect_source_files(project_path: Path) -> list[Path]:
    project_path = project_path.resolve()

    source_files = []

    for path in project_path.rglob("*"):
        if path.is_file() and path.suffix in SOURCE_SUFFIXES:
            source_files.append(path)

    return sorted(source_files)


def format_diagnostics(diagnostics: Iterable[Diagnostic]) -> str:
    lines = []

    for diagnostic in diagnostics:
        location_parts = []

        if diagnostic.file:
            location_parts.append(diagnostic.file)

        if diagnostic.line is not None:
            location_parts.append(f"line {diagnostic.line}")

        if diagnostic.column is not None:
            location_parts.append(f"column {diagnostic.column}")

        location = ", ".join(location_parts) if location_parts else "unknown location"

        lines.append(
            (
                f"- [{diagnostic.severity}] {location}: "
                f"{diagnostic.message}\n"
                f"  Raw: {diagnostic.raw}"
            )
        )

    if not lines:
        return "No structured diagnostics were parsed."

    return "\n".join(lines)


def format_source_files(project_path: Path) -> str:
    project_path = project_path.resolve()
    source_files = collect_source_files(project_path)

    if not source_files:
        return "No source files were found."

    sections = []

    for source_file in source_files:
        relative_path = source_file.relative_to(project_path).as_posix()
        content = source_file.read_text(encoding="utf-8", errors="replace")
        content = add_line_numbers(content)

        sections.append(
            (
                f"File: {relative_path}\n"
                "```cpp\n"
                f"{content}\n"
                "```"
            )
        )

    return "\n\n".join(sections)


def build_diagnosis_prompt(
    project_path: Path,
    diagnostics: list[Diagnostic],
    build_output: str | None = None,
) -> str:
    project_path = project_path.resolve()

    diagnostics_text = format_diagnostics(diagnostics)
    source_text = format_source_files(project_path)

    build_output_section = ""
    if build_output:
        build_output_section = (
            "\n\nFull build output:\n"
            "```text\n"
            f"{build_output}\n"
            "```"
        )

    return f"""
You are CircuitMind, an AI firmware debugging agent for Arduino-style embedded C/C++ projects.

Your job is to diagnose the build failure and propose one minimal unified diff patch that is likely to make the project compile.

Project name:
{project_path.name}

Target environment:
- Board: Arduino Uno
- FQBN: arduino:avr:uno
- Toolchain: Arduino AVR
- The project is compiled as an Arduino sketch.

Compiler diagnostics:
{diagnostics_text}
{build_output_section}

Source files:
{source_text}

Important Arduino Uno repair rules:
- The target board is Arduino Uno using the arduino:avr:uno toolchain.
- Prefer source-only fixes that compile on Arduino Uno.
- Do not add new third-party library dependencies unless the project already includes and supports that library.
- If the error involves a missing third-party header such as ArduinoJson.h, either remove the dependency, use already available Arduino/C++ features, or rewrite the code using Arduino Uno compatible code.
- The Arduino Uno AVR toolchain does not reliably support the full C++ STL.
- Avoid fixes that depend on std::vector, std::map, std::string, unordered_map, or other unsupported STL features.
- For AVR-compatible fixes, prefer fixed-size arrays, char buffers, simple structs, direct Serial.print calls, and Arduino core APIs.
- Keep the patch minimal and focused on making the sketch compile.
- Do not change the intended benchmark behavior unless required to make the code compile.
- Do not modify files outside the project source files shown above.
- Use paths relative to the project root in the patch.
- Do not include absolute paths in the patch.
- Do not include Markdown outside the JSON object.

Patch requirements:
- Return a unified diff only inside the "patch" field.
- The diff must use this format:
  --- a/filename.ino
  +++ b/filename.ino
  @@ ...
- Only edit files that were included in the source files section.
- Keep the patch under 200 lines.
- If multiple fixes are possible, choose the smallest safe fix.

Return only valid JSON with exactly these fields:

{{
  "diagnosis": "short explanation of the compiler/build problem",
  "root_cause": "specific root cause in the source code",
  "confidence": 0.0,
  "patch": "unified diff patch"
}}

The confidence value must be a number between 0.0 and 1.0.
""".strip()


def build_prompt(
    project_path: Path,
    diagnostics: list[Diagnostic],
    build_output: str | None = None,
) -> str:
    return build_diagnosis_prompt(
        project_path=project_path,
        diagnostics=diagnostics,
        build_output=build_output,
    )


def build_repair_prompt(
    project_path: Path,
    diagnostics: list[Diagnostic],
    build_output: str | None = None,
) -> str:
    return build_diagnosis_prompt(
        project_path=project_path,
        diagnostics=diagnostics,
        build_output=build_output,
    )