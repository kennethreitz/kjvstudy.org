"""Shared helpers for loading JSON data files."""
import json
from pathlib import Path


def load_merged_json_dir(directory: Path, legacy_path: Path) -> dict:
    """Merge every per-item JSON object in `directory` into a single dict.

    Files are read in sorted order and later keys win. Each file must contain a
    JSON object (non-object files are skipped). If `directory` does not exist,
    falls back to reading the single `legacy_path` file.
    """
    aggregated: dict = {}
    if directory.exists():
        for path in sorted(directory.glob("*.json")):
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
            if isinstance(content, dict):
                aggregated.update(content)
    elif legacy_path.exists():
        with open(legacy_path, "r", encoding="utf-8") as f:
            aggregated = json.load(f)
    return aggregated
