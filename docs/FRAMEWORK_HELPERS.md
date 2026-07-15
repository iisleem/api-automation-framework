# Framework Helpers Catalog

Reusable helpers for common API automation tasks. Each helper is designed to be small, explicit, and safe to use in tests without hiding real product issues.

## Search

Open this file in a browser or editor and use search for helper names, tags, or categories. For a browser-native searchable catalog, open:

```text
docs/helpers_catalog.html
```

## Helper Index

| Helper | Category | Tags | Description |
| --- | --- | --- | --- |
| `ApiClient` | API | rest, httpx, api | Primary HTTPX client for REST API tests. |
| `RequestsApiClient` | API | requests, session, api | Optional requests-based client for teams that prefer requests. |
| `GraphQLClient` | GraphQL | graphql, query, variables | Executes inline GraphQL queries or query files. |
| `assert_status`, `assert_json_path` | API | status, json, assertion | Asserts response status codes and nested JSON fields. |
| `SchemaValidator` | Contracts | json schema, contract | Validates payloads against JSON Schema Draft 2020-12. |
| `BearerTokenAuth`, `BasicAuth`, `ApiKeyAuth` | Auth | auth, token, api key | Builds authentication headers or query params. |
| `redact_headers` | Auth | redaction, secrets | Masks sensitive headers in logs and attachments. |
| `assert_security_headers` | Security | headers, smoke | Runs lightweight API security header checks. |
| `assert_no_sensitive_values_in_text` | Security | secrets, response body | Detects common secret-like values in response text. |
| `assert_no_sensitive_values_in_json` | Security | secrets, json | Detects common secret-like values in JSON payloads. |
| `assert_response_time_under` | Performance | timing, response | Validates response elapsed time. |
| `summarize_response_timings` | Performance | timing, summary | Summarizes multiple response timings. |
| `wait_until` | Wait | polling, retry, timeout | Repeats a condition until it returns a truthy value or times out. |
| `poll_until` | Wait | polling, predicate, api | Repeats an action until a predicate accepts its result. |
| `extract_otp` | Text | otp, regex, parsing | Extracts the first OTP-like value from text. |
| `extract_first_match` | Text | regex, parsing | Extracts the first regex match or first capture group. |
| `extract_numbers` | Text | numbers, parsing | Returns all numeric groups from text. |
| `normalize_text` | Text | cleanup, string | Collapses repeated whitespace for stable text comparisons. |
| `random_email` | Data | test data, email, random | Generates unique email addresses for test data. |
| `random_username` | Data | test data, user, random | Generates random usernames. |
| `random_phone` | Data | test data, phone, random | Generates random phone numbers. |
| `unique_id` | Data | id, unique, random | Generates short unique IDs with a prefix. |
| `timestamped_value` | Data | timestamp, unique | Generates timestamped values for stable uniqueness. |
| `booking_payload` | Data | payload, api, fixture | Generates a demo booking request payload. |
| `require_env`, `optional_env` | Environment | env, secrets | Reads required or optional environment variables. |
| `validate_required_envs` | Environment | env, validation | Validates a list of required environment variables. |
| `mask_secret` | Environment | secrets, logging | Masks secret values for safer logging. |
| `build_url` | URL | query, endpoint | Builds a URL with path and query parameters. |
| `parse_query_params`, `get_query_param` | URL | query, assertion | Reads query parameters from URLs. |
| `remove_query_param` | URL | query, cleanup | Removes a query parameter from a URL. |
| `wait_for_file` | Files | file, wait | Waits for a file matching a glob pattern. |
| `assert_file_exists` | Files | file, assertion | Asserts that a path exists and is a file. |
| `assert_file_extension` | Files | file, extension | Asserts file extension. |
| `read_csv_file`, `assert_csv_headers` | Files | csv, validation | Reads and validates CSV files. |
| `read_json_file`, `assert_json_file_field` | Files | json, validation | Reads and validates JSON files. |
| `today`, `tomorrow`, `yesterday` | Date/Time | date, timezone | Returns relative dates, optionally timezone-aware. |
| `add_days`, `format_date`, `parse_date` | Date/Time | date, formatting | Date arithmetic, formatting, and parsing helpers. |
| `CleanupRegistry`, `assert_cleanup_success` | Cleanup | cleanup, teardown, test data | Registers cleanup actions and validates teardown results. |
| `SoftAssert`, `soft_assert` | Assertions | soft assertion, grouped failures | Collects assertion failures and reports them together at the end. |
| `step`, `attach_json`, `attach_text`, `attach_file` | Allure Debug | allure, attachment, reporting | Adds reusable Allure steps and attachments. |

