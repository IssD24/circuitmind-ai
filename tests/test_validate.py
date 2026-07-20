from circuitmind.models import DiagnosisResult
from circuitmind.validate import validate_diagnosis_result


def test_validate_good_result():
    result = DiagnosisResult(
        diagnosis="Missing semicolon.",
        root_cause="Serial.begin line is missing semicolon.",
        confidence=0.95,
        patch="--- a/file.ino\n+++ b/file.ino\n@@ -1 +1 @@\n-old\n+new\n",
    )

    assert validate_diagnosis_result(result) == []


def test_validate_bad_confidence():
    result = DiagnosisResult(
        diagnosis="x",
        root_cause="y",
        confidence=1.5,
        patch="",
    )

    errors = validate_diagnosis_result(result)

    assert "confidence must be between 0 and 1" in errors