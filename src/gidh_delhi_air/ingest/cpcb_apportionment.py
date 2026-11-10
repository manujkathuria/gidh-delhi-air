"""
Ingestion module for CPCB and IIT Kanpur Source Apportionment Benchmarks.
Source: Comprehensive Study on Air Pollution and Green House Gases in Delhi (IIT Kanpur / CPCB / DPCC)
Methodology: Chemical Mass Balance (CMB) receptor modeling with speciated molecular filter tracers.
"""

from pathlib import Path
import pandas as pd

APPORTIONMENT_RECORDS = [
    # Winter Season PM2.5 Shares
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Secondary Inorganic Particles (Sulfates/Nitrates/Ammonium)",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 30.0,
        "primary_chemical_marker": "SO4(2-), NO3(-), NH4(+)",
        "notes": "Gas-to-particle conversion in high humidity and cold stagnation"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Biomass Burning (Crop Residue & Domestic Firewood)",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 26.0,
        "primary_chemical_marker": "Levoglucosan, Potassium (K), Organic Carbon",
        "notes": "Stubble burning inflow + localized space heating"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Vehicles (Internal Combustion Exhaust)",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 25.0,
        "primary_chemical_marker": "Elemental Carbon (Black Carbon), Hopanes, NO2",
        "notes": "Tailpipe emissions trapped by shallow boundary layer"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Municipal Solid Waste (MSW) Burning",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 8.0,
        "primary_chemical_marker": "Antimony (Sb), Chlorine, PAHs",
        "notes": "Open roadside garbage burning"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Coal and Fly Ash",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 4.8,
        "primary_chemical_marker": "Selenium (Se), Arsenic (As), SO2",
        "notes": "Thermal power plants and industrial kilns"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Soil and Road Dust",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 4.3,
        "primary_chemical_marker": "Silicon (Si), Aluminum (Al), Calcium (Ca)",
        "notes": "Low re-suspension due to morning dew and damp ground"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Others (Construction / Diesel Generators)",
        "season": "Winter",
        "pollutant": "PM2.5",
        "share_percentage": 1.9,
        "primary_chemical_marker": "Trace Elements",
        "notes": "Localized sources"
    },

    # Summer Season PM2.5 Shares
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Soil and Road Dust",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 27.1,
        "primary_chemical_marker": "Silicon (Si), Aluminum (Al), Calcium (Ca)",
        "notes": "Dry soil and high convective wind re-suspension"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Coal and Fly Ash",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 26.0,
        "primary_chemical_marker": "Selenium (Se), Fly Ash Cenospheres",
        "notes": "Industrial and brick kiln dispersion"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Secondary Inorganic Particles",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 14.9,
        "primary_chemical_marker": "SO4(2-), NO3(-)",
        "notes": "Photochemical gas-to-particle conversion"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Biomass Burning",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 12.2,
        "primary_chemical_marker": "Levoglucosan, Organic Carbon",
        "notes": "Wheat stubble burning + domestic solid fuel"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Vehicles (Internal Combustion Exhaust)",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 8.5,
        "primary_chemical_marker": "Elemental Carbon, NO2",
        "notes": "Masked by massive influx of crustal dust"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Municipal Solid Waste (MSW) Burning",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 7.2,
        "primary_chemical_marker": "PAHs, Trace Metals",
        "notes": "Open waste burning"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Construction Material",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 3.0,
        "primary_chemical_marker": "Calcium, Silica",
        "notes": "Concrete mixing and structural demolition"
    },
    {
        "study": "IIT_Kanpur_CPCB",
        "source_sector": "Others",
        "season": "Summer",
        "pollutant": "PM2.5",
        "share_percentage": 1.1,
        "primary_chemical_marker": "Trace Elements",
        "notes": "Miscellaneous"
    },
]


def ingest_cpcb_apportionment(output_dir: Path) -> Path:
    """Build and write the CPCB/IIT-K source apportionment benchmark CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "cpcb_iitk_source_apportionment.csv"
    df = pd.DataFrame(APPORTIONMENT_RECORDS)
    df.to_csv(out_path, index=False)
    return out_path

