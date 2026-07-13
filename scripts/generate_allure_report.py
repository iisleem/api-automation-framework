#!/usr/bin/env python3
"""Generate the built-in HTML report from Allure result files."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils.report_generator import generate_html_report
from utils.report_opener import open_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate API automation HTML report")
    parser.add_argument("--results", default="reports/allure-results", help="Allure results directory")
    parser.add_argument("--output", default="reports/allure-report", help="Report output directory")
    parser.add_argument("--open", action="store_true", help="Open the generated report in the default browser")
    args = parser.parse_args()

    report = generate_html_report(Path(args.results), Path(args.output))
    print(f"Report generated: {report}")
    if args.open:
        open_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
