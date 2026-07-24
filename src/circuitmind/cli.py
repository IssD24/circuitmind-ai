from pathlib import Path
import json

import click

from circuitmind.build import build_project
from circuitmind.parse import parse_arduino_cli_errors
from circuitmind.analyze import analyze_project
from circuitmind.diagnose import diagnose_project
from circuitmind.validate import collect_allowed_source_files, validate_diagnosis_result
from circuitmind.patch import apply_patch_to_workspace

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


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default=None)
def analyze(project_path: str, output: str | None):
    diagnostics = analyze_project(Path(project_path))

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

@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def diagnose(project_path: str):
    result = diagnose_project(Path(project_path))

    allowed_files = collect_allowed_source_files(Path(project_path))
    errors = validate_diagnosis_result(result, allowed_files=allowed_files)

    if errors:
        click.echo("Validation errors:", err=True)
        for error in errors:
            click.echo(f"- {error}", err=True)

    data = {
        "diagnosis": result.diagnosis,
        "root_cause": result.root_cause,
        "confidence": result.confidence,
        "patch": result.patch,
    }

    click.echo(json.dumps(data, indent=2))

@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def fix(project_path: str):
    result = diagnose_project(Path(project_path))

    allowed_files = collect_allowed_source_files(Path(project_path))
    errors = validate_diagnosis_result(result, allowed_files=allowed_files)

    if errors:
        click.echo("Validation errors:")
        for error in errors:
            click.echo(f"- {error}")
        return

    if not result.patch.strip():
        click.echo(result.diagnosis)
        click.echo("No patch was produced.")
        return

    patch_result = apply_patch_to_workspace(result.patch, Path(project_path))

    click.echo(result.diagnosis)
    click.echo(patch_result.message)
    click.echo(f"Workspace: {patch_result.workspace_dir}")

if __name__ == "__main__":
    cli()