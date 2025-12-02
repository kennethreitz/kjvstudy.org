"""
Bible reading plans for structured Scripture study.
Provides various reading schedules for different goals.
"""

import json
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_reading_plans():
    """Load reading plans from per-plan files (fallback to legacy)."""
    base_dir = Path(__file__).parent / "data"
    plans_dir = base_dir / "reading_plans"
    legacy_path = base_dir / "reading_plans.json"

    merged = {}
    if plans_dir.exists():
        for path in sorted(plans_dir.glob("*.json")):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    merged.update(data)
    elif legacy_path.exists():
        with open(legacy_path, "r", encoding="utf-8") as f:
            merged = json.load(f)

    return merged


_data = _load_reading_plans()

ONE_YEAR_PLAN = _data.get("one_year_plan", {})
CHRONOLOGICAL_PLAN = _data.get("chronological_plan", {})
NT_90_DAYS = _data.get("nt_90_days", {})
PSALMS_PROVERBS = _data.get("psalms_proverbs", {})
GOSPELS_ACTS_30 = _data.get("gospels_acts_30", {})
PAUL_EPISTLES_30 = _data.get("paul_epistles_30", {})
PENTATEUCH_40 = _data.get("pentateuch_40", {})
PROPHETS_60 = _data.get("prophets_60", {})
MINOR_PROPHETS_14 = _data.get("minor_prophets_14", {})
WISDOM_30 = _data.get("wisdom_30", {})
HISTORICAL_45 = _data.get("historical_45", {})
GENERAL_EPISTLES_14 = _data.get("general_epistles_14", {})

