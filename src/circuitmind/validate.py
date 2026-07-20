from circuitmind.models import DiagnosisResult


def validate_diagnosis_result(result: DiagnosisResult) -> list[str]:
    errors: list[str] = []

    if not result.diagnosis.strip():
        errors.append("diagnosis is empty")

    if not result.root_cause.strip():
        errors.append("root_cause is empty")

    if not (0.0 <= result.confidence <= 1.0):
        errors.append("confidence must be between 0 and 1")

    if result.patch and not (
        "--- " in result.patch and "+++ " in result.patch and "@@" in result.patch
    ):
        errors.append("patch does not look like a unified diff")

    if len(result.patch.splitlines()) > 200:
        errors.append("patch is over 200 lines")

    return errors