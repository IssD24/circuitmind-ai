from circuitmind.models import DiagnosisResult
from circuitmind.validate import extract_patch_files, validate_diagnosis_result


def test_validate_good_result():
    result = DiagnosisResult(
        diagnosis="Missing semicolon.",
        root_cause="Serial.begin line is missing semicolon.",
        confidence=0.95,
        patch=(
            "--- a/file.ino\n"
            "+++ b/file.ino\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        ),
    )

    assert validate_diagnosis_result(result, allowed_files={"file.ino"}) == []


def test_validate_bad_confidence():
    result = DiagnosisResult(
        diagnosis="x",
        root_cause="y",
        confidence=1.5,
        patch="",
    )

    errors = validate_diagnosis_result(result)

    assert "confidence must be between 0 and 1" in errors


def test_validate_rejects_malformed_patch():
    result = DiagnosisResult(
        diagnosis="x",
        root_cause="y",
        confidence=0.5,
        patch="this is not a diff",
    )

    errors = validate_diagnosis_result(result)

    assert "patch does not look like a unified diff" in errors


def test_extract_patch_files():
    patch = (
        "--- a/main.ino\n"
        "+++ b/main.ino\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
    )

    assert extract_patch_files(patch) == {"main.ino"}


def test_validate_rejects_patch_touching_unknown_file():
    result = DiagnosisResult(
        diagnosis="x",
        root_cause="y",
        confidence=0.9,
        patch=(
            "--- a/secret.txt\n"
            "+++ b/secret.txt\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        ),
    )

    errors = validate_diagnosis_result(result, allowed_files={"file.ino"})

    assert "patch edits file not included in input: secret.txt" in errors