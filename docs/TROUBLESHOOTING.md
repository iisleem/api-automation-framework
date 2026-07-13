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
