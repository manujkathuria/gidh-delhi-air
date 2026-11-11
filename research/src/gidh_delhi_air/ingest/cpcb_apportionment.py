"""Historical IIT Kanpur / DPCC CMB benchmarks, extracted from exact report tables."""
from pathlib import Path
import re
import pandas as pd
from pypdf import PdfReader
from gidh_delhi_air.evidence import EvidenceError, PROJECT_ROOT, source_path

SOURCE_ID = 'iitk_dpcc_2016'
OUTPUT_FILE = 'iitk_dpcc_pm25_apportionment.csv'
# Report column order; no invented chemical marker or causal interpretation fields.
SECTORS = ('Secondary particles', 'Biomass burning', 'Industrial', 'Coal and fly ash',
           'Construction material', 'Soil and road dust', 'Boiler', 'Solid waste burning', 'Vehicles')
TABLES = (('Winter', 293, '248', '4.20(b)'), ('Summer', 295, '250', '4.24(b)'))


def parse_apportionment_page(text: str, season: str, page: int,
                             printed_page: str, table: str) -> list[dict]:
    marker = f'Table {table}:'
    if marker not in text:
        raise EvidenceError(f'Missing IITK table {table}')
    section = text.split(marker, 1)[1]
    if 'PM2.5' not in re.sub(r'\s+', '', section[:250]):
        raise EvidenceError(f'Wrong pollutant in IITK table {table}')
    matches = re.findall(r'^\s*Overall\s+(.+)$', section, re.MULTILINE)
    if len(matches) != 1:
        raise EvidenceError(f'Expected one Overall row in IITK table {table}')
    values = matches[0].split()
    if len(values) != 10:
        raise EvidenceError(f'Expected measured mass and nine shares in IITK table {table}')
    try:
        shares = [float(v) for v in values[1:]]
    except ValueError as exc:
        raise EvidenceError(f'Non-numeric IITK share in table {table}') from exc
    if any(not 0 <= v <= 100 for v in shares) or abs(sum(shares) - 100) > 0.1:
        raise EvidenceError(f'Invalid IITK shares in table {table}')
    return [{
        'study': 'IIT Kanpur / DPCC Delhi final report (2016)',
        'season': season, 'pollutant': 'PM2.5', 'source_sector': sector,
        'share_percentage': value, 'statistic': 'Overall row, six study sites',
        'sampling_period': '2013-2014' if season == 'Winter' else '2014',
        'method': 'Chemical Mass Balance receptor modelling',
        'source_id': SOURCE_ID, 'source_pdf_page': page,
        'source_printed_page': int(printed_page), 'source_table': table, 'source_row': 'Overall',
    } for sector, value in zip(SECTORS, shares)]


def extract_apportionment(root: Path = PROJECT_ROOT) -> pd.DataFrame:
    reader = PdfReader(source_path(SOURCE_ID, root))
    cover = reader.pages[0].extract_text()
    if 'Comprehensive Study' not in cover or 'Delhi' not in cover:
        raise EvidenceError('Wrong IITK report identity')
    rows = []
    for season, page, printed, table in TABLES:
        rows.extend(parse_apportionment_page(
            reader.pages[page - 1].extract_text(extraction_mode='layout'), season, page, printed, table))
    return pd.DataFrame(rows)


def ingest_cpcb_apportionment(output_dir: Path, root: Path = PROJECT_ROOT) -> Path:
    """Compatibility name: issuer is IITK/DPCC, not a new CPCB observation series."""
    frame = extract_apportionment(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / OUTPUT_FILE
    frame.to_csv(path, index=False)
    return path
