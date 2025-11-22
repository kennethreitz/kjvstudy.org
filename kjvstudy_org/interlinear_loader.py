"""
Lazy loader for compressed interlinear Bible data.
Decompresses and loads the data on first access.
Optimized for fly.io production deployment.
"""

import gzip
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

_interlinear_data = None
_load_failed = False


def _load_interlinear_data():
    """Load and decompress interlinear data from gzipped file"""
    global _interlinear_data, _load_failed

    if _interlinear_data is not None:
        return _interlinear_data

    # If loading previously failed, return empty dict to avoid repeated errors
    if _load_failed:
        logger.warning("Interlinear data loading previously failed, returning empty data")
        return {}

    data_file = Path(__file__).parent / "interlinear_data.py.gz"

    try:
        logger.info(f"Loading interlinear data from {data_file}...")

        if not data_file.exists():
            raise FileNotFoundError(f"Interlinear data file not found: {data_file}")

        with gzip.open(data_file, 'rt', encoding='utf-8') as f:
            # Read the file and extract the JSON data
            content = f.read()

            # Find the INTERLINEAR_DATA = {...} section
            start = content.find('INTERLINEAR_DATA = ')
            if start == -1:
                raise ValueError("Could not find INTERLINEAR_DATA in compressed file")

            # Extract just the JSON part
            json_start = content.find('{', start)

            # Find the matching closing brace (simple approach - assumes well-formed JSON)
            brace_count = 0
            json_end = json_start
            for i, char in enumerate(content[json_start:], start=json_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break

            json_str = content[json_start:json_end]
            _interlinear_data = json.loads(json_str)

        logger.info(f"Successfully loaded {len(_interlinear_data)} verses")
        return _interlinear_data

    except Exception as e:
        _load_failed = True
        logger.error(f"Failed to load interlinear data: {e}", exc_info=True)
        _interlinear_data = {}
        return _interlinear_data


def get_interlinear_data(book: str, chapter: int, verse: int) -> Optional[List[Dict]]:
    """Get interlinear data for a specific verse"""
    data = _load_interlinear_data()
    key = f"{book}:{chapter}:{verse}"
    return data.get(key)


def has_interlinear_data(book: str, chapter: int, verse: int) -> bool:
    """Check if interlinear data exists for a verse"""
    data = _load_interlinear_data()
    key = f"{book}:{chapter}:{verse}"
    return key in data


def get_all_interlinear_verses() -> List[Dict]:
    """Get list of all verses with interlinear data"""
    data = _load_interlinear_data()
    verses = []
    for key in sorted(data.keys()):
        book, chapter, verse = key.split(":")
        verses.append({
            "book": book,
            "chapter": int(chapter),
            "verse": int(verse),
            "ref": f"{book} {chapter}:{verse}"
        })
    return verses
