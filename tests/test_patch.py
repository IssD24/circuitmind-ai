from pathlib import Path

from circuitmind.patch import apply_patch_to_workspace


def test_apply_patch_to_workspace_missing_semicolon():
    project_path = Path("benchmarks/broken_01_missing_semicolon")

    patch_text = (
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
    )

    result = apply_patch_to_workspace(patch_text, project_path)

    assert result.success
    assert result.workspace_dir.exists()

    fixed_file = result.workspace_dir / "broken_01_missing_semicolon.ino"
    assert "Serial.begin(9600);" in fixed_file.read_text()