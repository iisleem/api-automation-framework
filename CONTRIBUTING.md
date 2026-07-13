# Contributing

Thanks for improving the API automation framework.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
python framework.py doctor
pytest
```

## Guidelines

- Keep tests deterministic by default. Live API examples should be opt-in.
- Put reusable request logic in `clients/` or `services/`, not directly in test files.
- Keep secrets in environment variables or local `.env` files that are not committed.
- Add or update JSON schemas when response contracts change.
- Prefer focused fixtures and helpers over broad global state.
