"""Smoke tests for the HTTP API using the bundled dataset."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_datasets():
    r = client.get("/api/datasets")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(d["slug"] == "european-space-companies" for d in data)


def test_dataset_detail():
    r = client.get("/api/datasets/european-space-companies")
    assert r.status_code == 200
    payload = r.json()
    assert payload["rowCount"] > 0
    assert {"name", "type", "role"} <= set(payload["columns"][0])


def test_unknown_dataset_404():
    assert client.get("/api/datasets/does-not-exist").status_code == 404
