# API Contracts

The framework supports two contract layers:

- JSON Schema files in `schemas/` for response validation inside tests.
- OpenAPI files in `contracts/openapi/` for broader API documentation and compatibility checks.

## Recommended Workflow

1. Keep one schema per meaningful response type.
2. Validate smoke responses against schemas.
3. Add negative schemas when an API has a standard error shape.
4. Keep OpenAPI contracts close to the deployed API version.
5. Run `pytest -m contract` in CI.

## Schema Naming

Use readable names:

```text
schemas/rest/booking.schema.json
schemas/rest/token_response.schema.json
schemas/graphql/country_response.schema.json
```

## OpenAPI Naming

Use service or domain names:

```text
contracts/openapi/demo_booking_api.yaml
contracts/openapi/accounts_api.yaml
contracts/openapi/payments_api.yaml
```
