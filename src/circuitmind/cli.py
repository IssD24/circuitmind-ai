from pathlib import Path
import json

import click

from circuitmind.analyze import analyze_project
from circuitmind.build import build_project
from circuitmind.diagnose import diagnose_project
from circuitmind.fix import fix_project
from circuitmind.report import write_fix_report


@click.group()
def cli():
    """CircuitMind AI firmware debugging CLI."""
    pass


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default=None)
def build(project_path: str, output: str | None):
    """Build a firmware project and save parsed diagnostics."""
    project = Path(project_path)
    build_result = build_project(project)

    combined_output = build_result.stderr + "\n" + build_result.stdout
    diagnostics = analyze_project(project)

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
        Path(output).write_text(json.dumps(data, indent=2), encoding="utf-8")
        click.echo(f"Wrote diagnostics to {output}")
    else:
        click.echo(combined_output)


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default=None)
def analyze(project_path: str, output: str | None):
    """Analyze a firmware project and save parsed diagnostics."""
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
        Path(output).write_text(json.dumps(data, indent=2), encoding="utf-8")
        click.echo(f"Wrote diagnostics to {output}")
    else:
        click.echo(json.dumps(data, indent=2))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def diagnose(project_path: str):
    """Diagnose a firmware build failure."""
    result = diagnose_project(Path(project_path))

    click.echo(
        json.dumps(
            {
                "diagnosis": result.diagnosis,
                "root_cause": result.root_cause,
                "confidence": result.confidence,
                "patch": result.patch,
            },
            indent=2,
        )
    )


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--max-iterations", default=3, show_default=True)
@click.option("--report", type=click.Path(), default=None)
def fix(project_path: str, max_iterations: int, report: str | None):
    """Run the CircuitMind fix loop on a firmware project."""
    project = Path(project_path)
    result = fix_project(project, max_iterations=max_iterations)

    click.echo("CircuitMind Fix Session")
    click.echo()
    click.echo(f"Project: {project_path}")
    click.echo(f"Max iterations: {max_iterations}")
    click.echo()

    for iteration in result.iterations:
        click.echo(f"Iteration {iteration.iteration}:")
        click.echo(f"  Diagnosis: {iteration.diagnosis.diagnosis}")
        click.echo(f"  Message: {iteration.message}")
        if iteration.workspace_dir:
            click.echo(f"  Workspace: {iteration.workspace_dir}")
        if iteration.build_exit_code is not None:
            click.echo(f"  Build exit code: {iteration.build_exit_code}")
        click.echo()

    if result.success:
        click.echo("CircuitMind fixed the project.")
    else:
        click.echo("CircuitMind did not fix the project.")

    if report:
        report_path = write_fix_report(Path(report), project, result)
        click.echo(f"Report saved to: {report_path}")


if __name__ == "__main__":
    cli()