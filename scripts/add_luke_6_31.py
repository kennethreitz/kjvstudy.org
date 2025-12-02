#!/usr/bin/env python3
"""Add theological commentary for Luke 6:31 - The Golden Rule."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from kjvstudy_org.utils.commentary_loader import merge_commentary_entries

new_commentaries = {
    "Luke": {
        "6": {
            "31": {
                "analysis": "This verse encapsulates Jesus' ethical teaching through a comprehensive principle of reciprocal justice and love. 'As ye would that men should do to you, do ye also to them likewise' reformulates behavior based on the golden rule principle, the deepest expression of covenant love. The construction employs 'katheios' (just as, in the same way) to establish proportional response: our treatment of others should mirror the treatment we desire. This is not merely negative reciprocity (the silver rule: 'do not do unto others what you would not have them do unto you'), but positive reciprocity that proactively extends kindness, mercy, and justice. The emphasis on 'likewise' ('homoios') means not only frequency but quality and intention. Jesus teaches that moral behavior flows not from rules externally imposed but from internal transformation of desire - we naturally wish others well and extend kindness because we recognize our shared human condition. Greek philosophy recognized variations of this principle (Stoics, Confucius), but Jesus radicalizes it by grounding it in the nature of God's kingdom. This rule synthesizes the entire Torah and Prophets (Matthew 22:40) because it reflects God's character: a Creator who desires human flourishing and extends grace undeserved. The principle assumes anthropological parity - we recognize in others the same fundamental needs, vulnerabilities, and dignity we possess.",
                "historical": "Luke presents Jesus' Golden Rule in the Sermon on the Plain (Luke 6:20-49), paralleled in Matthew's Sermon on the Mount (Matthew 5-7). Luke's version emphasizes social ethics and care for the poor and marginalized, reflecting his consistent theme of God's preferential option for the economically vulnerable. This teaching countered the prevailing honor-shame cultural framework of first-century Mediterranean society, where reciprocity was transactional: you extended kindness to those of equal or greater status who could repay. Jesus inverts this entirely - the audience should 'do good to them which hate you, bless them that curse you' (Luke 6:27-28), extending kindness to those who cannot and will not repay. This was countercultural in a patronage society where social relationships were explicitly transactional. The principle also challenged Jewish teachers who restricted the definition of 'neighbor' to fellow Jews and righteous Gentiles. Jesus' parable of the Good Samaritan demonstrates that the 'neighbor' is any human we encounter who has need. The early church applied this principle radically: Acts 2:44-45 describes believers selling possessions to share with those in need, treating others' welfare as equivalent to their own. Church fathers like Augustine cited this verse when establishing Christian hospitality norms, fundamentally different from pagan reciprocity.",
                "questions": [
                    "How does the Golden Rule transcend mere reciprocal justice to become a principle of proactive benevolence?",
                    "Why would Jesus ground ethical behavior in empathy (imagining ourselves in others' circumstances) rather than in legal rules?",
                    "In what ways did Jesus' Golden Rule challenge first-century Mediterranean honor-shame culture?",
                    "How does this principle address the human tendency to rationalize unfair treatment of those we consider inferior?",
                    "What implications does the Golden Rule have for how Christians should approach justice, economics, and power?"
                ]
            }
        }
    }
}

merge_commentary_entries(new_commentaries)
print("✓ Added Luke 6:31 commentary")
