"""
Detailed biographical information for notable biblical figures.
Provides richer context than what's available in the GEDCOM data.
"""

BIOGRAPHIES = {
    "Adam": {
        "summary": "The first human created by God, Adam was formed from the dust of the ground and placed in the Garden of Eden. He named all the animals and was given Eve as his companion. After disobeying God by eating from the tree of knowledge of good and evil, Adam and Eve were expelled from Eden. Despite his fall, Adam is remembered as the father of all humanity.",
        "significance": "Adam represents humanity's original state and fall into sin, establishing the need for redemption that would come through Jesus Christ, often called the 'last Adam'.",
        "key_events": [
            {"age": 0, "event": "Created by God from the dust of the ground", "verse": "Genesis 2:7"},
            {"age": 0, "event": "Placed in the Garden of Eden", "verse": "Genesis 2:15"},
            {"age": 0, "event": "Eve created as his companion", "verse": "Genesis 2:21-22"},
            {"age": 130, "event": "Birth of Seth", "verse": "Genesis 5:3"},
            {"age": 930, "event": "Death", "verse": "Genesis 5:5"}
        ]
    },

    "Noah": {
        "summary": "A righteous man in a corrupt generation, Noah found grace in the eyes of the LORD. When God decided to flood the earth due to humanity's wickedness, Noah was chosen to build an ark to preserve his family and representatives of all animal kinds. After the flood, God established a covenant with Noah, promising never again to destroy the earth by water, signified by the rainbow.",
        "significance": "Noah demonstrates God's mercy in judgment and His faithfulness to preserve a remnant. The flood narrative foreshadows baptism and salvation through Christ.",
        "key_events": [
            {"age": 500, "event": "Birth of Shem, Ham, and Japheth", "verse": "Genesis 5:32"},
            {"age": 600, "event": "The Flood begins", "verse": "Genesis 7:6"},
            {"age": 601, "event": "Leaves the ark", "verse": "Genesis 8:13-19"},
            {"age": 950, "event": "Death", "verse": "Genesis 9:29"}
        ]
    },

    "Abraham": {
        "summary": "Originally named Abram, Abraham was called by God to leave his homeland and journey to Canaan, where God promised to make him into a great nation. Despite his and Sarah's old age, God gave them a son, Isaac, through whom the promise would continue. Abraham demonstrated remarkable faith when willing to sacrifice Isaac at God's command, though God provided a ram instead. He is called the 'father of faith' and the physical ancestor of Israel.",
        "significance": "Abraham is the father of the Hebrew nation and an example of faith for all believers. God's covenant with Abraham established the foundation for Israel and ultimately for the coming of the Messiah.",
        "key_events": [
            {"age": 75, "event": "Called by God to leave Ur", "verse": "Genesis 12:1-4"},
            {"age": 86, "event": "Birth of Ishmael through Hagar", "verse": "Genesis 16:16"},
            {"age": 99, "event": "Covenant of circumcision established", "verse": "Genesis 17:1-14"},
            {"age": 100, "event": "Birth of Isaac", "verse": "Genesis 21:5"},
            {"age": 137, "event": "Death of Sarah", "verse": "Genesis 23:1"},
            {"age": 175, "event": "Death", "verse": "Genesis 25:7"}
        ]
    },

    "Moses": {
        "summary": "Born during a time when Pharaoh ordered all Hebrew male babies to be killed, Moses was hidden by his mother and eventually raised in Pharaoh's household. After killing an Egyptian and fleeing to Midian, God called Moses from a burning bush to lead Israel out of Egyptian bondage. Through Moses, God gave the Ten Commandments and the Law, establishing Israel's covenant relationship with Him. Though he led Israel for forty years in the wilderness, Moses was not permitted to enter the Promised Land.",
        "significance": "Moses is the great lawgiver and prophet who mediated God's covenant with Israel. He prefigures Christ as a prophet, deliverer, and mediator between God and His people.",
        "key_events": [
            {"age": 0, "event": "Born in Egypt during oppression", "verse": "Exodus 2:1-2"},
            {"age": 40, "event": "Fled to Midian after killing an Egyptian", "verse": "Acts 7:23-29"},
            {"age": 80, "event": "Called by God at the burning bush", "verse": "Exodus 3:1-10"},
            {"age": 80, "event": "The Exodus from Egypt", "verse": "Exodus 12:31-42"},
            {"age": 80, "event": "Received the Ten Commandments", "verse": "Exodus 20:1-17"},
            {"age": 120, "event": "Death on Mount Nebo", "verse": "Deuteronomy 34:5-7"}
        ]
    },

    "David": {
        "summary": "The youngest son of Jesse, David was anointed as king while still a shepherd boy. He gained fame by defeating the Philistine giant Goliath and became a skilled warrior and musician in King Saul's court. After Saul's death, David united Israel and established Jerusalem as its capital. Despite his sins (notably with Bathsheba), David was called 'a man after God's own heart' and received God's promise that the Messiah would come from his lineage.",
        "significance": "David established Jerusalem and the monarchy that would culminate in Jesus Christ, the 'Son of David.' His psalms have been the prayer book of God's people for millennia.",
        "key_events": [
            {"age": 15, "event": "Anointed by Samuel as future king", "verse": "1 Samuel 16:13"},
            {"age": 17, "event": "Defeated Goliath", "verse": "1 Samuel 17:49-51"},
            {"age": 30, "event": "Became king of Judah", "verse": "2 Samuel 5:4"},
            {"age": 37, "event": "Became king over all Israel", "verse": "2 Samuel 5:4-5"},
            {"age": 37, "event": "Conquered Jerusalem", "verse": "2 Samuel 5:6-9"},
            {"age": 50, "event": "Sin with Bathsheba", "verse": "2 Samuel 11"},
            {"age": 70, "event": "Death", "verse": "1 Kings 2:10-11"}
        ]
    },

    "Jesus": {
        "summary": "Born of the Virgin Mary in Bethlehem, Jesus is the promised Messiah and the Son of God. He began His public ministry around age 30, teaching about the Kingdom of God, performing miracles, and calling disciples. He was crucified under Pontius Pilate as an atonement for sin, rose from the dead on the third day, and ascended to heaven forty days later. Jesus is both fully God and fully man, the perfect sacrifice for humanity's redemption.",
        "significance": "Jesus Christ is the central figure of all Scripture and human history. He is the promised seed who crushes the serpent's head, the fulfillment of all Old Testament prophecy, and the only way of salvation.",
        "key_events": [
            {"age": 0, "event": "Born in Bethlehem", "verse": "Luke 2:7"},
            {"age": 12, "event": "Taught in the temple", "verse": "Luke 2:42-52"},
            {"age": 30, "event": "Baptized by John", "verse": "Luke 3:21-23"},
            {"age": 30, "event": "Tempted in the wilderness", "verse": "Matthew 4:1-11"},
            {"age": 30, "event": "Began public ministry", "verse": "Luke 4:14-21"},
            {"age": 33, "event": "Transfiguration", "verse": "Matthew 17:1-9"},
            {"age": 33, "event": "Crucifixion and resurrection", "verse": "Matthew 27-28"},
            {"age": 33, "event": "Ascension", "verse": "Acts 1:9-11"}
        ]
    },

    "Eve": {
        "summary": "The first woman, created by God from Adam's rib to be his companion and helper. Eve was deceived by the serpent and ate the forbidden fruit, then gave some to Adam. Despite her role in the fall, Eve is the mother of all living and received the promise that her seed would one day crush the serpent's head.",
        "significance": "Eve represents humanity's susceptibility to temptation but also the promise of redemption through her offspring, ultimately fulfilled in Christ.",
        "key_events": [
            {"age": 0, "event": "Created from Adam's rib", "verse": "Genesis 2:21-22"},
            {"age": 0, "event": "Tempted by the serpent", "verse": "Genesis 3:1-6"},
            {"age": 0, "event": "Expelled from Eden", "verse": "Genesis 3:23-24"},
            {"age": 130, "event": "Birth of Seth", "verse": "Genesis 4:25"}
        ]
    },

    "Abraham's wife Sarah": {
        "summary": "Originally named Sarai, Sarah was Abraham's wife who accompanied him from Ur to Canaan. Despite her barrenness and old age, God promised she would bear a son. At age 90, she gave birth to Isaac, the child of promise. Sarah is remembered for her faith and is mentioned in the New Testament as an example for godly women.",
        "significance": "Sarah's miraculous conception of Isaac demonstrates God's power and faithfulness to His promises, even when circumstances seem impossible.",
        "key_events": [
            {"age": 65, "event": "Left Ur with Abraham", "verse": "Genesis 12:4-5"},
            {"age": 90, "event": "God promised her a son", "verse": "Genesis 17:15-19"},
            {"age": 90, "event": "Birth of Isaac", "verse": "Genesis 21:1-7"},
            {"age": 127, "event": "Death", "verse": "Genesis 23:1-2"}
        ]
    },

    "Isaac": {
        "summary": "The son of promise born to Abraham and Sarah in their old age. Isaac was nearly sacrificed by his father in the ultimate test of faith but was spared when God provided a ram. He married Rebekah and fathered twin sons, Esau and Jacob. Isaac was more passive than his father but faithfully continued the covenant line.",
        "significance": "Isaac represents the fulfillment of God's promise and prefigures Christ as the obedient son offered in sacrifice.",
        "key_events": [
            {"age": 0, "event": "Born to Abraham and Sarah", "verse": "Genesis 21:1-3"},
            {"age": 37, "event": "Offered as a sacrifice (averted)", "verse": "Genesis 22:1-19"},
            {"age": 40, "event": "Married Rebekah", "verse": "Genesis 25:20"},
            {"age": 60, "event": "Birth of Esau and Jacob", "verse": "Genesis 25:26"},
            {"age": 180, "event": "Death", "verse": "Genesis 35:28-29"}
        ]
    },

    "Jacob": {
        "summary": "The younger twin son of Isaac, Jacob obtained Esau's birthright and stole his blessing through deception. Fleeing his brother's anger, Jacob encountered God at Bethel and later wrestled with God, receiving the name Israel. He fathered twelve sons who became the twelve tribes of Israel. Despite his flawed character, God chose Jacob to continue the covenant line.",
        "significance": "Jacob (Israel) is the father of the twelve tribes and represents God's electing grace despite human unworthiness.",
        "key_events": [
            {"age": 0, "event": "Born grasping Esau's heel", "verse": "Genesis 25:24-26"},
            {"age": 77, "event": "Obtained Esau's blessing", "verse": "Genesis 27:1-40"},
            {"age": 77, "event": "Vision at Bethel", "verse": "Genesis 28:10-22"},
            {"age": 84, "event": "Married Leah and Rachel", "verse": "Genesis 29:21-30"},
            {"age": 97, "event": "Wrestled with God, renamed Israel", "verse": "Genesis 32:24-32"},
            {"age": 130, "event": "Moved to Egypt", "verse": "Genesis 47:9"},
            {"age": 147, "event": "Death", "verse": "Genesis 47:28"}
        ]
    },

    "Joseph": {
        "summary": "The favored son of Jacob, Joseph was sold into slavery by his jealous brothers but rose to become second-in-command in Egypt through God's providence. His interpretation of Pharaoh's dreams saved Egypt and his own family from famine. Joseph's forgiveness of his brothers demonstrates remarkable grace and faith in God's sovereign plan.",
        "significance": "Joseph's life prefigures Christ in his suffering, exaltation, and role as savior of his people.",
        "key_events": [
            {"age": 17, "event": "Sold into slavery by his brothers", "verse": "Genesis 37:28"},
            {"age": 28, "event": "Imprisoned in Egypt", "verse": "Genesis 39:20"},
            {"age": 30, "event": "Became second-in-command of Egypt", "verse": "Genesis 41:46"},
            {"age": 39, "event": "Reunited with his brothers", "verse": "Genesis 45:1-15"},
            {"age": 110, "event": "Death", "verse": "Genesis 50:26"}
        ]
    },

    "Solomon": {
        "summary": "The son of David and Bathsheba, Solomon became Israel's third king and was granted great wisdom by God. He built the magnificent temple in Jerusalem and authored much of Proverbs, Ecclesiastes, and Song of Solomon. Despite his wisdom, Solomon's many foreign wives led him into idolatry in his later years, setting the stage for the kingdom's division.",
        "significance": "Solomon's wisdom and the temple he built point to Christ, the wisdom of God and the true temple.",
        "key_events": [
            {"age": 20, "event": "Became king of Israel", "verse": "1 Kings 2:12"},
            {"age": 20, "event": "Asked God for wisdom", "verse": "1 Kings 3:5-14"},
            {"age": 24, "event": "Began building the temple", "verse": "1 Kings 6:1"},
            {"age": 31, "event": "Dedicated the temple", "verse": "1 Kings 8:1-66"},
            {"age": 60, "event": "Death", "verse": "1 Kings 11:42-43"}
        ]
    }
}


def get_biography(person_name: str) -> dict:
    """
    Get biographical information for a biblical figure.

    Args:
        person_name: Name of the person (e.g., "Abraham", "David")

    Returns:
        Dictionary with biography info, or None if not found
    """
    return BIOGRAPHIES.get(person_name)


def has_biography(person_name: str) -> bool:
    """Check if a person has detailed biographical information."""
    return person_name in BIOGRAPHIES
