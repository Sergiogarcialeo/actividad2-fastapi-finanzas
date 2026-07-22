"""Contratos Pydantic de entrada y salida de la API."""

from typing import Any

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    symbol: str = Field(..., description="Ticker del activo, por ejemplo AAPL")
    prediction_horizon: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Horizonte educativo de predicción en días",
    )
    use_cached_data: bool = Field(
        default=True,
        description="Usar dataset local cacheado en lugar de descargar en vivo",
    )


class PredictResponse(BaseModel):
    symbol: str
    prediction: str
    probability_up: float
    model_version: str
    prediction_horizon: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str | None = None


class MarketDataResponse(BaseModel):
    symbol: str
    latest_date: str
    close: float
    features: dict[str, float | None]


class ModelMetadataResponse(BaseModel):
    model_version: str
    model_type: str
    task: str
    description: str
    symbols: list[str]
    features: list[str]
    target: str
    prediction_horizon: str
    trained_at: str
    metrics: dict[str, Any]
    disclaimer: str
