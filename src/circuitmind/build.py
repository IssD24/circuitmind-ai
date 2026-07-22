from pathlib import Path
import subprocess

from circuitmind.models import BuildResult


def build_project(project_path: Path) -> BuildResult:
    project_path = project_path.resolve()
    sketch_name = project_path.name
    container_path = f"/workspace/{sketch_name}"

    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{project_path}:{container_path}",
        "circuitmind",
        "arduino-cli",
        "compile",
        "--fqbn",
        "arduino:avr:uno",
        container_path,
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired as exc:
        return BuildResult(
            command=command,
            exit_code=-1,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "Build timed out",
        )

    return BuildResult(
        command=command,
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )