# Troubleshooting

## `ModuleNotFoundError`

Activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Live Tests Are Skipped

Live tests are skipped by default. Enable them explicitly:

```bash
ENABLE_LIVE_API_EXAMPLES=true python framework.py run --live -m live --env qa
```

## Schema Validation Fails

Check the failure path in the assertion message, then compare:

- API response body
- JSON schema required fields
- enum values
- date or date-time formats

## CI Has No Secrets

The default CI suite runs mock and contract tests only. Add GitHub Actions secrets later for live smoke tests.

## Report Was Not Opened

The default generated report is the automation-core product report:

```text
reports/automation-report/index.html
reports/automation-report/report-data.json
```

Open it through the CLI when browser opening is disabled or skipped in CI:

```bash
python framework.py report open --type core
```

## Official Allure Is Missing

Official Allure is optional. Use the core report by default, or request Allure explicitly:

```bash
python framework.py run --report-kind both --install-allure-cli
python framework.py report generate --report-kind allure --install-allure-cli
```

When `--report-kind both` is used, missing or failing official Allure generation is reported as a warning while the core report remains available.
