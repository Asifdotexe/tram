import urllib.request
from urllib.error import URLError, HTTPError

def transform_github_url(url: str) -> str:
    """Converts standard GitHub blob URLs to raw user content URLs."""
    if url.startswith("https://github.com/") and "/blob/" in url:
        return url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
    return url

def fetch_payload(url: str) -> tuple[bytes, int]:
    """Executes GET request with a custom User-Agent header. Returns payload and HTTP status code."""
    req = urllib.request.Request(url, headers={'User-Agent': 'TRAM-CLI/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            payload = response.read()
            return payload, response.status
    except HTTPError as e:
        return b"", e.code
    except URLError as e:
        # 0 or standard error code for network errors without HTTP response
        return b"", 0
