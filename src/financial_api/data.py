"""Ingesta de datos históricos con yfinance y cache local."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf

from financial_api.features import build_processed_dataset

DEFAULT_SYMBOLS = ["AAPL", "MSFT", "GOOG"]
DEFAULT_PERIOD = "2y"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def download_symbol(symbol: str, period: str = DEFAULT_PERIOD) -> pd.DataFrame:
    """Descarga histórico OHLCV para un símbolo."""
    ticker = yf.Ticker(symbol)
    history = ticker.history(period=period, auto_adjust=True)

    if history.empty:
        raise ValueError(f"yfinance no devolvió datos para el símbolo {symbol}")

    history = history.reset_index()
    if "Datetime" in history.columns:
        history = history.rename(columns={"Datetime": "Date"})

    history["Date"] = pd.to_datetime(history["Date"]).dt.tz_localize(None)
    history["Symbol"] = symbol.upper()
    return history


def download_all(symbols: list[str], period: str = DEFAULT_PERIOD) -> None:
    """Descarga símbolos, guarda datos crudos y construye features procesadas."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_frames: list[pd.DataFrame] = []
    for symbol in symbols:
        print(f"Descargando {symbol}...")
        frame = download_symbol(symbol, period=period)
        raw_path = RAW_DIR / f"{symbol.lower()}.csv"
        frame.to_csv(raw_path, index=False)
        print(f"Guardado: {raw_path}")
        downloaded_frames.append(frame)

    combined_raw = pd.concat(downloaded_frames, ignore_index=True)
    combined_raw.to_csv(RAW_DIR / "all_symbols.csv", index=False)

    combined_processed = build_processed_dataset(symbols, RAW_DIR, PROCESSED_DIR)
    print(f"Dataset procesado: {combined_processed}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Descarga datos históricos con yfinance y genera dataset local."
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=DEFAULT_SYMBOLS,
        help="Lista de tickers a descargar (mínimo 3 recomendado).",
    )
    parser.add_argument(
        "--period",
        default=DEFAULT_PERIOD,
        help="Periodo de descarga aceptado por yfinance, por ejemplo 1y o 2y.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    download_all(args.symbols, period=args.period)


if __name__ == "__main__":
    main()
