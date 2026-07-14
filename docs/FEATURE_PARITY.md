# Feature Parity With Web Automation Framework

The web automation framework is the source of truth for portfolio structure, workflow, CLI behavior, reporting behavior, docs style, and helper philosophy. This API framework follows the same pattern while replacing web-only concepts with API-specific equivalents.

## Parity Map

| Web framework feature | API framework equivalent | Status |
| --- | --- | --- |
| Unified `framework.py` CLI | Unified `framework.py` CLI with same command groups | Implemented |
| `doctor` with readiness checks | `doctor` with Python, files, YAML, dependencies, Allure, artifact, and API env checks | Implemented |
| `doctor --strict` | Same behavior | Implemented |
| `doctor --install-allure` | Same behavior | Implemented |
| `run --smoke`, `--regression`, `--e2e`, `--negative`, `--helpers` | Same marker-driven behavior | Implemented |
| Raw `--markers` expression | Same behavior | Implemented |
| Extra pytest args after `--` | Same passthrough behavior | Implemented |
| Browser selection and browser matrix | API environment selection and environment matrix | Converted |
| `run --browser-workers` | `run --env-workers` | Converted |
| Browser matrix dashboard | API environment matrix dashboard | Converted |
| automation-core product report | Default post-run report generated at `reports/automation-report/index.html` | Implemented |
| Official Allure report generation | Optional through `--report-kind allure` or `--report-kind both` | Implemented |
| Built-in HTML report summary | Available through `--report-kind summary` | Implemented |
| Local Allure CLI install | Optional through `--install-allure-cli` or `doctor --install-allure` | Implemented |
| Safe report opening through local HTTP server | Same behavior | Implemented |
| `report open --type auto/matrix/core/allure` | Same behavior with environment matrix and core report | Implemented |
| `helpers` and `helpers --guide` | Same behavior | Implemented |
| `ConfigReader` class | Same style with env var expansion | Implemented |
| `DataReader` class | Same style for `data/` files | Implemented |
| JSON/YAML config layout | Same top-level style adapted for API | Implemented |
| Page Object Model | API service object layer | Converted |
| SauceDemo flows | API service flows and examples | Converted |
| Screenshots, videos, Playwright traces | Request/response Allure attachments and API reports | Converted |
| Self-healing locators | Not applicable to API tests | Not applicable |
| Browser storage/session helpers | API auth helpers and reusable clients | Converted |
| API helper for hybrid UI/API tests | API-first HTTPX and requests clients | Expanded |
| Security helper | API header and sensitive response leak helpers | Converted |
| Performance helper | API response timing helpers | Converted |
| Polling helper | Same behavior plus API predicate polling | Implemented |
| Text helper | Same behavior | Implemented |
| Data generators | Same behavior plus API payload generator | Implemented |
| File and structured file helpers | Same behavior | Implemented |
| URL helpers | Same behavior | Implemented |
| Date/time helpers | Same behavior | Implemented |
| Env/secrets helpers | Same behavior | Implemented |
| Cleanup registry | Same behavior for API-created resources | Implemented |
| Soft assertions | Same behavior | Implemented |
| Allure debug helpers | Same behavior without page-specific helpers | Implemented |
| Email OTP helpers | Useful but not core API framework; can be added when API auth scenarios need it | Deferred |
| Database helpers | Project-specific; can be added when API tests need DB-backed assertions | Deferred |
| PDF helpers | Not core API framework; can be added for document APIs | Deferred |
| Accessibility, visual, keyboard, form, table, notification, browser network helpers | Web-only | Not applicable |

## API-Specific Additions

- GraphQL client and query-file support
- JSON Schema response validation
- OpenAPI contract examples
- Auth providers for bearer token, basic auth, API keys, and query keys
- Request/response Allure attachments with sensitive header redaction
- automation-core product report with serializable API run metadata
- Environment matrix execution for API targets
- Live API examples skipped by default

## Maintainer Rule

When adding a feature to this repository:

1. Check whether the web framework already has a matching pattern.
2. Keep CLI names, docs style, config style, and marker behavior consistent where possible.
3. Convert web-only behavior into an API-native equivalent instead of copying it.
4. Document the decision here when a web feature is not applicable or intentionally deferred.
