"""
Data loader module for Delhi Air Quality monitoring dataset and official Indian sources.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

# Default paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR_CAAQMS = PROJECT_ROOT / "data" / "delhi_air_quality_monitoring_dataset"
DATA_DIR_OFFICIAL = PROJECT_ROOT / "data" / "indian_official_sources"


# --- Tier 1: Local Ground Telemetry (Kaggle / DPCC / CPCB) ---

def load_stations(data_dir: Path = DATA_DIR_CAAQMS) -> pd.DataFrame:
    """Load monitoring stations metadata."""
    path = data_dir / "stations.csv"
    return pd.read_csv(path)


def load_column_metadata(data_dir: Path = DATA_DIR_CAAQMS) -> pd.DataFrame:
    """Load column data dictionary."""
    path = data_dir / "column_metadata.csv"
    return pd.read_csv(path)


def load_source_files(data_dir: Path = DATA_DIR_CAAQMS) -> pd.DataFrame:
    """Load lineage metadata of source files."""
    path = data_dir / "source_files.csv"
    return pd.read_csv(path, parse_dates=["reporting_period_start", "reporting_period_end"])


def load_caaqms_hourly(
    data_dir: Path = DATA_DIR_CAAQMS,
    station_ids: Optional[list[int]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Load hourly CAAQMS telemetry observations.
    Parses timestamp with Asia/Kolkata timezone and sets up appropriate data types.
    """
    path = data_dir / "caaqms_hourly.csv"
    df = pd.read_csv(path, parse_dates=["timestamp"], low_memory=False)

    if station_ids:
        df = df[df["station_id"].isin(station_ids)]
    if start_date:
        df = df[df["timestamp"] >= pd.to_datetime(start_date).tz_localize("Asia/Kolkata")]
    if end_date:
        df = df[df["timestamp"] <= pd.to_datetime(end_date).tz_localize("Asia/Kolkata")]

    return df


def load_aqi_hourly(
    data_dir: Path = DATA_DIR_CAAQMS,
    station_ids: Optional[list[int]] = None,
) -> pd.DataFrame:
    """Load official CPCB calculated hourly AQI records."""
    path = data_dir / "aqi_hourly.csv"
    df = pd.read_csv(path, parse_dates=["timestamp"], low_memory=False)

    if station_ids:
        df = df[df["station_id"].isin(station_ids)]

    return df


# --- Tier 2: Official Indian External Government Datasets ---

def load_caqm_annual_totals(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Load CAQM multi-year seasonal stubble burning totals (2020-2025)."""
    path = data_dir / "caqm_stubble_burning_annual_totals.csv"
    return pd.read_csv(path)


def load_cpcb_apportionment(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Load CPCB / IIT Kanpur seasonal source apportionment benchmarks."""
    path = data_dir / "cpcb_iitk_source_apportionment.csv"
    return pd.read_csv(path)


def load_iari_district_fires(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Load ICAR-IARI district-daily stubble burning records (65 districts, 2023-2025)."""
    path = data_dir / "iari_district_daily_stubble_fires.csv"
    return pd.read_csv(path, parse_dates=["date"])
