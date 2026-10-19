from __future__ import annotations


def _create(client, name="Acme", domain="acme.com"):
    r = client.post("/competitors", json={"name": name, "domain": domain})
    return r.json()["id"]


def test_first_refresh_creates_snapshots_no_events(client, fake_fetcher):
    cid = _create(client)
    fake_fetcher.pages = {
        "https://acme.com/pricing": "Pro: $29",
        "https://acme.com/changelog": "v1",
        "https://acme.com": "Welcome",
    }
    r = client.post(f"/competitors/{cid}/refresh")
    assert r.status_code == 200
    assert r.json() == []


def test_second_identical_refresh_no_events(client, fake_fetcher):
    cid = _create(client)
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $29"}
    client.post(f"/competitors/{cid}/refresh")
    r = client.post(f"/competitors/{cid}/refresh")
    assert r.json() == []


def test_changed_price_creates_high_event(client, fake_fetcher):
    cid = _create(client)
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $29"}
    client.post(f"/competitors/{cid}/refresh")
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $39"}
    r = client.post(f"/competitors/{cid}/refresh")
    events = r.json()
    assert len(events) == 1
    assert events[0]["severity"] == "high"


def test_acknowledge(client, fake_fetcher):
    cid = _create(client)
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $29"}
    client.post(f"/competitors/{cid}/refresh")
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $39"}
    e = client.post(f"/competitors/{cid}/refresh").json()[0]
    r = client.post(f"/competitors/{cid}/changes/{e['id']}/acknowledge")
    assert r.status_code == 200
    assert r.json()["acknowledged"] is True


def test_acknowledge_unknown(client, fake_fetcher):
    cid = _create(client)
    r = client.post(f"/competitors/{cid}/changes/nope/acknowledge")
    assert r.status_code == 404


class TimeoutFetcher:
    async def fetch(self, url: str) -> str:
        raise TimeoutError("simulated timeout")


def test_timeout_returns_502(client):
    from app.main import app

    app.state.fetcher = TimeoutFetcher()
    cid = _create(client)
    r = client.post(f"/competitors/{cid}/refresh")
    assert r.status_code == 502