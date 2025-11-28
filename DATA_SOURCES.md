# Data Sources and Attributions

This document lists all data sources used in KJV Study, including their licenses, attributions, and any modifications made.

## Bible Text

### King James Version (1769 Cambridge Edition)
- **Source**: 1769 Cambridge King James Version
- **License**: Public Domain
- **Format**: 31,102 verses across 66 books
- **Location**: `kjvstudy_org/data/kjv.json`
- **Notes**: The Authorized Version (KJV) of 1769 is in the public domain worldwide.

## Cross-References

### Treasury of Scripture Knowledge (via OpenBible.info)
- **Source**: [OpenBible.info Cross-References](https://www.openbible.info/labs/cross-references/)
- **Original Work**: Treasury of Scripture Knowledge (TSK)
- **License**: Creative Commons Attribution (CC-BY)
- **GitHub Repository**: [shandran/openbible](https://github.com/shandran/openbible)
- **Data File**: `cross_references_expanded.csv`
- **Format**: 120,858 cross-reference entries covering 24,900 verses
- **Location**: `kjvstudy_org/data/cross_references.json`
- **Filtering**: Minimum 3 community votes, top 10 references per verse
- **Attribution**: © OpenBible.info 2024, CC-BY
- **Notes**:
  - TSK is a comprehensive cross-reference system originally compiled in the 19th century
  - OpenBible.info enhanced the dataset with community voting and additional references
  - Data blends TSK with other public domain resources including the Topical Bible
  - We filtered for quality (3+ votes) and limited to top 10 per verse by vote count

## Red Letter Edition

### Words of Christ Identification
- **Source**: Custom compilation based on traditional red letter Bibles
- **Location**: `kjvstudy_org/data/red_letter_verses.json`
- **Format**: 2,076 verses marked as words of Christ
- **Coverage**: Gospels, Acts, and Revelation
- **Notes**:
  - Identifies verses containing direct speech of Jesus Christ
  - Some verses contain partial quotes (only Jesus' words are marked)
  - Based on traditional red letter Bible conventions
  - Includes post-resurrection appearances and Revelation visions

## Interlinear Data

### Hebrew and Greek Word Analysis
- **Source**: [tahmmee/interlinear_bibledata](https://github.com/tahmmee/interlinear_bibledata)
- **Location**: `kjvstudy_org/data/interlinear.json.gz`
- **License**: Public Domain
- **Format**: 31,031 verses with original language words, transliterations, Strong's numbers, parsing, and definitions
- **Size**: 12 MB (gzip compressed from 141 MB)
- **Notes**:
  - Complete interlinear Bible data for Greek (New Testament) and Hebrew (Old Testament)
  - Includes Strong's Exhaustive Concordance numbers
  - Lazy-loaded on first access for performance
  - Cached in memory after first load

## Study Resources

### Topics Index
- **Source**: Custom compilation
- **Location**: `kjvstudy_org/topics.py`
- **License**: Original work
- **Notes**: Thematic organization of Bible verses by topic

### Reading Plans
- **Source**: Custom compilation and traditional plans
- **Location**: `kjvstudy_org/reading_plans.py`
- **License**: Original work
- **Notes**: Various Bible reading plans including chronological and thematic approaches

### Commentary
- **Source**: Custom AI-generated commentary
- **Location**: `kjvstudy_org/data/commentary.json`
- **Format**: 2,076 verse commentaries
- **License**: Original work
- **Notes**: Reformed theological perspective

## Attribution Requirements

When using data from this project:

1. **Bible Text (KJV 1769)**: Public domain, no attribution required
2. **Cross-References (OpenBible.info)**: Must attribute as "Cross-references from OpenBible.info, CC-BY"
3. **Original Content**: Attribution to kjvstudy.org appreciated

## Compliance

This project complies with:
- Creative Commons Attribution (CC-BY) requirements for OpenBible.info data
- Public domain usage of KJV 1769 text
- Fair use and original compilation of study resources

## Data Quality and Filtering

### Cross-References
- **Vote Threshold**: Minimum 3 community votes from OpenBible.info
- **Quantity Limit**: Top 10 cross-references per verse (by vote count)
- **Quality Rationale**: Higher vote counts indicate community validation and relevance

### Red Letter Edition
- **Methodology**: Traditional red letter Bible conventions
- **Partial Verses**: Only Jesus' actual words are marked, not narrative
- **Theological Basis**: Direct quotations of Christ's speech

## Updates and Maintenance

- **Last Updated**: 2024-11-28
- **Cross-References**: Imported from OpenBible.info snapshot (2024)
- **Bible Text**: Static (1769 Cambridge KJV)
- **Commentary**: Periodically updated

## Contact

For questions about data sources or licensing:
- GitHub: https://github.com/kennethreitz/kjvstudy.org
- Issues: https://github.com/kennethreitz/kjvstudy.org/issues

## Acknowledgments

- **OpenBible.info** - For comprehensive cross-reference dataset
- **Treasury of Scripture Knowledge** - Original cross-reference compilation
- **Cambridge University** - 1769 KJV edition preservation
- **Contributors** - All who have contributed to public domain Bible resources
