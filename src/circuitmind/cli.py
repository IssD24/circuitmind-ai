from pathlib import Path
import json

import click

from circuitmind.build import build_project
from circuitmind.parse import parse_arduino_cli_errors


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default=None)
def build(project_path: str, output: str | None):
    result = build_project(Path(project_path))

    combined_output = result.stderr + "\n" + result.stdout
    diagnostics = parse_arduino_cli_errors(combined_output)

    data = [
        {
            "file": diagnostic.file,
            "line": diagnostic.line,
            "column": diagnostic.column,
            "severity": diagnostic.severity,
            "message": diagnostic.message,
            "raw": diagnostic.raw,
        }
        for diagnostic in diagnostics
    ]

    if output:
        Path(output).write_text(json.dumps(data, indent=2))
        click.echo(f"Wrote diagnostics to {output}")
    else:
        click.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    cli()