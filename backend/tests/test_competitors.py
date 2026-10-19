from __future__ import annotations


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_list(client):
    r = client.post("/competitors", json={"name": "Acme", "domain": "acme.com"})
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Acme"
    assert body["id"]

    r2 = client.get("/competitors")
    assert len(r2.json()) == 1


def test_create_invalid_domain(client):
    r = client.post("/competitors", json={"name": "Bad", "domain": "nodot"})
    assert r.status_code == 422


def test_get_unknown(client):
    r = client.get("/competitors/nope")
    assert r.status_code == 404


def test_delete(client):
    r = client.post("/competitors", json={"name": "Acme", "domain": "acme.com"})
    cid = r.json()["id"]
    r2 = client.delete(f"/competitors/{cid}")
    assert r2.status_code == 204
    r3 = client.get(f"/competitors/{cid}")
    assert r3.status_code == 404