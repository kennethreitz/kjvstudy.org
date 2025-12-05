#!/usr/bin/env python3
"""Merge all section headings into one file."""
import json
from pathlib import Path

# Start with existing data
base_file = Path("kjvstudy_org/data/section_headings.json")
with open(base_file) as f:
    all_headings = json.load(f)

# Load major prophets
prophets_file = Path("section_headings_major_prophets.json")
with open(prophets_file) as f:
    prophets = json.load(f)
all_headings.update(prophets)

# Load Mark and Luke
gospels_file = Path("section_headings_mark_luke.json")
with open(gospels_file) as f:
    gospels = json.load(f)
all_headings.update(gospels)

# Pentateuch (from agent output)
pentateuch = {
  "Exodus": {
    "1": {"1": "Israel's Oppression in Egypt"},
    "2": {"1": "The Birth of Moses", "11": "Moses Flees to Midian"},
    "3": {"1": "The Burning Bush", "13": "God Reveals His Name"},
    "4": {"1": "Signs for Moses", "18": "Moses Returns to Egypt"},
    "5": {"1": "Pharaoh Increases Israel's Burden"},
    "6": {"1": "God Promises Deliverance", "14": "The Family of Moses and Aaron"},
    "7": {"1": "Moses and Aaron Before Pharaoh", "14": "The First Plague: Water to Blood"},
    "8": {"1": "The Second Plague: Frogs", "16": "The Third Plague: Gnats", "20": "The Fourth Plague: Flies"},
    "9": {"1": "The Fifth Plague: Livestock Disease", "8": "The Sixth Plague: Boils", "13": "The Seventh Plague: Hail"},
    "10": {"1": "The Eighth Plague: Locusts", "21": "The Ninth Plague: Darkness"},
    "11": {"1": "The Tenth Plague Announced"},
    "12": {"1": "The Passover Instituted", "29": "The Tenth Plague: Death of the Firstborn", "37": "The Exodus Begins"},
    "13": {"1": "Consecration of the Firstborn", "17": "The Pillar of Cloud and Fire"},
    "14": {"1": "Pharaoh Pursues Israel", "15": "The Red Sea Crossing"},
    "15": {"1": "The Song of Moses", "22": "Bitter Waters Made Sweet at Marah"},
    "16": {"1": "Manna and Quail from Heaven"},
    "17": {"1": "Water from the Rock at Rephidim", "8": "Victory over Amalek"},
    "18": {"1": "Jethro Visits Moses", "13": "Jethro's Advice on Leadership"},
    "19": {"1": "Israel Camps at Mount Sinai", "16": "The Lord Descends on Sinai"},
    "20": {"1": "The Ten Commandments", "18": "The People's Fear", "22": "Laws About Altars"},
    "21": {"1": "Laws About Servants", "12": "Laws About Violence", "28": "Laws About Property Damage"},
    "22": {"1": "Laws About Restitution", "16": "Laws About Social Responsibility", "29": "Firstfruits and Offerings"},
    "23": {"1": "Laws About Justice and Mercy", "10": "Sabbath Laws and Festivals", "20": "God's Angel to Lead Israel"},
    "24": {"1": "The Covenant Confirmed", "12": "Moses on the Mountain"},
    "25": {"1": "Offerings for the Tabernacle", "10": "The Ark of the Covenant", "23": "The Table and Lampstand"},
    "26": {"1": "The Tabernacle"},
    "27": {"1": "The Bronze Altar", "9": "The Court of the Tabernacle", "20": "Oil for the Lampstand"},
    "28": {"1": "Garments for the Priests"},
    "29": {"1": "Consecration of the Priests", "38": "The Daily Offerings"},
    "30": {"1": "The Altar of Incense", "11": "The Atonement Money", "17": "The Bronze Basin", "22": "The Anointing Oil and Incense"},
    "31": {"1": "Craftsmen for the Tabernacle", "12": "The Sabbath Command", "18": "The Stone Tablets"},
    "32": {"1": "The Golden Calf", "15": "Moses' Anger", "30": "Moses Intercedes for Israel"},
    "33": {"1": "The Lord's Presence Promised", "12": "Moses and the Glory of God"},
    "34": {"1": "New Stone Tablets", "10": "The Covenant Renewed", "29": "The Radiance of Moses' Face"},
    "35": {"1": "Sabbath Regulations", "4": "Offerings for the Tabernacle", "30": "Bezalel and Oholiab Called"},
    "36": {"1": "Construction of the Tabernacle Begins", "8": "The Tabernacle Curtains"},
    "37": {"1": "Making the Ark", "10": "Making the Table", "17": "Making the Lampstand", "25": "Making the Altars"},
    "38": {"1": "Making the Bronze Altar", "9": "Making the Court", "21": "Materials Used"},
    "39": {"1": "Making the Priestly Garments", "32": "The Tabernacle Completed", "42": "Moses Inspects the Work"},
    "40": {"1": "Setting Up the Tabernacle", "34": "The Glory of the Lord Fills the Tabernacle"}
  },
  "Leviticus": {
    "1": {"1": "The Burnt Offering"},
    "2": {"1": "The Grain Offering"},
    "3": {"1": "The Peace Offering"},
    "4": {"1": "The Sin Offering", "22": "For a Leader", "27": "For a Common Person"},
    "5": {"1": "Cases Requiring a Sin Offering", "14": "The Guilt Offering"},
    "6": {"1": "The Guilt Offering", "8": "The Burnt Offering", "14": "The Grain Offering", "24": "The Sin Offering"},
    "7": {"1": "The Guilt Offering", "11": "The Peace Offering", "22": "Fat and Blood Forbidden", "28": "The Priests' Portion"},
    "8": {"1": "The Ordination of Aaron and His Sons"},
    "9": {"1": "The First Offerings of Aaron", "23": "The Lord's Glory Appears"},
    "10": {"1": "The Sin of Nadab and Abihu", "8": "Restrictions for Priests", "16": "The Sin Offering Controversy"},
    "11": {"1": "Clean and Unclean Animals", "24": "Uncleanness from Dead Animals", "39": "Additional Regulations"},
    "12": {"1": "Purification After Childbirth"},
    "13": {"1": "Laws About Skin Diseases", "29": "Laws About Infections on the Head", "47": "Laws About Mildew in Clothing"},
    "14": {"1": "Cleansing from Skin Diseases", "33": "Laws About Mildew in Houses"},
    "15": {"1": "Male Bodily Discharges", "19": "Female Bodily Discharges"},
    "16": {"1": "The Day of Atonement"},
    "17": {"1": "The Sanctity of Blood", "10": "Eating Blood Forbidden"},
    "18": {"1": "Unlawful Sexual Relations"},
    "19": {"1": "Laws of Holiness and Justice", "26": "Occult Practices Forbidden"},
    "20": {"1": "Punishments for Sin", "22": "Call to Holiness"},
    "21": {"1": "Rules for Priests", "16": "Physical Defects and Priestly Service"},
    "22": {"1": "Priestly Purity", "17": "Acceptable Sacrifices", "26": "Regulations for Offerings"},
    "23": {"1": "The Sabbath", "4": "The Passover and Unleavened Bread", "9": "Firstfruits and Pentecost", "23": "The Feast of Trumpets", "26": "The Day of Atonement", "33": "The Feast of Tabernacles"},
    "24": {"1": "Oil and Bread in the Tabernacle", "10": "Punishment for Blasphemy"},
    "25": {"1": "The Sabbath Year", "8": "The Year of Jubilee", "35": "Redeeming the Poor"},
    "26": {"1": "Blessings for Obedience", "14": "Punishments for Disobedience", "40": "Repentance and Restoration"},
    "27": {"1": "Rules About Vows", "14": "Dedicating a House or Land", "30": "Tithes"}
  },
  "Numbers": {
    "1": {"1": "The Census of Israel's Troops"},
    "2": {"1": "Organization of the Camp"},
    "3": {"1": "The Levites", "14": "The Census of the Levites", "40": "Redeeming the Firstborn"},
    "4": {"1": "Duties of the Kohathites", "17": "Duties of the Gershonites", "29": "Duties of the Merarites"},
    "5": {"1": "Purity in the Camp", "5": "Restitution for Wrongs", "11": "The Test for an Unfaithful Wife"},
    "6": {"1": "The Nazirite Vow", "22": "The Priestly Blessing"},
    "7": {"1": "Offerings for the Tabernacle Dedication"},
    "8": {"1": "Setting Up the Lamps", "5": "Consecration of the Levites", "23": "Retirement of the Levites"},
    "9": {"1": "The Second Passover", "15": "The Cloud Above the Tabernacle"},
    "10": {"1": "The Silver Trumpets", "11": "Israel Leaves Sinai"},
    "11": {"1": "The People Complain", "10": "Moses' Burden", "16": "The Seventy Elders", "31": "Quail from the Lord"},
    "12": {"1": "Miriam and Aaron Oppose Moses", "9": "Miriam's Leprosy"},
    "13": {"1": "The Twelve Spies", "25": "The Spies' Report"},
    "14": {"1": "The People Rebel", "13": "Moses Intercedes", "26": "God's Judgment on Israel", "39": "Defeat at Hormah"},
    "15": {"1": "Laws About Offerings", "22": "Laws About Unintentional Sin", "32": "The Sabbath Breaker", "37": "Tassels on Garments"},
    "16": {"1": "Korah's Rebellion", "23": "The Earth Swallows the Rebels", "41": "The People Grumble and a Plague Strikes"},
    "17": {"1": "Aaron's Staff Buds"},
    "18": {"1": "Duties of Priests and Levites", "8": "Offerings for Priests and Levites"},
    "19": {"1": "The Water of Purification"},
    "20": {"1": "Water from the Rock at Meribah", "14": "Edom Refuses Passage", "22": "The Death of Aaron"},
    "21": {"1": "The Bronze Serpent", "10": "Journey to Moab", "21": "Victory over Sihon and Og"},
    "22": {"1": "Balak Summons Balaam", "21": "Balaam's Donkey Speaks"},
    "23": {"1": "Balaam's First Oracle", "13": "Balaam's Second Oracle", "27": "Balaam's Third Oracle"},
    "24": {"1": "Balaam's Fourth Oracle", "10": "Balaam's Final Oracles"},
    "25": {"1": "Israel's Sin with Moabite Women", "6": "The Zeal of Phinehas"},
    "26": {"1": "The Second Census of Israel"},
    "27": {"1": "The Daughters of Zelophehad", "12": "Joshua to Succeed Moses"},
    "28": {"1": "Daily Offerings", "9": "Sabbath and Monthly Offerings", "16": "Passover and Festival Offerings"},
    "29": {"1": "Offerings for the Feast of Trumpets", "7": "Offerings for the Day of Atonement", "12": "Offerings for the Feast of Tabernacles"},
    "30": {"1": "Laws About Vows"},
    "31": {"1": "Vengeance on Midian", "25": "Division of the Plunder"},
    "32": {"1": "The Tribes East of the Jordan"},
    "33": {"1": "The Stages of Israel's Journey", "50": "Instructions for Canaan"},
    "34": {"1": "The Boundaries of Canaan", "16": "Leaders to Divide the Land"},
    "35": {"1": "Cities for the Levites", "9": "Cities of Refuge"},
    "36": {"1": "Inheritance Laws for Women"}
  },
  "Deuteronomy": {
    "1": {"1": "Moses' Introduction", "9": "Leaders Appointed", "19": "The Twelve Spies and Israel's Rebellion", "41": "Defeat at Hormah"},
    "2": {"1": "Journey Through the Wilderness", "24": "Victory over Sihon"},
    "3": {"1": "Victory over Og", "12": "Land Divided East of the Jordan", "23": "Moses Forbidden to Cross the Jordan"},
    "4": {"1": "Call to Obedience", "15": "Warning Against Idolatry", "41": "Cities of Refuge East of the Jordan"},
    "5": {"1": "The Ten Commandments Repeated", "22": "Moses as Mediator"},
    "6": {"1": "The Greatest Commandment", "10": "Warning Against Forgetting God", "20": "Teaching Your Children"},
    "7": {"1": "Destroying the Nations", "12": "Blessings for Obedience"},
    "8": {"1": "Remember the Lord Your God"},
    "9": {"1": "Not Because of Israel's Righteousness", "7": "The Golden Calf Recalled", "25": "Moses Intercedes for Israel"},
    "10": {"1": "New Stone Tablets", "12": "What God Requires"},
    "11": {"1": "Love and Obey the Lord", "26": "Blessings and Curses"},
    "12": {"1": "The Place of Worship", "29": "Warning Against Idolatry"},
    "13": {"1": "Warnings Against False Prophets and Idolatry"},
    "14": {"1": "Clean and Unclean Foods", "22": "Tithes"},
    "15": {"1": "The Year of Release", "12": "Release of Servants", "19": "Consecration of Firstborn Animals"},
    "16": {"1": "The Passover", "9": "The Feast of Weeks", "13": "The Feast of Tabernacles", "18": "Judges and Justice"},
    "17": {"1": "Idolatry and Justice", "8": "Courts of Law", "14": "Laws Concerning a King"},
    "18": {"1": "Provisions for Priests and Levites", "9": "Occult Practices Forbidden", "15": "The Prophet Like Moses"},
    "19": {"1": "Cities of Refuge", "14": "Property Boundaries", "15": "Laws Concerning Witnesses"},
    "20": {"1": "Laws Concerning Warfare"},
    "21": {"1": "Atonement for Unsolved Murder", "10": "Marrying a Captive Woman", "15": "Rights of the Firstborn", "18": "A Rebellious Son", "22": "Displaying a Hanged Man's Body"},
    "22": {"1": "Various Laws of Responsibility", "13": "Laws Concerning Sexual Purity"},
    "23": {"1": "Exclusion from the Assembly", "9": "Cleanliness in the Camp", "15": "Miscellaneous Laws"},
    "24": {"1": "Laws About Divorce", "5": "Miscellaneous Laws", "14": "Justice for the Poor"},
    "25": {"1": "Justice and Mercy", "5": "Levirate Marriage", "11": "Honest Weights and Measures", "17": "Remember Amalek"},
    "26": {"1": "Firstfruits and Tithes", "16": "Call to Obedience"},
    "27": {"1": "The Altar on Mount Ebal", "9": "Curses from Mount Ebal"},
    "28": {"1": "Blessings for Obedience", "15": "Curses for Disobedience"},
    "29": {"1": "Renewing the Covenant"},
    "30": {"1": "Restoration After Repentance", "11": "The Choice of Life or Death"},
    "31": {"1": "Joshua to Succeed Moses", "9": "The Reading of the Law", "14": "The Lord's Charge to Moses and Joshua", "30": "The Song of Moses Introduced"},
    "32": {"1": "The Song of Moses", "48": "Moses to Die on Mount Nebo"},
    "33": {"1": "Moses' Blessing on Israel"},
    "34": {"1": "The Death of Moses"}
  }
}
all_headings.update(pentateuch)

