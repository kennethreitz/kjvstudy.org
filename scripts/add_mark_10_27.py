#!/usr/bin/env python3
"""Add theological commentary for Mark 10:27 - With God All Things Are Possible."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from kjvstudy_org.utils.commentary_loader import merge_commentary_entries

new_commentaries = {
    "Mark": {
        "10": {
            "27": {
                "analysis": "This verse articulates the fundamental principle of divine omnipotence and its pastoral application to human despair. 'With God all things are possible' (para theo panta dynata) establishes that the scope of divine capability encompasses all conceivable possibilities. The Greek 'dynata' (things able, possible) indicates not merely theoretical possibilities but practical possibilities - what God can actually accomplish. 'Para theo' (beside God, with God) uses a preposition suggesting God's presence and partnership, not distant transcendence. The statement follows Jesus' declaration that it is easier for a camel to enter a needle's eye than for a rich man to enter God's kingdom - an apparent impossibility suggesting human salvation through wealth-renunciation is humanly impossible. The disciples respond with existential despair: 'Who then can be saved?' This verse responds not by minimizing the difficulty but by recontextualizing it. The human impossibility of self-generated righteousness becomes irrelevant when divine omnipotence enters the equation. What cannot be accomplished through human effort, discipline, or achievement becomes possible through God's transformative grace. The theological movement here is essential to Christian soteriology: salvation requires not better human effort but divine intervention. The principle extends beyond soteriology - it addresses any human situation where circumstances appear intractable. Divine omnipotence provides the ultimate hope for believers facing terminal illness, seemingly impossible reconciliation, or entrenched patterns of sin and brokenness.",
                "historical": "Mark presents this verse in the context of Jesus' encounter with the rich young ruler (Mark 10:17-31), a narrative emphasizing the conflict between worldly security and kingdom allegiance. The young man possessed considerable wealth and asked what he must do to inherit eternal life. Jesus instructed him to sell all and distribute to the poor - a radical demand that wealth's security would become an obstacle to faith. The young man departed grieved, unable to relinquish his possessions. Jesus then teaches that 'How hardly shall they that have riches enter into the kingdom of God!' The disciples, understanding wealth as a sign of God's blessing (a common Deuteronomic assumption), respond with shock: if the blessed cannot enter easily, what of ordinary people? This verse answers their confusion. The first-century context valued wealth and security as indicators of God's favor. Jesus inverts this understanding: security in God comes not through wealth but through trusting God's transformative power. The historical Jesus directed this statement to disciples who would shortly face seemingly impossible challenges - persecution, execution of their leader, dispersion. Yet Mark's gospel, written after these events, demonstrates that what seemed impossible (the resurrection, the gospel's spread throughout the Roman Empire) proved possible through God's power. The verse thus serves as an apologetic justification for Christian hope amid suffering.",
                "questions": [
                    "How does acknowledging God's omnipotence specifically address the human tendency toward despair when circumstances seem insurmountable?",
                    "What is the relationship between recognizing human impossibility and receiving God's transformative power?",
                    "Why does Jesus emphasize this principle specifically in the context of wealth and kingdom entrance?",
                    "In what ways does divine omnipotence address the problem of apparently permanent brokenness in human relationships and personal sin patterns?",
                    "How does this promise account for situations where God's intervention does not occur in the ways believers desperately desire?"
                ]
            }
        }
    }
}

merge_commentary_entries(new_commentaries)
print("✓ Added Mark 10:27 commentary")
