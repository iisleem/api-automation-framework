#!/usr/bin/env python3
"""Generate API automation reports from Allure result files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from utils.reporting import REPORT_KIND_CHOICES, finalize_api_reporting, print_reporting_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate API automation reports")
    parser.add_argument("--results", default="reports/allure-results", help="Allure results directory")
    parser.add_argument("--output", default="reports/automation-report", help="Report output directory")
    parser.add_argument(
        "--report-kind",
        choices=REPORT_KIND_CHOICES,
        default="core",
        help="Report kind: core, summary, allure, or both. Defaults to core.",
    )
    parser.add_argument("--env", default="mock", help="Environment metadata to include in the core report")
    parser.add_argument("--base-url", help="REST API base URL metadata to include in the core report")
    parser.add_argument("--graphql-url", help="GraphQL URL metadata to include in the core report")
    parser.add_argument("--open", action="store_true", help="Open the generated report in the default browser")
    parser.add_argument(
        "--install-allure-cli",
        action="store_true",
        help="Install the official Allure CLI locally when --report-kind allure/both needs it.",
    )
    args = parser.parse_args()

    result = finalize_api_reporting(
        PROJECT_ROOT,
        results_dir=(PROJECT_ROOT / args.results).resolve(),
        output_dir=(PROJECT_ROOT / args.output).resolve(),
        report_kind=args.report_kind,
        open_report=args.open,
        env_name=args.env,
        base_url=args.base_url,
        graphql_url=args.graphql_url,
        install_allure_cli=args.install_allure_cli,
    )
    print_reporting_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
