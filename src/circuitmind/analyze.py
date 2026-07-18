from pathlib import Path
import subprocess

from circuitmind.build import build_project
from circuitmind.models import BuildResult, Diagnostic
from circuitmind.parse import parse_arduino_cli_errors


def run_cppcheck(project_path: Path) -> BuildResult:
    project_path = project_path.resolve()

    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{project_path}:/workspace/project",
        "circuitmind",
        "cppcheck",
        "--enable=all",
        "--inconclusive",
        "--std=c++17",
        "/workspace/project",
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return BuildResult(
        command=command,
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def analyze_project(project_path: Path) -> list[Diagnostic]:
    build_result = build_project(project_path)
    build_output = build_result.stderr + "\n" + build_result.stdout

    diagnostics = parse_arduino_cli_errors(build_output)

    cppcheck_result = run_cppcheck(project_path)
    cppcheck_output = cppcheck_result.stderr + "\n" + cppcheck_result.stdout

    for line in cppcheck_output.splitlines():
        if "error" in line.lower() or "warning" in line.lower():
            diagnostics.append(
                Diagnostic(
                    file=None,
                    line=None,
                    column=None,
                    severity="warning",
                    message=line.strip(),
                    raw=line,
                )
            )

    return diagnostics