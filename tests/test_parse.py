from circuitmind.parse import parse_arduino_cli_errors


def test_parse_missing_semicolon_error():
    text = "/workspace/broken_01_missing_semicolon/broken_01_missing_semicolon.ino:3:1: error: expected ';' before '}' token"

    diagnostics = parse_arduino_cli_errors(text)

    assert len(diagnostics) == 1
    assert diagnostics[0].severity == "error"
    assert diagnostics[0].line == 3
    assert diagnostics[0].column == 1
    assert "expected ';'" in diagnostics[0].message


def test_parse_returns_empty_list_for_clean_output():
    diagnostics = parse_arduino_cli_errors("Sketch uses 1234 bytes")

    assert diagnostics == []