#!/usr/bin/env python3
"""
Manually fix the remaining 33 verses with complex narrative structures.
"""

import json
from pathlib import Path

# Manual fixes for each verse
# Format: "verse_key": "spoken_words" or None (to remove entry if not Jesus speaking)
MANUAL_FIXES = {
    # Matthew
    "Matthew 16:8": "O ye of little faith, why reason ye among yourselves, because ye have brought no bread?",
    "Matthew 20:13": "Friend, I do thee no wrong: didst not thou agree with me for a penny?",

    # Mark
    "Mark 9:12": "Elias verily cometh first, and restoreth all things; and how it is written of the Son of man, that he must suffer many things, and be set at nought.",
    "Mark 12:38": "Beware of the scribes, which love to go in long clothing, and love salutations in the marketplaces,",
    "Mark 16:7": None,  # Angel speaking, not Jesus - remove

    # Luke
    "Luke 5:24": "But that ye may know that the Son of man hath power upon earth to forgive sins, (he said unto the sick of the palsy,) I say unto thee, Arise, and take up thy couch, and go into thine house.",
    "Luke 9:14": "Make them sit down by fifties in a company.",
    "Luke 9:23": "If any man will come after me, let him deny himself, and take up his cross daily, and follow me.",
    "Luke 9:33": None,  # Peter speaking, not Jesus - remove
    "Luke 12:22": "Therefore I say unto you, Take no thought for your life, what ye shall eat; neither for the body, what ye shall put on.",
    "Luke 12:54": "When ye see a cloud rise out of the west, straightway ye say, There cometh a shower; and so it is.",
    "Luke 13:20": "Whereunto shall I liken the kingdom of God?",
    "Luke 13:23": None,  # Verse ends with "And he said unto them," - answer is in v24 - remove
    "Luke 15:17": None,  # Prodigal son speaking, not Jesus - remove
    "Luke 16:1": "There was a certain rich man, which had a steward; and the same was accused unto him that he had wasted his goods.",
    "Luke 17:20": "The kingdom of God cometh not with observation:",
    "Luke 17:22": "The days will come, when ye shall desire to see one of the days of the Son of man, and ye shall not see it.",
    "Luke 18:4": None,  # Unjust judge speaking in parable, not Jesus - remove
    "Luke 18:22": "Yet lackest thou one thing: sell all that thou hast, and distribute unto the poor, and thou shalt have treasure in heaven: and come, follow me.",
    "Luke 18:24": "How hardly shall they that have riches enter into the kingdom of God!",
    "Luke 19:19": "Be thou also over five cities.",  # Jesus speaking as the nobleman in parable
    "Luke 19:24": "Take from him the pound, and give it to him that hath ten pounds.",
    "Luke 22:52": "Be ye come out, as against a thief, with swords and staves?",
    "Luke 23:46": "Father, into thy hands I commend my spirit:",

    # John
    "John 6:26": "Verily, verily, I say unto you, Ye seek me, not because ye saw the miracles, but because ye did eat of the loaves, and were filled.",
    "John 6:61": "Doth this offend you?",
    "John 8:10": "Woman, where are those thine accusers? hath no man condemned thee?",
    "John 13:10": "He that is washed needeth not save to wash his feet, but is clean every whit: and ye are clean, but not all.",
    "John 13:12": "Know ye what I have done to you?",
    "John 19:30": "It is finished:",
    "John 21:15": None,  # Mixed dialog (Jesus and Peter) - too complex to mark - remove
    "John 21:23": "If I will that he tarry till I come, what is that to thee?",  # The actual quote

    # Revelation
    "Revelation 21:5": "Behold, I make all things new.",  # God/Christ on throne speaking
}


def main():
    # Load the red letter data
    data_path = Path(__file__).parent.parent / "kjvstudy_org" / "data" / "red_letter_verses.json"

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    verses = data.get("verses", {})

    # Apply manual fixes
    removed = []
    updated = []

    for verse_key, spoken_words in MANUAL_FIXES.items():
        if verse_key in verses:
            if spoken_words is None:
                # Remove entry (not Jesus speaking)
                del verses[verse_key]
                removed.append(verse_key)
            else:
                # Update with correct spoken words
                verses[verse_key] = spoken_words
                updated.append(verse_key)
        else:
            print(f"Warning: {verse_key} not found in data")

    # Save updated data
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Updated {len(updated)} verses")
    print(f"✓ Removed {len(removed)} verses (not Jesus speaking)")
    print(f"\nTotal changes: {len(updated) + len(removed)}")

    print(f"\nRemoved verses:")
    for verse in removed:
        print(f"  - {verse}")

    print(f"\nUpdated verses:")
    for verse in updated[:10]:
        print(f"  - {verse}")
    if len(updated) > 10:
        print(f"  ... and {len(updated) - 10} more")


if __name__ == '__main__':
    main()
