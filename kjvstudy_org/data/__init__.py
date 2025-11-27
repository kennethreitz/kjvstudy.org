"""Biblical resource data - maps, angels, prophets, names of God, etc."""

import json
from pathlib import Path

# Load resources from JSON data file
_data_path = Path(__file__).parent / "resources.json"
with open(_data_path, "r", encoding="utf-8") as f:
    _data = json.load(f)

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
]