# Historical books
historical = {
  "Joshua": {
    "1": {"1": "God Commissions Joshua"},
    "2": {"1": "Rahab and the Spies"},
    "3": {"1": "Crossing the Jordan"},
    "4": {"1": "Memorial Stones Set Up"},
    "5": {"1": "Circumcision at Gilgal", "10": "The Commander of the Lord's Army"},
    "6": {"1": "The Fall of Jericho"},
    "7": {"1": "Achan's Sin and Israel's Defeat"},
    "8": {"1": "The Conquest of Ai", "30": "The Altar on Mount Ebal"},
    "9": {"1": "The Gibeonite Deception"},
    "10": {"1": "The Sun Stands Still", "16": "Victory Over Southern Canaan"},
    "11": {"1": "Conquest of Northern Canaan", "16": "Summary of Joshua's Conquests"},
    "12": {"1": "Kings Defeated by Moses", "7": "Kings Defeated by Joshua"},
    "13": {"1": "Land Yet to Be Conquered", "8": "Division of Land East of Jordan"},
    "14": {"1": "Caleb's Inheritance"},
    "15": {"1": "Judah's Territory"},
    "16": {"1": "Ephraim's Territory"},
    "17": {"1": "Manasseh's Territory"},
    "18": {"1": "Dividing the Remaining Land", "11": "Benjamin's Territory"},
    "19": {"1": "Territories of Six Tribes", "49": "Joshua's Inheritance"},
    "20": {"1": "Cities of Refuge"},
    "21": {"1": "Towns for the Levites", "43": "The Lord Gives Rest"},
    "22": {"1": "Eastern Tribes Return Home", "10": "The Altar of Witness"},
    "23": {"1": "Joshua's Farewell Address"},
    "24": {"1": "The Covenant at Shechem", "29": "Joshua's Death and Burial"}
  },
  "Judges": {
    "1": {"1": "Judah and Simeon Conquer", "22": "House of Joseph Conquers Bethel", "27": "Failure to Complete Conquest"},
    "2": {"1": "The Angel at Bokim", "6": "Israel's Disobedience", "16": "The Pattern of the Judges"},
    "3": {"1": "Nations Left to Test Israel", "7": "Othniel Delivers Israel", "12": "Ehud Delivers Israel", "31": "Shamgar Delivers Israel"},
    "4": {"1": "Deborah and Barak", "17": "Jael Kills Sisera"},
    "5": {"1": "The Song of Deborah"},
    "6": {"1": "Midian Oppresses Israel", "11": "The Call of Gideon", "25": "Gideon Destroys Baal's Altar", "33": "The Sign of the Fleece"},
    "7": {"1": "Gideon's Army Reduced", "9": "The Dream of the Barley Loaf", "16": "The Victory Over Midian"},
    "8": {"1": "Gideon Defeats Midian", "22": "Gideon's Ephod", "28": "Gideon's Death"},
    "9": {"1": "Abimelech Becomes King", "22": "Gaal's Rebellion", "46": "Abimelech's Death"},
    "10": {"1": "Tola and Jair", "6": "Oppression by the Ammonites", "17": "Israel Gathers at Mizpah"},
    "11": {"1": "Jephthah Becomes Leader", "12": "Jephthah's Message to Ammon", "29": "Jephthah's Vow and Victory"},
    "12": {"1": "Jephthah and Ephraim", "7": "Three Minor Judges"},
    "13": {"1": "The Birth of Samson"},
    "14": {"1": "Samson's Marriage", "10": "Samson's Riddle"},
    "15": {"1": "Samson's Revenge", "9": "Samson Defeats the Philistines", "18": "Water from the Jawbone"},
    "16": {"1": "Samson at Gaza", "4": "Samson and Delilah", "23": "Samson's Death"},
    "17": {"1": "Micah's Idols", "7": "The Levite Becomes Micah's Priest"},
    "18": {"1": "The Danites Seek Territory", "14": "The Danites Take Micah's Idols", "27": "The Danites Conquer Laish"},
    "19": {"1": "The Levite and His Concubine", "10": "The Crime at Gibeah"},
    "20": {"1": "Israel Assembles Against Benjamin", "18": "The War Against Benjamin"},
    "21": {"1": "Wives for the Benjamites", "15": "Women from Shiloh"}
  },
  "Ruth": {
    "1": {"1": "Naomi and Ruth Return to Bethlehem"},
    "2": {"1": "Ruth Meets Boaz"},
    "3": {"1": "Ruth's Appeal to Boaz"},
    "4": {"1": "Boaz Marries Ruth", "13": "The Genealogy of David"}
  },
  "1 Samuel": {
    "1": {"1": "Hannah's Prayer for a Son", "21": "Samuel's Birth and Dedication"},
    "2": {"1": "Hannah's Prayer of Thanksgiving", "12": "Eli's Wicked Sons", "27": "Prophecy Against Eli's House"},
    "3": {"1": "The Lord Calls Samuel", "11": "The Lord's Message to Samuel"},
    "4": {"1": "The Philistines Capture the Ark", "12": "Eli's Death"},
    "5": {"1": "The Ark in Philistine Cities"},
    "6": {"1": "The Ark Returned to Israel"},
    "7": {"1": "Samuel Leads Israel", "7": "Victory Over the Philistines"},
    "8": {"1": "Israel Demands a King"},
    "9": {"1": "Saul Seeks His Father's Donkeys", "15": "Saul Meets Samuel"},
    "10": {"1": "Saul Anointed King", "17": "Saul Chosen by Lot"},
    "11": {"1": "Saul Defeats the Ammonites", "12": "Saul Confirmed as King"},
    "12": {"1": "Samuel's Farewell Address"},
    "13": {"1": "Saul's Unlawful Sacrifice", "15": "Saul Rejected as King"},
    "14": {"1": "Jonathan's Bold Attack", "24": "Saul's Rash Oath", "47": "Summary of Saul's Reign"},
    "15": {"1": "Saul's Incomplete Obedience", "10": "Samuel Rebukes Saul", "32": "Samuel Kills Agag"},
    "16": {"1": "David Anointed King", "14": "David Enters Saul's Service"},
    "17": {"1": "Goliath's Challenge", "32": "David Volunteers to Fight", "41": "David Defeats Goliath"},
    "18": {"1": "Saul's Jealousy of David", "17": "David and Michal"},
    "19": {"1": "Saul Tries to Kill David", "8": "David's Escape", "18": "David Flees to Samuel"},
    "20": {"1": "Jonathan Warns David", "24": "Jonathan's Sign to David"},
    "21": {"1": "David at Nob", "10": "David Flees to Gath"},
    "22": {"1": "David at Adullam", "6": "Saul Kills the Priests of Nob"},
    "23": {"1": "David Saves Keilah", "14": "Saul Pursues David", "19": "The Ziphites Betray David"},
    "24": {"1": "David Spares Saul's Life"},
    "25": {"1": "Samuel's Death", "2": "David, Nabal, and Abigail"},
    "26": {"1": "David Spares Saul Again"},
    "27": {"1": "David Lives Among the Philistines"},
    "28": {"1": "Saul and the Witch of Endor"},
    "29": {"1": "The Philistines Reject David"},
    "30": {"1": "David Defeats the Amalekites"},
    "31": {"1": "Saul's Death"}
  },
  "2 Samuel": {
    "1": {"1": "David Learns of Saul's Death", "17": "David's Lament for Saul and Jonathan"},
    "2": {"1": "David Anointed King of Judah", "8": "War Between David and Ishbosheth"},
    "3": {"1": "Abner Defects to David", "22": "Joab Murders Abner"},
    "4": {"1": "Ishbosheth Murdered"},
    "5": {"1": "David Anointed King of Israel", "6": "David Conquers Jerusalem", "17": "David Defeats the Philistines"},
    "6": {"1": "The Ark Brought to Jerusalem", "12": "David Dances Before the Ark"},
    "7": {"1": "God's Covenant with David"},
    "8": {"1": "David's Military Victories", "15": "David's Officials"},
    "9": {"1": "David's Kindness to Mephibosheth"},
    "10": {"1": "War with the Ammonites and Arameans"},
    "11": {"1": "David and Bathsheba", "14": "David Has Uriah Killed"},
    "12": {"1": "Nathan Confronts David", "15": "The Death of David's Son", "24": "Solomon's Birth", "26": "The Capture of Rabbah"},
    "13": {"1": "Amnon and Tamar", "23": "Absalom Kills Amnon"},
    "14": {"1": "The Woman of Tekoa", "21": "Absalom Returns to Jerusalem"},
    "15": {"1": "Absalom's Conspiracy", "13": "David Flees Jerusalem"},
    "16": {"1": "Ziba and Mephibosheth", "5": "Shimei Curses David", "15": "Absalom Enters Jerusalem"},
    "17": {"1": "Hushai Counters Ahithophel", "24": "Absalom Pursues David"},
    "18": {"1": "Absalom's Death", "19": "David Mourns Absalom"},
    "19": {"1": "Joab Rebukes David", "9": "David Returns to Jerusalem", "24": "Mephibosheth's Loyalty", "31": "Barzillai Returns Home", "40": "Israel and Judah Quarrel"},
    "20": {"1": "Sheba's Rebellion", "14": "The Siege of Abel Beth Maacah"},
    "21": {"1": "The Gibeonites Avenged", "15": "Wars Against the Philistines"},
    "22": {"1": "David's Song of Deliverance"},
    "23": {"1": "David's Last Words", "8": "David's Mighty Warriors"},
    "24": {"1": "David's Census", "10": "Judgment for the Census", "18": "David Builds an Altar"}
  },
  "1 Kings": {
    "1": {"1": "Adonijah Sets Himself Up as King", "28": "David Makes Solomon King"},
    "2": {"1": "David's Charge to Solomon", "12": "Solomon's Throne Established", "26": "Solomon Removes His Enemies"},
    "3": {"1": "Solomon Asks for Wisdom", "16": "A Wise Ruling"},
    "4": {"1": "Solomon's Officials", "20": "Solomon's Prosperity and Wisdom"},
    "5": {"1": "Preparations for Building the Temple"},
    "6": {"1": "Solomon Builds the Temple"},
    "7": {"1": "Solomon Builds His Palace", "13": "The Temple Furnishings"},
    "8": {"1": "The Ark Brought to the Temple", "22": "Solomon's Prayer of Dedication", "54": "The Blessing and Benediction"},
    "9": {"1": "The Lord Appears to Solomon", "10": "Solomon's Other Activities"},
    "10": {"1": "The Queen of Sheba Visits", "14": "Solomon's Splendor"},
    "11": {"1": "Solomon's Wives Turn His Heart", "14": "Solomon's Adversaries", "26": "Jeroboam Rebels", "41": "Solomon's Death"},
    "12": {"1": "Israel Rebels Against Rehoboam", "25": "Jeroboam's Golden Calves"},
    "13": {"1": "The Man of God from Judah", "11": "The Prophet's Disobedience"},
    "14": {"1": "Ahijah's Prophecy Against Jeroboam", "21": "Rehoboam's Reign in Judah"},
    "15": {"1": "Abijam's Reign in Judah", "9": "Asa's Reign in Judah", "25": "Nadab's Reign in Israel", "33": "Baasha's Reign in Israel"},
    "16": {"1": "Prophecy Against Baasha", "8": "Elah's Reign in Israel", "15": "Zimri's Reign in Israel", "21": "Omri's Reign in Israel", "29": "Ahab's Reign in Israel"},
    "17": {"1": "Elijah Fed by Ravens", "8": "The Widow of Zarephath", "17": "Elijah Raises the Widow's Son"},
    "18": {"1": "Elijah and Obadiah", "16": "Elijah on Mount Carmel", "41": "The Coming of Rain"},
    "19": {"1": "Elijah Flees to Horeb", "9": "The Lord Appears to Elijah", "19": "The Call of Elisha"},
    "20": {"1": "Ben-Hadad Attacks Samaria", "13": "Ahab Defeats Ben-Hadad", "23": "Another Victory Over Ben-Hadad", "35": "A Prophet Condemns Ahab"},
    "21": {"1": "Naboth's Vineyard", "17": "Elijah Condemns Ahab"},
    "22": {"1": "Micaiah Prophesies Against Ahab", "29": "The Death of Ahab", "41": "Jehoshaphat's Reign in Judah", "51": "Ahaziah's Reign in Israel"}
  },
  "2 Kings": {
    "1": {"1": "Elijah and the Messengers of Ahaziah"},
    "2": {"1": "Elijah Taken Up to Heaven", "13": "Elisha Succeeds Elijah", "19": "Elisha Heals the Water", "23": "Elisha and the Youths"},
    "3": {"1": "Moab Rebels", "4": "Joram Seeks Elisha's Help", "21": "Moab's Defeat"},
    "4": {"1": "The Widow's Oil", "8": "The Shunammite Woman's Son", "38": "Death in the Pot", "42": "Feeding of a Hundred"},
    "5": {"1": "Naaman Healed of Leprosy", "19": "Gehazi's Greed and Punishment"},
    "6": {"1": "The Floating Ax Head", "8": "Elisha Traps Blinded Arameans", "24": "The Siege of Samaria"},
    "7": {"1": "The Siege Lifted"},
    "8": {"1": "The Shunammite's Land Restored", "7": "Hazael Murders Ben-Hadad", "16": "Jehoram's Reign in Judah", "25": "Ahaziah's Reign in Judah"},
    "9": {"1": "Jehu Anointed King of Israel", "14": "Jehu Kills Joram", "30": "The Death of Jezebel"},
    "10": {"1": "Ahab's Family Killed", "18": "Jehu Destroys Baal Worship", "29": "The Death of Jehu"},
    "11": {"1": "Athaliah and Joash", "13": "The Death of Athaliah", "17": "Jehoiada's Reforms"},
    "12": {"1": "Joash Repairs the Temple", "17": "Joash's Death"},
    "13": {"1": "Jehoahaz's Reign in Israel", "10": "Jehoash's Reign in Israel", "14": "The Death of Elisha", "22": "Jehoash Defeats Aram"},
    "14": {"1": "Amaziah's Reign in Judah", "8": "War Between Judah and Israel", "23": "Jeroboam II's Reign in Israel", "28": "Azariah's Reign in Judah"},
    "15": {"1": "Azariah's Reign in Judah", "8": "Zechariah's Reign in Israel", "13": "Shallum's Reign in Israel", "17": "Menahem's Reign in Israel", "23": "Pekahiah's Reign in Israel", "27": "Pekah's Reign in Israel", "32": "Jotham's Reign in Judah"},
    "16": {"1": "Ahaz's Reign in Judah", "7": "Ahaz Seeks Help from Assyria", "10": "The New Altar"},
    "17": {"1": "Hoshea's Reign in Israel", "5": "Israel Exiled to Assyria", "24": "Samaria Resettled"},
    "18": {"1": "Hezekiah's Reign in Judah", "9": "The Fall of Samaria", "13": "Sennacherib Threatens Jerusalem"},
    "19": {"1": "Hezekiah Seeks Isaiah's Help", "8": "Sennacherib's Fall Prophesied", "20": "Hezekiah's Prayer", "35": "Jerusalem Delivered"},
    "20": {"1": "Hezekiah's Illness and Recovery", "12": "Envoys from Babylon"},
    "21": {"1": "Manasseh's Reign in Judah", "19": "Amon's Reign in Judah"},
    "22": {"1": "Josiah's Reign in Judah", "8": "The Book of the Law Found"},
    "23": {"1": "Josiah's Reforms", "29": "Josiah's Death", "31": "Jehoahaz's Reign in Judah", "36": "Jehoiakim's Reign in Judah"},
    "24": {"1": "Jehoiakim's Rebellion", "8": "Jehoiachin's Reign in Judah", "18": "Zedekiah's Reign in Judah"},
    "25": {"1": "The Fall of Jerusalem", "8": "The Temple Destroyed", "22": "Gedaliah Appointed Governor", "27": "Jehoiachin Released"}
  },
  "1 Chronicles": {
    "1": {"1": "From Adam to Abraham", "28": "The Family of Abraham", "43": "The Kings of Edom"},
    "2": {"1": "The Sons of Israel", "18": "The Descendants of Hezron", "42": "The Descendants of Caleb"},
    "3": {"1": "The Sons of David", "10": "The Royal Line After Solomon"},
    "4": {"1": "Other Descendants of Judah", "24": "The Descendants of Simeon"},
    "5": {"1": "The Descendants of Reuben", "11": "The Descendants of Gad", "23": "The Half-Tribe of Manasseh"},
    "6": {"1": "The Descendants of Levi", "49": "The Descendants of Aaron", "54": "The Levite Towns"},
    "7": {"1": "The Descendants of Issachar", "6": "The Descendants of Benjamin", "13": "The Descendants of Naphtali", "14": "The Descendants of Manasseh", "20": "The Descendants of Ephraim", "30": "The Descendants of Asher"},
    "8": {"1": "The Genealogy of Saul"},
    "9": {"1": "Those Who Returned from Exile", "35": "The Genealogy of Saul"},
    "10": {"1": "Saul's Death"},
    "11": {"1": "David Becomes King Over Israel", "4": "David Captures Jerusalem", "10": "David's Mighty Warriors"},
    "12": {"1": "Warriors Join David", "23": "David's Army at Hebron"},
    "13": {"1": "The Ark Brought from Kiriath Jearim"},
    "14": {"1": "David's Palace and Family", "8": "David Defeats the Philistines"},
    "15": {"1": "Preparations to Move the Ark", "25": "The Ark Brought to Jerusalem"},
    "16": {"1": "David's Psalm of Thanks", "37": "Worship Before the Ark"},
    "17": {"1": "God's Covenant with David"},
    "18": {"1": "David's Military Victories", "14": "David's Officials"},
    "19": {"1": "War with the Ammonites and Arameans"},
    "20": {"1": "The Capture of Rabbah", "4": "Wars Against the Philistines"},
    "21": {"1": "David's Census", "7": "Judgment for the Census", "18": "David Builds an Altar"},
    "22": {"1": "Preparations for the Temple", "6": "David's Charge to Solomon"},
    "23": {"1": "The Levites Organized", "6": "The Gershonites", "12": "The Kohathites", "21": "The Merarites", "24": "The Work of the Levites"},
    "24": {"1": "The Divisions of the Priests", "20": "The Rest of the Levites"},
    "25": {"1": "The Musicians"},
    "26": {"1": "The Gatekeepers", "20": "The Treasurers and Other Officials"},
    "27": {"1": "The Army Divisions", "16": "The Leaders of the Tribes", "25": "The King's Overseers"},
    "28": {"1": "David's Plans for the Temple", "9": "David's Charge to Solomon"},
    "29": {"1": "Gifts for Building the Temple", "10": "David's Prayer", "20": "Solomon Acknowledged as King", "26": "The Death of David"}
  },
  "2 Chronicles": {
    "1": {"1": "Solomon Asks for Wisdom", "13": "Solomon's Wealth and Splendor"},
    "2": {"1": "Preparations for Building the Temple"},
    "3": {"1": "Solomon Builds the Temple"},
    "4": {"1": "The Temple Furnishings"},
    "5": {"1": "The Ark Brought to the Temple"},
    "6": {"1": "Solomon's Address to the People", "12": "Solomon's Prayer of Dedication"},
    "7": {"1": "The Dedication of the Temple", "11": "The Lord Appears to Solomon"},
    "8": {"1": "Solomon's Other Activities"},
    "9": {"1": "The Queen of Sheba Visits", "13": "Solomon's Splendor", "29": "Solomon's Death"},
    "10": {"1": "Israel Rebels Against Rehoboam"},
    "11": {"1": "Rehoboam Fortifies Judah", "13": "The Priests and Levites Come to Judah"},
    "12": {"1": "Shishak Attacks Jerusalem", "13": "Summary of Rehoboam's Reign"},
    "13": {"1": "Abijah's Reign in Judah", "3": "War Between Abijah and Jeroboam"},
    "14": {"1": "Asa's Reign in Judah", "9": "Asa Defeats the Cushites"},
    "15": {"1": "Asa's Reform", "16": "Asa's Later Years"},
    "16": {"1": "Asa's Treaty with Aram", "11": "The Death of Asa"},
    "17": {"1": "Jehoshaphat's Greatness", "7": "Teaching the Law Throughout Judah"},
    "18": {"1": "Micaiah Prophesies Against Ahab", "28": "The Death of Ahab"},
    "19": {"1": "Jehoshaphat Rebuked by Jehu", "4": "Jehoshaphat Appoints Judges"},
    "20": {"1": "Jehoshaphat Defeats Moab and Ammon", "31": "The End of Jehoshaphat's Reign"},
    "21": {"1": "Jehoram's Reign in Judah", "12": "Elijah's Letter to Jehoram", "18": "Jehoram's Death"},
    "22": {"1": "Ahaziah's Reign in Judah", "7": "The Death of Ahaziah", "10": "Athaliah Rules Judah"},
    "23": {"1": "Joash Made King", "12": "The Death of Athaliah", "16": "Jehoiada's Reforms"},
    "24": {"1": "Joash Repairs the Temple", "15": "The Death of Jehoiada", "17": "The Wickedness of Joash", "23": "The Death of Joash"},
    "25": {"1": "Amaziah's Reign in Judah", "5": "Amaziah's Victory Over Edom", "14": "Amaziah's Idolatry", "17": "War Between Judah and Israel", "25": "The Death of Amaziah"},
    "26": {"1": "Uzziah's Reign in Judah", "16": "Uzziah's Pride and Punishment"},
    "27": {"1": "Jotham's Reign in Judah"},
    "28": {"1": "Ahaz's Reign in Judah", "5": "Judah Defeated by Aram and Israel", "16": "Ahaz Seeks Help from Assyria", "22": "Ahaz's Further Sins"},
    "29": {"1": "Hezekiah's Reign and Reforms", "20": "The Temple Reconsecrated"},
    "30": {"1": "Hezekiah Celebrates the Passover"},
    "31": {"1": "Hezekiah's Religious Reforms", "2": "Contributions for Worship"},
    "32": {"1": "Sennacherib Threatens Jerusalem", "20": "Jerusalem Delivered", "24": "Hezekiah's Illness and Pride", "32": "Hezekiah's Death"},
    "33": {"1": "Manasseh's Reign in Judah", "11": "Manasseh's Repentance", "21": "Amon's Reign in Judah"},
    "34": {"1": "Josiah's Reign in Judah", "3": "Josiah's Reforms", "14": "The Book of the Law Found"},
    "35": {"1": "Josiah Celebrates the Passover", "20": "The Death of Josiah"},
    "36": {"1": "Jehoahaz's Reign in Judah", "5": "Jehoiakim's Reign in Judah", "9": "Jehoiachin's Reign in Judah", "11": "Zedekiah's Reign in Judah", "15": "The Fall of Jerusalem", "22": "The Proclamation of Cyrus"}
  },
  "Ezra": {
    "1": {"1": "Cyrus Helps the Exiles Return"},
    "2": {"1": "The List of the Exiles Who Returned"},
    "3": {"1": "The Altar Rebuilt", "7": "Rebuilding the Temple Begins", "10": "Opposition to the Rebuilding"},
    "4": {"1": "Enemies Oppose the Rebuilding", "6": "Later Opposition Under Xerxes and Artaxerxes"},
    "5": {"1": "The Rebuilding Resumed", "3": "Tattenai's Letter to Darius"},
    "6": {"1": "The Decree of Darius", "13": "The Temple Completed", "19": "The Passover Celebrated"},
    "7": {"1": "Ezra Comes to Jerusalem", "11": "Artaxerxes' Letter to Ezra", "27": "Ezra Praises God"},
    "8": {"1": "The List of Those Returning with Ezra", "21": "Ezra's Journey to Jerusalem"},
    "9": {"1": "Ezra's Prayer About Intermarriage"},
    "10": {"1": "The People's Response", "9": "The Assembly", "18": "Those Guilty of Intermarriage"}
  },
  "Nehemiah": {
    "1": {"1": "Nehemiah's Prayer for Jerusalem"},
    "2": {"1": "Nehemiah Sent to Jerusalem", "11": "Nehemiah Inspects the Walls"},
    "3": {"1": "The Builders of the Wall"},
    "4": {"1": "Opposition to the Rebuilding", "15": "The Work Continues"},
    "5": {"1": "Nehemiah Helps the Poor", "14": "Nehemiah's Generosity"},
    "6": {"1": "The Enemies' Plot Against Nehemiah", "15": "The Wall Completed"},
    "7": {"1": "The List of Exiles Who Returned", "73": "The People Settle in Their Towns"},
    "8": {"1": "Ezra Reads the Law", "13": "The Festival of Tabernacles"},
    "9": {"1": "The Israelites Confess Their Sins", "5": "A Prayer of Confession", "38": "The Agreement of the People"},
    "10": {"1": "Those Who Sealed the Covenant", "28": "The Obligations of the Covenant"},
    "11": {"1": "The New Residents of Jerusalem", "25": "The People in Other Towns"},
    "12": {"1": "The Priests and Levites", "27": "The Dedication of the Wall"},
    "13": {"1": "Nehemiah's Final Reforms", "4": "The Priest Eliashib and Tobiah", "10": "Nehemiah Restores Support for the Levites", "15": "The Sabbath Restored", "23": "Mixed Marriages Prohibited"}
  },
  "Esther": {
    "1": {"1": "Queen Vashti Deposed"},
    "2": {"1": "Esther Made Queen", "19": "Mordecai Uncovers a Conspiracy"},
    "3": {"1": "Haman's Plot to Destroy the Jews"},
    "4": {"1": "Mordecai Persuades Esther to Help"},
    "5": {"1": "Esther's First Banquet", "9": "Haman's Rage Against Mordecai"},
    "6": {"1": "Mordecai Honored"},
    "7": {"1": "Haman Hanged"},
    "8": {"1": "The King's Edict in Behalf of the Jews"},
    "9": {"1": "The Triumph of the Jews", "20": "The Festival of Purim Instituted"},
    "10": {"1": "The Greatness of Mordecai"}
  }
}
all_headings.update(historical)

