from types import SimpleNamespace

from circuitmind.models import DiagnosisResult
from circuitmind.report import write_fix_report


def test_report_file_is_created(tmp_path):
    output_path = tmp_path / "report.md"
    project_path = tmp_path / "broken_project"

    diagnosis = DiagnosisResult(
        diagnosis="Missing semicolon.",
        root_cause="Serial.begin is missing a terminating semicolon.",
        confidence=0.95,
        patch="--- a/test.ino\n+++ b/test.ino\n@@ -1 +1 @@\n-old\n+new\n",
    )

    iteration = SimpleNamespace(
        iteration=1,
        diagnosis=diagnosis,
        message="Build passed after patch.",
        build_exit_code=0,
    )

    result = SimpleNamespace(
        success=True,
        iterations=[iteration],
        final_workspace=tmp_path / "workspace",
    )

    write_fix_report(output_path, project_path, result)

    assert output_path.exists()


def test_report_contains_diagnosis_and_patch(tmp_path):
    output_path = tmp_path / "report.md"
    project_path = tmp_path / "broken_project"

    diagnosis = DiagnosisResult(
        diagnosis="Missing semicolon.",
        root_cause="Serial.begin is missing a terminating semicolon.",
        confidence=0.95,
        patch="--- a/test.ino\n+++ b/test.ino\n@@ -1 +1 @@\n-old\n+new\n",
    )

    iteration = SimpleNamespace(
        iteration=1,
        diagnosis=diagnosis,
        message="Build passed after patch.",
        build_exit_code=0,
    )

    result = SimpleNamespace(
        success=True,
        iterations=[iteration],
        final_workspace=tmp_path / "workspace",
    )

    write_fix_report(output_path, project_path, result)

    text = output_path.read_text(encoding="utf-8")

    assert "Missing semicolon." in text
    assert "Serial.begin is missing" in text
    assert "--- a/test.ino" in text
    assert "Build passed after patch." in text