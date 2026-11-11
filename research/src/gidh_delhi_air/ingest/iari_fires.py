"""Extract observations; never allocate seasonal counts into invented daily records."""
from datetime import datetime, timedelta
from pathlib import Path
import re
import pandas as pd
from pypdf import PdfReader
from gidh_delhi_air.evidence import EvidenceError, PROJECT_ROOT, source_path

SOURCE_ID = 'iari_paddy_2025_77'
STATES = ('Punjab', 'Haryana', 'Uttar Pradesh')
YEARS = tuple(range(2020, 2026))
DAILY_FILE = 'iari_state_daily_fires.csv'
ANNUAL_FILE = 'caqm_stubble_burning_annual_totals.csv'


def parse_daily_pages(pages: list[tuple[int, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Bulletin 77, one-based PDF pages 25-27: three states x six years.

    The final page starts another table; stop at the first Total row.
    """
    rows, totals, seen_dates, total_page = [], None, set(), None
    for page, text in pages:
        for line in text.splitlines():
            if re.match(r'^\s*Total\b', line):
                cells = line.split()[1:]
                if len(cells) != 18 or not all(c.isdigit() for c in cells):
                    raise EvidenceError('Malformed IARI total row')
                totals, total_page = [int(c) for c in cells], page
                break
            if not re.match(r'^\s*\d{2}-(Sep|Oct|Nov)\s', line):
                continue
            cells = line.split()
            if len(cells) != 19 or not all(c.isdigit() for c in cells[1:]):
                raise EvidenceError(f'Malformed IARI daily row on PDF page {page}')
            if cells[0] in seen_dates:
                raise EvidenceError(f'Duplicate IARI date: {cells[0]}')
            seen_dates.add(cells[0])
            for si, state in enumerate(STATES):
                for yi, year in enumerate(YEARS):
                    day = datetime.strptime(f'{cells[0]}-{year}', '%d-%b-%Y').date()
                    rows.append({
                        'date': day.isoformat(), 'year': year, 'state': state,
                        'geographic_scope': 'whole_state',
                        'daily_fire_count': int(cells[1 + si * 6 + yi]),
                        'reporting_agency': 'ICAR-IARI (CREAMS)',
                        'source_id': SOURCE_ID, 'source_pdf_page': page, 'source_row': cells[0],
                    })
        if totals is not None:
            break
    expected = {(datetime(2025, 9, 15) + timedelta(days=i)).strftime('%d-%b') for i in range(77)}
    if seen_dates != expected or totals is None:
        raise EvidenceError('IARI table must contain all 77 dates and a published total row')
    daily = pd.DataFrame(rows).sort_values(['year', 'state', 'date']).reset_index(drop=True)
    annual_rows = []
    for si, state in enumerate(STATES):
        for yi, year in enumerate(YEARS):
            published = totals[si * 6 + yi]
            actual = daily.loc[(daily.state == state) & (daily.year == year), 'daily_fire_count'].sum()
            if actual != published:
                raise EvidenceError(f'IARI daily/seasonal mismatch: {state} {year}: {actual} != {published}')
            annual_rows.append({
                'year': year, 'monitoring_window': '15 Sep - 30 Nov', 'state': state,
                'geographic_scope': 'whole_state', 'total_fire_incidents': published,
                'reporting_agency': 'ICAR-IARI (CREAMS)', 'source_id': SOURCE_ID,
                'source_pdf_page': total_page, 'source_row': 'Total',
            })
    annual = pd.DataFrame(annual_rows).sort_values(['year', 'state']).reset_index(drop=True)
    return daily, annual


def extract_iari(root: Path = PROJECT_ROOT) -> tuple[pd.DataFrame, pd.DataFrame]:
    reader = PdfReader(source_path(SOURCE_ID, root))
    cover = reader.pages[0].extract_text()
    if '2025' not in cover or '77' not in cover or '30-Nov' not in cover:
        raise EvidenceError('Wrong IARI bulletin identity')
    return parse_daily_pages([(p, reader.pages[p - 1].extract_text(extraction_mode='layout'))
                              for p in (25, 26, 27)])


def ingest_iari_state_fires(output_dir: Path, root: Path = PROJECT_ROOT) -> dict[str, Path]:
    daily, annual = extract_iari(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {'state_daily': output_dir / DAILY_FILE, 'annual_totals': output_dir / ANNUAL_FILE}
    daily.to_csv(paths['state_daily'], index=False)
    annual.to_csv(paths['annual_totals'], index=False)
    return paths


def ingest_iari_district_fires(output_dir: Path) -> Path:
    raise EvidenceError('District daily observations are unavailable. The former CSV was synthetic; '
                        'use ingest_iari_state_fires for source-backed state observations.')
