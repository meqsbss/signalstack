from __future__ import annotations


def test_latest_404_when_empty(client):
    r = client.get("/briefings/latest")
    assert r.status_code == 404


def test_generate_empty(client):
    r = client.post("/briefings/generate")
    assert r.status_code == 200
    assert "No changes" in r.json()["summary_text"]


def test_generate_with_events(client, fake_fetcher):
    cid = client.post("/competitors", json={"name": "Acme", "domain": "acme.com"}).json()["id"]
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $29"}
    client.post(f"/competitors/{cid}/refresh")
    fake_fetcher.pages = {"https://acme.com/pricing": "Pro: $39"}
    client.post(f"/competitors/{cid}/refresh")

    r = client.post("/briefings/generate")
    body = r.json()
    assert body["top_events"][0]["severity"] == "high"
    assert "changes across" in body["summary_text"]

    latest = client.get("/briefings/latest")
    assert latest.json()["id"] == body["id"]