# Wisdom books
wisdom = {
  "Job": {
    "1": {"1": "Job's Character and Wealth", "13": "Satan's First Attack"},
    "2": {"1": "Satan's Second Attack", "11": "Job's Three Friends Arrive"},
    "3": {"1": "Job Curses the Day of His Birth"},
    "4": {"1": "Eliphaz's First Speech: The Innocent Do Not Suffer"},
    "5": {"1": "Eliphaz Continues: God Disciplines Those He Loves"},
    "6": {"1": "Job's Reply: My Complaint Is Just"},
    "7": {"1": "Job Continues: Life Is Hard and Brief"},
    "8": {"1": "Bildad's First Speech: God Is Just"},
    "9": {"1": "Job's Reply: How Can Man Be Right Before God?"},
    "10": {"1": "Job Continues: Why Have You Made Me Your Target?"},
    "11": {"1": "Zophar's First Speech: Can You Fathom the Mysteries of God?"},
    "12": {"1": "Job's Reply: I Am Not Inferior to You", "13": "Wisdom Belongs to God Alone"},
    "13": {"1": "Job Continues: Let Me Speak to the Almighty", "13": "I Will Argue My Case Before God"},
    "14": {"1": "Job Continues: Man Born of Woman Has Few Days"},
    "15": {"1": "Eliphaz's Second Speech: The Wicked Suffer All Their Days"},
    "16": {"1": "Job's Reply: Miserable Comforters Are You All", "18": "My Witness Is in Heaven"},
    "17": {"1": "Job Continues: My Spirit Is Broken"},
    "18": {"1": "Bildad's Second Speech: The Fate of the Wicked"},
    "19": {"1": "Job's Reply: How Long Will You Torment Me?", "23": "I Know That My Redeemer Lives"},
    "20": {"1": "Zophar's Second Speech: The Triumph of the Wicked Is Short"},
    "21": {"1": "Job's Reply: Why Do the Wicked Prosper?"},
    "22": {"1": "Eliphaz's Third Speech: Can a Man Be of Use to God?"},
    "23": {"1": "Job's Reply: Oh, That I Knew Where to Find Him!"},
    "24": {"1": "Job Continues: Why Are Times Not Set by the Almighty?"},
    "25": {"1": "Bildad's Third Speech: How Can Man Be Righteous?"},
    "26": {"1": "Job's Reply: God's Power and Wisdom"},
    "27": {"1": "Job Continues: I Will Maintain My Integrity"},
    "28": {"1": "Job's Hymn to Wisdom: Where Can Wisdom Be Found?"},
    "29": {"1": "Job's Final Defense: My Life in the Past"},
    "30": {"1": "Job Continues: But Now They Mock Me"},
    "31": {"1": "Job Continues: I Have Made a Covenant with My Eyes", "35": "Job's Final Plea"},
    "32": {"1": "Elihu's First Speech: I Will Speak"},
    "33": {"1": "Elihu Continues: Hear My Words", "14": "God Speaks in Many Ways"},
    "34": {"1": "Elihu's Second Speech: God Is Just"},
    "35": {"1": "Elihu's Third Speech: Does Your Sin Affect God?"},
    "36": {"1": "Elihu's Fourth Speech: God Is Great and Just", "22": "God's Majesty Is Beyond Understanding"},
    "37": {"1": "Elihu Continues: God's Mighty Works in Nature"},
    "38": {"1": "The Lord Answers Job: Where Were You?", "25": "God Questions Job About Nature"},
    "39": {"1": "God Continues: Can You Control the Animals?"},
    "40": {"1": "The Lord Continues: Will You Condemn Me?", "15": "Behold Behemoth"},
    "41": {"1": "God Describes Leviathan"},
    "42": {"1": "Job's Repentance and Restoration", "7": "The Lord Rebukes Job's Friends", "10": "Job's Fortunes Restored"}
  },
  "Proverbs": {
    "1": {"1": "The Purpose of Proverbs", "8": "Warning Against Enticement", "20": "Wisdom's Call in the Streets"},
    "2": {"1": "The Benefits of Wisdom"},
    "3": {"1": "Trust in the Lord with All Your Heart", "13": "Blessed Is the One Who Finds Wisdom", "27": "Instructions for Daily Living"},
    "4": {"1": "A Father's Instruction: Get Wisdom", "14": "Avoid the Path of the Wicked", "20": "Guard Your Heart Above All Else"},
    "5": {"1": "Warning Against Adultery", "15": "Drink Water from Your Own Cistern"},
    "6": {"1": "Warnings Against Surety and Sloth", "12": "The Worthless Person", "16": "Seven Things the Lord Hates", "20": "Warning Against Adultery Continues"},
    "7": {"1": "A Father's Warning Against the Adulterous Woman"},
    "8": {"1": "Wisdom's Call", "22": "Wisdom's Role in Creation"},
    "9": {"1": "Wisdom Has Built Her House", "13": "The Way of Folly"},
    "10": {"1": "The Proverbs of Solomon: The Wise Son and the Foolish Son"},
    "11": {"1": "Proverbs Contrasting Righteousness and Wickedness"},
    "12": {"1": "Proverbs on Wisdom and Folly"},
    "13": {"1": "Proverbs on Discipline and Wealth"},
    "14": {"1": "Proverbs on Wisdom and Fear of the Lord"},
    "15": {"1": "Proverbs on the Power of Words"},
    "16": {"1": "Proverbs on the Lord's Sovereignty"},
    "17": {"1": "Proverbs on Family and Friendship"},
    "18": {"1": "Proverbs on Speech and Relationships"},
    "19": {"1": "Proverbs on Wealth and Poverty"},
    "20": {"1": "Proverbs on Justice and the King"},
    "21": {"1": "Proverbs on the King and Righteousness"},
    "22": {"1": "Proverbs on Reputation and Child-Rearing", "17": "Thirty Sayings of the Wise"},
    "23": {"1": "Sayings of the Wise Continue", "19": "Do Not Envy Sinners", "29": "Woe to Those Who Linger Over Wine"},
    "24": {"1": "More Sayings of the Wise", "23": "Further Sayings of the Wise"},
    "25": {"1": "More Proverbs of Solomon: Proverbs About Kings"},
    "26": {"1": "Proverbs About Fools", "13": "Proverbs About Sluggards", "17": "Proverbs About Meddlers and Quarrels"},
    "27": {"1": "Proverbs on Friendship and Prudence"},
    "28": {"1": "Proverbs on Justice and Righteousness"},
    "29": {"1": "Proverbs on Leadership and Discipline"},
    "30": {"1": "The Words of Agur: I Am Weary, O God", "7": "Four Requests", "11": "Four Generations of Wicked People", "15": "Four Insatiable Things", "18": "Four Wonderful Things", "21": "Four Things That Are Unbearable", "24": "Four Small but Wise Creatures", "29": "Four Stately Things"},
    "31": {"1": "The Words of King Lemuel", "10": "The Excellent Wife"}
  },
  "Ecclesiastes": {
    "1": {"1": "Vanity of Vanities", "12": "The Preacher's Quest for Meaning"},
    "2": {"1": "The Futility of Pleasure and Possessions", "12": "The Futility of Wisdom", "18": "The Futility of Labor"},
    "3": {"1": "A Time for Everything", "11": "God's Works Are Eternal", "16": "Injustice and the Judgment to Come"},
    "4": {"1": "The Vanity of Labor and Isolation", "13": "Wisdom Is Better Than Folly"},
    "5": {"1": "Fear God and Keep Your Vows", "8": "The Vanity of Wealth"},
    "6": {"1": "The Vanity of Wealth Without Enjoyment"},
    "7": {"1": "Wisdom and Folly Compared", "15": "The Limits of Human Wisdom"},
    "8": {"1": "Obey the King", "10": "The Wicked Prosper While the Righteous Suffer"},
    "9": {"1": "Death Comes to All", "13": "Wisdom Is Better Than Strength"},
    "10": {"1": "The Folly of Fools"},
    "11": {"1": "Cast Your Bread Upon the Waters", "7": "Rejoice in Your Youth"},
    "12": {"1": "Remember Your Creator in Your Youth", "9": "The Conclusion of the Matter"}
  },
  "Song of Solomon": {
    "1": {"1": "The Bride's Longing for Her Beloved", "9": "Solomon Praises His Beloved"},
    "2": {"1": "The Bride and the Bridegroom Rejoice", "8": "The Bride Hears Her Beloved", "14": "The Bridegroom Speaks to His Beloved"},
    "3": {"1": "The Bride's Dream", "6": "Solomon Arrives in His Splendor"},
    "4": {"1": "Solomon Praises His Beloved", "12": "The Bride Is a Garden Locked"},
    "5": {"1": "The Bridegroom Comes to His Garden", "2": "The Bride's Dream of Separation", "10": "The Bride Praises Her Beloved"},
    "6": {"1": "Others Ask Where the Beloved Has Gone", "4": "Solomon Praises His Beloved Again", "11": "The Bride Returns to the Garden"},
    "7": {"1": "Solomon Praises the Shulamite's Beauty", "10": "The Bride's Longing for Her Beloved"},
    "8": {"1": "The Bride Yearns for Her Beloved", "8": "The Bride's Brothers Speak", "11": "Solomon's Vineyard"}
  }
}
all_headings.update(wisdom)

