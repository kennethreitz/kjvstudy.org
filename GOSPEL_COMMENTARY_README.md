# Gospel Commentary Generation System

## Overview

This system provides tools and resources for generating comprehensive, scholarly commentary for all 3,779 verses across the four Gospels (Matthew, Mark, Luke, and John).

## Files Included

### Scripts

1. **generate_comprehensive_gospel_commentary.py**
   - Framework for systematic commentary generation
   - Includes batch processing and progress tracking
   - Template for AI-assisted generation

2. **generate_john_commentary.py**
   - Specialized script for Gospel of John
   - Includes theological templates for key verses
   - Demonstrates high-quality commentary structure

3. **gospel_commentary_generator.py**
   - Focused on key theological passages
   - Prioritizes most important verses
   - Good for Phase 1 implementation

### Data Files

4. **gospels_commentary_sample.json**
   - High-quality sample commentary for 5 key verses
   - Demonstrates proper structure and depth
   - Ready to merge into verse_commentary.json

5. **COMMENTARY_PROJECT_PLAN.md**
   - Comprehensive project roadmap
   - Defines phases and timelines
   - Lists required resources

## Current Status

**Commentary Generated:**
- John 3:16 ✅
- John 1:1 ✅
- John 1:14 ✅
- John 3:3 ✅
- John 14:6 ✅
- Matthew 5:3 ✅
- Plus existing verses in verse_commentary.json

**Remaining:**
- John: 879 verses
- Matthew: 1,071 verses
- Mark: 678 verses
- Luke: 1,151 verses

## Quality Standards

Each commentary entry includes:

### 1. Analysis (200-400 words)
- **Strong theological content** with Greek word studies
- **Doctrinal significance** and biblical theology connections
- **Literary context** within the Gospel narrative
- **HTML formatting**: `<strong>` for verse text, `<em>` for Greek/Hebrew, `<br><br>` for paragraphs

### 2. Historical Context (200-400 words)
- **First-century setting**: cultural, political, religious background
- **Gospel-specific perspective**: author's purpose and audience
- **Archaeological/historical evidence** where relevant
- **Old Testament connections** and fulfillment themes

### 3. Application
- Left **empty** (per existing schema)

### 4. Reflection Questions (2-3 per verse)
- **Theologically probing**: challenge understanding
- **Contextually specific**: tailored to the verse
- **Practically relevant**: encourage application

## Usage Instructions

### Merging Sample Commentary

```bash
# Load and merge the sample commentary
python3 -c "
import json
from pathlib import Path

# Load existing commentary
with open('kjvstudy_org/data/verse_commentary.json', 'r') as f:
    existing = json.load(f)

# Load sample commentary
with open('gospels_commentary_sample.json', 'r') as f:
    sample = json.load(f)

# Merge
existing.update(sample)

# Save
with open('kjvstudy_org/data/verse_commentary.json', 'w') as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)

print(f'Merged {len(sample)} new commentary entries')
print(f'Total entries: {len(existing)}')
"
```

### Generating Additional Commentary

For AI-assisted generation using Claude or GPT-4:

```python
#!/usr/bin/env python
import anthropic
import json
from kjvstudy_org.kjv import bible

client = anthropic.Anthropic(api_key="your-api-key")

def generate_verse_commentary(book, chapter, verse_num):
    """Generate commentary using Claude API."""

    verse_text = bible.get_verse_text(book, chapter, verse_num)

    prompt = f"""Generate comprehensive theological commentary for:

{book} {chapter}:{verse_num}
"{verse_text}"

Provide JSON with this structure:
{{
  "analysis": "200-400 words with Greek analysis, theological significance...",
  "historical_context": "200-400 words with first-century context...",
  "application": "",
  "questions": ["Question 1", "Question 2", "Question 3"]
}}

Be scholarly, theologically sound, and specific to this verse."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.content[0].text)

# Example usage
commentary = generate_verse_commentary("John", 1, 1)
print(json.dumps(commentary, indent=2))
```

## Recommended Approach

### Phase 1: High-Value Verses (Weeks 1-2)
Focus on ~200-300 theologically significant verses:

**John**
- Prologue (1:1-18)
- "I am" statements (6:35, 8:12, 10:11, 11:25, 14:6, 15:5)
- Key conversations (3:1-21, 4:1-42)
- Upper Room discourse (13-17)
- Passion and resurrection (18-21)

**Matthew**
- Beatitudes (5:3-12)
- Lord's Prayer (6:9-13)
- Great Commission (28:18-20)
- Key parables (13, 18, 20, 21-22, 24-25)

**Mark**
- Messianic secret passages
- Suffering Servant predictions
- Key miracles and teachings

**Luke**
- Birth narratives (1-2)
- Unique parables (10, 15, 16, 18, 19)
- Resurrection appearances (24)

### Phase 2: Systematic Completion (Weeks 3-8)
- Process each Gospel chapter by chapter
- Use AI for initial drafts
- Human review for theological accuracy
- Batch process to manage costs

### Phase 3: Review and Enhancement (Weeks 9-12)
- Quality review of all commentary
- Add cross-references
- Enhance weak entries
- Final theological review

## Integration with Existing System

The commentary integrates seamlessly with the kjvstudy.org application:

```python
# In server.py or template rendering
from pathlib import Path
import json

# Load commentary
commentary_path = Path(__file__).parent / "data/verse_commentary.json"
with open(commentary_path) as f:
    verse_commentary = json.load(f)

# Use in route
@app.get("/verse/{book}/{chapter}/{verse}")
def get_verse_with_commentary(book, chapter, verse):
    reference = f"{book} {chapter}:{verse}"

    verse_data = {
        "reference": reference,
        "text": bible.get_verse_text(book, chapter, verse),
        "commentary": verse_commentary.get(reference, None)
    }

    return verse_data
```

## Resources

### Theological References
- **Greek Lexicons**: BDAG, Thayer's, Strong's
- **Commentaries**: Matthew Henry, John MacArthur, NIV/ESV Study Bibles
- **Word Studies**: Vine's, Zodhiates, Robertson's Word Pictures

### Technical Resources
- **Anthropic Claude API**: https://docs.anthropic.com
- **OpenAI GPT-4**: https://platform.openai.com
- **Python libraries**: `anthropic`, `openai`, `pydantic`

## Cost Estimates

### AI-Assisted Generation
Using Claude 3.5 Sonnet:
- ~500 tokens per verse commentary
- 3,779 verses × 500 tokens = ~1.9M tokens
- Input: ~$3/million tokens
- Output: ~$15/million tokens
- **Total estimated cost: ~$35-50** for complete Gospel commentary

### Time Estimates
- **AI generation**: 2-3 weeks for all verses
- **Human review**: 4-6 weeks for quality control
- **Total project time**: 6-10 weeks with dedicated effort

## Quality Assurance

Before merging commentary:

1. **Theological Review**: Ensure doctrinal accuracy
2. **Grammar Check**: Professional editing
3. **Format Validation**: JSON schema compliance
4. **Cross-Reference**: Check against standard commentaries
5. **Uniqueness**: Avoid plagiarism, create original content

## Support

For questions or issues:
- Review existing commentary in `kjvstudy_org/data/verse_commentary.json`
- Check schema at `kjvstudy_org/data/schemas/verse_commentary.schema.json`
- Refer to project structure in `CLAUDE.md`

## License

Commentary should be:
- **Original work** or properly attributed
- **Theologically sound** and orthodox
- **Accessible** to general Christian readers
- **Scholarly** enough for serious study
