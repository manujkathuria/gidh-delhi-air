"""
Data loader module for Delhi Air Quality monitoring dataset and official Indian sources.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
from pandas.testing import assert_frame_equal
from gidh_delhi_air.evidence import EvidenceError, PROJECT_ROOT
from gidh_delhi_air.paths import PATHS

# Default paths relative to project root
DATA_DIR_CAAQMS = PATHS.telemetry
DATA_DIR_OFFICIAL = PATHS.reference


# --- Third-party telemetry redistribution (Kaggle); upstream exports not verified ---

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
    """Load redistributed AQI; publisher attributes its upstream source to CPCB."""
    path = data_dir / "aqi_hourly.csv"
    df = pd.read_csv(path, parse_dates=["timestamp"], low_memory=False)

    if station_ids:
        df = df[df["station_id"].isin(station_ids)]

    return df


# --- Tier 2: Official Indian External Government Datasets ---

def load_caqm_annual_totals(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Load IARI seasonal totals; historical filename retained for compatibility."""
    from gidh_delhi_air.ingest.iari_fires import extract_iari
    path = data_dir / "caqm_stubble_burning_annual_totals.csv"
    return _verified_table(path, extract_iari()[1])


def load_cpcb_apportionment(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Compatibility alias for historical IITK/DPCC benchmarks, not current attribution."""
    return load_iitk_apportionment(data_dir)


def load_iitk_apportionment(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    from gidh_delhi_air.ingest.cpcb_apportionment import extract_apportionment, OUTPUT_FILE
    return _verified_table(data_dir / OUTPUT_FILE, extract_apportionment())


def load_iari_state_fires(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Source-backed state daily observations (2020-2025, Sep 15-Nov 30)."""
    from gidh_delhi_air.ingest.iari_fires import extract_iari, DAILY_FILE
    df = _verified_table(data_dir / DAILY_FILE, extract_iari()[0])
    df['date'] = pd.to_datetime(df['date'])
    return df


def _verified_table(path: Path, expected: pd.DataFrame) -> pd.DataFrame:
    frame = pd.read_csv(path)
    try:
        assert_frame_equal(frame, expected, check_dtype=False, check_exact=True)
    except AssertionError as exc:
        raise EvidenceError(f'{path.name} does not match its primary evidence') from exc
    return frame


def load_iari_district_fires(data_dir: Path = DATA_DIR_OFFICIAL) -> pd.DataFrame:
    """Reject the former synthetic dataset, including copies at alternate paths."""
    raise EvidenceError('District daily observations are not verified. The former dataset was '
                        'synthetic and is quarantined. Use load_iari_state_fires for real state data.')
