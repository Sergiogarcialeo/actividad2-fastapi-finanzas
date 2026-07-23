# Actividad 2 - API Financiera con FastAPI

Proyecto educativo de inferencia financiera con datos cacheados, modelo serializado,
FastAPI, pruebas automatizadas y Docker.

Repositorio: [actividad2-fastapi-finanzas](https://github.com/Sergiogarcialeo/actividad2-fastapi-finanzas)

## Qué incluye

- Descarga de **3 activos** con `yfinance`: `AAPL`, `MSFT`, `GOOG`
- Datos crudos en `data/raw/` y features en `data/processed/`
- Modelo entrenado en `artifacts/model.joblib`
- Metadatos del modelo en `artifacts/model_metadata.json`
- API FastAPI con contratos Pydantic
- Pruebas automatizadas con `pytest`
- `Dockerfile` y `compose.yaml` para ejecución local reproducible

### Módulos principales

| Módulo | Responsabilidad |
|---|---|
| `src/financial_api/data.py` | Ingesta con yfinance y cache local |
| `src/financial_api/features.py` | Cálculo de variables de mercado |
| `src/financial_api/train.py` | Entrenamiento y serialización del modelo |
| `src/financial_api/predict.py` | Inferencia offline con datos cacheados |
| `src/financial_api/api.py` | Endpoints FastAPI |
| `src/financial_api/schemas.py` | Contratos Pydantic |

## Tarea modelada

Clasificación educativa de tendencia: predice si el retorno del **día siguiente**
será positivo (`up`) o negativo (`down`).

## Flujo completo del proyecto

Desde la raíz del repositorio, con rama `main`:

```bash
poetry install
poetry run python -m financial_api.data
poetry run python -m financial_api.train
poetry run uvicorn financial_api.api:app --reload --app-dir src
poetry run pytest
docker build -t financial-api:local .
docker run --rm -p 8000:8080 financial-api:local
docker compose up --build
```

> Los dos primeros pasos son opcionales si ya existen `data/processed/` y `artifacts/`
> en el repositorio. La evaluación offline usa esos archivos cacheados.

### Regenerar datos (opcional)

```bash
poetry run python -m financial_api.data --symbols AAPL MSFT GOOG --period 2y
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API y disponibilidad del modelo |
| GET | `/market-data/{symbol}` | Observación reciente y features procesadas |
| POST | `/predict` | Predicción educativa up/down |
| GET | `/model/metadata` | Metadatos del modelo serializado |
| GET | `/docs` | Swagger UI |

Documentación interactiva: `http://localhost:8000/docs`

## Ejemplo de predicción

Request (`POST /predict`):

```json
{
  "symbol": "AAPL",
  "prediction_horizon": 1,
  "use_cached_data": true
}
```

Response esperada:

```json
{
  "symbol": "AAPL",
  "prediction": "up",
  "probability_up": 0.63,
  "model_version": "random_forest_v1",
  "prediction_horizon": "next_day"
}
```

## Salidas esperadas

- `data/raw/aapl.csv`, `msft.csv`, `goog.csv`, `all_symbols.csv`
- `data/processed/all_features.parquet`, `all_features.csv`
- `artifacts/model.joblib`
- `artifacts/model_metadata.json`

## Features generadas

- `return_1d`: retorno diario
- `sma_5`, `sma_20`: medias móviles
- `volatility_10`: volatilidad rolling
- `return_lag_1`, `return_lag_2`: rezagos
- `target_up_next_day`: variable objetivo educativa

## Docker Compose (recomendado)

```bash
docker compose up --build
```

La API queda disponible en `http://localhost:8000/docs`.

## Despliegue en Azure

API publicada en Azure Container Apps (entorno de evaluación):

| Recurso | URL |
|---|---|
| Swagger UI | https://actividad2-finanzas-api.mangoflower-7aebfde9.eastus.azurecontainerapps.io/docs |
| Health check | https://actividad2-finanzas-api.mangoflower-7aebfde9.eastus.azurecontainerapps.io/health |

## Equipo

Ver `TEAM.md` e `Integrantes.md` para roles y responsabilidades.

## Disclaimer

Herramienta académica de análisis de señales financieras.
**No constituye asesoría financiera** ni recomendación de inversión.
