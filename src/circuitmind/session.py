from datetime import datetime
from pathlib import Path
import json


def create_session_dir(base_dir: Path = Path("sessions")) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    session_dir = base_dir / timestamp
    session_dir.mkdir(parents=True, exist_ok=False)
    return session_dir


def write_text_artifact(session_dir: Path, name: str, content: str) -> Path:
    path = session_dir / name
    path.write_text(content, encoding="utf-8")
    return path


def write_json_artifact(session_dir: Path, name: str, data: dict) -> Path:
    path = session_dir / name
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def append_session_index(entry: dict, index_path: Path = Path("sessions.jsonl")) -> None:
    with index_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")


def write_report(
    session_dir: Path,
    project: str,
    success: bool,
    iterations: int,
    diagnosis: str,
    root_cause: str,
    patch: str,
    final_message: str,
    build_before_exit_code: int | None = None,
    build_after_exit_code: int | None = None,
) -> Path:
    report = (
        "# CircuitMind Session Report\n\n"
        "## Summary\n\n"
        f"- Project: {project}\n"
        f"- Success: {success}\n"
        f"- Iterations: {iterations}\n\n"
        f"- Build before exit code: {build_before_exit_code}\n"
        f"- Build after exit code: {build_after_exit_code}\n\n"
        "## Diagnosis\n\n"
        f"{diagnosis}\n\n"
        "## Root Cause\n\n"
        f"{root_cause}\n\n"
        "## Patch\n\n"
        "```diff\n"
        f"{patch}\n"
        "```\n\n"
        "## Final Message\n\n"
        f"{final_message}\n"
    )

    return write_text_artifact(session_dir, "report.md", report)