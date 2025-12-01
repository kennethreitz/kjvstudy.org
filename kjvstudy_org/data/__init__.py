"""Biblical resource data - maps, angels, prophets, names of God, etc."""

import json
import re
from pathlib import Path


def _load_resources() -> dict:
    """Load resources from per-category JSON files, fallback to legacy single file."""
    base_dir = Path(__file__).parent
    resources_dir = base_dir / "resources"
    legacy_path = base_dir / "resources.json"

    aggregated = {}

    if resources_dir.exists():
        for path in sorted(resources_dir.glob("*.json")):
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict):
                    aggregated.update(content)

    elif legacy_path.exists():
        with open(legacy_path, "r", encoding="utf-8") as f:
            aggregated = json.load(f)

    return aggregated


_data = _load_resources()
if not _data:
    raise FileNotFoundError("Resource data not found. Ensure data/resources/*.json exists.")


def _create_slug(text: str) -> str:
    """Convert text to URL-friendly slug."""
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


# Build slug index for O(1) lookups
_RESOURCE_SLUG_INDEX = {}


def _build_slug_index(data: dict):
    """Build a slug index for fast resource lookups."""
    index = {}
    for category_name, category in data.items():
        if isinstance(category, dict):
            for item_name, item_data in category.items():
                slug = _create_slug(item_name)
                # Store with data dict key for quick lookup
                index[slug] = (item_data, item_name, category_name, data)
    return index

BIBLICAL_LOCATIONS = _data["biblical_locations"]
ANGELS_DATA = _data["angels"]
PROPHETS_DATA = _data["prophets"]
NAMES_DATA = _data["names"]
PARABLES_DATA = _data["parables"]
COVENANTS_DATA = _data["covenants"]
APOSTLES_DATA = _data["apostles"]
WOMEN_DATA = _data["women"]
FESTIVALS_DATA = _data["festivals"]
FRUITS_DATA = _data["fruits"]
MIRACLES_DATA = _data["miracles"]
PRAYERS_DATA = _data["prayers"]
BEATITUDES_DATA = _data["beatitudes"]
TEN_COMMANDMENTS_DATA = _data["ten_commandments"]
ARMOR_OF_GOD_DATA = _data["armor_of_god"]
I_AM_STATEMENTS_DATA = _data["i_am_statements"]

# Theological Resources
TRINITY_DATA = _data["trinity"]
CHRISTOLOGY_DATA = _data["christology"]
SOTERIOLOGY_DATA = _data["soteriology"]
PNEUMATOLOGY_DATA = _data["pneumatology"]
ESCHATOLOGY_DATA = _data["eschatology"]
ECCLESIOLOGY_DATA = _data["ecclesiology"]
TYPES_AND_SHADOWS_DATA = _data["types_and_shadows"]
MESSIANIC_PROPHECIES_DATA = _data["messianic_prophecies"]
BLOOD_IN_SCRIPTURE_DATA = _data["blood_in_scripture"]
KINGDOM_OF_GOD_DATA = _data["kingdom_of_god"]
NAMES_OF_CHRIST_DATA = _data["names_of_christ"]
SPIRITS_AND_DEMONS_DATA = _data["spirits_and_demons"]
PERSONIFICATIONS_DATA = _data["personifications"]

# Additional Systematic Theology Resources
BIBLIOLOGY_DATA = _data["bibliology"]
THEOLOGY_PROPER_DATA = _data["theology_proper"]
ANTHROPOLOGY_DATA = _data["anthropology"]
HAMARTIOLOGY_DATA = _data["hamartiology"]
PROVIDENCE_DATA = _data["providence"]
GRACE_DATA = _data["grace"]
JUSTIFICATION_DATA = _data["justification"]
SANCTIFICATION_DATA = _data["sanctification"]
LAW_AND_GOSPEL_DATA = _data["law_and_gospel"]
WORSHIP_DATA = _data["worship"]