# Minor prophets
minor_prophets = {
  "Hosea": {
    "1": {"1": "Hosea's Unfaithful Wife"},
    "2": {"1": "Israel's Unfaithfulness", "14": "God's Promise of Restoration"},
    "3": {"1": "Hosea Redeems His Wife"},
    "4": {"1": "The Charge Against Israel"},
    "5": {"1": "Judgment on Israel and Judah"},
    "6": {"1": "Israel's Insincere Repentance", "4": "The Sins of Israel and Judah"},
    "7": {"1": "Israel's Wickedness Exposed"},
    "8": {"1": "Israel Reaps the Whirlwind"},
    "9": {"1": "Punishment for Israel's Sin"},
    "10": {"1": "Judgment for Israel's Idolatry"},
    "11": {"1": "God's Love for Israel", "8": "God's Compassion Prevails"},
    "12": {"1": "The Lord's Charge Against Judah"},
    "13": {"1": "The Lord's Anger Against Israel"},
    "14": {"1": "A Plea to Return to the Lord", "4": "God's Promise of Healing"}
  },
  "Joel": {
    "1": {"1": "The Locust Plague", "13": "A Call to Repentance"},
    "2": {"1": "The Day of the Lord", "12": "Return to the Lord", "28": "The Promise of the Spirit"},
    "3": {"1": "Judgment on the Nations", "9": "The Valley of Decision", "18": "Blessings for God's People"}
  },
  "Amos": {
    "1": {"1": "Judgment on Israel's Neighbors"},
    "2": {"1": "Judgment on Judah and Israel", "6": "Israel's Guilt and Punishment"},
    "3": {"1": "Witnesses Against Israel"},
    "4": {"1": "Israel's Failure to Return to God"},
    "5": {"1": "A Lament for Israel", "18": "The Day of the Lord"},
    "6": {"1": "Woe to the Complacent"},
    "7": {"1": "Visions of Judgment", "10": "Amos and Amaziah"},
    "8": {"1": "The Vision of Ripe Fruit", "4": "The Coming Famine"},
    "9": {"1": "Israel to Be Destroyed", "11": "Israel's Restoration"}
  },
  "Obadiah": {
    "1": {"1": "The Doom of Edom", "15": "The Day of the Lord"}
  },
  "Jonah": {
    "1": {"1": "Jonah Flees from the Lord", "4": "The Great Storm"},
    "2": {"1": "Jonah's Prayer from the Fish"},
    "3": {"1": "Jonah Goes to Nineveh", "5": "Nineveh Repents"},
    "4": {"1": "Jonah's Anger at the Lord's Mercy", "5": "The Lord's Lesson"}
  },
  "Micah": {
    "1": {"1": "Judgment Against Samaria and Jerusalem"},
    "2": {"1": "Woe to Oppressors", "12": "Promise of Deliverance"},
    "3": {"1": "Leaders and Prophets Rebuked"},
    "4": {"1": "The Mountain of the Lord", "9": "The Lord's Plan and Deliverance"},
    "5": {"1": "The Ruler from Bethlehem", "5": "Deliverance and Judgment"},
    "6": {"1": "The Lord's Case Against Israel", "6": "What the Lord Requires"},
    "7": {"1": "Israel's Misery and Hope", "7": "Prayer and Praise", "14": "God's Compassion on Israel"}
  },
  "Nahum": {
    "1": {"1": "The Lord's Anger Against Nineveh", "7": "The Lord is Good"},
    "2": {"1": "Nineveh to Fall"},
    "3": {"1": "Woe to Nineveh", "8": "Nineveh's Inevitable Destruction"}
  },
  "Habakkuk": {
    "1": {"1": "Habakkuk's Complaint", "5": "The Lord's Answer", "12": "Habakkuk's Second Complaint"},
    "2": {"1": "The Lord's Second Answer", "6": "Woe to the Wicked"},
    "3": {"1": "Habakkuk's Prayer", "16": "Rejoicing in the Lord"}
  },
  "Zephaniah": {
    "1": {"1": "The Great Day of the Lord"},
    "2": {"1": "A Call to Repentance", "4": "Judgment on the Nations"},
    "3": {"1": "Woe to Jerusalem", "8": "Jerusalem's Restoration", "14": "Song of Joy"}
  },
  "Haggai": {
    "1": {"1": "A Call to Rebuild the Temple"},
    "2": {"1": "The Glory of the New Temple", "10": "Blessings for a Defiled People", "20": "Zerubbabel the Lord's Signet Ring"}
  },
  "Zechariah": {
    "1": {"1": "A Call to Return to the Lord", "7": "The Vision of the Horses"},
    "2": {"1": "The Vision of the Measuring Line", "6": "The Call to Flee Babylon"},
    "3": {"1": "The Vision of Joshua the High Priest"},
    "4": {"1": "The Vision of the Golden Lampstand"},
    "5": {"1": "The Vision of the Flying Scroll", "5": "The Vision of the Woman in the Basket"},
    "6": {"1": "The Vision of the Four Chariots", "9": "The Crowning of Joshua"},
    "7": {"1": "Justice and Mercy, Not Fasting"},
    "8": {"1": "The Lord's Promises to Zion", "18": "Joyful Fasting"},
    "9": {"1": "Judgment on Israel's Enemies", "9": "The Coming King"},
    "10": {"1": "The Lord Will Restore Israel"},
    "11": {"1": "The Shepherds of Israel", "4": "The Two Shepherds"},
    "12": {"1": "Jerusalem's Enemies to Be Destroyed", "10": "Mourning for the Pierced One"},
    "13": {"1": "Cleansing from Sin", "7": "The Shepherd Struck"},
    "14": {"1": "The Coming Day of the Lord", "9": "The Lord's Reign", "16": "The Nations Worship the King"}
  },
  "Malachi": {
    "1": {"1": "The Lord's Love for Israel", "6": "Defiled Offerings"},
    "2": {"1": "Warning to the Priests", "10": "Judah's Unfaithfulness"},
    "3": {"1": "The Messenger of the Covenant", "6": "Robbing God", "13": "The Book of Remembrance"},
    "4": {"1": "The Day of the Lord", "4": "Remember the Law of Moses"}
  }
}
all_headings.update(minor_prophets)

