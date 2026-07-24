from pathlib import Path

from circuitmind.fix import fix_project
from circuitmind.models import DiagnosisResult


def test_fix_clean_project_succeeds_without_patch():
    result = fix_project(Path("benchmarks/clean_01_blink"))

    assert result.success
    assert len(result.iterations) == 1
    assert result.iterations[0].diagnosis.diagnosis == "Project already compiles."


def test_fix_broken_project_with_fake_patch():
    def fake_diagnose(project_path: Path) -> DiagnosisResult:
        return DiagnosisResult(
            diagnosis="Missing semicolon.",
            root_cause="Serial.begin line is missing a semicolon.",
            confidence=0.95,
            patch=(
                "--- a/broken_01_missing_semicolon.ino\n"
                "+++ b/broken_01_missing_semicolon.ino\n"
                "@@ -1,8 +1,8 @@\n"
                " void setup() {\n"
                "-  Serial.begin(9600)\n"
                "+  Serial.begin(9600);\n"
                " }\n"
                "\n"
                " void loop() {\n"
                "   Serial.println(\"Hello\");\n"
                "   delay(1000);\n"
                " }\n"
            ),
            raw_response=None,
        )

    result = fix_project(
        Path("benchmarks/broken_01_missing_semicolon"),
        diagnose_func=fake_diagnose,
    )

    assert result.success
    assert len(result.iterations) == 1
    assert result.iterations[0].build_exit_code == 0
    assert result.final_workspace is not None