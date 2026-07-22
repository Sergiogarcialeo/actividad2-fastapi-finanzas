"""Pruebas de la ingesta y del dataset procesado."""

from pathlib import Path

import pandas as pd

from financial_api.features import FEATURE_COLUMNS, load_processed_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def test_raw_files_exist_for_three_symbols() -> None:
    for symbol in ("aapl", "msft", "goog"):
        assert (RAW_DIR / f"{symbol}.csv").exists()


def test_processed_dataset_exists() -> None:
    assert (PROCESSED_DIR / "all_features.parquet").exists()
    assert (PROCESSED_DIR / "all_features.csv").exists()


def test_processed_dataset_has_three_symbols() -> None:
    dataset = load_processed_dataset(PROCESSED_DIR)
    assert dataset["Symbol"].nunique() == 3
    assert set(dataset["Symbol"].unique()) == {"AAPL", "MSFT", "GOOG"}


def test_processed_dataset_has_expected_columns() -> None:
    dataset = load_processed_dataset(PROCESSED_DIR)
    for column in FEATURE_COLUMNS:
        assert column in dataset.columns


def test_processed_dataset_has_rows_after_feature_window() -> None:
    dataset = load_processed_dataset(PROCESSED_DIR)
    assert len(dataset) > 100
    assert dataset["return_1d"].notna().sum() > 0
