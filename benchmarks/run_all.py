from pathlib import Path
import json
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
RESULTS_DIR = REPO_ROOT / "benchmark_results"


def run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    benchmark_dirs = sorted(
        path
        for path in BENCHMARKS_DIR.iterdir()
        if path.is_dir() and path.name.startswith("broken_")
    )

    print(f"{'Benchmark':40} {'Before':10} {'Fix':10} Status")
    print("-" * 75)

    for benchmark in benchmark_dirs:
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

        if "CircuitMind fixed the project." in fix_result.stdout:
            fix_status = "fixed"
        elif "CircuitMind did not fix the project." in fix_result.stdout:
            fix_status = "not fixed"
        else:
            fix_status = "unknown"

        status = "ok" if build_result.returncode == 0 and fix_result.returncode == 0 else "error"

        print(
            f"{benchmark.name:40} "
            f"{before_status:10} "
            f"{fix_status:10} "
            f"{status}"
        )


if __name__ == "__main__":
    main()