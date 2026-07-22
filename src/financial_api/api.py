"""Aplicación FastAPI para inferencia financiera educativa."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException

from financial_api.predict import (
    get_market_snapshot,
    load_metadata,
    load_model,
    predict_symbol,
)
from financial_api.schemas import (
    HealthResponse,
    MarketDataResponse,
    ModelMetadataResponse,
    PredictRequest,
    PredictResponse,
)

_model: Any | None = None
_metadata: dict[str, Any] | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Carga el modelo al iniciar la aplicación."""
    global _model, _metadata
    _model = load_model()
    _metadata = load_metadata()
    yield
    _model = None
    _metadata = None


app = FastAPI(
    title="API Financiera Educativa",
    description=(
        "Servicio académico de inferencia sobre señales financieras. "
        "No constituye asesoría financiera."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Confirma que la API está activa y que el modelo está disponible."""
    return HealthResponse(
        status="ok",
        model_loaded=_model is not None,
        model_version=_metadata["model_version"] if _metadata else None,
    )


@app.get("/market-data/{symbol}", response_model=MarketDataResponse)
def market_data(symbol: str) -> MarketDataResponse:
    """Devuelve la observación más reciente y features procesadas de un activo."""
    try:
        snapshot = get_market_snapshot(symbol)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return MarketDataResponse(**snapshot)


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    """Genera una predicción usando el modelo serializado y datos cacheados."""
    if not request.use_cached_data:
        raise HTTPException(
            status_code=400,
            detail="Esta versión educativa solo soporta inferencia con datos cacheados.",
        )

    try:
        result = predict_symbol(request.symbol)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return PredictResponse(**result)


@app.get("/model/metadata", response_model=ModelMetadataResponse)
def model_metadata() -> ModelMetadataResponse:
    """Retorna metadatos del modelo entrenado."""
    if _metadata is None:
        raise HTTPException(status_code=503, detail="Metadatos del modelo no disponibles.")
    return ModelMetadataResponse(**_metadata)