# Reading plans database
READING_PLANS = {
    "chronological": {
        "name": "Chronological Bible Reading Plan",
        "description": "Read the Bible in the order events occurred historically",
        "duration_days": 365,
        "overview": "This plan arranges Scripture in chronological order, allowing you to read the Bible as a narrative of God's redemptive plan. Job is read with Genesis, Psalms with the life of David, prophets with the kings, and Gospels are harmonized.",
        "days": CHRONOLOGICAL_PLAN,
        "sample_days": [
            {"day": 1, "readings": ["Genesis 1-3"], "theme": "Creation and Fall"},
            {"day": 2, "readings": ["Genesis 4-7"], "theme": "From Cain to Noah"},
            {"day": 3, "readings": ["Genesis 8-11"], "theme": "The Flood and Tower of Babel"},
            {"day": 30, "readings": ["Job 1-5"], "theme": "Job's trials begin"},
            {"day": 100, "readings": ["Exodus 1-4"], "theme": "Moses and the Burning Bush"},
            {"day": 200, "readings": ["2 Samuel 11-12", "Psalms 51"], "theme": "David's sin and repentance"},
            {"day": 300, "readings": ["Matthew 5-7"], "theme": "Sermon on the Mount"},
            {"day": 365, "readings": ["Revelation 21-22"], "theme": "New Heaven and Earth"},
        ]
    },
    "one-year": {
        "name": "One Year Bible Reading Plan",
        "description": "Read through the entire Bible in one year",
        "duration_days": 365,
        "overview": "This classic plan divides Scripture into daily readings of approximately 3-4 chapters, systematically progressing through the Old and New Testaments, Psalms, and Proverbs.",
        "days": ONE_YEAR_PLAN,
        "sample_days": [
            {"day": 1, "readings": ["Genesis 1-3", "Matthew 1", "Psalms 1"], "theme": "In the beginning"},
            {"day": 7, "readings": ["Genesis 16-18", "Matthew 7", "Psalms 7"], "theme": "Week one complete"},
            {"day": 30, "readings": ["Exodus 13-15", "Matthew 30", "Psalms 30"], "theme": "First month milestone"},
            {"day": 100, "readings": ["Leviticus 23-25", "Mark 9", "Psalms 100"], "theme": "The feasts"},
            {"day": 200, "readings": ["1 Chronicles 10-12", "Acts 1", "Psalms 52"], "theme": "The early church"},
            {"day": 300, "readings": ["Jeremiah 14-16", "1 Thessalonians 1", "Proverbs 26"], "theme": "Prophets and epistles"},
            {"day": 365, "readings": ["Malachi 3-4", "Revelation 22", "Psalms 150"], "theme": "Journey complete"},
        ]
    },
    "new-testament": {
        "name": "New Testament in 90 Days",
        "description": "Read the entire New Testament in three months",
        "duration_days": 90,
        "overview": "Focus on Christ and the early church by reading through all 27 New Testament books in 90 days. Ideal for new believers or those wanting to deepen their understanding of Christian doctrine.",
        "days": NT_90_DAYS,
        "sample_days": [
            {"day": 1, "readings": ["Matthew 1-3"], "theme": "Christ's genealogy and birth"},
            {"day": 10, "readings": ["Matthew 22-24"], "theme": "Olivet Discourse"},
            {"day": 20, "readings": ["Mark 11-13"], "theme": "Passion week begins"},
            {"day": 30, "readings": ["Luke 15-17"], "theme": "Parables of grace"},
            {"day": 40, "readings": ["John 11-13"], "theme": "Upper room discourse"},
            {"day": 50, "readings": ["Acts 13-15"], "theme": "Paul's first journey"},
            {"day": 60, "readings": ["Romans 12-14"], "theme": "Christian living"},
            {"day": 70, "readings": ["Ephesians 4-6"], "theme": "Unity and armor"},
            {"day": 80, "readings": ["Hebrews 9-11"], "theme": "Faith and better covenant"},
            {"day": 90, "readings": ["Revelation 21-22"], "theme": "All things new"},
        ]
    },
    "gospels-acts": {
        "name": "Gospels and Acts in 30 Days",
        "description": "Immerse yourself in the life of Christ and the early church",
        "duration_days": 30,
        "overview": "Read the four Gospels and Acts in one month, gaining a comprehensive view of Christ's ministry, death, resurrection, and the establishment of His church.",
        "days": GOSPELS_ACTS_30,
        "sample_days": [
            {"day": 1, "readings": ["Matthew 1-4"], "theme": "Birth and temptation of Christ"},
            {"day": 5, "readings": ["Matthew 17-20"], "theme": "Transfiguration and teachings"},
            {"day": 10, "readings": ["Mark 11-14"], "theme": "Passion week"},
            {"day": 15, "readings": ["Luke 15-18"], "theme": "Parables and prayers"},
            {"day": 20, "readings": ["John 13-17"], "theme": "Upper room teachings"},
            {"day": 25, "readings": ["Acts 10-13"], "theme": "Gospel to Gentiles"},
            {"day": 30, "readings": ["Acts 26-28"], "theme": "Paul reaches Rome"},
        ]
    },
    "psalms-proverbs": {
        "name": "Psalms and Proverbs Daily",
        "description": "Read through wisdom literature multiple times per year",
        "duration_days": 31,
        "overview": "Read one Psalm and one chapter of Proverbs each day. The 31-day cycle allows you to read Proverbs 12 times and Psalms 5 times per year.",
        "days": PSALMS_PROVERBS,
        "sample_days": [
            {"day": 1, "readings": ["Psalms 1", "Proverbs 1"], "theme": "Wisdom's foundation"},
            {"day": 15, "readings": ["Psalms 15", "Proverbs 15"], "theme": "Righteous living"},
            {"day": 31, "readings": ["Psalms 31", "Proverbs 31"], "theme": "Trust and the virtuous woman"},
        ]
    },
    "pentateuch": {
        "name": "Books of Moses in 40 Days",
        "description": "Study the Law and foundational narratives",
        "duration_days": 40,
        "overview": "Read Genesis through Deuteronomy in 40 days, exploring creation, the patriarchs, the Exodus, and the giving of the Law.",
        "days": PENTATEUCH_40,
        "sample_days": [
            {"day": 1, "readings": ["Genesis 1-3"], "theme": "Creation and Fall"},
            {"day": 10, "readings": ["Genesis 37-40"], "theme": "Joseph in Egypt"},
            {"day": 20, "readings": ["Exodus 19-22"], "theme": "The Law given"},
            {"day": 30, "readings": ["Numbers 13-16"], "theme": "Wilderness wandering"},
            {"day": 40, "readings": ["Deuteronomy 31-34"], "theme": "Moses' death"},
        ]
    },
    "prophets": {
        "name": "Major Prophets in 60 Days",
        "description": "Read Isaiah, Jeremiah, Ezekiel, and Daniel",
        "duration_days": 60,
        "overview": "Study the major prophets, their messages of judgment and hope, and their Messianic prophecies fulfilled in Christ.",
        "days": PROPHETS_60,
        "sample_days": [
            {"day": 1, "readings": ["Isaiah 1-3"], "theme": "Isaiah's call"},
            {"day": 15, "readings": ["Isaiah 40-42"], "theme": "Comfort and the Servant"},
            {"day": 30, "readings": ["Jeremiah 30-33"], "theme": "The New Covenant"},
            {"day": 45, "readings": ["Ezekiel 36-39"], "theme": "Restoration promised"},
            {"day": 60, "readings": ["Daniel 10-12"], "theme": "End times revealed"},
        ]
    },
    "paul-epistles": {
        "name": "Paul's Letters in 30 Days",
        "description": "Study apostolic doctrine through Paul's epistles",
        "duration_days": 30,
        "overview": "Read all thirteen letters attributed to Paul, from Romans to Philemon, grasping the depth of Christian theology and practical living.",
        "days": PAUL_EPISTLES_30,
        "sample_days": [
            {"day": 1, "readings": ["Romans 1-3"], "theme": "Justification by faith"},
            {"day": 5, "readings": ["Romans 12-14"], "theme": "Christian living"},
            {"day": 10, "readings": ["1 Corinthians 12-14"], "theme": "Spiritual gifts and love"},
            {"day": 15, "readings": ["Galatians 1-3"], "theme": "Freedom in Christ"},
            {"day": 20, "readings": ["Ephesians 4-6"], "theme": "Unity and warfare"},
            {"day": 25, "readings": ["1 Timothy 3-5"], "theme": "Church order"},
            {"day": 30, "readings": ["Philemon"], "theme": "Forgiveness and brotherhood"},
        ]
    },
    "minor-prophets": {
        "name": "Minor Prophets in 14 Days",
        "description": "Read Hosea through Malachi",
        "duration_days": 14,
        "overview": "Study the twelve Minor Prophets in two weeks, exploring themes of judgment, repentance, and the coming Messiah. These shorter books pack powerful messages of God's justice and mercy.",
        "days": MINOR_PROPHETS_14,
        "sample_days": [
            {"day": 1, "readings": ["Hosea 1-7"], "theme": "God's Faithful Love for Unfaithful Israel"},
            {"day": 6, "readings": ["Obadiah", "Jonah 1-4"], "theme": "Edom's Doom, Jonah and God's Mercy"},
            {"day": 9, "readings": ["Habakkuk 1-3"], "theme": "The Just Shall Live by Faith"},
            {"day": 14, "readings": ["Malachi 1-4"], "theme": "Messenger of the Covenant, Elijah Returns"},
        ]
    },
    "wisdom": {
        "name": "Wisdom Literature in 30 Days",
        "description": "Study Job, Psalms, Proverbs, Ecclesiastes, and Song of Solomon",
        "duration_days": 30,
        "overview": "Immerse yourself in the wisdom books of Scripture, from Job's suffering to the praises of the Psalms, the practical wisdom of Proverbs, the philosophical reflections of Ecclesiastes, and the poetry of the Song of Solomon.",
        "days": WISDOM_30,
        "sample_days": [
            {"day": 1, "readings": ["Job 1-3"], "theme": "Job's Suffering Begins"},
            {"day": 9, "readings": ["Job 38-42"], "theme": "God Speaks, Job Restored"},
            {"day": 19, "readings": ["Psalms 119"], "theme": "The Word of God"},
            {"day": 27, "readings": ["Proverbs 26-31"], "theme": "Fools, Agur, The Virtuous Woman"},
            {"day": 30, "readings": ["Song of Solomon 1-8"], "theme": "The Beloved and the Lover"},
        ]
    },
    "historical": {
        "name": "Historical Books in 45 Days",
        "description": "Read Joshua through Esther",
        "duration_days": 45,
        "overview": "Journey through Israel's history from conquering the Promised Land to the exile and return. Experience the judges, kings, prophets, and God's faithfulness through triumph and tragedy.",
        "days": HISTORICAL_45,
        "sample_days": [
            {"day": 1, "readings": ["Joshua 1-5"], "theme": "Entering the Promised Land"},
            {"day": 11, "readings": ["Ruth 1-4"], "theme": "Loyalty, Redemption, David's Ancestry"},
            {"day": 24, "readings": ["1 Kings 5-8"], "theme": "Temple Built and Dedicated"},
            {"day": 34, "readings": ["2 Kings 24-25"], "theme": "Jerusalem Falls, Exile"},
            {"day": 45, "readings": ["Nehemiah 3-13", "Esther 1-10"], "theme": "Walls Rebuilt, Esther Saves Her People"},
        ]
    },
    "general-epistles": {
        "name": "General Epistles in 14 Days",
        "description": "Read Hebrews through Jude plus Revelation's letters",
        "duration_days": 14,
        "overview": "Study the non-Pauline letters of the New Testament, exploring themes of faith, perseverance, practical Christian living, and warnings against false teaching.",
        "days": GENERAL_EPISTLES_14,
        "sample_days": [
            {"day": 1, "readings": ["Hebrews 1-4"], "theme": "Christ Superior to Angels and Moses"},
            {"day": 5, "readings": ["James 1-3"], "theme": "Faith and Works, Taming the Tongue"},
            {"day": 10, "readings": ["1 John 1-3"], "theme": "Fellowship, Walking in Light, Love"},
            {"day": 13, "readings": ["Jude"], "theme": "Contending for the Faith"},
            {"day": 14, "readings": ["Revelation 1-3"], "theme": "Vision of Christ, Letters to Churches"},
        ]
    }
}


def get_plan(plan_id: str) -> dict:
    """Get a reading plan by ID"""
    return READING_PLANS.get(plan_id)


def get_all_plans() -> dict:
    """Get all available reading plans"""
    return READING_PLANS


def get_plan_summary() -> list:
    """Get summary list of all plans"""
    return [
        {
            "id": plan_id,
            "name": plan["name"],
            "description": plan["description"],
            "days": plan["duration_days"]
        }
        for plan_id, plan in READING_PLANS.items()
    ]
