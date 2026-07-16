from click.testing import CliRunner

from circuitmind.cli import cli


def test_cli_build_writes_output_file(tmp_path):
    runner = CliRunner()
    output_path = tmp_path / "diagnostics.json"

    result = runner.invoke(
        cli,
        [
            "build",
            "benchmarks/broken_01_missing_semicolon",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    assert "Wrote diagnostics" in result.output