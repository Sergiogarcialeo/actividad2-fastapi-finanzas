# Actividad 2 - API Financiera con FastAPI

Proyecto educativo de inferencia financiera con datos cacheados, modelo serializado y entrenamiento reproducible.

## Rama actual

`feature/model-training`

## Flujo de esta rama

```bash
poetry install
poetry run python -m financial_api.data
poetry run python -m financial_api.train
poetry run pytest
```

## Qué hace el entrenamiento

- Usa `data/processed/all_features.parquet`
- Entrena un `RandomForestClassifier`
- Tarea: clasificar si el retorno del siguiente día será positivo
- Guarda:
  - `artifacts/model.joblib`
  - `artifacts/model_metadata.json`

## Disclaimer

Herramienta académica de análisis de señales financieras. No constituye asesoría financiera ni recomendación de inversión.
