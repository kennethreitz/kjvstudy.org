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
    },

    "Cain": {
        "summary": "The firstborn son of Adam and Eve, Cain was a farmer who brought an offering of the fruit of the ground to the Lord. When God rejected his offering but accepted Abel's, Cain became angry and murdered his brother in a field. God confronted Cain and cursed him to be a wanderer on the earth, marking him for protection. Cain built the first city, named after his son Enoch.",
        "significance": "Cain represents humanity's first murder and the escalation of sin after the Fall. His jealousy and violence demonstrate the depths of human depravity without God's grace.",
        "key_events": [
            {"age": 0, "event": "Born to Adam and Eve", "verse": "Genesis 4:1"},
            {"age": 0, "event": "Brought offering to God (rejected)", "verse": "Genesis 4:3-5"},
            {"age": 0, "event": "Murdered his brother Abel", "verse": "Genesis 4:8"},
            {"age": 0, "event": "Cursed and marked by God", "verse": "Genesis 4:11-15"},
            {"age": 0, "event": "Built the city of Enoch", "verse": "Genesis 4:17"}
        ]
    },

    "Abel": {
        "summary": "The second son of Adam and Eve, Abel was a shepherd who brought the firstborn of his flock as an offering to the Lord. God respected Abel's offering, which was given in faith. His brother Cain, consumed with jealousy, murdered him in the field. Abel's blood cried out from the ground, and he became the first martyr. The New Testament commends his faith.",
        "significance": "Abel represents righteous suffering and is the first martyr. His acceptable sacrifice by faith prefigures Christ's perfect sacrifice and demonstrates that God looks at the heart.",
        "key_events": [
            {"age": 0, "event": "Born to Adam and Eve", "verse": "Genesis 4:2"},
            {"age": 0, "event": "Brought acceptable offering to God", "verse": "Genesis 4:4"},
            {"age": 0, "event": "Murdered by Cain", "verse": "Genesis 4:8"},
            {"age": 0, "event": "His blood cries out from the ground", "verse": "Genesis 4:10"}
        ]
    },

    "Enoch": {
        "summary": "A descendant of Seth, Enoch walked with God for 300 years after the birth of his son Methuselah. In a unique act, God took Enoch directly to heaven without experiencing death at age 365. Enoch prophesied about the Lord's coming with His holy ones to execute judgment. He stands as one of only two people in Scripture taken directly to heaven.",
        "significance": "Enoch demonstrates that intimate fellowship with God leads to life. His translation to heaven without death prefigures the rapture of the church and eternal life for believers.",
        "key_events": [
            {"age": 65, "event": "Birth of Methuselah", "verse": "Genesis 5:21"},
            {"age": 65, "event": "Began to walk with God", "verse": "Genesis 5:22"},
            {"age": 365, "event": "Taken by God (did not see death)", "verse": "Genesis 5:24"}
        ]
    },

    "Methuselah": {
        "summary": "The son of Enoch and grandfather of Noah, Methuselah lived longer than any other person recorded in Scripture: 969 years. His name possibly means 'when he dies, it shall come,' and indeed, the Flood came in the year of his death. He represents God's patience and longsuffering before judgment.",
        "significance": "Methuselah's extraordinary lifespan demonstrates God's patience in delaying judgment. His death in the year of the Flood shows God's mercy in waiting.",
        "key_events": [
            {"age": 0, "event": "Born to Enoch", "verse": "Genesis 5:21"},
            {"age": 187, "event": "Birth of Lamech", "verse": "Genesis 5:25"},
            {"age": 969, "event": "Death (year of the Flood)", "verse": "Genesis 5:27"}
        ]
    },

    "Shem": {
        "summary": "One of Noah's three sons, Shem was on the ark during the Flood and received his father's blessing. From Shem's line came Abraham and the Semitic peoples. After the Flood, Shem and his brothers covered their father's nakedness with respect. Shem lived 600 years and saw ten generations of his descendants.",
        "significance": "Shem's line was chosen for the covenant and the Messiah. The Semitic peoples, including the Israelites, descended from him.",
        "key_events": [
            {"age": 98, "event": "Entered the ark", "verse": "Genesis 7:13"},
            {"age": 100, "event": "Birth of Arphaxad (after the Flood)", "verse": "Genesis 11:10"},
            {"age": 0, "event": "Covered Noah's nakedness", "verse": "Genesis 9:23"},
            {"age": 600, "event": "Death", "verse": "Genesis 11:11"}
        ]
    },

    "Lot": {
        "summary": "Abraham's nephew who traveled with him to Canaan. Lot chose to live in the well-watered plain near Sodom despite its wickedness. When God destroyed Sodom and Gomorrah, angels rescued Lot and his family, though his wife looked back and became a pillar of salt. Peter calls Lot a righteous man tormented by the wickedness around him.",
        "significance": "Lot demonstrates the danger of choosing worldly prosperity over spiritual separation. His rescue from Sodom prefigures God's deliverance of believers from judgment.",
        "key_events": [
            {"age": 0, "event": "Traveled to Canaan with Abraham", "verse": "Genesis 12:4-5"},
            {"age": 0, "event": "Chose to live near Sodom", "verse": "Genesis 13:10-12"},
            {"age": 0, "event": "Captured and rescued by Abraham", "verse": "Genesis 14:12-16"},
            {"age": 0, "event": "Escaped destruction of Sodom", "verse": "Genesis 19:15-29"}
        ]
    },

    "Ishmael": {
        "summary": "The son of Abraham through Hagar, Sarah's Egyptian maidservant. Born when Abraham was 86, Ishmael was not the child of promise. After Isaac's birth, Sarah demanded Hagar and Ishmael be sent away. God promised to make Ishmael a great nation, and he became the father of twelve princes. Ishmael lived 137 years.",
        "significance": "Ishmael represents works of the flesh and human effort to fulfill God's promises. His conflict with Isaac illustrates the opposition between the flesh and the Spirit.",
        "key_events": [
            {"age": 0, "event": "Born to Abraham and Hagar", "verse": "Genesis 16:15-16"},
            {"age": 13, "event": "Circumcised with Abraham", "verse": "Genesis 17:25"},
            {"age": 14, "event": "Sent away with Hagar", "verse": "Genesis 21:14-21"},
            {"age": 0, "event": "God's promise to make him a great nation", "verse": "Genesis 21:18"},
            {"age": 137, "event": "Death", "verse": "Genesis 25:17"}
        ]
    },

    "Esau": {
        "summary": "The firstborn twin son of Isaac and Rebekah, Esau was a skillful hunter and his father's favorite. In a moment of weakness, he sold his birthright to Jacob for a bowl of stew, despising his inheritance. Later, Jacob stole the blessing intended for Esau. Though Esau vowed revenge, the brothers eventually reconciled. Esau became the father of the Edomites.",
        "significance": "Esau represents those who despise spiritual blessings for temporary earthly pleasures. The New Testament uses him as a warning against godlessness and refusing God's grace.",
        "key_events": [
            {"age": 0, "event": "Born second, grasping Jacob's heel", "verse": "Genesis 25:24-26"},
            {"age": 0, "event": "Sold birthright for stew", "verse": "Genesis 25:29-34"},
            {"age": 40, "event": "Married Hittite women", "verse": "Genesis 26:34"},
            {"age": 77, "event": "Lost his father's blessing to Jacob", "verse": "Genesis 27:30-41"},
            {"age": 97, "event": "Reconciled with Jacob", "verse": "Genesis 33:4"}
        ]
    },

    "Aaron": {
        "summary": "Moses' older brother and Israel's first high priest. Aaron served as Moses' spokesman before Pharaoh and performed miracles with his staff. He was consecrated as high priest and his descendants continued the priestly line. Despite witnessing God's power, Aaron made the golden calf and later challenged Moses' authority with Miriam. He died on Mount Hor at age 123.",
        "significance": "Aaron established the Levitical priesthood that prefigures Christ's perfect high priesthood. His role as mediator between God and Israel points to Christ's mediatorial work.",
        "key_events": [
            {"age": 83, "event": "Called by God to join Moses", "verse": "Exodus 4:27-28"},
            {"age": 83, "event": "Confronted Pharaoh with Moses", "verse": "Exodus 7:1-7"},
            {"age": 0, "event": "Made the golden calf", "verse": "Exodus 32:1-6"},
            {"age": 0, "event": "Consecrated as high priest", "verse": "Leviticus 8:1-36"},
            {"age": 123, "event": "Death on Mount Hor", "verse": "Numbers 33:38-39"}
        ]
    },

    "Joshua": {
        "summary": "Moses' assistant and successor, Joshua led Israel into the Promised Land after Moses' death. As a young man, he was one of twelve spies who explored Canaan, and only he and Caleb trusted God to give them victory. Joshua led the conquest of Canaan, including the miraculous fall of Jericho. He challenged Israel to choose whom they would serve, declaring his household would serve the Lord.",
        "significance": "Joshua (whose name means 'the Lord saves') prefigures Jesus Christ as the one who leads God's people into their inheritance and rest.",
        "key_events": [
            {"age": 0, "event": "Led Israel in battle against Amalek", "verse": "Exodus 17:9-13"},
            {"age": 40, "event": "Spied out Canaan with Caleb", "verse": "Numbers 14:6-9"},
            {"age": 80, "event": "Appointed as Moses' successor", "verse": "Deuteronomy 31:23"},
            {"age": 80, "event": "Crossed the Jordan River", "verse": "Joshua 3:14-17"},
            {"age": 80, "event": "Conquest of Jericho", "verse": "Joshua 6:1-27"},
            {"age": 110, "event": "Death", "verse": "Joshua 24:29"}
        ]
    },

    "Samson": {
        "summary": "A Nazirite judge of Israel who possessed extraordinary strength from the Lord. Samson judged Israel for twenty years during Philistine oppression. Despite his strength, he struggled with moral weakness, particularly regarding women. His relationship with Delilah led to the revelation of his strength's source, resulting in his capture. In his death, Samson killed more Philistines than during his life.",
        "significance": "Samson demonstrates that God's calling and gifts don't depend on human perfection, yet sin has consequences. His final act shows that God can use even our failures for His purposes.",
        "key_events": [
            {"age": 0, "event": "Birth announced by angel", "verse": "Judges 13:3-5"},
            {"age": 0, "event": "Killed a lion with bare hands", "verse": "Judges 14:5-6"},
            {"age": 0, "event": "Killed 1000 Philistines with jawbone", "verse": "Judges 15:15"},
            {"age": 0, "event": "Betrayed by Delilah", "verse": "Judges 16:18-21"},
            {"age": 0, "event": "Death destroying Philistine temple", "verse": "Judges 16:28-30"}
        ]
    },

    "Samuel": {
        "summary": "The last judge of Israel and a prophet who anointed Israel's first two kings. Born to Hannah in answer to prayer, Samuel was dedicated to God's service from childhood. He served in the tabernacle under Eli and received God's word as a young boy. Samuel judged Israel faithfully and established the monarchy by anointing Saul and later David. He represents the transition from judges to kings.",
        "significance": "Samuel bridges the period between judges and kings, demonstrating godly leadership and obedience to God's word. His life shows the importance of hearing and obeying God's voice.",
        "key_events": [
            {"age": 0, "event": "Born in answer to Hannah's prayer", "verse": "1 Samuel 1:20"},
            {"age": 3, "event": "Dedicated to service at the tabernacle", "verse": "1 Samuel 1:24-28"},
            {"age": 12, "event": "Called by God in the night", "verse": "1 Samuel 3:1-10"},
            {"age": 0, "event": "Anointed Saul as king", "verse": "1 Samuel 10:1"},
            {"age": 0, "event": "Anointed David as king", "verse": "1 Samuel 16:13"}
        ]
    },

    "Saul": {
        "summary": "Israel's first king, chosen for his impressive physical stature. Initially humble, Saul began well but disobeyed God's commands, offering unauthorized sacrifice and sparing King Agag when commanded to destroy the Amalekites. God rejected Saul as king and chose David to replace him. Consumed by jealousy of David, Saul's later years were marked by madness and pursuit of David. He died by suicide after defeat in battle.",
        "significance": "Saul's reign demonstrates the danger of partial obedience and the priority of obeying God rather than fearing man. His rejection shows that God looks at the heart, not outward appearance.",
        "key_events": [
            {"age": 30, "event": "Anointed as Israel's first king", "verse": "1 Samuel 10:1"},
            {"age": 30, "event": "Publicly chosen as king", "verse": "1 Samuel 10:24"},
            {"age": 0, "event": "Disobeyed by offering unauthorized sacrifice", "verse": "1 Samuel 13:8-14"},
            {"age": 0, "event": "Rejected as king for sparing Agag", "verse": "1 Samuel 15:22-23"},
            {"age": 0, "event": "Attempted to kill David", "verse": "1 Samuel 18:10-11"},
            {"age": 72, "event": "Suicide after defeat by Philistines", "verse": "1 Samuel 31:4"}
        ]
    },

    "Elijah": {
        "summary": "A powerful prophet during Israel's apostasy under King Ahab and Queen Jezebel. Elijah confronted Baal worship, called down fire from heaven on Mount Carmel, and pronounced drought upon the land. He was fed by ravens and multiplied a widow's food. After defeating the prophets of Baal, Jezebel's threats sent him fleeing, but God met him in a still small voice. Elijah did not die but was taken to heaven in a whirlwind.",
        "significance": "Elijah represents bold prophetic ministry and appears with Moses at Jesus' transfiguration. His return is prophesied before the great day of the Lord, associated with John the Baptist and future end-times ministry.",
        "key_events": [
            {"age": 0, "event": "Pronounced drought on Israel", "verse": "1 Kings 17:1"},
            {"age": 0, "event": "Fed by ravens at Cherith", "verse": "1 Kings 17:4-6"},
            {"age": 0, "event": "Multiplied widow's oil and flour", "verse": "1 Kings 17:14-16"},
            {"age": 0, "event": "Defeated prophets of Baal on Carmel", "verse": "1 Kings 18:38-40"},
            {"age": 0, "event": "Heard God's still small voice", "verse": "1 Kings 19:12"},
            {"age": 0, "event": "Taken to heaven in a whirlwind", "verse": "2 Kings 2:11"}
        ]
    },

    "Elisha": {
        "summary": "The prophet who succeeded Elijah after receiving a double portion of his spirit. Elisha performed many miracles including purifying water, multiplying oil, raising a dead boy, healing Naaman's leprosy, and making an axe head float. He advised kings and demonstrated God's power through numerous signs and wonders. His ministry lasted over fifty years, touching both rich and poor.",
        "significance": "Elisha's double portion and numerous miracles demonstrate God's power and compassion. His healings and provisions prefigure Christ's ministry of mercy and power.",
        "key_events": [
            {"age": 0, "event": "Called by Elijah", "verse": "1 Kings 19:19-21"},
            {"age": 0, "event": "Received double portion of Elijah's spirit", "verse": "2 Kings 2:9-14"},
            {"age": 0, "event": "Purified poisoned water", "verse": "2 Kings 2:21-22"},
            {"age": 0, "event": "Multiplied widow's oil", "verse": "2 Kings 4:1-7"},
            {"age": 0, "event": "Raised Shunammite's son", "verse": "2 Kings 4:32-37"},
            {"age": 0, "event": "Healed Naaman of leprosy", "verse": "2 Kings 5:10-14"}
        ]
    },

    "Jonah": {
        "summary": "The prophet called to preach to Nineveh but who fled to Tarshish instead. God sent a great storm, and Jonah was thrown overboard and swallowed by a great fish for three days. After being vomited onto dry land, Jonah obeyed and preached to Nineveh, which repented. Jonah's anger at God's mercy revealed his hard heart. His experience in the fish prefigures Christ's resurrection.",
        "significance": "Jonah's three days in the fish prefigure Christ's death and resurrection. His reluctant ministry to Gentiles foreshadows the gospel going to all nations and reveals God's compassion for all people.",
        "key_events": [
            {"age": 0, "event": "Called to preach to Nineveh", "verse": "Jonah 1:1-2"},
            {"age": 0, "event": "Fled to Tarshish", "verse": "Jonah 1:3"},
            {"age": 0, "event": "Thrown into sea during storm", "verse": "Jonah 1:15"},
            {"age": 0, "event": "Swallowed by great fish", "verse": "Jonah 1:17"},
            {"age": 0, "event": "Vomited onto dry land", "verse": "Jonah 2:10"},
            {"age": 0, "event": "Preached to Nineveh (city repented)", "verse": "Jonah 3:4-10"}
        ]
    },

    "John the Baptist": {
        "summary": "The forerunner of Jesus Christ, born to Zechariah and Elizabeth in their old age. John lived in the wilderness, wore camel's hair, and ate locusts and wild honey. He preached repentance and baptized in the Jordan River, preparing the way for the Messiah. John baptized Jesus and declared Him the Lamb of God. He was imprisoned by Herod and beheaded for denouncing Herod's unlawful marriage.",
        "significance": "John fulfilled Isaiah's prophecy as the voice crying in the wilderness. He represents the last of the Old Testament prophets and the bridge to the New Covenant, pointing people to Jesus.",
        "key_events": [
            {"age": 0, "event": "Birth announced to Zechariah", "verse": "Luke 1:13"},
            {"age": 30, "event": "Began ministry in wilderness", "verse": "Luke 3:1-3"},
            {"age": 30, "event": "Baptized Jesus", "verse": "Matthew 3:13-17"},
            {"age": 30, "event": "Declared Jesus the Lamb of God", "verse": "John 1:29"},
            {"age": 32, "event": "Imprisoned by Herod", "verse": "Matthew 14:3-4"},
            {"age": 32, "event": "Beheaded by Herod", "verse": "Matthew 14:10"}
        ]
    },

    "Mary": {
        "summary": "The virgin chosen by God to be the mother of Jesus Christ. A young woman from Nazareth, betrothed to Joseph, Mary received the angel Gabriel's announcement with humble submission. She gave birth to Jesus in Bethlehem and raised Him with Joseph. Mary witnessed Jesus' ministry, His crucifixion, and was present with the disciples after His ascension. She is called blessed among women.",
        "significance": "Mary's obedient faith demonstrates true discipleship. Her role as the mother of Jesus fulfills prophecy and shows God's ability to work through humble, faithful servants.",
        "key_events": [
            {"age": 14, "event": "Angel announced Jesus' birth", "verse": "Luke 1:26-38"},
            {"age": 14, "event": "Visited Elizabeth", "verse": "Luke 1:39-45"},
            {"age": 15, "event": "Gave birth to Jesus", "verse": "Luke 2:7"},
            {"age": 15, "event": "Presented Jesus at the temple", "verse": "Luke 2:22-38"},
            {"age": 27, "event": "Found Jesus teaching in temple", "verse": "Luke 2:46-50"},
            {"age": 48, "event": "At wedding in Cana", "verse": "John 2:1-5"},
            {"age": 51, "event": "Witnessed Jesus' crucifixion", "verse": "John 19:25-27"}
        ]
    },

    "Peter": {
        "summary": "Originally named Simon, a fisherman called by Jesus to be a fisher of men. Peter was part of Jesus' inner circle and often served as spokesman for the disciples. Despite his bold confession of Jesus as Christ, Peter denied Jesus three times during His trial. After Jesus' resurrection, Peter was restored and became a pillar of the early church, preaching at Pentecost and writing two epistles.",
        "significance": "Peter demonstrates both human weakness and divine restoration. His transformation from denier to church leader shows the power of Christ's grace and forgiveness.",
        "key_events": [
            {"age": 30, "event": "Called by Jesus", "verse": "Matthew 4:18-20"},
            {"age": 33, "event": "Walked on water", "verse": "Matthew 14:28-31"},
            {"age": 33, "event": "Confessed Jesus as the Christ", "verse": "Matthew 16:16"},
            {"age": 33, "event": "Witnessed the Transfiguration", "verse": "Matthew 17:1-8"},
            {"age": 33, "event": "Denied Jesus three times", "verse": "Matthew 26:69-75"},
            {"age": 33, "event": "Restored by Jesus", "verse": "John 21:15-19"},
            {"age": 33, "event": "Preached at Pentecost", "verse": "Acts 2:14-41"}
        ]
    },

    "Paul": {
        "summary": "Originally Saul of Tarsus, a Pharisee who persecuted Christians. Converted dramatically on the road to Damascus when confronted by the risen Christ. Paul became the greatest missionary of the early church, making three missionary journeys and writing much of the New Testament. He suffered imprisonment, beatings, shipwreck, and eventual martyrdom for the gospel. Paul's theology shaped Christian doctrine.",
        "significance": "Paul's conversion demonstrates the transforming power of Christ's grace. His missionary work and writings established churches and doctrine throughout the Gentile world.",
        "key_events": [
            {"age": 33, "event": "Conversion on Damascus road", "verse": "Acts 9:3-6"},
            {"age": 36, "event": "Began preaching Christ", "verse": "Acts 9:20"},
            {"age": 46, "event": "First missionary journey", "verse": "Acts 13:2-3"},
            {"age": 49, "event": "Jerusalem Council", "verse": "Acts 15:2"},
            {"age": 51, "event": "Second missionary journey", "verse": "Acts 15:36"},
            {"age": 54, "event": "Third missionary journey", "verse": "Acts 18:23"},
            {"age": 58, "event": "Arrested in Jerusalem", "verse": "Acts 21:33"},
            {"age": 68, "event": "Martyrdom in Rome (tradition)", "verse": "2 Timothy 4:6-8"}
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
