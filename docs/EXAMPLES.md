# API Examples

This repository includes runnable examples for both local mock coverage and opt-in live API coverage.

## Mock API Example

Run the local mock example when you want a quick end-to-end API framework recipe without external calls:

```bash
python framework.py run --env mock --markers examples --report-kind core --no-open-report
```

The mock example in `tests/examples/test_mock_api_example.py` demonstrates:

- `ApiClient` with `httpx.MockTransport`.
- A service wrapper through `BookingService`.
- JSON Schema validation against `schemas/rest/booking.schema.json`.
- Reusable assertion helpers for status, headers, and JSON paths.
- Request/response artifacts in the generated core report.

The default report output is:

```text
reports/automation-report/index.html
reports/automation-report/report-data.json
```

`report-data.json` includes structured run summary, timeline, and signals data for downstream inspection.

## Live API Example

The live example in `tests/examples/test_live_api_example.py` is opt-in because it can call a deployed API.
Use it only after configuring the target environment and any required secrets:

```bash
python framework.py run --env qa --live --report-kind core --no-open-report
```

Live examples are skipped unless `--live` is provided.
