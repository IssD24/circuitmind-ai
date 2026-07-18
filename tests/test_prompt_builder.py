from circuitmind.prompt_builder import add_line_numbers


def test_add_line_numbers():
    source = "void setup() {\n}"
    numbered = add_line_numbers(source)

    assert "1" in numbered
    assert "void setup()" in numbered
    assert "2" in numbered