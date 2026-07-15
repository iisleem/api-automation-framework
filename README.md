# API Automation Framework User Guide

[![Python API Tests](https://github.com/iisleem/api-automation-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/iisleem/api-automation-framework/actions/workflows/api-tests.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)](https://pytest.org/)
[![HTTPX](https://img.shields.io/badge/http-client-httpx-2EAD33.svg)](https://www.python-httpx.org/)
[![Requests](https://img.shields.io/badge/http-client-requests-20232A.svg)](https://requests.readthedocs.io/)
[![Reports](https://img.shields.io/badge/reports-automation--core-2EAD33.svg)](https://github.com/iisleem/automation-core)
[![Allure](https://img.shields.io/badge/Allure-optional-orange.svg)](https://allurereport.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python API automation framework built with Pytest, HTTPX, Requests, JSON Schema, OpenAPI contracts, GraphQL support, automation-core product reporting, optional official Allure reporting, retry support, parallel execution, and GitHub Actions CI.

This repository is the API-focused sibling of the web and mobile automation frameworks in the Fullstack Automation portfolio.
Shared, domain-neutral utilities are consumed from [`automation-core`](https://github.com/iisleem/automation-core) so config, logging, reporting, waits, retries, files, text, data, security, performance, cleanup, and soft assertions stay consistent across the web, mobile, and API frameworks.

## What This Framework Gives You

- Clean API service layer with request details kept out of test files
- Pytest fixtures for API clients, GraphQL clients, config, schemas, users, and payload data
- Unified framework CLI for health checks, test execution, reports, and helper docs
- CLI support for environment, base URL, GraphQL URL, markers, retries, live examples, and parallel execution
- Settings-driven API environment matrix execution with a main dashboard and drill-down environment reports
- Automatic post-run core product report generation from Allure result files
- Official Allure report generation is optional through `--report-kind allure` or `--report-kind both`
- Missing or failing official Allure CLI does not block the core report when `--report-kind both` is used
- Automatic local report opening after test runs, skipped safely in CI/server environments
- REST API client built on `httpx`
- Optional `requests.Session` client for teams that prefer requests
- GraphQL client with query file support
- JSON Schema response validation and OpenAPI contract examples
- Authentication helpers for bearer tokens, basic auth, API keys, and header redaction
- API security smoke helpers for headers and sensitive data leaks
- API performance smoke helpers for response timing
- Cleanup registry and soft assertion helpers for API setup/teardown flows
- Reusable helper library for polling, text extraction, URL building, files, env secrets, and common automation utilities
- JSON test data files for users and request payloads
- YAML environment and framework settings
- Smoke, regression, e2e, negative, contract, REST, GraphQL, auth, helpers, live, and reporting demo markers
- GitHub Actions workflow for CI

## Project Structure

```text
api-automation-framework/
├── clients/
│   ├── api_client.py              # Primary HTTPX REST client
│   ├── graphql_client.py          # GraphQL client wrapper
│   └── requests_client.py         # Optional requests-based client
├── config/
│   ├── settings.yaml              # Timeouts, artifacts, environment matrix, retry defaults
│   └── environments.yaml          # Environment names and API URLs
├── contracts/
│   └── openapi/                   # OpenAPI contracts
├── data/
│   ├── graphql/                   # GraphQL query documents
│   ├── payloads/                  # Request payload data
│   └── users.json                 # Example API users
├── schemas/
│   ├── graphql/                   # GraphQL response schemas
│   └── rest/                      # REST response schemas
├── services/
│   ├── booking_service.py         # Example REST service object
│   └── country_service.py         # Example GraphQL service object
├── tests/
│   ├── smoke/                     # Fast critical API tests
│   ├── regression/                # Broader API behavior tests
│   ├── graphql/                   # GraphQL operation tests
│   ├── contracts/                 # Schema and OpenAPI contract checks
│   ├── helpers/                   # Helper simulation/unit tests
│   └── examples/                  # Opt-in live API examples
├── templates/
│   └── starter_project/           # Copyable product API suite starter
├── utils/
│   ├── allure_cli.py              # Compatibility wrapper over automation-core
│   ├── assertions.py              # Reusable assertion helpers
│   ├── config_reader.py           # API config wrapper over automation-core
│   ├── data_reader.py             # JSON data reader
│   ├── helpers/                   # API helpers plus automation-core compatibility wrappers
│   ├── logger.py                  # Framework logger wrapper over automation-core
│   ├── report_generator.py        # Reporting wrapper over automation-core
│   └── report_opener.py           # Report opener wrapper over automation-core
├── scripts/
│   ├── generate_allure_report.py  # Manual report finalizer helper
│   └── run_environment_matrix.py  # API environment matrix runner and dashboard builder
├── docs/
│   ├── API_CONTRACTS.md           # Contract testing notes
│   ├── EXAMPLES.md                # Runnable mock and opt-in live examples
│   ├── FEATURE_PARITY.md          # Web-to-API feature mapping
│   ├── FRAMEWORK_HELPERS.md       # Helper usage guide
│   ├── SCREENSHOTS.md             # Core report screenshot index
│   ├── WALKTHROUGH.md             # Mock run walkthrough with report screenshots
│   └── helpers_catalog.html       # Searchable helper catalog
├── reports/                       # Allure results, core reports, optional Allure reports, matrix reports, logs
├── logs/                          # Framework logs
├── .github/workflows/
│   └── api-tests.yml              # GitHub Actions pipeline
├── conftest.py                    # Pytest hooks and fixtures
├── framework.py                   # Unified framework CLI
├── pytest.ini                     # Pytest config, markers, Allure results path
├── requirements.txt               # Python dependencies
└── .gitignore
```

## Quick Start

```bash
cd api-automation-framework
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python framework.py doctor
python framework.py run
```

Install `requirements-dev.txt` as well when contributing changes that need local Ruff or CI-equivalent checks.

For a guided mock run with screenshots of the core report and request/response artifacts, see the [API Framework Walkthrough](docs/WALKTHROUGH.md).
For a compact image index, see the [Screenshot Index](docs/SCREENSHOTS.md).
For runnable mock and opt-in live API examples, see the [Examples Guide](docs/EXAMPLES.md).

## GitHub Template And Starter Project

This repository is configured as a GitHub template. For a product-specific API suite, create a new repository from
this template, then copy the starter files into the generated repository root:

For the shared portfolio template approach, see the
[automation-core template strategy](https://github.com/iisleem/automation-core/blob/main/docs/template_strategy.md).

```bash
cp -R templates/starter_project/config/* config/
cp -R templates/starter_project/services/* services/
cp -R templates/starter_project/schemas/* schemas/
cp -R templates/starter_project/tests/* tests/
```

The starter project includes a small service object, schema, environment config, and smoke test under:

```text
templates/starter_project/
```

After copying it, rename the sample service and test around your product API, update `config/environments.yaml`,
and run:

```bash
pytest tests/smoke/test_catalog_api.py --no-open-report
python framework.py report open --type core
```

## Unified Framework CLI

The easiest entry point is `framework.py`. It wraps the common framework workflows while still allowing direct `pytest` commands whenever you need them.

Check whether the machine is ready:

```bash
python framework.py doctor
```

Run the default green suite:

```bash
python framework.py run
```

Run smoke tests:

```bash
python framework.py run --smoke
```

Run an API environment matrix:

```bash
python framework.py run --matrix
```

Run selected environments:

```bash
python framework.py run --envs mock qa
```

Run environments in parallel and tests in parallel inside each environment:

```bash
python framework.py run --envs mock qa staging --env-workers 3 --parallel 2
```

Open the latest report:

```bash
python framework.py report open
```

Generate a report from existing Allure results:

```bash
python framework.py report generate
```

Open the searchable helper catalog:

```bash
python framework.py helpers
```

Print the helper guide path:

```bash
python framework.py helpers --guide
```

Doctor checks include:

- Python version
- Required project files
- YAML config validity
- Python dependency imports
- Core report readiness and optional Allure CLI availability
- Writable artifact folders
- Optional API authentication environment variables

Use strict mode when warnings should fail setup validation:

```bash
python framework.py doctor --strict
```

The default report does not require the official Allure CLI. Install it only when you want official Allure output:

```bash
python framework.py doctor --install-allure
python framework.py run --report-kind both --install-allure-cli
```

## Daily Test Commands

Run the default green suite:

```bash
python framework.py run
pytest
```

Run smoke tests:

```bash
python framework.py run --smoke
pytest -m smoke
```

Run regression tests:

```bash
python framework.py run --regression
pytest -m regression
```

Run contract tests:

```bash
python framework.py run --contract
pytest -m contract
```

Run GraphQL tests:

```bash
python framework.py run --graphql
pytest -m graphql
```

Run negative tests:

```bash
python framework.py run --negative
pytest -m negative
```

Run in parallel:

```bash
python framework.py run --parallel 2
pytest -n 2
```

Retry failures:

```bash
python framework.py run --reruns 2 --reruns-delay 1
pytest --reruns 2 --reruns-delay 1
```

Run one test file:

```bash
pytest tests/smoke/test_rest_client.py
```

Run one test case:

```bash
pytest tests/smoke/test_rest_client.py::test_rest_client_create_booking_matches_schema
```

Run helper unit tests:

```bash
python framework.py run --helpers --no-generate-report
pytest tests/helpers --no-generate-report
pytest -m helpers --no-generate-report
```

Run opt-in live API examples:

```bash
ENABLE_LIVE_API_EXAMPLES=true python framework.py run --live --env qa
pytest -m live --enable-live-api-examples --env qa
```

## Pytest CLI Options

| Option | Example | Purpose |
| --- | --- | --- |
| `--env` | `pytest --env qa` | Select an environment from `config/environments.yaml` |
| `--base-url` | `pytest --base-url https://qa-api.example.test` | Override the REST API base URL |
| `--graphql-url` | `pytest --graphql-url https://qa-api.example.test/graphql` | Override the GraphQL endpoint URL |
| `--api-timeout` | `pytest --api-timeout 20` | Override request timeout in seconds |
| `-m` | `pytest -m smoke` | Select tests by marker |
| `-n` | `pytest -n 2` | Run tests in parallel with pytest-xdist |
| `--reruns` | `pytest --reruns 2` | Retry failed tests |
| `--reruns-delay` | `pytest --reruns 2 --reruns-delay 1` | Wait between retries |
| `--enable-live-api-examples` | `pytest -m live --enable-live-api-examples` | Include tests that call live APIs |
| `--run-reporting-demo` | `pytest --run-reporting-demo -m reporting_demo` | Include the intentionally failing reporting demo |
| `--report-kind` | `pytest --report-kind core` | Select post-run report kind: `core`, `summary`, `allure`, or `both` |
| `--install-allure-cli` | `pytest --report-kind both --install-allure-cli` | Install official Allure CLI when optional Allure output needs it |
| `--no-open-report` | `pytest --no-open-report` | Generate report but do not open browser |
| `--no-generate-report` | `pytest --no-generate-report` | Disable post-run report generation |

## Unified CLI Options

| Command | Example | Purpose |
| --- | --- | --- |
| `doctor` | `python framework.py doctor` | Validate local setup and project readiness |
| `doctor --strict` | `python framework.py doctor --strict` | Fail when warnings exist |
| `doctor --install-allure` | `python framework.py doctor --install-allure` | Preinstall local Allure CLI if needed |
| `run` | `python framework.py run` | Run the default pytest suite |
| `run --smoke` | `python framework.py run --smoke` | Run smoke tests |
| `run --regression` | `python framework.py run --regression` | Run regression tests |
| `run --contract` | `python framework.py run --contract` | Run contract tests |
| `run --graphql` | `python framework.py run --graphql` | Run GraphQL tests |
| `run --rest` | `python framework.py run --rest` | Run REST tests |
| `run --auth` | `python framework.py run --auth` | Run auth tests |
| `run --negative` | `python framework.py run --negative` | Run negative tests |
| `run --helpers` | `python framework.py run --helpers --no-generate-report` | Run helper simulation/unit tests |
| `run --env` | `python framework.py run --env qa` | Run a normal pytest session in one environment |
| `run --envs` | `python framework.py run --envs mock qa` | Run environment matrix execution |
| `run --env-workers` | `python framework.py run --envs mock qa --env-workers 2` | Run environment suites in parallel |
| `run --parallel` | `python framework.py run --parallel 4` | Run test cases in parallel using pytest-xdist |
| `run --markers` | `python framework.py run --markers "smoke and not flaky"` | Use a raw pytest marker expression |
| `run --reruns` | `python framework.py run --reruns 2 --reruns-delay 1` | Retry failed tests |
| `run --run-reporting-demo` | `python framework.py run --run-reporting-demo --markers reporting_demo` | Include intentional failure demo |
| `run --report-kind` | `python framework.py run --report-kind both` | Generate core, summary, official Allure, or both report kinds |
| `report open` | `python framework.py report open` | Open latest matrix, core, or optional Allure report |
| `report generate` | `python framework.py report generate` | Generate report from existing Allure results |
| `helpers` | `python framework.py helpers` | Open searchable helper catalog |
| `helpers --guide` | `python framework.py helpers --guide` | Print Markdown helper guide path |

Multiple shortcut marker flags are combined as a union. For example, `python framework.py run --smoke --contract`
runs tests marked `smoke or contract`. Use `--markers` for raw pytest expressions such as `smoke and not flaky`.

You can pass extra pytest arguments after `--`:

```bash
python framework.py run --smoke -- --maxfail=1 -k create_booking
```

## API Environment Matrix Execution

The framework supports matrix execution across API environments.

Recommended environment matrix execution:

```bash
python framework.py run --matrix
python scripts/run_environment_matrix.py
```

This reads environments from `config/settings.yaml`:

```yaml
execution:
  environments:
    - mock
  env_workers: 1
```

The matrix runner executes pytest once per environment, then creates:

```text
reports/environment-matrix/index.html              # Main dashboard
reports/environment-matrix/reports/mock/           # Mock environment core product report
reports/environment-matrix/results/mock/           # Mock environment Allure results
reports/environment-matrix/logs/mock.log           # Mock pytest output
```

The main dashboard is the entry point. It shows:

- Environment-level status
- Total tests per environment
- Passed, failed, broken, and skipped counts
- Pass rate
- Duration
- Attention-needed summary
- Links to each environment's detailed core product report
- Links to each environment's execution log

The matrix command returns a non-zero exit code if any environment run fails, so CI can fail correctly while still keeping dashboards and reports available as artifacts.

Environment matrix runs can also execute environments in parallel:

```bash
python scripts/run_environment_matrix.py --envs mock qa staging --env-workers 3
python framework.py run --envs mock qa staging --env-workers 3
```

Parallel execution has two levels:

- Test-case level parallelism: `-n 4` runs test cases in parallel inside each environment using pytest-xdist.
- Environment-level parallelism: `--env-workers 3` runs environment suites in parallel.

Warning: these levels multiply. This command can create up to 12 concurrent test workers:

```bash
python framework.py run --envs mock qa staging --env-workers 3 --parallel 4
```

Start conservatively, then increase based on API rate limits and CI runner capacity.

## Marker Reference

| Marker | Purpose | Example |
| --- | --- | --- |
| `smoke` | Critical fast confidence tests | `pytest -m smoke` |
| `regression` | Broader API behavior coverage | `pytest -m regression` |
| `e2e` | Full API journeys | `pytest -m e2e` |
| `negative` | Validation and error scenarios | `pytest -m negative` |
| `contract` | JSON Schema and OpenAPI checks | `pytest -m contract` |
| `rest` | REST endpoint tests | `pytest -m rest` |
| `graphql` | GraphQL operation tests | `pytest -m graphql` |
| `auth` | Authentication and authorization tests | `pytest -m auth` |
| `security` | Header and sensitive data smoke checks | `pytest -m security` |
| `performance` | Response timing smoke checks | `pytest -m performance` |
| `live` | Tests that call deployed APIs | `pytest -m live --enable-live-api-examples` |
| `reporting_demo` | Intentional failure for artifacts/reporting | `pytest --run-reporting-demo -m reporting_demo` |
| `flaky` | Marker available for retry-oriented tests | `pytest -m flaky --reruns 2` |
| `helpers` | Unit-style helper library tests | `pytest -m helpers --no-generate-report` |

The `reporting_demo` and `live` tests are skipped by default so local and CI runs stay green.

## Reporting Behavior

Every pytest run writes raw Allure results to:

```text
reports/allure-results/
```

At the end of the test session, the framework automatically generates:

```text
reports/automation-report/index.html
reports/automation-report/report-data.json
```

Report generation flow:

1. `--report-kind core` is the default and generates the automation-core product report.
2. `--report-kind summary` generates the legacy single-page summary.
3. `--report-kind allure` generates only the official Allure report and requires the Allure CLI.
4. `--report-kind both` generates the core product report first, then tries official Allure.
5. If official Allure is missing or fails in `both` mode, the core report remains available and the run only logs a warning.
6. If the run is local, the framework opens the selected report through a lightweight local HTTP server unless opening is disabled.
7. If the run is in CI/server mode or browser opening fails, the framework logs a note and does not fail the test run.

Open generated reports through the framework CLI:

```bash
python framework.py report open --type matrix
python framework.py report open --type core
python framework.py report open --type allure
```

Generate report but do not open it:

```bash
python framework.py run --no-open-report
pytest --no-open-report
```

Skip report generation:

```bash
python framework.py run --no-generate-report
pytest --no-generate-report
```

Generate reports manually from existing results:

```bash
python framework.py report generate --report-kind core
python scripts/generate_allure_report.py --report-kind core
python framework.py report generate --report-kind both
```

## Framework Helpers

The framework includes reusable helpers for common API automation tasks so engineers do not need to rebuild the same utilities in every project.

Helper documentation:

- [Framework Helpers Guide](docs/FRAMEWORK_HELPERS.md)
- [Searchable Helpers Catalog](docs/helpers_catalog.html)

Open the searchable catalog from the CLI:

```bash
python framework.py helpers
```

Current helper categories:

- API clients and assertions
- GraphQL query execution
- JSON Schema validation
- API auth and redaction helpers
- API security smoke helpers
- API performance smoke helpers
- Polling and retry helpers
- Text extraction helpers
- Test data generators
- Environment/secrets helpers
- File and structured file helpers
- URL/query parameter helpers
- Date/time helpers
- Cleanup registry helpers
- Soft assertion helpers
- Allure/debug helpers for reusable steps and attachments

Helper tests live under:

```text
tests/helpers/
```

Run them with:

```bash
python framework.py run --helpers --no-generate-report
pytest tests/helpers --no-generate-report
pytest -m helpers --no-generate-report
```

## Working With Test Data

Users are stored in:

```text
data/users.json
```

Payloads are stored in:

```text
data/payloads/
```

GraphQL queries are stored in:

```text
data/graphql/
```

The fixtures `users`, `booking_payload`, `api_client`, `graphql_client`, and `schema_validator` load reusable data and clients for tests.

## Working With Environments

Environment URLs live in:

```text
config/environments.yaml
```

Example:

```yaml
qa:
  base_url: ${API_BASE_URL:-https://api.example.test}
  graphql_url: ${GRAPHQL_BASE_URL:-https://api.example.test/graphql}
```

Run against an environment:

```bash
python framework.py run --env qa
pytest --env qa
```

Override URLs without editing config:

```bash
python framework.py run --base-url https://qa-api.example.test --graphql-url https://qa-api.example.test/graphql
pytest --base-url https://qa-api.example.test --graphql-url https://qa-api.example.test/graphql
```

## Writing New Tests

Follow these rules:

- Keep request construction inside `clients/` or `services/`, not directly inside test files.
- Add endpoint-specific actions to a service object when tests reuse them.
- Use `utils/assertions.py` and `utils.helpers.assertions` for clear assertion steps.
- Use test data from `data/` when values are reusable.
- Add JSON Schema files under `schemas/` for stable response contracts.
- Add a marker such as `smoke`, `regression`, `contract`, `graphql`, `negative`, or `auth`.
- Keep tests readable as API business flows.

Example pattern:

```python
import pytest

from services.booking_service import BookingService


@pytest.mark.smoke
@pytest.mark.rest
def test_create_booking(api_client, schema_validator, booking_payload):
    booking_service = BookingService(api_client)

    response = booking_service.create_booking(booking_payload)

    schema_validator.assert_matches_schema(response.json(), "schemas/rest/booking.schema.json")
```

## Service Object Guidelines

Good API service usage:

- Keep endpoint paths in service classes.
- Expose business actions such as `create_booking`, `get_booking`, and `country_by_code`.
- Keep expected status checks close to the request method.
- Return the raw response when tests need headers, schema validation, or detailed assertions.
- Keep auth and default headers in fixtures/config instead of hardcoding them in tests.

Avoid:

- Repeated endpoint URLs across many tests
- Sleeps or fixed waits
- Assertions hidden inside low-level request helpers
- Tokens or API keys in repository files
- Live API tests in the default CI suite

## CI/CD

The GitHub Actions workflow is:

```text
.github/workflows/api-tests.yml
```

The pipeline:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies from `requirements.txt` and `requirements-dev.txt`.
4. Runs `python framework.py doctor`.
5. Runs the API environment matrix against `mock`.
6. Skips live examples and the intentional reporting demo by default.
7. Generates the environment matrix dashboard and environment drill-down report.
8. Uploads reports and logs as artifacts.

## GitHub Project 4

This repository is part of GitHub Project 4. Use project issues for roadmap slices such as authentication coverage, contract coverage, API environments, reporting improvements, and live example expansion.

## Troubleshooting

If dependencies are missing:

```bash
python framework.py doctor
pip install -r requirements.txt
```

If you want to regenerate the report without rerunning tests:

```bash
python framework.py report generate
python scripts/generate_allure_report.py
```

The generated core product report is written to `reports/automation-report/index.html`, with structured report data in `reports/automation-report/report-data.json`. Official Allure output is optional with `--report-kind allure` or `--report-kind both`.

If you need parallel execution, prefer the supported commands:

```bash
pytest -n 4
python framework.py run --envs mock qa staging --env-workers 3
```

Avoid starting multiple independent `pytest` commands at the same time against the same `reports/allure-results` directory. Each pytest session cleans that directory before writing Allure results, so separate concurrent sessions can race with each other.

## Notes

- The framework is intentionally beginner-friendly but keeps production-style boundaries.
- Normal `pytest` runs stay green because live examples and the reporting demo are skipped by default.
- Use `--run-reporting-demo -m reporting_demo` when you specifically want to demonstrate failed-test reporting.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
