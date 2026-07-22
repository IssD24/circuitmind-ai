from pathlib import Path

from circuitmind.models import DiagnosisResult


def validate_diagnosis_result(
    result: DiagnosisResult,
    allowed_files: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []

    if not result.diagnosis.strip():
        errors.append("diagnosis is empty")

    if not result.root_cause.strip():
        errors.append("root_cause is empty")

    if not (0.0 <= result.confidence <= 1.0):
        errors.append("confidence must be between 0 and 1")

    if len(result.patch.splitlines()) > 200:
        errors.append("patch is over 200 lines")

    if result.patch:
        if not (
            "--- " in result.patch
            and "+++ " in result.patch
            and "@@" in result.patch
        ):
            errors.append("patch does not look like a unified diff")

        if allowed_files is not None:
            touched_files = extract_patch_files(result.patch)

            for file in touched_files:
                if file not in allowed_files:
                    errors.append(f"patch edits file not included in input: {file}")

    return errors


def extract_patch_files(patch: str) -> set[str]:
    files: set[str] = set()

    for line in patch.splitlines():
        if line.startswith("--- a/") or line.startswith("+++ b/"):
            path = line[6:].strip()
            files.add(path)

    return files


def collect_allowed_source_files(project_path: Path) -> set[str]:
    allowed: set[str] = set()

    for path in project_path.rglob("*"):
        if path.suffix in {".ino", ".cpp", ".h", ".hpp", ".c"}:
            allowed.add(str(path.relative_to(project_path)).replace("\\", "/"))

    return allowed