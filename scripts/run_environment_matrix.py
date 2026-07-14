#!/usr/bin/env python3
"""Run pytest once per API environment and build an environment matrix dashboard."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from utils.config_reader import ConfigReader
from utils.logger import get_logger
from utils.report_generator import (
    generate_environment_matrix_dashboard,
    read_allure_results,
    summarize_results,
)
from utils.report_opener import open_report
from utils.reporting import REPORT_KIND_CHOICES, finalize_api_reporting, generated_report_path, log_reporting_result

LOGGER = get_logger("environment-matrix")


def main() -> int:
    args, extra_pytest_args = _parse_args()
    settings = ConfigReader(PROJECT_ROOT).read_settings()
    environments = _resolve_environments(args.envs, settings)
    env_workers = _resolve_env_workers(args.env_workers, settings, len(environments))
    _warn_about_nested_parallelism(env_workers, args.parallel_workers)

    matrix_dir = PROJECT_ROOT / "reports" / "environment-matrix"
    results_root = matrix_dir / "results"
    reports_root = matrix_dir / "reports"
    logs_root = matrix_dir / "logs"
    matrix_dir.mkdir(parents=True, exist_ok=True)
    for run_root in (results_root, logs_root):
        if run_root.exists():
            shutil.rmtree(run_root)
        run_root.mkdir(parents=True, exist_ok=True)
    if not args.no_generate_report:
        if reports_root.exists():
            shutil.rmtree(reports_root)
        reports_root.mkdir(parents=True, exist_ok=True)

    pytest_runs = _run_pytest_environment_matrix(
        environments,
        env_workers,
        args,
        extra_pytest_args,
        results_root,
        logs_root,
    )

    if args.no_generate_report:
        return max((pytest_run["exit_code"] for pytest_run in pytest_runs), default=0)

    environment_runs: list[dict] = []
    exit_code = 0

    for pytest_run in pytest_runs:
        env = pytest_run["env"]
        results_dir = pytest_run["results_dir"]
        report_dir = reports_root / env
        env_exit_code = pytest_run["exit_code"]
        exit_code = max(exit_code, env_exit_code)

        report_path = _generate_environment_report(
            results_dir,
            report_dir,
            report_kind=args.report_kind,
            env_name=env,
            install_allure_cli=args.install_allure_cli,
        )
        tests = read_allure_results(results_dir)
        summary = summarize_results(tests)
        if env_exit_code != 0 and summary["status"] == "passed":
            summary["status"] = "failed"

        environment_runs.append(
            {
                "env": env,
                "exit_code": env_exit_code,
                "summary": summary,
                "report_path": report_path,
                "report_href": f"reports/{env}/index.html",
                "log_href": f"logs/{env}.log",
            }
        )

    dashboard_path = generate_environment_matrix_dashboard(environment_runs, matrix_dir)
    LOGGER.info("Generated API environment matrix dashboard: %s", dashboard_path)

    if not args.no_open_report:
        open_report(dashboard_path, LOGGER)

    return exit_code


def _parse_args() -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description="Run pytest once per API environment and build an environment matrix dashboard."
    )
    parser.add_argument(
        "--envs",
        nargs="+",
        help="Environments to run. Defaults to execution.environments in config/settings.yaml.",
    )
    parser.add_argument("--base-url", help="Override REST API base URL for every environment run.")
    parser.add_argument("--graphql-url", help="Override GraphQL endpoint URL for every environment run.")
    parser.add_argument("-m", "--markers", help="Pytest marker expression.")
    parser.add_argument("-n", "--parallel-workers", help="pytest-xdist worker count.")
    parser.add_argument(
        "--env-workers",
        type=int,
        help="Number of environments to execute in parallel. Defaults to execution.env_workers.",
    )
    parser.add_argument("--reruns", help="Retry failed tests.")
    parser.add_argument("--reruns-delay", help="Delay between retries.")
    parser.add_argument("--enable-live-api-examples", action="store_true", help="Run tests marked live.")
    parser.add_argument(
        "--run-reporting-demo",
        action="store_true",
        help="Include the intentional reporting demo failure.",
    )
    parser.add_argument(
        "--no-open-report",
        action="store_true",
        help="Do not open the matrix dashboard in the default browser.",
    )
    parser.add_argument(
        "--no-generate-report",
        action="store_true",
        help="Run pytest per environment without generating reports or the matrix dashboard.",
    )
    parser.add_argument(
        "--report-kind",
        choices=REPORT_KIND_CHOICES,
        default="core",
        help="Per-environment report kind: core, summary, allure, or both. Defaults to core.",
    )
    parser.add_argument(
        "--install-allure-cli",
        action="store_true",
        help="Install the official Allure CLI locally when --report-kind allure/both needs it.",
    )
    return parser.parse_known_args()


def _resolve_environments(
    cli_envs: list[str] | None,
    settings: dict,
) -> list[str]:
    configured_envs = settings.get("execution", {}).get("environments", ["mock"])
    return cli_envs or configured_envs


def _resolve_env_workers(
    cli_env_workers: int | None,
    settings: dict,
    env_count: int,
) -> int:
    configured_workers = settings.get("execution", {}).get("env_workers", 1)
    workers = cli_env_workers if cli_env_workers is not None else configured_workers
    if workers < 1:
        raise SystemExit("--env-workers must be 1 or greater")
    return min(workers, env_count)


def _warn_about_nested_parallelism(
    env_workers: int,
    test_workers: str | None,
) -> None:
    if env_workers <= 1 or not test_workers:
        return
    if not test_workers.isdigit():
        LOGGER.warning(
            "Environment-level parallelism is enabled with pytest workers '%s'. "
            "Check API rate limits because both levels multiply load.",
            test_workers,
        )
        return

    total_workers = env_workers * int(test_workers)
    LOGGER.warning(
        "Nested parallelism enabled: %s environment workers x %s pytest workers = up to %s concurrent test workers. "
        "Lower --env-workers or -n if the API or CI runner becomes unstable.",
        env_workers,
        test_workers,
        total_workers,
    )


def _run_pytest_environment_matrix(
    environments: list[str],
    env_workers: int,
    args: argparse.Namespace,
    extra_pytest_args: list[str],
    results_root: Path,
    logs_root: Path,
) -> list[dict]:
    LOGGER.info(
        "Executing API environment matrix with %s environment worker(s): %s",
        env_workers,
        ", ".join(environments),
    )
    if env_workers == 1:
        return [
            _run_pytest_for_environment(
                env,
                args,
                extra_pytest_args,
                results_root / env,
                logs_root / f"{env}.log",
            )
            for env in environments
        ]

    results_by_env: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=env_workers) as executor:
        futures = {
            executor.submit(
                _run_pytest_for_environment,
                env,
                args,
                extra_pytest_args,
                results_root / env,
                logs_root / f"{env}.log",
            ): env
            for env in environments
        }
        for future in as_completed(futures):
            env = futures[future]
            results_by_env[env] = future.result()
            LOGGER.info(
                "Finished API environment matrix run: %s with exit code %s",
                env,
                results_by_env[env]["exit_code"],
            )

    return [results_by_env[env] for env in environments]


def _run_pytest_for_environment(
    env: str,
    args: argparse.Namespace,
    extra_pytest_args: list[str],
    results_dir: Path,
    log_path: Path,
) -> dict:
    LOGGER.info("Starting API environment matrix run: %s", env)
    results_dir.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "pytest",
        "--env",
        env,
        f"--alluredir={results_dir}",
        "--clean-alluredir",
        "--no-generate-report",
        "--no-open-report",
    ]
    if args.markers:
        command.extend(["-m", args.markers])
    if args.base_url:
        command.extend(["--base-url", args.base_url])
    if args.graphql_url:
        command.extend(["--graphql-url", args.graphql_url])
    if args.parallel_workers:
        command.extend(["-n", args.parallel_workers])
    if args.reruns:
        command.extend(["--reruns", args.reruns])
    if args.reruns_delay:
        command.extend(["--reruns-delay", args.reruns_delay])
    if args.enable_live_api_examples:
        command.append("--enable-live-api-examples")
    if args.run_reporting_demo:
        command.append("--run-reporting-demo")
    command.extend(extra_pytest_args)

    LOGGER.info("Executing: %s", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    _write_environment_log(log_path, command, completed)
    LOGGER.info(
        "Environment %s finished with exit code %s. Log: %s",
        env,
        completed.returncode,
        log_path,
    )
    return {
        "env": env,
        "exit_code": completed.returncode,
        "results_dir": results_dir,
        "log_path": log_path,
    }


def _write_environment_log(
    log_path: Path,
    command: list[str],
    completed: subprocess.CompletedProcess,
) -> None:
    log_path.write_text(
        "$ "
        + " ".join(command)
        + "\n\n=== STDOUT ===\n"
        + completed.stdout
        + "\n\n=== STDERR ===\n"
        + completed.stderr,
        encoding="utf-8",
    )


def _generate_environment_report(
    results_dir: Path,
    report_dir: Path,
    *,
    report_kind: str,
    env_name: str,
    install_allure_cli: bool,
) -> Path:
    allure_output_dir = report_dir if report_kind == "allure" else report_dir / "allure"
    result = finalize_api_reporting(
        PROJECT_ROOT,
        results_dir=results_dir,
        output_dir=report_dir,
        report_kind=report_kind,
        open_report=False,
        env_name=env_name,
        history_dir=PROJECT_ROOT / "reports" / "environment-matrix" / "history" / env_name,
        allure_output_dir=allure_output_dir,
        missing_ok=True,
        install_allure_cli=install_allure_cli,
        logger=LOGGER,
    )
    log_reporting_result(result, LOGGER)
    return generated_report_path(result) or report_dir / "index.html"


if __name__ == "__main__":
    raise SystemExit(main())
