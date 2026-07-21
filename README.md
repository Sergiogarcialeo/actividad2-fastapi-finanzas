# Actividad 2 - API Financiera con FastAPI

Proyecto educativo de inferencia financiera con datos cacheados, modelo serializado, FastAPI, pruebas automatizadas y Docker.

## Rama actual

`feature/fastapi-service`

## Flujo completo

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

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API y disponibilidad del modelo |
| GET | `/market-data/{symbol}` | Datos recientes y features procesadas |
| POST | `/predict` | Predicción educativa up/down |
| GET | `/model/metadata` | Metadatos del modelo serializado |
| GET | `/docs` | Swagger UI |

## Ejemplo de predicción

```json
{
  "symbol": "AAPL",
  "prediction_horizon": 1,
  "use_cached_data": true
}
```

## Disclaimer

Herramienta académica de análisis de señales financieras. No constituye asesoría financiera ni recomendación de inversión.
