"""
Network interaction and payload retrieval utilities.

This module handles all outbound HTTP requests to fetch skill payloads and
manifests. It acts as an isolated networking layer, providing functions that
`core.py` uses to pull remote data without exposing the underlying `urllib`
implementation details.

Example:
    >>> url = transform_github_url("https://github.com/user/repo/blob/main/skill.md")
    >>> payload, status = fetch_payload(url)
    >>> if status == 200:
    ...     print("Success!")
"""

import urllib.request
from urllib.error import HTTPError, URLError


def transform_github_url(url: str) -> str:
    """
    Converts standard GitHub blob URLs to raw user content URLs.

    :param url: The standard GitHub URL to process.
    :return: The transformed raw URL.
    """
    if url.startswith("https://github.com/") and "/blob/" in url:
        return url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
    return url


def fetch_payload(url: str) -> tuple[bytes, int]:
    """
    Executes a GET request with a custom User-Agent header.

    :param url: The target URL to fetch.
    :return: A tuple containing the response payload bytes and the HTTP status code.
    """
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
