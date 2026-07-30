import re

from circuitmind.models import Diagnostic


ERROR_PATTERNS = [
    re.compile(
        r"(?P<file>.*?):(?P<line>\d+):(?P<column>\d+):\s+"
        r"fatal error:\s+(?P<message>.*)"
    ),
    re.compile(
        r"(?P<file>.*?):(?P<line>\d+):(?P<column>\d+):\s+"
        r"(?P<severity>error|warning):\s+(?P<message>.*)"
    ),
    re.compile(
        r"(?P<file>.*?):(?P<line>\d+):\s+"
        r"(?P<severity>error|warning):\s+(?P<message>.*)"
    ),
]


def parse_arduino_cli_errors(output: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for line in output.splitlines():
        for pattern in ERROR_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue

            groups = match.groupdict()

            diagnostics.append(
                Diagnostic(
                    file=groups.get("file"),
                    line=int(groups["line"]) if groups.get("line") else None,
                    column=int(groups["column"]) if groups.get("column") else None,
                    severity=groups.get("severity") or "error",
                    message=groups.get("message", "").strip(),
                    raw=line,
                )
            )
            break

    return diagnostics