# NT Epistles Part 1
epistles1 = {
  "Acts": {
    "1": {"1": "The Promise of the Holy Spirit", "6": "The Ascension", "12": "Matthias Chosen to Replace Judas"},
    "2": {"1": "The Day of Pentecost", "14": "Peter's Sermon at Pentecost", "37": "Three Thousand Converted"},
    "3": {"1": "A Lame Man Healed", "11": "Peter's Second Sermon"},
    "4": {"1": "Peter and John Before the Council", "23": "The Believers Pray for Boldness", "32": "Believers Share All Things"},
    "5": {"1": "Ananias and Sapphira", "12": "Many Signs and Wonders", "27": "The Apostles Before the Council"},
    "6": {"1": "Seven Chosen to Serve", "8": "Stephen's Arrest"},
    "7": {"1": "Stephen's Defense Before the Council", "54": "The Stoning of Stephen"},
    "8": {"1": "Saul Persecutes the Church", "4": "Philip Preaches in Samaria", "26": "Philip and the Ethiopian Eunuch"},
    "9": {"1": "The Conversion of Saul", "19": "Saul Preaches in Damascus", "32": "Peter Heals Aeneas and Raises Dorcas"},
    "10": {"1": "Cornelius Sends for Peter", "17": "Peter's Vision", "34": "Peter Preaches to the Gentiles"},
    "11": {"1": "Peter's Report to the Church", "19": "The Church in Antioch"},
    "12": {"1": "James Killed and Peter Imprisoned", "6": "Peter's Miraculous Escape", "20": "The Death of Herod"},
    "13": {"1": "Barnabas and Saul Sent Out", "13": "Paul Preaches in Antioch of Pisidia", "44": "Paul Turns to the Gentiles"},
    "14": {"1": "Paul and Barnabas in Iconium", "8": "A Cripple Healed at Lystra", "21": "The Return to Antioch"},
    "15": {"1": "The Jerusalem Council", "22": "The Council's Letter to Gentile Believers", "36": "Paul and Barnabas Separate"},
    "16": {"1": "Timothy Joins Paul and Silas", "6": "The Macedonian Call", "16": "Paul and Silas in Prison"},
    "17": {"1": "Uproar in Thessalonica", "10": "Paul in Berea", "16": "Paul in Athens"},
    "18": {"1": "Paul in Corinth", "18": "Paul Returns to Antioch", "24": "Apollos Speaks Boldly in Ephesus"},
    "19": {"1": "Paul in Ephesus", "11": "The Sons of Sceva", "23": "The Riot in Ephesus"},
    "20": {"1": "Paul in Macedonia and Greece", "7": "Eutychus Raised from the Dead", "17": "Paul's Farewell to the Ephesian Elders"},
    "21": {"1": "Paul's Journey to Jerusalem", "17": "Paul Visits James", "27": "Paul Arrested in the Temple"},
    "22": {"1": "Paul's Defense Before the Crowd", "22": "Paul and the Roman Tribune"},
    "23": {"1": "Paul Before the Council", "12": "A Plot to Kill Paul", "23": "Paul Sent to Felix"},
    "24": {"1": "Paul Before Felix", "22": "Paul Held in Custody"},
    "25": {"1": "Paul Appeals to Caesar", "13": "Paul Before Agrippa and Bernice"},
    "26": {"1": "Paul's Defense Before Agrippa", "19": "Paul Recounts His Conversion and Calling"},
    "27": {"1": "Paul Sails for Rome", "13": "The Storm at Sea", "27": "The Shipwreck"},
    "28": {"1": "Paul on Malta", "11": "Paul Arrives at Rome", "17": "Paul Preaches in Rome"}
  },
  "Romans": {
    "1": {"1": "Greeting", "8": "Paul's Desire to Visit Rome", "16": "The Power of the Gospel", "18": "God's Wrath Against Sin"},
    "2": {"1": "God's Righteous Judgment", "17": "The Jews and the Law"},
    "3": {"1": "God's Faithfulness", "9": "No One is Righteous", "21": "Righteousness Through Faith in Christ"},
    "4": {"1": "Abraham Justified by Faith", "13": "The Promise Through Faith"},
    "5": {"1": "Peace with God Through Faith", "12": "Death Through Adam, Life Through Christ"},
    "6": {"1": "Dead to Sin, Alive in Christ", "15": "Slaves to Righteousness"},
    "7": {"1": "Released from the Law", "7": "The Law and Sin", "14": "The Struggle with Sin"},
    "8": {"1": "Life in the Spirit", "18": "Future Glory", "28": "God's Love in Christ Jesus"},
    "9": {"1": "God's Sovereign Choice", "14": "God's Mercy", "30": "Israel's Unbelief"},
    "10": {"1": "Righteousness by Faith", "14": "The Message for All People"},
    "11": {"1": "A Remnant of Israel", "11": "Gentiles Grafted In", "25": "The Mystery of Israel's Salvation", "33": "A Hymn to God's Wisdom"},
    "12": {"1": "Living Sacrifices", "3": "Gifts of Grace", "9": "Marks of the True Christian"},
    "13": {"1": "Submission to Authorities", "8": "Love Fulfills the Law", "11": "Put On the Lord Jesus Christ"},
    "14": {"1": "Do Not Pass Judgment", "13": "Do Not Cause Another to Stumble"},
    "15": {"1": "Bear with the Weak", "7": "Christ the Hope of Jews and Gentiles", "14": "Paul's Ministry to the Gentiles", "22": "Paul's Plan to Visit Rome"},
    "16": {"1": "Personal Greetings", "17": "Final Instructions and Greetings", "25": "Doxology"}
  },
  "1 Corinthians": {
    "1": {"1": "Greeting", "10": "Divisions in the Church", "18": "The Wisdom of God"},
    "2": {"1": "Proclaiming Christ Crucified", "6": "The Wisdom of the Spirit"},
    "3": {"1": "Divisions in the Church", "10": "Christ Our Foundation", "16": "God's Temple and God's Wisdom"},
    "4": {"1": "The Ministry of Apostles", "14": "Paul's Fatherly Admonition"},
    "5": {"1": "Sexual Immorality Judged", "9": "Cleanse Out the Old Leaven"},
    "6": {"1": "Lawsuits Among Believers", "12": "Glorify God in Your Body"},
    "7": {"1": "Principles for Marriage", "17": "Living in the Calling of God", "25": "The Unmarried and Widowed"},
    "8": {"1": "Food Offered to Idols", "7": "Do Not Cause Another to Stumble"},
    "9": {"1": "Paul's Rights as an Apostle", "19": "Paul's Self-Discipline"},
    "10": {"1": "Warning Against Idolatry", "14": "Flee from Idolatry", "23": "Do All to the Glory of God"},
    "11": {"1": "Head Coverings", "17": "Abuses at the Lord's Supper", "23": "The Institution of the Lord's Supper"},
    "12": {"1": "Concerning Spiritual Gifts", "12": "One Body with Many Members"},
    "13": {"1": "The Way of Love", "8": "Love Never Ends"},
    "14": {"1": "Prophecy and Tongues", "20": "Orderly Worship", "26": "Orderly Worship"},
    "15": {"1": "The Resurrection of Christ", "12": "The Resurrection of the Dead", "35": "The Resurrection Body", "50": "Victory Over Death"},
    "16": {"1": "The Collection for the Saints", "5": "Paul's Plans", "13": "Final Exhortations and Greetings"}
  },
  "2 Corinthians": {
    "1": {"1": "Greeting", "3": "God of All Comfort", "12": "Paul's Change of Plans"},
    "2": {"1": "Forgive the Sinner", "12": "Triumph in Christ"},
    "3": {"1": "Ministers of the New Covenant", "12": "The Glory of the New Covenant"},
    "4": {"1": "The Light of the Gospel", "7": "Treasure in Jars of Clay", "16": "Our Heavenly Dwelling"},
    "5": {"1": "Our Heavenly Dwelling", "11": "The Ministry of Reconciliation"},
    "6": {"1": "The Temple of the Living God", "14": "Do Not Be Unequally Yoked"},
    "7": {"1": "Paul's Joy", "5": "Paul's Joy Over the Church's Repentance"},
    "8": {"1": "The Collection for the Saints", "16": "Commendation of Titus"},
    "9": {"1": "The Cheerful Giver", "6": "The Blessings of Generosity"},
    "10": {"1": "Paul Defends His Ministry", "7": "Paul's Authority"},
    "11": {"1": "Paul and the False Apostles", "16": "Paul's Sufferings as an Apostle"},
    "12": {"1": "Paul's Visions and Revelations", "7": "Paul's Thorn in the Flesh", "11": "Concern for the Corinthian Church", "19": "Final Warnings"},
    "13": {"1": "Final Warnings", "5": "Examine Yourselves", "11": "Final Greetings"}
  },
  "Galatians": {
    "1": {"1": "Greeting", "6": "No Other Gospel", "11": "Paul Called by God"},
    "2": {"1": "Paul Accepted by the Apostles", "11": "Paul Opposes Peter", "15": "Justified by Faith"},
    "3": {"1": "By Faith or by Works of the Law?", "15": "The Law and the Promise", "23": "Children of God Through Faith"},
    "4": {"1": "Sons and Heirs", "8": "Paul's Concern for the Galatians", "21": "The Example of Hagar and Sarah"},
    "5": {"1": "Christ Has Set Us Free", "13": "Freedom in Christ", "16": "Walking by the Spirit"},
    "6": {"1": "Bear One Another's Burdens", "7": "Reaping What You Sow", "11": "Final Warning and Benediction"}
  }
}
all_headings.update(epistles1)

