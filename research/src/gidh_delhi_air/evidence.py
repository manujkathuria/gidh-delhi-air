"""Pinned evidence, separate from scientific or milestone acceptance."""
import hashlib
import json
from pathlib import Path
from gidh_delhi_air.paths import PROJECT_ROOT, ProjectPaths



class EvidenceError(ValueError):
    """Evidence is missing, changed, or does not support the requested data."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_manifest(root: Path = PROJECT_ROOT) -> dict:
    manifest = json.loads(ProjectPaths(root).source_manifest.read_text())
    if manifest.get('schema_version') != 1:
        raise EvidenceError('Unsupported source manifest schema')
    return manifest


def source_path(source_id: str, root: Path = PROJECT_ROOT) -> Path:
    matches = [s for s in read_manifest(root)['sources'] if s['source_id'] == source_id]
    if len(matches) != 1:
        raise EvidenceError(f'Expected exactly one manifest entry for {source_id}')
    source = matches[0]
    path = (root / source['local_path']).resolve()
    if root.resolve() not in path.parents:
        raise EvidenceError('Source path escapes project root')
    if not path.is_file():
        raise EvidenceError(f"Missing evidence: {source['local_path']}")
    if sha256(path) != source['sha256']:
        raise EvidenceError(f"Evidence checksum mismatch: {source['local_path']}")
    return path
