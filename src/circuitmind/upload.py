from pathlib import Path
import subprocess

from circuitmind.models import BuildResult


def upload_project(
    project_path: Path,
    port: str,
    fqbn: str = "arduino:avr:uno",
) -> BuildResult:
    project_path = project_path.resolve()

    command = [
        "arduino-cli",
        "compile",
        "--upload",
        "-p",
        port,
        "--fqbn",
        fqbn,
        str(project_path),
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=120,
    )

    return BuildResult(
        command=command,
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )