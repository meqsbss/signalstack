from __future__ import annotations

from typing import Protocol


class Fetcher(Protocol):
    async def fetch(self, url: str) -> str:
        """Return the visible text of the page at url. Raise on network error."""
        ...


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