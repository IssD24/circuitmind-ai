from dataclasses import dataclass
from pathlib import Path

from circuitmind.build import build_project
from circuitmind.diagnose import diagnose_project
from circuitmind.models import DiagnosisResult
from circuitmind.patch import apply_patch_to_workspace
from circuitmind.validate import collect_allowed_source_files, validate_diagnosis_result

from collections.abc import Callable


@dataclass
class FixIteration:
    iteration: int
    diagnosis: DiagnosisResult
    workspace_dir: Path | None
    build_exit_code: int | None
    success: bool
    message: str


@dataclass
class FixResult:
    success: bool
    iterations: list[FixIteration]
    final_workspace: Path | None


def fix_project(
    project_path: Path,
    max_iterations: int = 3,
    diagnose_func: Callable[[Path], DiagnosisResult] = diagnose_project,
) -> FixResult:
    current_path = project_path
    iterations: list[FixIteration] = []

    for iteration in range(1, max_iterations + 1):
        diagnosis = diagnose_func(current_path)
        allowed_files = collect_allowed_source_files(current_path)
        validation_errors = validate_diagnosis_result(
            diagnosis,
            allowed_files=allowed_files,
        )

        if validation_errors:
            iterations.append(
                FixIteration(
                    iteration=iteration,
                    diagnosis=diagnosis,
                    workspace_dir=None,
                    build_exit_code=None,
                    success=False,
                    message="Validation failed: " + "; ".join(validation_errors),
                )
            )

            return FixResult(
                success=False,
                iterations=iterations,
                final_workspace=None,
            )

        if not diagnosis.patch.strip():
            success = diagnosis.diagnosis == "Project already compiles."

            iterations.append(
                FixIteration(
                    iteration=iteration,
                    diagnosis=diagnosis,
                    workspace_dir=None,
                    build_exit_code=0 if success else None,
                    success=success,
                    message="No patch produced.",
                )
            )

            return FixResult(
                success=success,
                iterations=iterations,
                final_workspace=None,
            )

        patch_result = apply_patch_to_workspace(diagnosis.patch, current_path)

        if not patch_result.success:
            iterations.append(
                FixIteration(
                    iteration=iteration,
                    diagnosis=diagnosis,
                    workspace_dir=patch_result.workspace_dir,
                    build_exit_code=None,
                    success=False,
                    message=patch_result.message,
                )
            )

            return FixResult(
                success=False,
                iterations=iterations,
                final_workspace=patch_result.workspace_dir,
            )

        build_result = build_project(patch_result.workspace_dir)
        fixed = build_result.exit_code == 0

        iterations.append(
            FixIteration(
                iteration=iteration,
                diagnosis=diagnosis,
                workspace_dir=patch_result.workspace_dir,
                build_exit_code=build_result.exit_code,
                success=fixed,
                message=(
                    "Build passed after patch."
                    if fixed
                    else "Build still fails after patch."
                ),
            )
        )

        if fixed:
            return FixResult(
                success=True,
                iterations=iterations,
                final_workspace=patch_result.workspace_dir,
            )

        current_path = patch_result.workspace_dir

    return FixResult(
        success=False,
        iterations=iterations,
        final_workspace=iterations[-1].workspace_dir if iterations else None,
    )