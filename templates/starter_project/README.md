# Starter Project

Use this starter after creating a product-specific repository from `api-automation-framework`.
It shows the smallest useful shape for a product API suite while reusing the framework clients,
fixtures, schema validator, reporting, and CLI.

For the shared portfolio template approach, see the
[automation-core template strategy](https://github.com/iisleem/automation-core/blob/main/docs/template_strategy.md).

## Copy Into A New Product Suite

From the generated repository root:

```bash
cp -R templates/starter_project/config/* config/
cp -R templates/starter_project/services/* services/
cp -R templates/starter_project/schemas/* schemas/
cp -R templates/starter_project/tests/* tests/
```

Then update:

- `config/environments.yaml` with your API hosts.
- `services/product_catalog_service.py` with your product endpoints.
- `schemas/rest/catalog_item.schema.json` with your response contract.
- `tests/smoke/test_catalog_api.py` with your first smoke checks.

## Run The Starter Test

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
pytest tests/smoke/test_catalog_api.py --no-open-report
python framework.py report open --type core
```

The sample test uses a local `httpx.MockTransport`, so it can run before a real API endpoint is available.