# NT Epistles Part 2
epistles2 = {
  "Ephesians": {
    "1": {"1": "Greeting", "3": "Spiritual Blessings in Christ", "15": "Paul's Prayer for the Ephesians"},
    "2": {"1": "Made Alive in Christ", "11": "One in Christ", "19": "Christ Our Cornerstone"},
    "3": {"1": "The Mystery of the Gospel Revealed", "14": "Prayer for Spiritual Strength"},
    "4": {"1": "Unity in the Body of Christ", "7": "Spiritual Gifts for the Church", "17": "The New Life in Christ"},
    "5": {"1": "Walking in Love and Light", "15": "Filled with the Spirit", "22": "Wives and Husbands"},
    "6": {"1": "Children and Parents", "5": "Slaves and Masters", "10": "The Armor of God", "21": "Final Greetings"}
  },
  "Philippians": {
    "1": {"1": "Greeting", "3": "Thanksgiving and Prayer", "12": "Paul's Chains Advance the Gospel", "27": "Standing Firm in the Gospel"},
    "2": {"1": "Imitating Christ's Humility", "12": "Working Out Salvation", "19": "Timothy and Epaphroditus"},
    "3": {"1": "Warning Against False Teachers", "4": "Righteousness Through Faith in Christ", "12": "Pressing Toward the Goal"},
    "4": {"1": "Exhortations to Stand Firm", "4": "Rejoice in the Lord Always", "10": "God's Provision", "21": "Final Greetings"}
  },
  "Colossians": {
    "1": {"1": "Greeting", "3": "Thanksgiving and Prayer", "15": "The Supremacy of Christ", "24": "Paul's Ministry to the Church"},
    "2": {"1": "Paul's Concern for the Colossians", "6": "Freedom in Christ", "16": "Warning Against False Philosophy"},
    "3": {"1": "The New Life in Christ", "5": "Put to Death the Old Self", "12": "Put on the New Self", "18": "Christian Household Rules"},
    "4": {"1": "Masters and Slaves", "2": "Devoted to Prayer", "7": "Final Greetings and Instructions"}
  },
  "1 Thessalonians": {
    "1": {"1": "Greeting", "2": "Thanksgiving for the Thessalonians' Faith"},
    "2": {"1": "Paul's Ministry in Thessalonica", "13": "Thanksgiving for Reception of the Gospel", "17": "Paul's Longing to See the Thessalonians"},
    "3": {"1": "Timothy's Visit and Report", "6": "Encouragement from Timothy's Report", "11": "Prayer for the Thessalonians"},
    "4": {"1": "Living to Please God", "9": "Brotherly Love", "13": "The Coming of the Lord"},
    "5": {"1": "The Day of the Lord", "12": "Final Instructions and Exhortations", "23": "Benediction and Farewell"}
  },
  "2 Thessalonians": {
    "1": {"1": "Greeting", "3": "Thanksgiving and Prayer", "5": "God's Righteous Judgment"},
    "2": {"1": "The Day of the Lord", "13": "Stand Firm in the Gospel"},
    "3": {"1": "Request for Prayer", "6": "Warning Against Idleness", "16": "Final Greetings and Benediction"}
  },
  "1 Timothy": {
    "1": {"1": "Greeting", "3": "Warning Against False Teachers", "12": "God's Mercy to Paul", "18": "Charge to Timothy"},
    "2": {"1": "Instructions on Worship", "8": "Instructions for Men and Women"},
    "3": {"1": "Qualifications for Overseers", "8": "Qualifications for Deacons", "14": "The Mystery of Godliness"},
    "4": {"1": "Warning Against False Teachers", "6": "Training in Godliness", "12": "Timothy's Charge"},
    "5": {"1": "Instructions for Various Groups", "3": "Widows in the Church", "17": "Honoring Elders"},
    "6": {"1": "Instructions for Slaves", "3": "False Teachers and Love of Money", "11": "Fight the Good Fight of Faith", "17": "Instructions to the Rich", "20": "Guard the Deposit"}
  },
  "2 Timothy": {
    "1": {"1": "Greeting", "3": "Thanksgiving and Encouragement", "8": "Not Ashamed of the Gospel", "15": "Examples of Faithfulness and Unfaithfulness"},
    "2": {"1": "Be Strong in Grace", "8": "Remember Jesus Christ", "14": "A Worker Approved by God", "22": "Flee Youthful Passions"},
    "3": {"1": "Godlessness in the Last Days", "10": "Paul's Charge to Timothy", "14": "Abide in Scripture"},
    "4": {"1": "Preach the Word", "6": "Paul's Final Testimony", "9": "Personal Instructions", "19": "Final Greetings and Benediction"}
  },
  "Titus": {
    "1": {"1": "Greeting", "5": "Qualifications for Elders", "10": "Rebuke False Teachers"},
    "2": {"1": "Teach Sound Doctrine", "11": "The Grace of God Brings Salvation"},
    "3": {"1": "Do Good Works", "3": "Saved by God's Mercy", "9": "Avoid Foolish Controversies", "12": "Final Instructions and Greetings"}
  },
  "Philemon": {
    "1": {"1": "Greeting", "4": "Thanksgiving and Prayer", "8": "Paul's Plea for Onesimus", "17": "Paul's Appeal and Promise", "23": "Final Greetings and Benediction"}
  }
}
all_headings.update(epistles2)

