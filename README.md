# Actividad 2 - API Financiera con FastAPI

Proyecto educativo de inferencia financiera con datos cacheados, modelo serializado y entrenamiento reproducible.

## Rama actual

`feature/model-training`

## Qué incluye

- Descarga de **3 activos** con `yfinance`: `AAPL`, `MSFT`, `GOOG`
- Datos crudos en `data/raw/`
- Features procesadas en `data/processed/`
- Entrenamiento y serialización del modelo en `artifacts/`
- Módulos:
  - `src/financial_api/data.py`
  - `src/financial_api/features.py`
  - `src/financial_api/train.py`

## Flujo de esta rama

```bash
poetry install
poetry run python -m financial_api.data
poetry run python -m financial_api.train
poetry run pytest
```

Opcional, volver a descargar con otros símbolos:

```bash
poetry run python -m financial_api.data --symbols AAPL MSFT GOOG --period 2y
```

## Salidas esperadas

- `data/raw/aapl.csv`, `msft.csv`, `goog.csv`, `all_symbols.csv`
- `data/processed/aapl_features.parquet`, etc.
- `data/processed/all_features.parquet`
- `data/processed/all_features.csv`
- `artifacts/model.joblib`
- `artifacts/model_metadata.json`

## Features generadas

- `return_1d`: retorno diario
- `sma_5`, `sma_20`: medias móviles
- `volatility_10`: volatilidad rolling
- `return_lag_1`, `return_lag_2`: rezagos
- `target_up_next_day`: variable objetivo educativa (sube al día siguiente)

## Qué hace el entrenamiento

- Usa `data/processed/all_features.parquet`
- Entrena un `RandomForestClassifier`
- Tarea: clasificar si el retorno del siguiente día será positivo
- Guarda:
  - `artifacts/model.joblib`
  - `artifacts/model_metadata.json`

## Disclaimer

Herramienta académica de análisis de señales financieras. No constituye asesoría financiera ni recomendación de inversión.