# Build slug indexes for all resource dictionaries
_SLUG_INDEXES = {
    'angels': _build_slug_index(ANGELS_DATA),
    'prophets': _build_slug_index(PROPHETS_DATA),
    'names': _build_slug_index(NAMES_DATA),
    'parables': _build_slug_index(PARABLES_DATA),
    'covenants': _build_slug_index(COVENANTS_DATA),
    'apostles': _build_slug_index(APOSTLES_DATA),
    'women': _build_slug_index(WOMEN_DATA),
    'festivals': _build_slug_index(FESTIVALS_DATA),
    'fruits': _build_slug_index(FRUITS_DATA),
    'miracles': _build_slug_index(MIRACLES_DATA),
    'prayers': _build_slug_index(PRAYERS_DATA),
    'beatitudes': _build_slug_index(BEATITUDES_DATA),
    'ten_commandments': _build_slug_index(TEN_COMMANDMENTS_DATA),
    'armor_of_god': _build_slug_index(ARMOR_OF_GOD_DATA),
    'i_am_statements': _build_slug_index(I_AM_STATEMENTS_DATA),
    'trinity': _build_slug_index(TRINITY_DATA),
    'christology': _build_slug_index(CHRISTOLOGY_DATA),
    'soteriology': _build_slug_index(SOTERIOLOGY_DATA),
    'pneumatology': _build_slug_index(PNEUMATOLOGY_DATA),
    'eschatology': _build_slug_index(ESCHATOLOGY_DATA),
    'ecclesiology': _build_slug_index(ECCLESIOLOGY_DATA),
    'types_and_shadows': _build_slug_index(TYPES_AND_SHADOWS_DATA),
    'messianic_prophecies': _build_slug_index(MESSIANIC_PROPHECIES_DATA),
    'blood_in_scripture': _build_slug_index(BLOOD_IN_SCRIPTURE_DATA),
    'kingdom_of_god': _build_slug_index(KINGDOM_OF_GOD_DATA),
    'names_of_christ': _build_slug_index(NAMES_OF_CHRIST_DATA),
    'spirits_and_demons': _build_slug_index(SPIRITS_AND_DEMONS_DATA),
    'personifications': _build_slug_index(PERSONIFICATIONS_DATA),
    'bibliology': _build_slug_index(BIBLIOLOGY_DATA),
    'theology_proper': _build_slug_index(THEOLOGY_PROPER_DATA),
    'anthropology': _build_slug_index(ANTHROPOLOGY_DATA),
    'hamartiology': _build_slug_index(HAMARTIOLOGY_DATA),
    'providence': _build_slug_index(PROVIDENCE_DATA),
    'grace': _build_slug_index(GRACE_DATA),
    'justification': _build_slug_index(JUSTIFICATION_DATA),
    'sanctification': _build_slug_index(SANCTIFICATION_DATA),
    'law_and_gospel': _build_slug_index(LAW_AND_GOSPEL_DATA),
    'worship': _build_slug_index(WORSHIP_DATA),
}


