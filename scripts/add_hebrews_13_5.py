#!/usr/bin/env python3
"""Add theological commentary for Hebrews 13:5 - I Will Never Leave Thee."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from kjvstudy_org.utils.commentary_loader import merge_commentary_entries

new_commentaries = {
    "Hebrews": {
        "13": {
            "5": {
                "analysis": "This verse constitutes one of Scripture's most comprehensive promises regarding God's unfailing presence. The statement 'I will never leave thee, nor forsake thee' employs double negation in Greek ('ou me se afiso oute me sekataleipo') - a construction that emphasizes absolute, unconditional commitment. The two-fold promise addresses both active abandonment (leaving) and passive dereliction (forsaking), ensuring comprehensive coverage against any perception of divine withdrawal. 'Never' (Greek 'ou me') is the strongest negation available in Greek, indicating something that is literally impossible. The verb 'forsake' (kataleipo) specifically means to leave behind or abandon in a place of trial - a term frequently used of desertion under duress. This promise directly contradicts the experience of spiritual despair where believers often report feeling abandoned. Yet the writer insists this feeling is deceptive - God's presence persists irrespective of subjective emotional experience. The historical antecedent echoes God's promise to Joshua (Joshua 1:5): 'I will never leave thee, nor forsake thee,' establishing a pattern where God reiterates this covenant promise during seasons of significant transition and challenge. The promise applies not to extraordinary circumstances but to ordinary Christian existence, addressing the daily temptation to believe ourselves abandoned when facing ordinary struggles.",
                "historical": "Hebrews was written to Jewish Christians around 64-70 AD (possibly before the destruction of Jerusalem) who faced severe pressure to abandon their faith in Jesus and return to Jewish observance. They endured public reproach, confiscation of property (Hebrews 10:34), and community ostracism. Some may have experienced imprisonment (Hebrews 13:3). In this context of hardship testing their faith, the writer grounds Christian perseverance not in individual strength but in Christ's perpetual intercession and presence. The quotation of Joshua 1:5 activates typological thinking: as Joshua faced the daunting task of conquering Canaan yet received this promise, so these Hebrew Christians faced the demanding pilgrimage of faith amid cultural pressure. The historical Jesus had promised 'lo, I am with you alway' (Matthew 28:20), establishing the risen Christ as the fulfillment of God's covenant presence. The Hebrews audience, facing the collapse of the old covenant system (the temple destruction was imminent), needed reassurance that Christ himself was their sanctuary and presence. Church fathers like Chrysostom interpreted this verse as foundational for Christian courage under persecution - believers need not fear persecution or death if Christ's presence remains. The verse addressed the psychological reality that faith is tested precisely when feelings of abandonment seem most overwhelming.",
                "questions": [
                    "How does God's promise of never forsaking us address the common experience of feeling spiritually abandoned during trials?",
                    "What is the significance of the double promise (neither leaving nor forsaking) rather than a single statement of presence?",
                    "Why is the historical context of Joshua's conquest relevant to Hebrew Christians facing cultural and social pressure?",
                    "In what ways does this promise address the fear of gradual spiritual decline or the loss of God's guidance?",
                    "How does Christ's continued intercession (Hebrews 7:25) relate to this promise of perpetual presence?"
                ]
            }
        }
    }
}

merge_commentary_entries(new_commentaries)
print("✓ Added Hebrews 13:5 commentary")
