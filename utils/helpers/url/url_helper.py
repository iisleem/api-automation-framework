from __future__ import annotations

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def build_url(base_url: str, path: str = "", query_params: dict | None = None) -> str:
    base = base_url.rstrip("/")
    normalized_path = path if path.startswith("/") or not path else f"/{path}"
    url = f"{base}{normalized_path}"
    if not query_params:
        return url
    return f"{url}?{urlencode(query_params, doseq=True)}"


def parse_query_params(url: str) -> dict[str, list[str]]:
    return parse_qs(urlparse(url).query, keep_blank_values=True)


def get_query_param(url: str, name: str) -> str | None:
    values = parse_query_params(url).get(name)
    if not values:
        return None
    return values[0]


def remove_query_param(url: str, name: str) -> str:
    parsed = urlparse(url)
    params = parse_query_params(url)
    params.pop(name, None)
    query = urlencode(params, doseq=True)
    return urlunparse(parsed._replace(query=query))
