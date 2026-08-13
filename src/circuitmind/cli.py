from pathlib import Path
import json

import click

from circuitmind.analyze import analyze_project
from circuitmind.build import build_project
from circuitmind.diagnose import diagnose_project
from circuitmind.fix import fix_project
from circuitmind.report import write_fix_report
from circuitmind.upload import upload_project


@click.group()
def cli():
    """CircuitMind AI firmware debugging CLI."""
    pass


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default=None)
def build(project_path: str, output: str | None):
    """Compile an Arduino firmware project in Docker."""
    result = build_project(Path(project_path))

    data = {
        "command": result.command,
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

    text = json.dumps(data, indent=2)

    if output:
        Path(output).write_text(text, encoding="utf-8")
        click.echo(f"Wrote diagnostics to: {output}")
    else:
        click.echo(text)


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def analyze(project_path: str):
    """Compile a project and parse diagnostics."""
    diagnostics = analyze_project(Path(project_path))

    output = []
    for diagnostic in diagnostics:
        output.append(
            {
                "file": diagnostic.file,
                "line": diagnostic.line,
                "column": diagnostic.column,
                "severity": diagnostic.severity,
                "message": diagnostic.message,
                "raw": diagnostic.raw,
            }
        )

    click.echo(json.dumps(output, indent=2))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def diagnose(project_path: str):
    """Use the LLM to diagnose a firmware build failure."""
    result = diagnose_project(Path(project_path))

    output = {
        "diagnosis": result.diagnosis,
        "root_cause": result.root_cause,
        "confidence": result.confidence,
        "patch": result.patch,
    }

    click.echo(json.dumps(output, indent=2))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--max-iterations", default=3, show_default=True)
@click.option("--report", type=click.Path(), default=None)
@click.option(
    "--upload",
    is_flag=True,
    help="Upload the fixed workspace to a board after repair.",
)
@click.option(
    "--port",
    default=None,
    help="Serial port for board upload, such as COM3.",
)
@click.option(
    "--fqbn",
    default="arduino:avr:uno",
    show_default=True,
    help="Arduino board FQBN.",
)
def fix(
    project_path: str,
    max_iterations: int,
    report: str | None,
    upload: bool,
    port: str | None,
    fqbn: str,
):
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

    if upload:
        if not result.success:
            click.echo("Upload skipped because the fix did not succeed.")
            return

        if result.final_workspace is None:
            click.echo("Upload skipped because no fixed workspace was produced.")
            return

        if not port:
            click.echo("Upload skipped because --port was not provided.")
            return

        upload_result = upload_project(
            result.final_workspace,
            port=port,
            fqbn=fqbn,
        )

        click.echo()
        click.echo("Upload Result")
        click.echo(f"Command: {' '.join(upload_result.command)}")
        click.echo(f"Exit code: {upload_result.exit_code}")

        if upload_result.stdout:
            click.echo(upload_result.stdout)

        if upload_result.stderr:
            click.echo(upload_result.stderr)


if __name__ == "__main__":
    cli()