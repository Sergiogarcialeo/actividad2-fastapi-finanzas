"""Pruebas del entrenamiento y artefactos del modelo."""

import json
from pathlib import Path

import joblib

from financial_api.predict import load_metadata, load_model, predict_symbol

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


def test_model_artifact_exists() -> None:
    assert (ARTIFACTS_DIR / "model.joblib").exists()


def test_metadata_artifact_exists() -> None:
    assert (ARTIFACTS_DIR / "model_metadata.json").exists()


def test_model_can_be_loaded() -> None:
    model = load_model()
    assert hasattr(model, "predict")


def test_metadata_has_required_fields() -> None:
    metadata = load_metadata()
    for field in (
        "model_version",
        "symbols",
        "features",
        "prediction_horizon",
        "metrics",
    ):
        assert field in metadata


def test_predict_symbol_returns_contract_fields() -> None:
    result = predict_symbol("AAPL")
    assert result["symbol"] == "AAPL"
    assert result["prediction"] in {"up", "down"}
    assert 0.0 <= result["probability_up"] <= 1.0
    assert result["model_version"]
    assert result["prediction_horizon"] == "next_day"


def test_metadata_symbols_include_three_assets() -> None:
    metadata = load_metadata()
    assert len(metadata["symbols"]) >= 3


def test_model_metadata_is_valid_json_file() -> None:
    content = (ARTIFACTS_DIR / "model_metadata.json").read_text(encoding="utf-8")
    payload = json.loads(content)
    assert payload["model_type"] == "RandomForestClassifier"


def test_model_joblib_is_deserializable() -> None:
    model = joblib.load(ARTIFACTS_DIR / "model.joblib")
    assert model is not None
