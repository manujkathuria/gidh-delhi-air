"""Describe the first investigation's reproducible execution plan.

This module does not yet calculate daily means, benchmark counts or streaks.
"""
from dataclasses import asdict, replace
from gidh_delhi_air.evidence import read_manifest
from gidh_delhi_air.paths import PATHS, ProjectPaths
from gidh_delhi_air.investigations.models import AnalysisPlan
from gidh_delhi_air.investigations.clean_days import DEFINITION
from gidh_delhi_air.investigations.clean_days.config import CleanDaysConfig


def build_plan(config: CleanDaysConfig, paths: ProjectPaths = PATHS) -> AnalysisPlan:
    manifest = read_manifest(paths.root)
    telemetry = manifest['telemetry']
    source = next(s for s in manifest['sources'] if s['source_id'] == telemetry['source_id'])
    needed = {'caaqms_hourly.csv', 'stations.csv'}
    selected = [entry for entry in telemetry['files'] if entry['archive_member'] in needed]
    if {entry['archive_member'] for entry in selected} != needed or len(selected) != len(needed):
        raise ValueError('The investigation requires exactly one telemetry and station-table manifest entry')
    # Inspection is read-only; plans neither create directories nor publish placeholder results.
    inputs = tuple({
        'path': entry['path'], 'sha256': entry['sha256'], 'source_id': source['source_id'],
        'source_url': source['url'], 'source_status': source['status'],
        'use': 'Accepted project telemetry; original government export chain remains unaudited',
    } for entry in selected)
    relative = lambda path: path.relative_to(paths.root).as_posix()
    return AnalysisPlan(
        investigation=replace(DEFINITION,
            title=f'Can You Find {config.target_days} Clean Days in Delhi?',
            question=f'Can we find {config.target_days} qualifying days and a continuous stretch in {config.year}?'),
        parameters={**asdict(config), 'timezone': 'Asia/Kolkata', 'pollutant': 'pm25', 'unit': 'µg/m³',
                    'benchmarks': ['Indian NAAQS', 'WHO AQG'], 'min_valid_hours_per_day': None,
                    'multi_station_rule': None},
        inputs=inputs,
        outputs={
            'shared_preprocessing_directory': relative(paths.shared_processed),
            'working_directory': relative(paths.investigation_processed(DEFINITION.id)),
            'public_export_directory': relative(paths.investigation_published(DEFINITION.id)),
            'planned_artifacts': ['daily-calendar.csv', 'station-summary.csv', 'findings.json', 'figures/'],
            'publication_status': 'not_generated',
        },
        steps=(
            'Inspect source integrity and the selected year/station coverage.',
            'Prepare station/day PM2.5 observations through the shared preprocessing package.',
            'Apply documented completeness and benchmark rules; retain unknown days.',
            'Count qualifying days and consecutive stretches by station and under the chosen station-combination rule.',
            'Render charts and export reviewed results for both the website and video.',
        ),
        pending_decisions=(
            'Choose and document the minimum valid hours required for a daily value.',
            'Register the exact benchmark levels, averaging periods and source versions before comparing values.',
            'Define the multi-station qualification rule and how missing stations affect a day.',
            'Decide how PM10 is used as an additional check on the PM2.5-focused challenge.',
        ),
    )


def plan_from_parameters(parameters: dict, paths: ProjectPaths = PATHS) -> AnalysisPlan:
    try:
        config = CleanDaysConfig(**parameters)
    except TypeError as exc:
        raise ValueError(f'Invalid clean-days configuration: {exc}') from exc
    return build_plan(config, paths)
