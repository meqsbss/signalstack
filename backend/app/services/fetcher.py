from __future__ import annotations

import re
from typing import Protocol

import httpx

SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


class Fetcher(Protocol):
    async def fetch(self, url: str) -> str:
        """Return the visible text of the page at url. Raise on network error."""
        ...


class HttpFetcher:
    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout

    async def fetch(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            res = await client.get(url)
            if res.status_code >= 400:
                raise FileNotFoundError(f"{url} returned {res.status_code}")
            return self._extract_text(res.text)

    @staticmethod
    def _extract_text(html: str) -> str:
        html = SCRIPT_STYLE_RE.sub("", html)
        text = TAG_RE.sub("", html)
        text = text.replace("&nbsp;", " ").replace("&amp;", "&")
        return WS_RE.sub(" ", text).strip()


class FakeFetcher:
    """Test fetcher. Returns pre-seeded content keyed by URL."""

    def __init__(self, pages: dict[str, str]) -> None:
        self.pages = pages

    async def fetch(self, url: str) -> str:
        if url not in self.pages:
            raise FileNotFoundError(f"No fake page for {url}")
        return self.pages[url]


def urls_for(domain: str) -> dict[str, str]:
    return {
        "pricing": f"https://{domain}/pricing",
        "changelog": f"https://{domain}/changelog",
        "homepage": f"https://{domain}",
    }