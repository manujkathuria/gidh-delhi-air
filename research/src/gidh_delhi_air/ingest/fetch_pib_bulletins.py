"""Retired: the former implementation emitted constants rather than parsed PIB data."""
from pathlib import Path
from gidh_delhi_air.evidence import EvidenceError


def parse_pib_bulletin(year: int, file_path: Path) -> list[dict]:
    raise EvidenceError('PIB ingestion retired: invalid release references and hard-coded outputs. '
                        'Use the pinned IARI bulletin via python -m gidh_delhi_air.ingest.')


def run_pib_fetcher() -> Path:
    raise EvidenceError('PIB ingestion retired; use the source-backed IARI ingestion pipeline.')


if __name__ == '__main__':
    run_pib_fetcher()
