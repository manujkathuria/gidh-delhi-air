# Official Data Provenance & Primary Source Registry

**Project:** GIDH Delhi Air Quality & Pollution Source Attribution  
**Corporate Standards:** ISO 8000 / DAMA-DMBOK Data Provenance Framework  
**Document Purpose:** Define the primary issuing authorities, exact permanent URLs, document identifiers, physical collection methodologies, and known limitations for every dataset used in this project.

---

## 1. Primary Source 1: Local Ground Telemetry (Inside Delhi)

### Metadata & Issuing Authority
* **Primary Authority:** Delhi Pollution Control Committee (DPCC) & Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change (MoEFCC), Government of India.
* **Official Portals:** 
  * CPCB Official Portal: [https://cpcb.nic.in](https://cpcb.nic.in)
  * CPCB Central CAAQMS Dashboard: [https://app.cpcbccr.com/ccr/#/caaqms-dashboard-all](https://app.cpcbccr.com/ccr/#/caaqms-dashboard-all)
  * DPCC Real-Time Air Quality: [https://www.dpcc.delhigovt.nic.in](https://www.dpcc.delhigovt.nic.in)
* **Ingestion Archive:** [Kaggle Delhi Air Quality Monitoring Dataset 2023–2026](https://www.kaggle.com/datasets/siddharthdongardive/delhi-air-quality-monitoring-dataset-2023-2026)
* **Local Project Location:** `data/delhi_air_quality_monitoring_dataset/`

### Telemetry Details
* **Volume:** 162,096 hourly CAAQMS multi-pollutant observations + 57,946 official AQI hourly records.
* **Stations (7 Active Monitors):**
  1. **Anand Vihar (DPCC):** Major transit hub (ISBT, UP border, railway).
  2. **Bawana (DPCC):** Northwest industrial manufacturing cluster.
  3. **Dwarka Sector-8 (DPCC):** Southwest residential / airport boundary.
  4. **ITO (CPCB):** Central Delhi arterial vehicular junction.
  5. **Jahangirpuri (DPCC):** North Delhi GT Karnal road / landfill corridor.
  6. **Punjabi Bagh (DPCC):** West Delhi dense urban arterial junction.
  7. **R K Puram (DPCC):** South Delhi mixed residential / commercial sector.

### Collection Methodology & Instruments
* **Particulate Matter ($PM_{2.5}, PM_{10}$):** Beta Attenuation Monitors (BAM) / Optical Particle Counters using 1-hour automated sampling.
* **Gaseous Pollutants ($NO_2, SO_2, CO, O_3$):** 
  * $NO_x$: Chemiluminescence analyzers.
  * $SO_2$: Ultraviolet (UV) fluorescence analyzers.
  * $CO$: Non-Dispersive Infrared (NDIR) spectroscopy.
  * $O_3$: UV photometric analyzers.
* **Meteorology:** Co-located automatic weather stations (ultrasonic anemometers for wind speed/direction, RTDs for ambient temperature, capacitive hygrometers for relative humidity).

### Known Physical & Sensor Limitations
1. **Sensor Saturation:** Optical counters experience hardware capping around $\sim 998\text{--}1000\ \mu\text{g/m}^3$ during extreme smog events.
2. **Missing July 2026 Telemetry:** A 744-hour telemetry outage occurred across 6 stations during July 2026. Station 5 (Dwarka) provides an unbroken timeline from 2023 to 2025.

---

## 2. Primary Source 2: Agricultural Crop Residue Burning (Upwind Regional Plains)

### Metadata & Issuing Authority
* **Primary Authority:** Consortium for Research on Agroecosystem Monitoring and Modeling from Space (CREAMS Laboratory), Division of Agricultural Physics, ICAR - Indian Agricultural Research Institute (IARI), Pusa, New Delhi.
* **Statutory Body:** Commission for Air Quality Management in NCR & Adjoining Areas (CAQM), Ministry of Environment, Forest & Climate Change (MoEFCC).
* **Official Portals:**
  * ICAR-IARI CREAMS Crop Residue Portal: [https://creams.iari.res.in](https://creams.iari.res.in)
  * CAQM Portal: [https://caqm.nic.in](https://caqm.nic.in)
  * Press Information Bureau (PIB) MoEFCC Archive: [https://pib.gov.in](https://pib.gov.in)
* **Local Project Location:** `data/indian_official_sources/`
* **Raw Archival Location:** `data/raw_bulletins/` (contains exact downloaded PIB official audit releases).

### Source Documents & Report Identifiers
1. **Standard Operational Protocol:** *Standard Protocol for Estimation of Crop Residue Burning Fire Events using Satellite Data*, established in consultation with ISRO (NRSC/SAC).
2. **Daily Bulletins:** Numbered daily bulletins published from September 15 to November 30 annually:
   * Title: *"Monitoring Paddy Residue Burning in India Using Satellite Remote Sensing"*.
   * Examples: Bulletin No. 14 (28-Sep-2023), Bulletin No. 34 (18-Oct-2023), Bulletin No. 76 (29-Nov-2024).
3. **Official Annual Audit Gazette Releases (PIB MoEFCC):**
   * **2023 Harvest Audit:** [PIB Press Release PRID: 1981276](https://pib.gov.in/PressReleasePage.aspx?PRID=1981276) (01-DEC-2023).  
     *Audited totals: Punjab = 36,663; Haryana = 2,303; UP = 5,143.*
   * **2024 Harvest Audit:** [PIB Press Release PRID: 2078652](https://pib.gov.in/PressReleasePage.aspx?PRID=2078652) (01-DEC-2024).  
     *Audited totals: Punjab = 10,885; Haryana = 1,406; UP = 5,769.*
   * **2025 Harvest Audit:** [PIB Press Release PRID: 2196420](https://pib.gov.in/PressReleasePage.aspx?PRID=2196420) (01-DEC-2025).  
     *Audited totals: Punjab = 5,114; Haryana = 662; UP = 3,215.*

### Collection Methodology & Instruments
* **Satellites / Sensors:**
  * **S-NPP (Suomi National Polar-orbiting Partnership):** VIIRS (Visible Infrared Imaging Radiometer Suite) 375-meter resolution.
  * **Aqua & Terra:** MODIS (Moderate Resolution Imaging Spectroradiometer) 1-kilometer resolution.
* **Detection Principle:** Thermal anomalies are detected using Mid-Infrared (MIR at $3.9\ \mu\text{m}$) and Thermal Infrared (TIR at $10.8\ \mu\text{m}$) brightness temperature differences.

### Known Limitations
1. **Cloud & Smog Obscuration:** Optical and thermal satellite sensors cannot penetrate dense cloud cover or thick stratiform fog.
2. **Overpass Timing Window:** Polar-orbiting satellites capture data during specific overpasses (typically around 10:30 AM and 1:30 PM local time); fires lit late in the evening may not be captured by day passes.

---

## 3. Primary Source 3: Chemical Source Apportionment Study (Delhi Chemical Fingerprint)

### Metadata & Issuing Authority
* **Primary Authority:** Indian Institute of Technology (IIT) Kanpur, Department of Civil Engineering.
* **Commissioning Authority:** Delhi Pollution Control Committee (DPCC) & Department of Environment, Government of NCT of Delhi.
* **Principal Investigators:** Prof. Mukesh Sharma & Prof. Onkar Dikshit (IIT Kanpur).
* **Official Report Title:** *Comprehensive Study on Air Pollution and Green House Gases in Delhi (Final Report)*.
* **Academic & Government Repository:** [CERCA IIT Delhi Portal](https://cerca.iitd.ac.in) / [Delhi Govt Environment Department](https://delhi.gov.in).
* **Local Project Location:** `data/indian_official_sources/cpcb_iitk_source_apportionment.csv`

### Methodology: Chemical Mass Balance (CMB) Receptor Modeling
Unlike particle counters that only measure physical size, this landmark study collected particulate mass on Teflon and quartz fiber filters across multiple sites in Delhi across Winter and Summer seasons, followed by chemical speciation analysis:

| Source Category | Specific Chemical Marker (Fingerprint) | Detection Laboratory Technique |
| :--- | :--- | :--- |
| **Biomass Burning** | **Levoglucosan**, Water-Soluble Potassium ($K^+$) | High-Performance Anion-Exchange Chromatography |
| **Vehicles (Internal Combustion)** | **Elemental Carbon (Black Carbon)**, Hopanes, Steranes | Thermal-Optical Transmittance (TOT) / GC-MS |
| **Soil & Road Dust** | **Silica ($Si$), Aluminum ($Al$), Calcium ($Ca$)** | Energy Dispersive X-ray Fluorescence (ED-XRF) |
| **Secondary Sulfates / Nitrates** | **Sulfate ($\text{SO}_4^{2-}$), Nitrate ($\text{NO}_3^-$), Ammonium ($\text{NH}_4^+$)** | Ion Chromatography (IC) |
| **Municipal Waste Burning** | **Antimony ($Sb$), Chlorine, Toxic PAHs** | Inductively Coupled Plasma Mass Spectrometry (ICP-MS) |
| **Coal & Fly Ash** | **Selenium ($Se$), Arsenic ($As$), Cenospheres** | ED-XRF and Scanning Electron Microscopy |

### Benchmarked Percentage Shares ($PM_{2.5}$):
* **Winter Season:** Secondary Inorganic Aerosols ($30.0\%$), Biomass Burning ($26.0\%$), Vehicles ($25.0\%$), Municipal Waste Burning ($8.0\%$), Coal & Fly Ash ($4.8\%$), Soil & Road Dust ($4.3\%$), Others ($1.9\%$).
* **Summer Season:** Soil & Road Dust ($27.1\%$), Coal & Fly Ash ($26.0\%$), Secondary Aerosols ($14.9\%$), Biomass Burning ($12.2\%$), Vehicles ($8.5\%$), Municipal Waste Burning ($7.2\%$), Construction Material ($3.0\%$), Others ($1.1\%$).

---

## 4. Primary Source Summary & Lineage Matrix

| Project File | Issuing Agency | Primary Document Title | Collection Mode |
| :--- | :--- | :--- | :--- |
| `caaqms_hourly.csv` | DPCC / CPCB | CAAQMS Automated Telemetry Database | Continuous Optical/Chemical Intake |
| `aqi_hourly.csv` | CPCB | National Air Quality Index (NAQI) Reporting Portal | CPCB Sub-Index Algorithm |
| `pib_release_*.html` | MoEFCC / CAQM | PIB Official Harvest Review Press Releases | Multi-Agency Audit Verification |
| `iari_district_daily_stubble_fires.csv` | ICAR-IARI | Paddy Residue Burning Monitoring Bulletins | ISRO Satellite Protocol (VIIRS/MODIS) |
| `cpcb_iitk_source_apportionment.csv` | IIT Kanpur / DPCC | Comprehensive Study on Air Pollution in Delhi | Filter Chemical Speciation (CMB) |