def find_resource_by_slug(data: dict, slug: str):
    """Fast O(1) lookup for resource items by slug using pre-built indexes."""
    # Find which resource type this data dict corresponds to
    data_to_key = {
        id(ANGELS_DATA): 'angels',
        id(PROPHETS_DATA): 'prophets',
        id(NAMES_DATA): 'names',
        id(PARABLES_DATA): 'parables',
        id(COVENANTS_DATA): 'covenants',
        id(APOSTLES_DATA): 'apostles',
        id(WOMEN_DATA): 'women',
        id(FESTIVALS_DATA): 'festivals',
        id(FRUITS_DATA): 'fruits',
        id(MIRACLES_DATA): 'miracles',
        id(PRAYERS_DATA): 'prayers',
        id(BEATITUDES_DATA): 'beatitudes',
        id(TEN_COMMANDMENTS_DATA): 'ten_commandments',
        id(ARMOR_OF_GOD_DATA): 'armor_of_god',
        id(I_AM_STATEMENTS_DATA): 'i_am_statements',
        id(TRINITY_DATA): 'trinity',
        id(CHRISTOLOGY_DATA): 'christology',
        id(SOTERIOLOGY_DATA): 'soteriology',
        id(PNEUMATOLOGY_DATA): 'pneumatology',
        id(ESCHATOLOGY_DATA): 'eschatology',
        id(ECCLESIOLOGY_DATA): 'ecclesiology',
        id(TYPES_AND_SHADOWS_DATA): 'types_and_shadows',
        id(MESSIANIC_PROPHECIES_DATA): 'messianic_prophecies',
        id(BLOOD_IN_SCRIPTURE_DATA): 'blood_in_scripture',
        id(KINGDOM_OF_GOD_DATA): 'kingdom_of_god',
        id(NAMES_OF_CHRIST_DATA): 'names_of_christ',
        id(SPIRITS_AND_DEMONS_DATA): 'spirits_and_demons',
        id(PERSONIFICATIONS_DATA): 'personifications',
        id(BIBLIOLOGY_DATA): 'bibliology',
        id(THEOLOGY_PROPER_DATA): 'theology_proper',
        id(ANTHROPOLOGY_DATA): 'anthropology',
        id(HAMARTIOLOGY_DATA): 'hamartiology',
        id(PROVIDENCE_DATA): 'providence',
        id(GRACE_DATA): 'grace',
        id(JUSTIFICATION_DATA): 'justification',
        id(SANCTIFICATION_DATA): 'sanctification',
        id(LAW_AND_GOSPEL_DATA): 'law_and_gospel',
        id(WORSHIP_DATA): 'worship',
    }

    data_key = data_to_key.get(id(data))
    if data_key and data_key in _SLUG_INDEXES:
        result = _SLUG_INDEXES[data_key].get(slug)
        if result:
            item_data, item_name, category_name, _ = result
            return item_data, item_name, category_name

    return None, None, None


__all__ = [
    'BIBLICAL_LOCATIONS',
    'ANGELS_DATA',
    'PROPHETS_DATA',
    'NAMES_DATA',
    'PARABLES_DATA',
    'COVENANTS_DATA',
    'APOSTLES_DATA',
    'WOMEN_DATA',
    'FESTIVALS_DATA',
    'FRUITS_DATA',
    'MIRACLES_DATA',
    'PRAYERS_DATA',
    'BEATITUDES_DATA',
    'TEN_COMMANDMENTS_DATA',
    'ARMOR_OF_GOD_DATA',
    'I_AM_STATEMENTS_DATA',
    # Theological Resources
    'TRINITY_DATA',
    'CHRISTOLOGY_DATA',
    'SOTERIOLOGY_DATA',
    'PNEUMATOLOGY_DATA',
    'ESCHATOLOGY_DATA',
    'ECCLESIOLOGY_DATA',
    'TYPES_AND_SHADOWS_DATA',
    'MESSIANIC_PROPHECIES_DATA',
    'BLOOD_IN_SCRIPTURE_DATA',
    'KINGDOM_OF_GOD_DATA',
    'NAMES_OF_CHRIST_DATA',
    'SPIRITS_AND_DEMONS_DATA',
    'PERSONIFICATIONS_DATA',
    # Additional Systematic Theology
    'BIBLIOLOGY_DATA',
    'THEOLOGY_PROPER_DATA',
    'ANTHROPOLOGY_DATA',
    'HAMARTIOLOGY_DATA',
    'PROVIDENCE_DATA',
    'GRACE_DATA',
    'JUSTIFICATION_DATA',
    'SANCTIFICATION_DATA',
    'LAW_AND_GOSPEL_DATA',
    'WORSHIP_DATA',
    # Functions
    'find_resource_by_slug',
]
