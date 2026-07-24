from pathlib import Path

from circuitmind.fix import fix_project


def test_fix_clean_project_succeeds_without_patch():
    result = fix_project(Path("benchmarks/clean_01_blink"))

    assert result.success
    assert len(result.iterations) == 1
    assert result.iterations[0].diagnosis.diagnosis == "Project already compiles."