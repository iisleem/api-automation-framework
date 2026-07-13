# Security Policy

Do not commit secrets, access tokens, cookies, API keys, private URLs, or production payloads.

Use environment variables for credentials:

```bash
export API_BEARER_TOKEN="..."
export API_KEY="..."
```

When adding logs or reports, redact sensitive headers and fields. The framework redacts common authorization headers by default, but reviewers should still check generated artifacts before publishing them.
