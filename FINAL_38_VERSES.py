#!/usr/bin/env python3
"""
FINAL 38 VERSES - Complete Luke Commentary
Luke 17:34-37, 18:28-43, 19:45-48, 20:39-47, 21:34-38
"""
import json

with open('kjvstudy_org/data/verse_commentary/luke.json', 'r') as f:
    data = json.load(f)

c = data['commentary']

def add(ch, v, a, h, q):
    cs, vs = str(ch), str(v)
    if cs not in c: c[cs] = {}
    if vs not in c[cs]:
        c[cs][vs] = {"analysis": a, "historical": h, "questions": q}
        return True
    return False

added = 0

#==============================================================================
# LUKE 17:34-37 - Second Coming Separation (4 verses)
#==============================================================================

if add(17, 34,
    "<strong>I tell you, in that night there shall be two men in one bed; the one shall be taken, and the other shall be left</strong> (λέγω ὑμῖν, ταύτῃ τῇ νυκτὶ ἔσονται δύο ἐπὶ κλίνης μιᾶς, ὁ εἷς παραλημφθήσεται καὶ ὁ ἕτερος ἀφεθήσεται)—Jesus describes the Second Coming's sudden discrimination. <em>En tautē tē nukti</em> (in that night) emphasizes unexpectedness. Two in <em>klinē</em> (bed)—one <em>paralēmphthēsetai</em> (taken) and the other <em>aphethēsetai</em> (left). The passive verbs indicate divine agency—God makes the separation.<br><br>Context suggests 'taken' may mean taken in judgment (like Noah's flood taking the wicked), not rapture. The previous verses (vv.26-30) parallel Noah and Lot—in both cases, the wicked were 'taken' in judgment while the righteous were 'left' or delivered. Jesus emphasizes sudden separation based on internal spiritual state, not external circumstances.",
    "The pairing of two in one bed reflects ancient sleeping arrangements—families often shared sleeping spaces. Jesus's point: physical proximity doesn't guarantee spiritual unity. Two people in identical external circumstances face opposite eternal destinies based on their response to Christ. The Second Coming will expose and finalize this division.",
    ["What does this passage teach about the suddenness and finality of Christ's return—are you prepared?", "How does knowing that 'two in one bed' face opposite judgments challenge cultural or nominal Christianity?", "In what relationships are you closest to people who may face opposite eternal destinies—how does this affect your witness?"]
): added += 1

if add(17, 35,
    "<strong>Two women shall be grinding together; the one shall be taken, and the other left</strong> (ἔσονται δύο ἀλήθουσαι ἐπὶ τὸ αὐτό, ἡ μία παραλημφθήσεται, ἡ δὲ ἑτέρα ἀφεθήσεται)—Jesus continues the separation imagery. Two women <em>alēthousai epi to auto</em> (grinding at the same place)—engaged in identical daily labor. Again, one taken, one left. The repetition emphasizes that external activity, social position, or religious practice doesn't determine destiny—internal heart condition does.<br><br>Grinding grain was daily women's work, often done communally. Jesus uses mundane activity to illustrate eschatological separation. No sphere of life—domestic, agricultural, commercial—escapes divine judgment. The Second Coming interrupts ordinary life, revealing and finalizing hidden spiritual realities.",
    "Hand-grinding grain between millstones was arduous daily work for women in ancient Near Eastern households. Pairs often worked together, singing and talking while grinding. This familiar domestic scene provides Jesus with imagery for sudden eschatological separation—judgment interrupting normal life without warning, discriminating based on invisible spiritual realities.",
    ["How does the ordinariness of these examples (sleeping, grinding) challenge expectations of dramatic pre-judgment warnings?", "What does it mean that judgment comes during normal daily activities—how should this affect present priorities?", "Are you spiritually prepared for Christ's return to interrupt your ordinary day at any moment?"]
): added += 1

if add(17, 36,
    "<strong>Two men shall be in the field; the one shall be taken, and the other left</strong> (δύο ἔσονται ἐν τῷ ἀγρῷ, ὁ εἷς παραλημφθήσεται καὶ ὁ ἕτερος ἀφεθήσεται)—Jesus provides a third example: two men <em>en tō agrō</em> (in the field), one taken, one left. Note: this verse doesn't appear in earliest Greek manuscripts and may be a later scribal addition harmonizing with Matthew 24:40. Whether original or not, it continues the pattern: identical external circumstances, opposite eternal destinies.<br><br>The agricultural setting represents men's labor parallel to women's domestic labor (v.35). If authentic, it emphasizes the comprehensiveness of eschatological separation—no sphere of human activity escapes judgment. The Second Coming discriminates based on internal relationship with Christ, not external religious performance or moral respectability.",
    "Field labor (plowing, harvesting, shepherding) was primary male occupation in agrarian first-century Palestine. If this verse is original, Jesus covers all sectors of society: domestic (bed), women's labor (grinding), men's labor (field). The textual uncertainty doesn't affect the passage's overall message: Christ's return brings sudden, comprehensive, final separation based on hidden spiritual realities.",
    ["How do you live with awareness that normal activities could be interrupted at any moment by Christ's return?", "What does separation based on heart condition rather than external circumstances teach about the nature of saving faith?", "Are you living today in a way you'd want Christ to find you if he returned this instant?"]
): added += 1

if add(17, 37,
    "<strong>And they answered and said unto him, Where, Lord? And he said unto them, Wheresoever the body is, thither will the eagles be gathered together</strong> (καὶ ἀποκριθέντες λέγουσιν αὐτῷ, Ποῦ, κύριε; ὁ δὲ εἶπεν αὐτοῖς, Ὅπου τὸ σῶμα, ἐκεῖ καὶ οἱ ἀετοὶ ἐπισυναχθήσονται)—the disciples ask <em>pou</em> (where?) regarding the separation. Jesus responds proverbially: <em>hopou to sōma, ekei kai hoi aetoi</em> (where the body/corpse, there the eagles/vultures). <em>Aetos</em> can mean eagles or vultures; given the corpse context, vultures are likely. <em>Episunachthēsontai</em> (gathered together) describes inevitable congregation.<br><br>Jesus's answer is cryptic but suggests judgment's inevitability and obviousness. As vultures instinctively gather where death occurs, so judgment congregates where spiritual death exists. The comparison may indicate Jerusalem's destruction (AD 70) when Roman 'eagles' (their military standards) gathered to devour the spiritually dead city. Or more generally: judgment is as certain and conspicuous as vultures on a carcass.",
    "Roman military standards featured eagles, and Josephus describes the AD 70 siege with imagery matching Jesus's prophecy. Alternatively, the proverb may simply illustrate inevitability—vultures gathering on corpses is natural law, just as divine judgment on spiritual death is moral law. The disciples' question about location ('where?') receives an answer about certainty: judgment is as inevitable as vultures finding carcasses.",
    ["How does vulture imagery challenge comfortable views of judgment—is divine wrath as natural and inevitable as vultures on corpses?", "What does this passage teach about spiritual death attracting divine judgment as certainly as physical death attracts scavengers?", "Are you living as spiritually alive (protected from judgment) or spiritually dead (awaiting divine vultures)?"]
): added += 1

print(f"Added {added} verses so far...")

# Save progress
data['commentary'] = c
with open('kjvstudy_org/data/verse_commentary/luke.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved progress. Continuing with remaining verses...")
print("Still need: Luke 18:28-43 (16 verses), 19:45-48 (4 verses), 20:39-47 (9 verses), 21:34-38 (5 verses)")
print("Total remaining: 34 verses")
