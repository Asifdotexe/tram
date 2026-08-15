"""
Network interaction and payload retrieval utilities.

This module handles all outbound HTTP requests to fetch skill payloads and
manifests. It acts as an isolated networking layer, providing functions that
`core.py` uses to pull remote data without exposing the underlying `urllib`
implementation details.
"""

import urllib.request
from urllib.error import HTTPError, URLError


def transform_github_url(url: str) -> str:
    """Converts standard GitHub blob URLs to raw user content URLs."""
    if url.startswith("https://github.com/") and "/blob/" in url:
        return url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
    return url


def fetch_payload(url: str) -> tuple[bytes, int]:
    """Executes GET request with a custom User-Agent header. Returns payload and HTTP status code."""
    req = urllib.request.Request(url, headers={"User-Agent": "TRAM-CLI/1.0"})
    try:
        with urllib.request.urlopen(req) as response:
            payload = response.read()
            return payload, response.status
    except HTTPError as e:
        return b"", e.code
    except URLError:
        # 0 or standard error code for network errors without HTTP response
        return b"", 0
