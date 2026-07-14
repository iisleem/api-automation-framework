## What Changed

- TODO

## Why

- TODO

## Validation

- [ ] `ruff check .`
- [ ] `ruff format --check .`
- [ ] `pytest tests/helpers --no-generate-report --no-open-report -q`
- [ ] `pytest -m "not live and not reporting_demo" --no-open-report -q`
- [ ] `python framework.py run --matrix --envs mock --markers "smoke or contract" --parallel auto --no-open-report`
- [ ] Report generation was checked where relevant, for example `python framework.py report generate --report-kind core --no-open`.

## Impact Checklist

- [ ] Setup, dependency, or `automation-core` changes are documented, or this PR does not affect setup.
- [ ] Config and `.env.example` changes are documented, or this PR does not affect config/secrets.
- [ ] Reports, artifacts, or CI behavior are documented, or this PR does not affect reporting/CI.
- [ ] API-only ownership is preserved; no web, mobile, or core code was changed.

## Notes

- TODO
