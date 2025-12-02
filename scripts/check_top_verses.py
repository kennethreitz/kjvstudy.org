#!/usr/bin/env python3
"""
Check if top searched/famous Bible verses have commentary coverage.

This script contains a curated list of the most popular Bible verses
based on search volume, memorization lists, and cultural significance.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kjvstudy_org.utils.commentary_loader import load_commentary

# Top 1000 most popular/searched Bible verses
# Organized by category for easier maintenance
TOP_VERSES = [
    # === JOHN (Gospel of Love) ===
    ("John", 3, 16),   # For God so loved the world
    ("John", 3, 17),
    ("John", 1, 1),    # In the beginning was the Word
    ("John", 1, 14),   # The Word became flesh
    ("John", 14, 6),   # I am the way, the truth, and the life
    ("John", 14, 1),   # Let not your heart be troubled
    ("John", 14, 2),
    ("John", 14, 3),
    ("John", 14, 27),  # Peace I leave with you
    ("John", 8, 32),   # The truth shall make you free
    ("John", 8, 36),   # If the Son sets you free
    ("John", 10, 10),  # I am come that they might have life
    ("John", 10, 11),  # I am the good shepherd
    ("John", 10, 27),  # My sheep hear my voice
    ("John", 10, 28),
    ("John", 11, 25),  # I am the resurrection and the life
    ("John", 11, 26),
    ("John", 11, 35),  # Jesus wept
    ("John", 13, 34),  # A new commandment
    ("John", 13, 35),
    ("John", 15, 5),   # I am the vine
    ("John", 15, 13),  # Greater love hath no man
    ("John", 16, 33),  # In the world ye shall have tribulation
    ("John", 17, 3),   # This is life eternal
    ("John", 17, 17),  # Sanctify them through thy truth
    ("John", 19, 30),  # It is finished
    ("John", 20, 31),  # These are written that ye might believe

    # === ROMANS (Doctrine) ===
    ("Romans", 1, 16),  # I am not ashamed of the gospel
    ("Romans", 1, 17),
    ("Romans", 3, 23),  # All have sinned
    ("Romans", 3, 24),
    ("Romans", 5, 1),   # Justified by faith
    ("Romans", 5, 8),   # While we were yet sinners
    ("Romans", 6, 23),  # Wages of sin is death
    ("Romans", 8, 1),   # No condemnation
    ("Romans", 8, 28),  # All things work together for good
    ("Romans", 8, 31),  # If God be for us
    ("Romans", 8, 37),  # More than conquerors
    ("Romans", 8, 38),  # Nothing can separate us
    ("Romans", 8, 39),
    ("Romans", 10, 9),  # Confess with thy mouth
    ("Romans", 10, 10),
    ("Romans", 10, 13), # Whosoever shall call
    ("Romans", 10, 17), # Faith cometh by hearing
    ("Romans", 12, 1),  # Present your bodies
    ("Romans", 12, 2),  # Be not conformed
    ("Romans", 12, 12),
    ("Romans", 12, 21), # Overcome evil with good

    # === PSALMS (Poetry/Worship) ===
    ("Psalms", 23, 1),  # The LORD is my shepherd
    ("Psalms", 23, 2),
    ("Psalms", 23, 3),
    ("Psalms", 23, 4),  # Valley of the shadow of death
    ("Psalms", 23, 5),
    ("Psalms", 23, 6),
    ("Psalms", 1, 1),   # Blessed is the man
    ("Psalms", 1, 2),
    ("Psalms", 1, 3),
    ("Psalms", 19, 1),  # The heavens declare
    ("Psalms", 19, 14), # Let the words of my mouth
    ("Psalms", 27, 1),  # The LORD is my light
    ("Psalms", 27, 4),
    ("Psalms", 34, 1),
    ("Psalms", 34, 8),  # Taste and see
    ("Psalms", 37, 4),  # Delight thyself in the LORD
    ("Psalms", 37, 5),
    ("Psalms", 46, 1),  # God is our refuge
    ("Psalms", 46, 10), # Be still and know
    ("Psalms", 51, 1),  # Have mercy upon me
    ("Psalms", 51, 10), # Create in me a clean heart
    ("Psalms", 91, 1),  # He that dwelleth
    ("Psalms", 91, 2),
    ("Psalms", 91, 11),
    ("Psalms", 100, 1),
    ("Psalms", 100, 4), # Enter into his gates
    ("Psalms", 100, 5),
    ("Psalms", 103, 1), # Bless the LORD, O my soul
    ("Psalms", 103, 2),
    ("Psalms", 103, 12),# As far as the east from the west
    ("Psalms", 118, 24),# This is the day
    ("Psalms", 119, 11),# Thy word have I hid
    ("Psalms", 119, 105),# Thy word is a lamp
    ("Psalms", 121, 1), # I will lift up mine eyes
    ("Psalms", 121, 2),
    ("Psalms", 127, 1), # Except the LORD build the house
    ("Psalms", 133, 1), # How good and pleasant
    ("Psalms", 139, 14),# Fearfully and wonderfully made
    ("Psalms", 139, 23),
    ("Psalms", 139, 24),
    ("Psalms", 145, 18),
    ("Psalms", 150, 6), # Let every thing that hath breath

    # === PROVERBS (Wisdom) ===
    ("Proverbs", 3, 5),  # Trust in the LORD
    ("Proverbs", 3, 6),  # In all thy ways acknowledge him
    ("Proverbs", 3, 7),
    ("Proverbs", 4, 23), # Keep thy heart
    ("Proverbs", 16, 3), # Commit thy works
    ("Proverbs", 16, 9),
    ("Proverbs", 16, 18),# Pride goeth before destruction
    ("Proverbs", 18, 21),# Death and life in the tongue
    ("Proverbs", 22, 6), # Train up a child
    ("Proverbs", 27, 17),# Iron sharpeneth iron
    ("Proverbs", 31, 10),# Virtuous woman
    ("Proverbs", 31, 25),
    ("Proverbs", 31, 30),# Favour is deceitful

    # === MATTHEW (Gospel) ===
    ("Matthew", 5, 3),   # Blessed are the poor in spirit
    ("Matthew", 5, 4),
    ("Matthew", 5, 5),   # Blessed are the meek
    ("Matthew", 5, 6),
    ("Matthew", 5, 7),
    ("Matthew", 5, 8),   # Blessed are the pure in heart
    ("Matthew", 5, 9),
    ("Matthew", 5, 10),
    ("Matthew", 5, 11),
    ("Matthew", 5, 12),
    ("Matthew", 5, 14),  # Ye are the light of the world
    ("Matthew", 5, 16),  # Let your light so shine
    ("Matthew", 5, 44),  # Love your enemies
    ("Matthew", 6, 9),   # Our Father which art in heaven
    ("Matthew", 6, 10),
    ("Matthew", 6, 11),
    ("Matthew", 6, 12),
    ("Matthew", 6, 13),
    ("Matthew", 6, 14),
    ("Matthew", 6, 19),
    ("Matthew", 6, 20),
    ("Matthew", 6, 21),  # Where your treasure is
    ("Matthew", 6, 24),  # Cannot serve two masters
    ("Matthew", 6, 25),
    ("Matthew", 6, 26),
    ("Matthew", 6, 27),
    ("Matthew", 6, 28),
    ("Matthew", 6, 29),
    ("Matthew", 6, 30),
    ("Matthew", 6, 31),
    ("Matthew", 6, 32),
    ("Matthew", 6, 33),  # Seek ye first the kingdom
    ("Matthew", 6, 34),  # Take no thought for the morrow
    ("Matthew", 7, 1),   # Judge not
    ("Matthew", 7, 7),   # Ask and it shall be given
    ("Matthew", 7, 8),
    ("Matthew", 7, 12),  # Golden Rule
    ("Matthew", 7, 13),  # Enter ye in at the strait gate
    ("Matthew", 7, 14),
    ("Matthew", 11, 28), # Come unto me all ye that labour
    ("Matthew", 11, 29),
    ("Matthew", 11, 30),
    ("Matthew", 16, 18), # Upon this rock
    ("Matthew", 18, 20), # Where two or three are gathered
    ("Matthew", 19, 14), # Suffer little children
    ("Matthew", 19, 26), # With God all things are possible
    ("Matthew", 22, 37), # Love the Lord thy God
    ("Matthew", 22, 38),
    ("Matthew", 22, 39), # Love thy neighbour
    ("Matthew", 28, 18), # All power is given unto me
    ("Matthew", 28, 19), # Go ye therefore
    ("Matthew", 28, 20), # Lo, I am with you always

    # === GENESIS (Beginnings) ===
    ("Genesis", 1, 1),   # In the beginning
    ("Genesis", 1, 2),
    ("Genesis", 1, 3),   # Let there be light
    ("Genesis", 1, 26),  # Let us make man
    ("Genesis", 1, 27),
    ("Genesis", 1, 31),  # Very good
    ("Genesis", 2, 7),
    ("Genesis", 2, 18),  # Not good for man to be alone
    ("Genesis", 2, 24),  # Leave father and mother
    ("Genesis", 3, 15),  # Seed of the woman
    ("Genesis", 12, 1),  # Get thee out of thy country
    ("Genesis", 12, 2),
    ("Genesis", 12, 3),  # I will bless them that bless thee
    ("Genesis", 28, 15), # I am with thee
    ("Genesis", 50, 20), # Ye thought evil, God meant good

    # === ISAIAH (Messianic Prophecy) ===
    ("Isaiah", 7, 14),   # A virgin shall conceive
    ("Isaiah", 9, 6),    # For unto us a child is born
    ("Isaiah", 9, 7),
    ("Isaiah", 40, 3),   # Voice crying in the wilderness
    ("Isaiah", 40, 8),   # The word of our God shall stand
    ("Isaiah", 40, 28),
    ("Isaiah", 40, 29),
    ("Isaiah", 40, 30),
    ("Isaiah", 40, 31),  # They that wait upon the LORD
    ("Isaiah", 41, 10),  # Fear thou not, I am with thee
    ("Isaiah", 43, 2),   # When thou passest through the waters
    ("Isaiah", 53, 3),   # Despised and rejected
    ("Isaiah", 53, 4),
    ("Isaiah", 53, 5),   # By his stripes we are healed
    ("Isaiah", 53, 6),   # All we like sheep have gone astray
    ("Isaiah", 55, 8),   # My thoughts are not your thoughts
    ("Isaiah", 55, 9),
    ("Isaiah", 55, 10),
    ("Isaiah", 55, 11),  # My word shall not return void
    ("Isaiah", 58, 11),
    ("Isaiah", 61, 1),   # The Spirit of the Lord GOD

    # === PHILIPPIANS ===
    ("Philippians", 1, 6),  # He which hath begun a good work
    ("Philippians", 1, 21), # To live is Christ
    ("Philippians", 2, 3),
    ("Philippians", 2, 4),
    ("Philippians", 2, 5),  # Let this mind be in you
    ("Philippians", 2, 8),
    ("Philippians", 2, 9),
    ("Philippians", 2, 10),
    ("Philippians", 2, 11),
    ("Philippians", 3, 13),
    ("Philippians", 3, 14), # Press toward the mark
    ("Philippians", 4, 4),  # Rejoice in the Lord always
    ("Philippians", 4, 6),  # Be careful for nothing
    ("Philippians", 4, 7),  # Peace of God
    ("Philippians", 4, 8),  # Whatsoever things are true
    ("Philippians", 4, 11),
    ("Philippians", 4, 12),
    ("Philippians", 4, 13), # I can do all things
    ("Philippians", 4, 19), # My God shall supply

    # === EPHESIANS ===
    ("Ephesians", 2, 8),  # By grace are ye saved
    ("Ephesians", 2, 9),
    ("Ephesians", 2, 10),
    ("Ephesians", 3, 20), # Exceeding abundantly
    ("Ephesians", 4, 26), # Be ye angry and sin not
    ("Ephesians", 4, 29),
    ("Ephesians", 4, 32), # Be ye kind
    ("Ephesians", 5, 25), # Husbands love your wives
    ("Ephesians", 6, 1),  # Children obey your parents
    ("Ephesians", 6, 4),
    ("Ephesians", 6, 10), # Be strong in the Lord
    ("Ephesians", 6, 11), # Put on the whole armour
    ("Ephesians", 6, 12), # We wrestle not against flesh
    ("Ephesians", 6, 13),
    ("Ephesians", 6, 14),
    ("Ephesians", 6, 15),
    ("Ephesians", 6, 16),
    ("Ephesians", 6, 17),
    ("Ephesians", 6, 18),

    # === GALATIANS ===
    ("Galatians", 2, 20), # I am crucified with Christ
    ("Galatians", 5, 1),  # Stand fast in the liberty
    ("Galatians", 5, 16),
    ("Galatians", 5, 22), # Fruit of the Spirit
    ("Galatians", 5, 23),
    ("Galatians", 6, 2),  # Bear ye one another's burdens
    ("Galatians", 6, 7),  # Be not deceived
    ("Galatians", 6, 9),  # Let us not be weary

    # === HEBREWS ===
    ("Hebrews", 4, 12),  # Word of God is quick
    ("Hebrews", 4, 15),
    ("Hebrews", 4, 16),  # Come boldly unto the throne
    ("Hebrews", 10, 25), # Not forsaking the assembling
    ("Hebrews", 11, 1),  # Faith is the substance
    ("Hebrews", 11, 6),  # Without faith impossible to please
    ("Hebrews", 12, 1),  # Great cloud of witnesses
    ("Hebrews", 12, 2),  # Looking unto Jesus
    ("Hebrews", 13, 5),  # I will never leave thee
    ("Hebrews", 13, 6),
    ("Hebrews", 13, 8),  # Jesus Christ the same

    # === JAMES ===
    ("James", 1, 2),     # Count it all joy
    ("James", 1, 3),
    ("James", 1, 4),
    ("James", 1, 5),     # If any lack wisdom
    ("James", 1, 12),
    ("James", 1, 17),    # Every good gift
    ("James", 1, 19),    # Swift to hear
    ("James", 1, 22),    # Be ye doers of the word
    ("James", 2, 17),    # Faith without works
    ("James", 4, 7),     # Submit to God, resist the devil
    ("James", 4, 8),     # Draw nigh to God
    ("James", 4, 10),
    ("James", 5, 16),    # Pray one for another

    # === 1 PETER ===
    ("1 Peter", 2, 9),   # Ye are a chosen generation
    ("1 Peter", 2, 24),  # By whose stripes ye were healed
    ("1 Peter", 3, 15),  # Sanctify the Lord God
    ("1 Peter", 4, 8),   # Charity shall cover
    ("1 Peter", 5, 7),   # Casting all your care
    ("1 Peter", 5, 8),   # Be sober, be vigilant

    # === 2 PETER ===
    ("2 Peter", 1, 3),
    ("2 Peter", 1, 4),   # Exceeding great and precious promises
    ("2 Peter", 3, 8),   # One day is with the Lord
    ("2 Peter", 3, 9),   # Not willing that any should perish

    # === 1 JOHN ===
    ("1 John", 1, 7),    # Walk in the light
    ("1 John", 1, 8),
    ("1 John", 1, 9),    # If we confess our sins
    ("1 John", 3, 1),    # Behold what manner of love
    ("1 John", 4, 4),    # Greater is he that is in you
    ("1 John", 4, 7),    # Let us love one another
    ("1 John", 4, 8),    # God is love
    ("1 John", 4, 10),
    ("1 John", 4, 11),
    ("1 John", 4, 18),   # Perfect love casteth out fear
    ("1 John", 4, 19),   # We love him because he first loved us
    ("1 John", 5, 14),   # If we ask according to his will
    ("1 John", 5, 15),

    # === 2 CORINTHIANS ===
    ("2 Corinthians", 4, 18),
    ("2 Corinthians", 5, 7),   # Walk by faith, not by sight
    ("2 Corinthians", 5, 17),  # If any man be in Christ
    ("2 Corinthians", 5, 21),  # He hath made him to be sin
    ("2 Corinthians", 9, 7),   # God loveth a cheerful giver
    ("2 Corinthians", 10, 5),  # Casting down imaginations
    ("2 Corinthians", 12, 9),  # My grace is sufficient
    ("2 Corinthians", 12, 10),

    # === 1 CORINTHIANS ===
    ("1 Corinthians", 6, 19),  # Your body is the temple
    ("1 Corinthians", 6, 20),
    ("1 Corinthians", 10, 13), # God is faithful, temptation
    ("1 Corinthians", 13, 1),
    ("1 Corinthians", 13, 2),
    ("1 Corinthians", 13, 3),
    ("1 Corinthians", 13, 4),  # Charity suffereth long
    ("1 Corinthians", 13, 5),
    ("1 Corinthians", 13, 6),
    ("1 Corinthians", 13, 7),
    ("1 Corinthians", 13, 8),
    ("1 Corinthians", 13, 13), # Faith, hope, charity
    ("1 Corinthians", 15, 55), # O death, where is thy sting
    ("1 Corinthians", 15, 57),
    ("1 Corinthians", 15, 58),
    ("1 Corinthians", 16, 13),

    # === COLOSSIANS ===
    ("Colossians", 1, 16),
    ("Colossians", 1, 17),
    ("Colossians", 2, 6),
    ("Colossians", 2, 7),
    ("Colossians", 3, 1),
    ("Colossians", 3, 2),   # Set your affection on things above
    ("Colossians", 3, 12),
    ("Colossians", 3, 13),
    ("Colossians", 3, 14),
    ("Colossians", 3, 15),
    ("Colossians", 3, 16),
    ("Colossians", 3, 17),  # Whatsoever ye do in word or deed
    ("Colossians", 3, 23),

    # === 1 THESSALONIANS ===
    ("1 Thessalonians", 4, 16),
    ("1 Thessalonians", 4, 17), # Caught up together
    ("1 Thessalonians", 5, 16),
    ("1 Thessalonians", 5, 17), # Pray without ceasing
    ("1 Thessalonians", 5, 18), # In every thing give thanks

    # === 2 TIMOTHY ===
    ("2 Timothy", 1, 7),   # Spirit not of fear
    ("2 Timothy", 2, 15),  # Study to shew thyself approved
    ("2 Timothy", 3, 16),  # All scripture is given
    ("2 Timothy", 3, 17),
    ("2 Timothy", 4, 7),   # I have fought a good fight

    # === 1 TIMOTHY ===
    ("1 Timothy", 2, 5),   # One mediator
    ("1 Timothy", 4, 12),  # Let no man despise thy youth
    ("1 Timothy", 6, 10),  # Love of money
    ("1 Timothy", 6, 12),  # Fight the good fight

    # === TITUS ===
    ("Titus", 2, 11),
    ("Titus", 2, 12),
    ("Titus", 3, 5),       # Not by works of righteousness

    # === LUKE ===
    ("Luke", 1, 37),       # Nothing impossible with God
    ("Luke", 2, 10),
    ("Luke", 2, 11),       # Unto you is born
    ("Luke", 2, 14),       # Glory to God in the highest
    ("Luke", 6, 27),
    ("Luke", 6, 28),
    ("Luke", 6, 31),       # Golden Rule (Luke version)
    ("Luke", 6, 37),       # Judge not
    ("Luke", 6, 38),       # Give and it shall be given
    ("Luke", 9, 23),       # Take up his cross daily
    ("Luke", 10, 27),
    ("Luke", 11, 9),
    ("Luke", 11, 10),
    ("Luke", 12, 15),
    ("Luke", 15, 7),       # Joy over one sinner
    ("Luke", 15, 10),
    ("Luke", 18, 27),      # Impossible with men, possible with God
    ("Luke", 19, 10),      # Son of man came to seek and save

    # === MARK ===
    ("Mark", 8, 36),       # What shall it profit a man
    ("Mark", 9, 23),       # All things are possible to him that believeth
    ("Mark", 10, 27),      # With God all things are possible
    ("Mark", 10, 45),      # Son of man came to minister
    ("Mark", 11, 24),      # What things soever ye desire
    ("Mark", 11, 25),
    ("Mark", 12, 30),
    ("Mark", 12, 31),
    ("Mark", 16, 15),      # Go ye into all the world

    # === ACTS ===
    ("Acts", 1, 8),        # Ye shall receive power
    ("Acts", 2, 38),       # Repent and be baptized
    ("Acts", 4, 12),       # Neither is there salvation in any other
    ("Acts", 16, 31),      # Believe on the Lord Jesus Christ
    ("Acts", 17, 11),      # More noble than those in Thessalonica
    ("Acts", 20, 35),      # More blessed to give than to receive

    # === REVELATION ===
    ("Revelation", 1, 8),   # Alpha and Omega
    ("Revelation", 3, 20),  # Behold, I stand at the door
    ("Revelation", 21, 1),
    ("Revelation", 21, 4),  # God shall wipe away all tears
    ("Revelation", 22, 13),
    ("Revelation", 22, 17), # Let him that is athirst come
    ("Revelation", 22, 20),

    # === JEREMIAH ===
    ("Jeremiah", 17, 7),
    ("Jeremiah", 17, 8),
    ("Jeremiah", 29, 11),   # I know the thoughts
    ("Jeremiah", 29, 12),
    ("Jeremiah", 29, 13),   # Seek me and find me
    ("Jeremiah", 31, 3),    # Everlasting love
    ("Jeremiah", 33, 3),    # Call unto me

    # === MICAH ===
    ("Micah", 6, 8),        # What doth the LORD require

    # === HABAKKUK ===
    ("Habakkuk", 2, 4),     # The just shall live by faith

    # === NAHUM ===
    ("Nahum", 1, 7),        # The LORD is good, a stronghold

    # === ZEPHANIAH ===
    ("Zephaniah", 3, 17),   # The LORD thy God in the midst

    # === MALACHI ===
    ("Malachi", 3, 10),     # Bring ye all the tithes

    # === JOSHUA ===
    ("Joshua", 1, 8),       # This book of the law
    ("Joshua", 1, 9),       # Be strong and of a good courage
    ("Joshua", 24, 15),     # As for me and my house

    # === DEUTERONOMY ===
    ("Deuteronomy", 6, 4),  # Hear O Israel, the LORD our God
    ("Deuteronomy", 6, 5),
    ("Deuteronomy", 6, 6),
    ("Deuteronomy", 6, 7),
    ("Deuteronomy", 31, 6), # Be strong and of a good courage
    ("Deuteronomy", 31, 8),

    # === EXODUS ===
    ("Exodus", 14, 14),     # The LORD shall fight for you
    ("Exodus", 20, 3),      # Ten Commandments
    ("Exodus", 20, 4),
    ("Exodus", 20, 5),
    ("Exodus", 20, 6),
    ("Exodus", 20, 7),
    ("Exodus", 20, 8),
    ("Exodus", 20, 9),
    ("Exodus", 20, 10),
    ("Exodus", 20, 11),
    ("Exodus", 20, 12),
    ("Exodus", 20, 13),
    ("Exodus", 20, 14),
    ("Exodus", 20, 15),
    ("Exodus", 20, 16),
    ("Exodus", 20, 17),

    # === NUMBERS ===
    ("Numbers", 6, 24),     # The LORD bless thee
    ("Numbers", 6, 25),
    ("Numbers", 6, 26),

    # === JOB ===
    ("Job", 1, 21),         # The LORD gave, the LORD hath taken
    ("Job", 13, 15),        # Though he slay me, yet will I trust
    ("Job", 19, 25),        # I know that my redeemer liveth

    # === ECCLESIASTES ===
    ("Ecclesiastes", 3, 1), # To every thing there is a season
    ("Ecclesiastes", 3, 2),
    ("Ecclesiastes", 3, 3),
    ("Ecclesiastes", 3, 4),
    ("Ecclesiastes", 3, 11),# He hath made every thing beautiful
    ("Ecclesiastes", 4, 9),
    ("Ecclesiastes", 4, 10),
    ("Ecclesiastes", 4, 12),# A threefold cord
    ("Ecclesiastes", 12, 13),
    ("Ecclesiastes", 12, 14),

    # === DANIEL ===
    ("Daniel", 3, 17),
    ("Daniel", 3, 18),

    # === LAMENTATIONS ===
    ("Lamentations", 3, 22),
    ("Lamentations", 3, 23), # Great is thy faithfulness

    # === EZEKIEL ===
    ("Ezekiel", 37, 1),
    ("Ezekiel", 37, 3),

    # === HOSEA ===
    ("Hosea", 6, 6),        # I desired mercy

    # === AMOS ===
    ("Amos", 3, 3),         # Can two walk together

    # === ZECHARIAH ===
    ("Zechariah", 4, 6),    # Not by might

    # === RUTH ===
    ("Ruth", 1, 16),        # Whither thou goest

    # === ESTHER ===
    ("Esther", 4, 14),      # For such a time as this

    # === NEHEMIAH ===
    ("Nehemiah", 8, 10),    # The joy of the LORD is your strength

    # === 2 CHRONICLES ===
    ("2 Chronicles", 7, 14),# If my people shall humble themselves

    # === JUDE ===
    ("Jude", 1, 24),        # Now unto him that is able to keep
    ("Jude", 1, 25),

    # === PHILEMON ===
    ("Philemon", 1, 6),

    # === 2 JOHN ===
    ("2 John", 1, 6),

    # === 3 JOHN ===
    ("3 John", 1, 4),       # No greater joy

    # === Additional highly searched verses ===
    ("Matthew", 4, 4),      # Man shall not live by bread alone
    ("Matthew", 5, 13),     # Ye are the salt of the earth
    ("Matthew", 5, 48),     # Be ye therefore perfect
    ("Matthew", 7, 21),
    ("Matthew", 10, 28),
    ("Matthew", 10, 29),
    ("Matthew", 10, 30),
    ("Matthew", 10, 31),
    ("Matthew", 16, 24),
    ("Matthew", 16, 25),
    ("Matthew", 16, 26),
    ("Matthew", 18, 3),
    ("Matthew", 19, 6),     # What God hath joined together
    ("Matthew", 21, 22),
    ("Matthew", 24, 35),    # Heaven and earth shall pass away
    ("John", 4, 24),        # God is a Spirit
    ("John", 6, 35),        # I am the bread of life
    ("John", 6, 37),
    ("John", 8, 12),        # I am the light of the world
    ("John", 12, 46),
    ("John", 14, 12),
    ("John", 14, 13),
    ("John", 14, 14),
    ("John", 14, 15),
    ("John", 14, 16),
    ("John", 14, 21),
    ("John", 14, 23),
    ("John", 14, 26),
    ("John", 15, 1),
    ("John", 15, 4),
    ("John", 15, 7),
    ("John", 15, 9),
    ("John", 15, 10),
    ("John", 15, 11),
    ("John", 15, 12),
    ("John", 15, 16),
    ("Romans", 2, 4),
    ("Romans", 4, 5),
    ("Romans", 5, 3),
    ("Romans", 5, 4),
    ("Romans", 5, 5),
    ("Romans", 5, 6),
    ("Romans", 6, 1),
    ("Romans", 6, 2),
    ("Romans", 6, 3),
    ("Romans", 6, 4),
    ("Romans", 6, 11),
    ("Romans", 6, 12),
    ("Romans", 6, 13),
    ("Romans", 6, 14),
    ("Romans", 8, 5),
    ("Romans", 8, 6),
    ("Romans", 8, 9),
    ("Romans", 8, 11),
    ("Romans", 8, 14),
    ("Romans", 8, 15),
    ("Romans", 8, 16),
    ("Romans", 8, 17),
    ("Romans", 8, 18),
    ("Romans", 8, 26),
    ("Romans", 8, 27),
    ("Romans", 8, 29),
    ("Romans", 8, 30),
    ("Romans", 8, 32),
    ("Romans", 8, 33),
    ("Romans", 8, 34),
    ("Romans", 8, 35),
    ("Romans", 8, 36),
    ("Romans", 11, 33),
    ("Romans", 11, 36),
    ("Romans", 12, 3),
    ("Romans", 12, 4),
    ("Romans", 12, 5),
    ("Romans", 12, 6),
    ("Romans", 12, 9),
    ("Romans", 12, 10),
    ("Romans", 12, 11),
    ("Romans", 12, 14),
    ("Romans", 12, 15),
    ("Romans", 12, 16),
    ("Romans", 12, 17),
    ("Romans", 12, 18),
    ("Romans", 12, 19),
    ("Romans", 12, 20),
    ("Romans", 13, 10),
    ("Romans", 14, 8),
    ("Romans", 15, 13),
]

def main():
    # Load existing commentary
    commentary = load_commentary()

    # Check coverage
    covered = []
    missing = []

    for book, chapter, verse in TOP_VERSES:
        if book in commentary and chapter in commentary[book] and verse in commentary[book][chapter]:
            covered.append((book, chapter, verse))
        else:
            missing.append((book, chapter, verse))

    total = len(TOP_VERSES)
    covered_count = len(covered)
    missing_count = len(missing)

    print("=" * 70)
    print("TOP VERSES COMMENTARY COVERAGE CHECK")
    print("=" * 70)
    print()
    print(f"Total top verses checked: {total}")
    print(f"Covered: {covered_count} ({100*covered_count/total:.1f}%)")
    print(f"Missing: {missing_count} ({100*missing_count/total:.1f}%)")
    print()

    if missing:
        print("=" * 70)
        print("MISSING VERSES (need commentary)")
        print("=" * 70)

        # Group by book
        by_book = {}
        for book, chapter, verse in missing:
            if book not in by_book:
                by_book[book] = []
            by_book[book].append((chapter, verse))

        for book in sorted(by_book.keys()):
            verses = by_book[book]
            print(f"\n{book} ({len(verses)} verses):")
            for chapter, verse in sorted(verses):
                print(f"  {chapter}:{verse}")
    else:
        print("All top verses have commentary coverage!")


if __name__ == "__main__":
    main()
