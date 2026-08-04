from pathlib import Path
from typing import Any


def write_fix_report(
    output_path: Path,
    project_path: Path,
    result: Any,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    benchmark_name = project_path.name
    final_iteration = result.iterations[-1] if result.iterations else None

    if final_iteration is None:
        diagnosis = "No diagnosis was produced."
        root_cause = "No iterations ran."
        patch = ""
        final_message = "No fix attempt was completed."
        build_exit_code = None
    else:
        diagnosis = final_iteration.diagnosis.diagnosis
        root_cause = final_iteration.diagnosis.root_cause
        patch = final_iteration.diagnosis.patch
        final_message = final_iteration.message
        build_exit_code = final_iteration.build_exit_code

    text = (
        f"# CircuitMind Report — {benchmark_name}\n\n"
        "## Result\n\n"
        f"Success: {result.success}\n\n"
        f"Iterations: {len(result.iterations)}\n\n"
        f"Final build exit code: {build_exit_code}\n\n"
        "## Project\n\n"
        f"`{project_path}`\n\n"
        "## Diagnosis\n\n"
        f"{diagnosis}\n\n"
        "## Root Cause\n\n"
        f"{root_cause}\n\n"
        "## Patch\n\n"
        "```diff\n"
        f"{patch}\n"
        "```\n\n"
        "## Final Message\n\n"
        f"{final_message}\n\n"
        "## Final Workspace\n\n"
        f"`{result.final_workspace}`\n"
    )

    output_path.write_text(text, encoding="utf-8")
    return output_path