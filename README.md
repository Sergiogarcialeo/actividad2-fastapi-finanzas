# Ingesta de datos (`feature/data-ingestion`)

Este paquete corresponde a la rama **`feature/data-ingestion`** del proyecto.

## Qué incluye

- Descarga de **3 activos** con `yfinance`: `AAPL`, `MSFT`, `GOOG`
- Datos crudos en `data/raw/`
- Features procesadas en `data/processed/`
- Módulos:
  - `src/financial_api/data.py`
  - `src/financial_api/features.py`

## Comandos

```bash
poetry install
poetry run python -m financial_api.data
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

## Features generadas

- `return_1d`: retorno diario
- `sma_5`, `sma_20`: medias móviles
- `volatility_10`: volatilidad rolling
- `return_lag_1`, `return_lag_2`: rezagos
- `target_up_next_day`: variable objetivo educativa (sube al día siguiente)

> Herramienta académica. No es asesoría financiera.
