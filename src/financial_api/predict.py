"""Carga del modelo y generación de predicciones offline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from financial_api.features import MODEL_FEATURE_COLUMNS, get_symbol_features

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_model() -> Any:
    """Carga el modelo serializado desde artifacts/."""
    model_path = ARTIFACTS_DIR / "model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en {model_path}. "
            "Ejecuta: poetry run python -m financial_api.train"
        )
    return joblib.load(model_path)


def load_metadata() -> dict[str, Any]:
    """Carga los metadatos del modelo desde JSON."""
    metadata_path = ARTIFACTS_DIR / "model_metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"No se encontraron metadatos en {metadata_path}. "
            "Ejecuta: poetry run python -m financial_api.train"
        )
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def get_latest_feature_row(symbol: str) -> pd.Series:
    """Obtiene la fila más reciente con features completas para un símbolo."""
    symbol_data = get_symbol_features(PROCESSED_DIR, symbol)
    valid_rows = symbol_data.dropna(subset=MODEL_FEATURE_COLUMNS)
    if valid_rows.empty:
        raise ValueError(f"No hay features válidas para el símbolo {symbol}")
    return valid_rows.iloc[-1]


def predict_symbol(symbol: str) -> dict[str, Any]:
    """Genera una predicción up/down usando datos cacheados locales."""
    model = load_model()
    metadata = load_metadata()
    latest_row = get_latest_feature_row(symbol)

    feature_frame = latest_row[MODEL_FEATURE_COLUMNS].to_frame().T
    probabilities = model.predict_proba(feature_frame)[0]
    prediction_value = int(model.predict(feature_frame)[0])

    classes = list(model.classes_)
    probability_up = float(probabilities[classes.index(1)]) if 1 in classes else 0.0

    return {
        "symbol": symbol.upper(),
        "prediction": "up" if prediction_value == 1 else "down",
        "probability_up": round(probability_up, 4),
        "model_version": metadata["model_version"],
        "prediction_horizon": metadata["prediction_horizon"],
    }


def get_market_snapshot(symbol: str) -> dict[str, Any]:
    """Devuelve la observación más reciente disponible para un activo."""
    latest_row = get_latest_feature_row(symbol)
    features = {
        column: None if pd.isna(latest_row[column]) else float(latest_row[column])
        for column in MODEL_FEATURE_COLUMNS
    }

    return {
        "symbol": symbol.upper(),
        "latest_date": pd.Timestamp(latest_row["Date"]).date().isoformat(),
        "close": float(latest_row["Close"]),
        "features": features,
    }