## API Clients

### `ApiClient`

Use the primary HTTPX client for REST API tests.

```python
from clients import ApiClient


client = ApiClient("https://api.example.test")
response = client.get("/health", expected_status=200)
```

### `GraphQLClient`

Use inline GraphQL queries or query files.

```python
from clients import GraphQLClient


client = GraphQLClient("https://api.example.test", endpoint="/graphql")
response = client.execute_file(
    "data/graphql/country_query.graphql",
    variables={"code": "JO"},
    operation_name="CountryByCode",
)
client.assert_no_errors(response.json())
```

### `RequestsApiClient`

Use this only when a project needs requests-specific behavior.

```python
from clients import RequestsApiClient


client = RequestsApiClient("https://api.example.test")
response = client.get("/health", expected_status=200)
```

## Auth Helpers

```python
from utils.helpers.auth import ApiKeyAuth, BasicAuth, BearerTokenAuth, build_auth_from_env


auth = BearerTokenAuth("token")
headers = auth.headers()
```

Environment-based auth order:

1. `API_BEARER_TOKEN`
2. `API_KEY` with optional `API_KEY_NAME`
3. `API_USERNAME` and `API_PASSWORD`
4. No auth

## Schema Validation

```python
from utils.helpers.schema import SchemaValidator


validator = SchemaValidator()
validator.assert_matches_schema(response.json(), "schemas/rest/health.schema.json")
```

## API Assertions

```python
from utils.helpers.assertions import assert_json_path, assert_status


assert_status(response, 200)
assert_json_path(response.json(), "data.users[0].id", 123)
```

## Security Helpers

```python
from utils.helpers.security import assert_no_sensitive_values_in_json, assert_security_headers


assert_security_headers(response)
assert_no_sensitive_values_in_json(response.json())
```

Tune required security headers per API. Lower environments often differ from production.

## Performance Helpers

```python
from utils.helpers.performance import assert_response_time_under


assert_response_time_under(response, 1000)
```

Use realistic thresholds per environment because CI runners and shared test APIs can be slower than local runs.

## Wait Helpers

Use for eventually consistent APIs, async jobs, emails, files, or database state.

```python
from utils.helpers.wait import wait_until


job = wait_until(
    lambda: get_job_if_ready(),
    timeout_seconds=30,
    interval_seconds=2,
    failure_message="Job was not completed.",
)
```

## Test Data Generators

```python
from utils.helpers.data import random_email, timestamped_value, unique_id


email = random_email(domain="example.test", prefix="qa")
order_id = unique_id("order")
run_name = timestamped_value("run")
```

## Cleanup Helpers

Use `CleanupRegistry` when a test creates API resources and needs reliable teardown.

```python
from utils.helpers.cleanup import CleanupRegistry, assert_cleanup_success


cleanup = CleanupRegistry()
cleanup.add("delete user", api_client.delete, "/users/123", expected_status=[200, 204, 404])

results = cleanup.run_all()
assert_cleanup_success(results)
```

## Soft Assertions

```python
from utils.helpers.soft_assertions import soft_assert


softly = soft_assert()
softly.assert_equal(payload["status"], "ok", "status should be ok")
softly.assert_in("id", payload, "payload should include id")
softly.assert_all()
```

## Allure Debug Helpers

```python
from utils.helpers.allure_debug import attach_json, step


with step("Validate health response"):
    attach_json(response.json(), "health response")
```

These helpers write Allure-compatible steps and attachments. The default post-run report is still the
automation-core product report at `reports/automation-report/index.html`, with structured data at
`reports/automation-report/report-data.json`; official Allure is optional with
`--report-kind allure` or `--report-kind both`.

## Helper Tests

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