# General Epistles and Revelation
general = {
  "Hebrews": {
    "1": {"1": "The Supremacy of God's Son"},
    "2": {"1": "Warning Against Neglect", "5": "Jesus Made Lower Than Angels"},
    "3": {"1": "Jesus Greater Than Moses", "7": "Warning Against Unbelief"},
    "4": {"1": "The Promise of Rest", "11": "The Word of God Is Living"},
    "5": {"1": "Jesus Our High Priest", "11": "Warning Against Immaturity"},
    "6": {"1": "Press On to Maturity", "9": "The Certainty of God's Promise"},
    "7": {"1": "The Priesthood of Melchizedek", "11": "Jesus the Perfect High Priest"},
    "8": {"1": "The New Covenant"},
    "9": {"1": "The Earthly Tabernacle", "11": "The Perfect Sacrifice of Christ"},
    "10": {"1": "Christ's Sacrifice Once for All", "19": "Draw Near to God", "26": "Warning Against Apostasy"},
    "11": {"1": "Faith Defined", "8": "The Faith of the Patriarchs", "32": "The Triumph of Faith"},
    "12": {"1": "Jesus the Founder and Perfecter of Faith", "4": "God Disciplines His Children", "14": "Pursue Peace and Holiness", "25": "The Unshakeable Kingdom"},
    "13": {"1": "Sacrifices Pleasing to God", "7": "Obey Your Leaders", "20": "Benediction and Final Greetings"}
  },
  "James": {
    "1": {"1": "Greeting", "2": "Testing and Temptation", "19": "Hearing and Doing the Word"},
    "2": {"1": "Warning Against Favoritism", "14": "Faith Without Works Is Dead"},
    "3": {"1": "Taming the Tongue", "13": "Wisdom from Above"},
    "4": {"1": "Warning Against Worldliness", "7": "Submit to God", "13": "Boasting About Tomorrow"},
    "5": {"1": "Warning to the Rich", "7": "Patience and Prayer", "19": "Restoring the Wanderer"}
  },
  "1 Peter": {
    "1": {"1": "Greeting", "3": "Born Again to a Living Hope", "13": "Called to Be Holy"},
    "2": {"1": "Living Stones and a Chosen People", "11": "Living as Strangers in the World", "18": "Submission of Servants"},
    "3": {"1": "Submission of Wives and Husbands", "8": "Suffering for Righteousness", "18": "Christ's Death and Triumph"},
    "4": {"1": "Living for God", "7": "The End of All Things", "12": "Suffering as a Christian"},
    "5": {"1": "Instructions to Elders and Young Men", "6": "Humble Yourselves", "12": "Final Greetings"}
  },
  "2 Peter": {
    "1": {"1": "Greeting", "3": "Confirming Your Calling", "12": "Peter's Approaching Death", "16": "Eyewitnesses of Christ's Glory"},
    "2": {"1": "False Teachers and Their Destruction", "10": "The Character of False Teachers"},
    "3": {"1": "The Day of the Lord", "8": "God's Patience and the New Heavens", "14": "Final Exhortation"}
  },
  "1 John": {
    "1": {"1": "The Word of Life", "5": "God Is Light"},
    "2": {"1": "Christ Our Advocate", "7": "The New Commandment", "15": "Do Not Love the World", "18": "Warning Against Antichrists", "28": "Children of God"},
    "3": {"1": "Children of God", "11": "Love One Another", "19": "Confidence Before God"},
    "4": {"1": "Test the Spirits", "7": "God Is Love", "16": "Perfect Love Casts Out Fear"},
    "5": {"1": "Faith in the Son of God", "6": "Witnesses to the Son", "13": "Confidence in Prayer", "16": "Prayer for Sinners"}
  },
  "2 John": {
    "1": {"1": "Greeting", "4": "Walking in Truth and Love", "7": "Warning Against Deceivers", "12": "Final Greetings"}
  },
  "3 John": {
    "1": {"1": "Greeting", "5": "Supporting Fellow Workers", "9": "Diotrephes and Demetrius", "13": "Final Greetings"}
  },
  "Jude": {
    "1": {"1": "Greeting", "3": "Contend for the Faith", "5": "Judgment on False Teachers", "17": "A Call to Persevere", "24": "Doxology"}
  },
  "Revelation": {
    "1": {"1": "Prologue", "9": "John's Vision of Christ"},
    "2": {"1": "To the Church in Ephesus", "8": "To the Church in Smyrna", "12": "To the Church in Pergamum", "18": "To the Church in Thyatira"},
    "3": {"1": "To the Church in Sardis", "7": "To the Church in Philadelphia", "14": "To the Church in Laodicea"},
    "4": {"1": "The Throne in Heaven"},
    "5": {"1": "The Scroll and the Lamb"},
    "6": {"1": "The Seven Seals", "12": "The Sixth Seal"},
    "7": {"1": "The 144,000 Sealed", "9": "The Great Multitude in White Robes"},
    "8": {"1": "The Seventh Seal and Golden Censer", "6": "The First Four Trumpets"},
    "9": {"1": "The Fifth and Sixth Trumpets", "13": "The Sixth Trumpet"},
    "10": {"1": "The Angel and the Little Scroll"},
    "11": {"1": "The Two Witnesses", "15": "The Seventh Trumpet"},
    "12": {"1": "The Woman and the Dragon", "7": "War in Heaven", "13": "The Dragon Persecutes the Woman"},
    "13": {"1": "The Beast from the Sea", "11": "The Beast from the Earth"},
    "14": {"1": "The Lamb and the 144,000", "6": "The Three Angels", "14": "The Harvest of the Earth"},
    "15": {"1": "The Seven Angels with Seven Plagues"},
    "16": {"1": "The Seven Bowls of God's Wrath"},
    "17": {"1": "The Woman and the Beast", "9": "The Mystery Explained"},
    "18": {"1": "The Fall of Babylon", "9": "Lament Over Babylon"},
    "19": {"1": "Hallelujah! Salvation and Glory", "6": "The Marriage Supper of the Lamb", "11": "The Rider on the White Horse", "17": "The Great Supper of God"},
    "20": {"1": "The Thousand Years", "7": "Satan's Final Defeat", "11": "The Great White Throne Judgment"},
    "21": {"1": "The New Heaven and New Earth", "9": "The New Jerusalem", "22": "The River of Life"},
    "22": {"1": "The River of Life", "6": "Jesus Is Coming", "18": "Warning and Invitation"}
  }
}
all_headings.update(general)

# Canonical book order
book_order = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms",
    "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
    "Hosea", "Joel", "Amos", "Obadiah", "Jonah",
    "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]

# Sort by canonical order
sorted_headings = {}
for book in book_order:
    if book in all_headings:
        sorted_headings[book] = all_headings[book]

# Write merged file
output_path = Path("kjvstudy_org/data/section_headings.json")
with open(output_path, "w") as f:
    json.dump(sorted_headings, f, indent=2)

print(f"Merged {len(sorted_headings)} books into {output_path}")

# Clean up temp files
prophets_file.unlink(missing_ok=True)
gospels_file.unlink(missing_ok=True)
print("Cleaned up temp files")
