from pathlib import Path
import json
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
RESULTS_DIR = REPO_ROOT / "benchmark_results"
SCOREBOARD_PATH = RESULTS_DIR / "scoreboard.md"


def run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def load_metadata(benchmark: Path) -> dict:
    metadata_path = benchmark / "benchmark.json"

    if not metadata_path.exists():
        return {
            "category": "compiler",
            "expected_issue": "",
            "expected_fix": "",
            "should_compile_before_fix": False,
        }

    return json.loads(metadata_path.read_text(encoding="utf-8"))


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    benchmark_dirs = sorted(
        path
        for path in BENCHMARKS_DIR.iterdir()
        if path.is_dir() and path.name.startswith("broken_")
    )

    rows = []

    print(f"{'Benchmark':40} {'Type':12} {'Before':10} {'Fix':14} Status")
    print("-" * 95)

    for benchmark in benchmark_dirs:
        metadata = load_metadata(benchmark)
        category = metadata.get("category", "compiler")

        diagnostics_path = RESULTS_DIR / f"{benchmark.name}.json"

        build_result = run_command(
            [
                "python",
                "-m",
                "circuitmind.cli",
                "build",
                str(benchmark.relative_to(REPO_ROOT)),
                "--output",
                str(diagnostics_path.relative_to(REPO_ROOT)),
            ]
        )

        diagnostics = []
        if diagnostics_path.exists():
            diagnostics = json.loads(diagnostics_path.read_text(encoding="utf-8"))

        before_status = "pass" if len(diagnostics) == 0 else "fail"

        fix_result = run_command(
            [
                "python",
                "-m",
                "circuitmind.cli",
                "fix",
                str(benchmark.relative_to(REPO_ROOT)),
                "--max-iterations",
                "3",
            ]
        )

        if category in {"logic", "warning"} and before_status == "pass":
            fix_status = "compile-pass"
        elif "CircuitMind fixed the project." in fix_result.stdout:
            fix_status = "fixed"
        elif "CircuitMind did not fix the project." in fix_result.stdout:
            fix_status = "not fixed"
        else:
            fix_status = "unknown"

        status = "ok" if build_result.returncode == 0 and fix_result.returncode == 0 else "error"

        rows.append((benchmark.name, category, before_status, fix_status, status))

        print(
            f"{benchmark.name:40} "
            f"{category:12} "
            f"{before_status:10} "
            f"{fix_status:14} "
            f"{status}"
        )

    scoreboard = [
        "# CircuitMind Benchmark Scoreboard",
        "",
        "| Benchmark | Type | Before | Fix Result | Status |",
        "|---|---|---|---|---|",
    ]

    for benchmark_name, category, before_status, fix_status, status in rows:
        scoreboard.append(
            f"| {benchmark_name} | {category} | {before_status} | {fix_status} | {status} |"
        )

    SCOREBOARD_PATH.write_text("\n".join(scoreboard) + "\n", encoding="utf-8")

    print()
    print(f"Wrote scoreboard to {SCOREBOARD_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()