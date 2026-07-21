"""Pruebas de la API FastAPI."""

import pytest
from fastapi.testclient import TestClient

from financial_api.api import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_loaded"] is True
    assert payload["model_version"] == "random_forest_v1"


def test_market_data_endpoint(client: TestClient) -> None:
    response = client.get("/market-data/AAPL")
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "AAPL"
    assert "close" in payload
    assert "features" in payload


def test_market_data_unknown_symbol(client: TestClient) -> None:
    response = client.get("/market-data/UNKNOWN")
    assert response.status_code == 404


def test_predict_endpoint(client: TestClient) -> None:
    response = client.post(
        "/predict",
        json={
            "symbol": "MSFT",
            "prediction_horizon": 1,
            "use_cached_data": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "MSFT"
    assert payload["prediction"] in {"up", "down"}
    assert 0.0 <= payload["probability_up"] <= 1.0


def test_predict_rejects_live_download_flag(client: TestClient) -> None:
    response = client.post(
        "/predict",
        json={
            "symbol": "GOOG",
            "prediction_horizon": 1,
            "use_cached_data": False,
        },
    )
    assert response.status_code == 400


def test_model_metadata_endpoint(client: TestClient) -> None:
    response = client.get("/model/metadata")
    assert response.status_code == 200
    payload = response.json()
    assert payload["model_version"] == "random_forest_v1"
    assert len(payload["symbols"]) >= 3
    assert "metrics" in payload
