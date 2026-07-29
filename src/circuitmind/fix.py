from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from circuitmind.build import build_project
from circuitmind.diagnose import diagnose_project
from circuitmind.models import DiagnosisResult
from circuitmind.patch import apply_patch_to_workspace
from circuitmind.session import (
    append_session_index,
    create_session_dir,
    write_json_artifact,
    write_report,
    write_text_artifact,
)
from circuitmind.validate import collect_allowed_source_files, validate_diagnosis_result


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
    session_dir = create_session_dir()

    build_before = build_project(project_path)

    write_text_artifact(
        session_dir,
        "build_before.txt",
        "STDOUT:\n"
        + build_before.stdout
        + "\n\nSTDERR:\n"
        + build_before.stderr
        + f"\n\nEXIT CODE: {build_before.exit_code}\n",
    )

    for iteration in range(1, max_iterations + 1):
        diagnosis = diagnose_func(current_path)

        write_json_artifact(
            session_dir,
            f"diagnosis_{iteration}.json",
            {
                "diagnosis": diagnosis.diagnosis,
                "root_cause": diagnosis.root_cause,
                "confidence": diagnosis.confidence,
                "patch": diagnosis.patch,
            },
        )

        write_text_artifact(
            session_dir,
            f"patch_{iteration}.diff",
            diagnosis.patch,
        )

        allowed_files = collect_allowed_source_files(current_path)
        validation_errors = validate_diagnosis_result(
            diagnosis,
            allowed_files=allowed_files,
        )

        if validation_errors:
            message = "Validation failed: " + "; ".join(validation_errors)

            iterations.append(
                FixIteration(
                    iteration=iteration,
                    diagnosis=diagnosis,
                    workspace_dir=None,
                    build_exit_code=None,
                    success=False,
                    message=message,
                )
            )

            write_report(
                session_dir=session_dir,
                project=str(project_path),
                success=False,
                iterations=len(iterations),
                diagnosis=diagnosis.diagnosis,
                root_cause=diagnosis.root_cause,
                patch=diagnosis.patch,
                final_message=message,
                build_before_exit_code=build_before.exit_code,
                build_after_exit_code=None,
            )

            append_session_index(
                {
                    "session": str(session_dir),
                    "project": str(project_path),
                    "success": False,
                    "iterations": len(iterations),
                    "final_exit_code": None,
                }
            )

            return FixResult(
                success=False,
                iterations=iterations,
                final_workspace=None,
            )

        if not diagnosis.patch.strip():
            success = diagnosis.diagnosis == "Project already compiles."
            message = "No patch produced."

            iterations.append(
                FixIteration(
                    iteration=iteration,
                    diagnosis=diagnosis,
                    workspace_dir=None,
                    build_exit_code=0 if success else None,
                    success=success,
                    message=message,
                )
            )

            write_report(
                session_dir=session_dir,
                project=str(project_path),
                success=success,
                iterations=len(iterations),
                diagnosis=diagnosis.diagnosis,
                root_cause=diagnosis.root_cause,
                patch=diagnosis.patch,
                final_message=message,
                build_before_exit_code=build_before.exit_code,
                build_after_exit_code=None,
            )

            append_session_index(
                {
                    "session": str(session_dir),
                    "project": str(project_path),
                    "success": success,
                    "iterations": len(iterations),
                    "final_exit_code": 0 if success else None,
                }
            )

            return FixResult(
                success=success,
                iterations=iterations,
                final_workspace=None,
            )

        patch_result = apply_patch_to_workspace(diagnosis.patch, current_path)

        if not patch_result.success:
            message = patch_result.message

            iterations.append(
                FixIteration(
                    iteration=iteration,
                    diagnosis=diagnosis,
                    workspace_dir=patch_result.workspace_dir,
                    build_exit_code=None,
                    success=False,
                    message=message,
                )
            )

            write_report(
                session_dir=session_dir,
                project=str(project_path),
                success=False,
                iterations=len(iterations),
                diagnosis=diagnosis.diagnosis,
                root_cause=diagnosis.root_cause,
                patch=diagnosis.patch,
                final_message=message,
                build_before_exit_code=build_before.exit_code,
                build_after_exit_code=None,
            )

            append_session_index(
                {
                    "session": str(session_dir),
                    "project": str(project_path),
                    "success": False,
                    "iterations": len(iterations),
                    "final_exit_code": None,
                }
            )

            return FixResult(
                success=False,
                iterations=iterations,
                final_workspace=patch_result.workspace_dir,
            )

        build_result = build_project(patch_result.workspace_dir)
        fixed = build_result.exit_code == 0
        message = "Build passed after patch." if fixed else "Build still fails after patch."

        write_text_artifact(
            session_dir,
            f"build_after_{iteration}.txt",
            "STDOUT:\n"
            + build_result.stdout
            + "\n\nSTDERR:\n"
            + build_result.stderr
            + f"\n\nEXIT CODE: {build_result.exit_code}\n",
        )

        iterations.append(
            FixIteration(
                iteration=iteration,
                diagnosis=diagnosis,
                workspace_dir=patch_result.workspace_dir,
                build_exit_code=build_result.exit_code,
                success=fixed,
                message=message,
            )
        )

        if fixed:
            write_report(
                session_dir=session_dir,
                project=str(project_path),
                success=True,
                iterations=len(iterations),
                diagnosis=diagnosis.diagnosis,
                root_cause=diagnosis.root_cause,
                patch=diagnosis.patch,
                final_message=message,
                build_before_exit_code=build_before.exit_code,
                build_after_exit_code=build_result.exit_code,
            )

            append_session_index(
                {
                    "session": str(session_dir),
                    "project": str(project_path),
                    "success": True,
                    "iterations": len(iterations),
                    "final_exit_code": build_result.exit_code,
                }
            )

            return FixResult(
                success=True,
                iterations=iterations,
                final_workspace=patch_result.workspace_dir,
            )

        current_path = patch_result.workspace_dir

    final_iteration = iterations[-1] if iterations else None

    if final_iteration:
        final_diagnosis = final_iteration.diagnosis
        final_message = final_iteration.message
        final_exit_code = final_iteration.build_exit_code
    else:
        final_diagnosis = DiagnosisResult(
            diagnosis="No diagnosis.",
            root_cause="No iterations ran.",
            confidence=0.0,
            patch="",
            raw_response=None,
        )
        final_message = "No iterations ran."
        final_exit_code = None

    write_report(
        session_dir=session_dir,
        project=str(project_path),
        success=False,
        iterations=len(iterations),
        diagnosis=final_diagnosis.diagnosis,
        root_cause=final_diagnosis.root_cause,
        patch=final_diagnosis.patch,
        final_message=final_message,
        build_before_exit_code=build_before.exit_code,
        build_after_exit_code=final_exit_code,
    )

    append_session_index(
        {
            "session": str(session_dir),
            "project": str(project_path),
            "success": False,
            "iterations": len(iterations),
            "final_exit_code": final_exit_code,
        }
    )

    return FixResult(
        success=False,
        iterations=iterations,
        final_workspace=iterations[-1].workspace_dir if iterations else None,
    )