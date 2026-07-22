"""Construcción de features a partir de datos crudos de mercado."""

from pathlib import Path

import pandas as pd

FEATURE_COLUMNS = [
    "Date",
    "Symbol",
    "Close",
    "return_1d",
    "sma_5",
    "sma_20",
    "volatility_10",
    "return_lag_1",
    "return_lag_2",
    "target_up_next_day",
]


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula variables simples de mercado para cada activo."""
    featured = df.copy()
    featured["Date"] = pd.to_datetime(featured["Date"])
    featured = featured.sort_values("Date").reset_index(drop=True)

    featured["return_1d"] = featured["Close"].pct_change()
    featured["sma_5"] = featured["Close"].rolling(window=5).mean()
    featured["sma_20"] = featured["Close"].rolling(window=20).mean()
    featured["volatility_10"] = featured["return_1d"].rolling(window=10).std()
    featured["return_lag_1"] = featured["return_1d"].shift(1)
    featured["return_lag_2"] = featured["return_1d"].shift(2)
    featured["target_up_next_day"] = (featured["return_1d"].shift(-1) > 0).astype("Int64")

    return featured


def build_processed_dataset(
    symbols: list[str],
    raw_dir: Path,
    processed_dir: Path,
) -> Path:
    """Genera archivos procesados por símbolo y un dataset combinado."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_frames: list[pd.DataFrame] = []

    for symbol in symbols:
        raw_path = raw_dir / f"{symbol.lower()}.csv"
        if not raw_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo crudo: {raw_path}")

        raw_df = pd.read_csv(raw_path, parse_dates=["Date"])
        featured = compute_features(raw_df)
        featured["Symbol"] = symbol.upper()

        symbol_path = processed_dir / f"{symbol.lower()}_features.parquet"
        featured.to_parquet(symbol_path, index=False)
        processed_frames.append(featured)

    combined = pd.concat(processed_frames, ignore_index=True)
    combined_path = processed_dir / "all_features.parquet"
    combined.to_parquet(combined_path, index=False)
    combined.to_csv(processed_dir / "all_features.csv", index=False)

    return combined_path


def load_processed_dataset(processed_dir: Path) -> pd.DataFrame:
    """Carga el dataset procesado combinado desde disco."""
    combined_path = processed_dir / "all_features.parquet"
    if not combined_path.exists():
        raise FileNotFoundError(
            "No existe data/processed/all_features.parquet. "
            "Ejecuta primero: poetry run python -m financial_api.data"
        )
    return pd.read_parquet(combined_path)
