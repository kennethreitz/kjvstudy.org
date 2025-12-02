#!/usr/bin/env python3
"""Add theological commentary for 1 John 4:18 - Perfect Love Casts Out Fear."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from kjvstudy_org.utils.commentary_loader import merge_commentary_entries

new_commentaries = {
    "1 John": {
        "4": {
            "18": {
                "analysis": "This verse presents the paradox that defines Christian maturity: the inverse relationship between love and fear. The Greek word 'agape' (divine love) represents God's self-giving, covenant love demonstrated through Christ's sacrifice. 'Perfect love casteth out fear' employs the word 'ekstasis' in translation principle - meaning to drive out, expel, or displace completely. Fear (Greek 'phobos') here denotes a specific spiritual fear: the fear of judgment, rejection, or separation from God that characterizes those who have not fully apprehended God's character. John establishes that love and fear are fundamentally incompatible emotional states when the love is mature and established. The phrase 'There is no fear in love' is absolute - a categorical statement that where authentic agape exists, existential fear of divine judgment cannot coexist. This is not mere sentiment but theological reality: when we comprehend that God has loved us with infinite, self-sacrificial love (cf. John 3:16), fear of His judgment becomes irrational. The believer's fear gives way to 'perfect love' - which means love that has reached its completion, maturity, or full expression in our understanding and practice.",
                "historical": "John writes this epistle in the late first century (approximately 90-95 AD) to combat early Gnostic heresies that denied Christ's incarnation and the reality of loving community. His audience comprised second or third-generation Christians facing persecution and existential anxiety about their standing with God. In this context, John's emphasis that God is love (1 John 4:8) was revolutionary - it contradicted the capricious, wrathful deity concepts prevalent in Greco-Roman religious thinking. The Roman Empire under Domitian (81-96 AD) intensified persecution of Christians, creating genuine fear of execution, property loss, and family separation. Yet John argues that the Christian's understanding of Christ's redeeming love should enable transcendence of this fear. The epistle also addresses perfectionist anxieties - the fear that any sin disqualifies believers from God's love. John's theology of 1 John 1:8-9 (God's ongoing cleansing) combines with this passage to assure believers that love persists despite human failure. Early church fathers like Augustine interpreted this passage to mean that God's love expressed through Christ's atonement provides the foundation for believers to reorient their deepest emotions from fear to confident trust. The passage became foundational for understanding Christian psychology - that belief shapes emotions more than emotions shape belief.",
                "questions": [
                    "What is the distinction between the fear of God (reverence) and the fear that love casts out (terror of judgment)?",
                    "How does understanding Christ's sacrificial love specifically address the existential fear of judgment and separation from God?",
                    "In what ways does 'perfect love' require maturity and development, suggesting that immature believers may not yet experience fear's departure?",
                    "How might John's audience under Domitian's persecution have found comfort in this verse despite their very real physical danger?",
                    "What does this passage suggest about the relationship between theological knowledge ('knowing') and emotional transformation ('feeling')?"
                ]
            }
        }
    }
}

merge_commentary_entries(new_commentaries)
print("✓ Added 1 John 4:18 commentary")
