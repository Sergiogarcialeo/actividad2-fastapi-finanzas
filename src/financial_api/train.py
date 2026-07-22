"""Entrenamiento y serialización del modelo predictivo."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from financial_api.features import (
    MODEL_FEATURE_COLUMNS,
    TARGET_COLUMN,
    load_processed_dataset,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODEL_VERSION = "random_forest_v1"


def prepare_training_frame(dataset: pd.DataFrame) -> pd.DataFrame:
    """Limpia filas incompletas y deja listo el dataset para entrenamiento."""
    frame = dataset.copy()
    frame = frame.dropna(subset=[*MODEL_FEATURE_COLUMNS, TARGET_COLUMN])
    frame[TARGET_COLUMN] = frame[TARGET_COLUMN].astype(int)
    return frame


def train_model(dataset: pd.DataFrame) -> tuple[RandomForestClassifier, dict[str, float]]:
    """Entrena un clasificador de tendencia up/down para el día siguiente."""
    training_frame = prepare_training_frame(dataset)
    features = training_frame[MODEL_FEATURE_COLUMNS]
    target = training_frame[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1_score": float(f1_score(y_test, predictions, zero_division=0)),
    }
    return model, metrics


def save_artifacts(
    model: RandomForestClassifier,
    dataset: pd.DataFrame,
    metrics: dict[str, float],
) -> None:
    """Persiste el modelo serializado y sus metadatos."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = ARTIFACTS_DIR / "model.joblib"
    metadata_path = ARTIFACTS_DIR / "model_metadata.json"

    joblib.dump(model, model_path)

    metadata = {
        "model_version": MODEL_VERSION,
        "model_type": "RandomForestClassifier",
        "task": "trend_classification",
        "description": (
            "Clasificación educativa de tendencia: predice si el retorno "
            "del siguiente día será positivo."
        ),
        "symbols": sorted(dataset["Symbol"].dropna().unique().tolist()),
        "features": MODEL_FEATURE_COLUMNS,
        "target": TARGET_COLUMN,
        "prediction_horizon": "next_day",
        "trained_at": datetime.now(UTC).isoformat(),
        "metrics": metrics,
        "disclaimer": "Herramienta académica. No constituye asesoría financiera.",
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> None:
    dataset = load_processed_dataset(PROCESSED_DIR)
    model, metrics = train_model(dataset)
    save_artifacts(model, dataset, metrics)
    print(f"Modelo guardado en: {ARTIFACTS_DIR / 'model.joblib'}")
    print(f"Metadatos guardados en: {ARTIFACTS_DIR / 'model_metadata.json'}")
    print(f"Métricas: {metrics}")


if __name__ == "__main__":
    main()
