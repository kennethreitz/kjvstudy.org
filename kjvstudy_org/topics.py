"""
Topical index for finding Bible verses by theme.
Organized by major theological and practical topics.
"""

TOPICS = {
    "Salvation": {
        "description": "God's gift of eternal life through faith in Jesus Christ",
        "subtopics": {
            "Grace": {
                "description": "Salvation by grace alone, not by works",
                "verses": [
                    {"ref": "Ephesians 2:8-9", "note": "Saved by grace through faith"},
                    {"ref": "Titus 3:5", "note": "Not by works of righteousness"},
                    {"ref": "Romans 3:24", "note": "Justified freely by His grace"},
                    {"ref": "Romans 11:6", "note": "If by grace, then not by works"},
                ]
            },
            "Faith": {
                "description": "Believing in Christ for salvation",
                "verses": [
                    {"ref": "Acts 16:31", "note": "Believe on the Lord Jesus Christ"},
                    {"ref": "John 3:16", "note": "Whosoever believeth in Him"},
                    {"ref": "Romans 10:9", "note": "Confess and believe"},
                    {"ref": "Ephesians 2:8", "note": "Through faith, not of yourselves"},
                ]
            },
            "Justification": {
                "description": "Declared righteous through faith in Christ",
                "verses": [
                    {"ref": "Romans 5:1", "note": "Justified by faith, we have peace"},
                    {"ref": "Romans 3:28", "note": "Justified by faith without works"},
                    {"ref": "Galatians 2:16", "note": "Not justified by works of law"},
                    {"ref": "Romans 4:5", "note": "Faith counted for righteousness"},
                ]
            },
            "Regeneration": {
                "description": "Born again by the Spirit",
                "verses": [
                    {"ref": "John 3:3", "note": "Ye must be born again"},
                    {"ref": "2 Corinthians 5:17", "note": "New creature in Christ"},
                    {"ref": "Titus 3:5", "note": "Washing of regeneration"},
                    {"ref": "1 Peter 1:23", "note": "Born again by the Word"},
                ]
            }
        }
    },
    "Prayer": {
        "description": "Communion with God through prayer",
        "subtopics": {
            "How to Pray": {
                "description": "Instruction on effective prayer",
                "verses": [
                    {"ref": "Matthew 6:9-13", "note": "The Lord's Prayer"},
                    {"ref": "Philippians 4:6", "note": "With thanksgiving"},
                    {"ref": "1 Thessalonians 5:17", "note": "Pray without ceasing"},
                    {"ref": "James 1:6", "note": "Ask in faith, nothing wavering"},
                ]
            },
            "Power of Prayer": {
                "description": "God's response to prayer",
                "verses": [
                    {"ref": "James 5:16", "note": "Effectual fervent prayer"},
                    {"ref": "Matthew 21:22", "note": "Whatsoever ye ask in prayer"},
                    {"ref": "1 John 5:14-15", "note": "Ask according to His will"},
                    {"ref": "John 14:13-14", "note": "Ask in Jesus' name"},
                ]
            },
            "Prayer and Forgiveness": {
                "description": "Forgiving others when we pray",
                "verses": [
                    {"ref": "Mark 11:25", "note": "Forgive when ye stand praying"},
                    {"ref": "Matthew 6:14-15", "note": "Forgive to be forgiven"},
                    {"ref": "1 Peter 3:7", "note": "Prayers not hindered"},
                ]
            }
        }
    },
    "Love": {
        "description": "God's love and our love for Him and others",
        "subtopics": {
            "God's Love": {
                "description": "The nature and extent of God's love",
                "verses": [
                    {"ref": "1 John 4:8", "note": "God is love"},
                    {"ref": "John 3:16", "note": "God so loved the world"},
                    {"ref": "Romans 5:8", "note": "Christ died for us"},
                    {"ref": "1 John 4:10", "note": "Herein is love"},
                ]
            },
            "Love for God": {
                "description": "Our response of love to God",
                "verses": [
                    {"ref": "Matthew 22:37", "note": "Love the Lord with all your heart"},
                    {"ref": "1 John 4:19", "note": "We love Him because He first loved us"},
                    {"ref": "John 14:15", "note": "If ye love me, keep my commandments"},
                ]
            },
            "Love for Others": {
                "description": "Loving our neighbors as ourselves",
                "verses": [
                    {"ref": "John 13:34-35", "note": "Love one another"},
                    {"ref": "1 Corinthians 13:4-7", "note": "Characteristics of love"},
                    {"ref": "Romans 13:10", "note": "Love fulfills the law"},
                    {"ref": "1 Peter 4:8", "note": "Charity covers sins"},
                ]
            }
        }
    },
    "Faith": {
        "description": "Trust and confidence in God and His promises",
        "subtopics": {
            "Nature of Faith": {
                "description": "What faith is",
                "verses": [
                    {"ref": "Hebrews 11:1", "note": "Substance of things hoped for"},
                    {"ref": "2 Corinthians 5:7", "note": "Walk by faith, not sight"},
                    {"ref": "Romans 10:17", "note": "Faith comes by hearing"},
                ]
            },
            "Faith and Works": {
                "description": "Faith demonstrated through obedience",
                "verses": [
                    {"ref": "James 2:17", "note": "Faith without works is dead"},
                    {"ref": "James 2:26", "note": "Body without spirit is dead"},
                    {"ref": "Ephesians 2:10", "note": "Created unto good works"},
                ]
            },
            "Examples of Faith": {
                "description": "Biblical models of faith",
                "verses": [
                    {"ref": "Hebrews 11:4", "note": "Abel offered by faith"},
                    {"ref": "Hebrews 11:7", "note": "Noah prepared an ark"},
                    {"ref": "Hebrews 11:8", "note": "Abraham obeyed"},
                    {"ref": "Hebrews 11:17", "note": "Abraham offered Isaac"},
                ]
            }
        }
    },
    "Forgiveness": {
        "description": "God's forgiveness and forgiving others",
        "subtopics": {
            "God's Forgiveness": {
                "description": "Receiving forgiveness from God",
                "verses": [
                    {"ref": "1 John 1:9", "note": "Confess and He will forgive"},
                    {"ref": "Ephesians 1:7", "note": "Forgiveness through His blood"},
                    {"ref": "Colossians 1:14", "note": "Redemption and forgiveness"},
                    {"ref": "Acts 13:38", "note": "Forgiveness through Christ"},
                ]
            },
            "Forgiving Others": {
                "description": "Extending forgiveness to those who wrong us",
                "verses": [
                    {"ref": "Matthew 6:14-15", "note": "Forgive to be forgiven"},
                    {"ref": "Ephesians 4:32", "note": "Forgiving one another"},
                    {"ref": "Colossians 3:13", "note": "As Christ forgave you"},
                    {"ref": "Matthew 18:21-22", "note": "Seventy times seven"},
                ]
            }
        }
    },
    "Holy Spirit": {
        "description": "The third person of the Trinity and His work",
        "subtopics": {
            "Person and Deity": {
                "description": "The Holy Spirit is God",
                "verses": [
                    {"ref": "Acts 5:3-4", "note": "Lying to the Holy Ghost is lying to God"},
                    {"ref": "2 Corinthians 3:17", "note": "The Lord is that Spirit"},
                    {"ref": "1 Corinthians 2:11", "note": "Spirit knows things of God"},
                ]
            },
            "Indwelling": {
                "description": "The Spirit lives in believers",
                "verses": [
                    {"ref": "Romans 8:9", "note": "Spirit of God dwells in you"},
                    {"ref": "1 Corinthians 6:19", "note": "Your body is His temple"},
                    {"ref": "Galatians 4:6", "note": "Spirit sent into hearts"},
                ]
            },
            "Fruit of the Spirit": {
                "description": "Character produced by the Spirit",
                "verses": [
                    {"ref": "Galatians 5:22-23", "note": "Love, joy, peace, etc."},
                    {"ref": "Romans 8:5", "note": "Mind the things of the Spirit"},
                    {"ref": "Galatians 5:16", "note": "Walk in the Spirit"},
                ]
            },
            "Gifts of the Spirit": {
                "description": "Spiritual abilities given to believers",
                "verses": [
                    {"ref": "1 Corinthians 12:4-11", "note": "Diversity of gifts"},
                    {"ref": "Romans 12:6-8", "note": "Gifts differ"},
                    {"ref": "1 Peter 4:10", "note": "Minister gifts to one another"},
                ]
            }
        }
    },
    "Hope": {
        "description": "Confident expectation based on God's promises",
        "subtopics": {
            "Source of Hope": {
                "description": "Hope grounded in God",
                "verses": [
                    {"ref": "Romans 15:13", "note": "God of hope"},
                    {"ref": "Psalms 39:7", "note": "My hope is in Thee"},
                    {"ref": "1 Peter 1:3", "note": "Living hope through resurrection"},
                ]
            },
            "Eternal Hope": {
                "description": "Hope of eternal life",
                "verses": [
                    {"ref": "Titus 1:2", "note": "Hope of eternal life"},
                    {"ref": "Titus 3:7", "note": "Heirs according to hope"},
                    {"ref": "Colossians 1:5", "note": "Hope laid up in heaven"},
                ]
            }
        }
    },
    "Peace": {
        "description": "The peace of God and peace with God",
        "subtopics": {
            "Peace with God": {
                "description": "Reconciliation through Christ",
                "verses": [
                    {"ref": "Romans 5:1", "note": "Peace with God through Christ"},
                    {"ref": "Colossians 1:20", "note": "Peace through His blood"},
                    {"ref": "Ephesians 2:14", "note": "Christ is our peace"},
                ]
            },
            "Peace of God": {
                "description": "Inner peace from God",
                "verses": [
                    {"ref": "Philippians 4:7", "note": "Peace that passes understanding"},
                    {"ref": "John 14:27", "note": "My peace I give unto you"},
                    {"ref": "Colossians 3:15", "note": "Let peace rule in hearts"},
                ]
            }
        }
    },
    "Wisdom": {
        "description": "Godly wisdom for righteous living",
        "subtopics": {
            "Source of Wisdom": {
                "description": "Wisdom comes from God",
                "verses": [
                    {"ref": "James 1:5", "note": "Ask God for wisdom"},
                    {"ref": "Proverbs 2:6", "note": "The LORD gives wisdom"},
                    {"ref": "1 Corinthians 1:30", "note": "Christ made unto us wisdom"},
                ]
            },
            "Value of Wisdom": {
                "description": "The importance of wisdom",
                "verses": [
                    {"ref": "Proverbs 4:7", "note": "Wisdom is the principal thing"},
                    {"ref": "Proverbs 3:13-14", "note": "Happy is he that finds wisdom"},
                    {"ref": "Ecclesiastes 7:12", "note": "Wisdom gives life"},
                ]
            },
            "Fear of the Lord": {
                "description": "Beginning of wisdom",
                "verses": [
                    {"ref": "Proverbs 9:10", "note": "Fear of the LORD is beginning"},
                    {"ref": "Proverbs 1:7", "note": "Fear of LORD is beginning of knowledge"},
                    {"ref": "Psalms 111:10", "note": "Good understanding to those who fear"},
                ]
            }
        }
    },
    "Suffering": {
        "description": "God's purposes in trials and afflictions",
        "subtopics": {
            "Purpose of Suffering": {
                "description": "Why God allows suffering",
                "verses": [
                    {"ref": "Romans 5:3-4", "note": "Tribulation works patience"},
                    {"ref": "James 1:2-4", "note": "Trying of faith produces patience"},
                    {"ref": "2 Corinthians 4:17", "note": "Light affliction, eternal weight of glory"},
                    {"ref": "1 Peter 1:7", "note": "Trial of faith more precious than gold"},
                ]
            },
            "Comfort in Suffering": {
                "description": "God's comfort in trials",
                "verses": [
                    {"ref": "2 Corinthians 1:3-4", "note": "God of all comfort"},
                    {"ref": "Psalms 23:4", "note": "Walk through valley of shadow"},
                    {"ref": "Isaiah 41:10", "note": "Fear not, I am with thee"},
                ]
            },
            "Christ's Example": {
                "description": "Following Christ in suffering",
                "verses": [
                    {"ref": "1 Peter 2:21", "note": "Christ suffered for us"},
                    {"ref": "Hebrews 12:2", "note": "Looking unto Jesus"},
                    {"ref": "Philippians 3:10", "note": "Fellowship of His sufferings"},
                ]
            },
            "Grief": {
                "description": "Mourning and sorrow",
                "verses": [
                    {"ref": "Psalms 34:18", "note": "The LORD is nigh unto them of a broken heart"},
                    {"ref": "Matthew 5:4", "note": "Blessed are they that mourn"},
                    {"ref": "John 11:35", "note": "Jesus wept"},
                    {"ref": "Psalms 30:5", "note": "Weeping may endure for a night"},
                    {"ref": "2 Corinthians 1:3-4", "note": "Father of mercies and God of all comfort"},
                    {"ref": "Revelation 21:4", "note": "God shall wipe away all tears"},
                    {"ref": "1 Thessalonians 4:13", "note": "Sorrow not as others who have no hope"},
                    {"ref": "Psalms 147:3", "note": "He heals the broken in heart"},
                ]
            }
        }
    },
    "Parenting": {
        "description": "Biblical principles for raising children",
        "subtopics": {
            "Teaching Children": {
                "description": "Instructing children in God's ways",
                "verses": [
                    {"ref": "Deuteronomy 6:6-7", "note": "Teach children diligently"},
                    {"ref": "Proverbs 22:6", "note": "Train up a child in the way he should go"},
                    {"ref": "Ephesians 6:4", "note": "Bring them up in nurture and admonition"},
                    {"ref": "Psalms 78:4-6", "note": "Show children the praises of the LORD"},
                    {"ref": "2 Timothy 3:15", "note": "Known the Scriptures from childhood"},
                ]
            },
            "Discipline": {
                "description": "Godly correction and discipline",
                "verses": [
                    {"ref": "Proverbs 13:24", "note": "He that spareth his rod hateth his son"},
                    {"ref": "Proverbs 29:15", "note": "Rod and reproof give wisdom"},
                    {"ref": "Proverbs 23:13-14", "note": "Withhold not correction from the child"},
                    {"ref": "Hebrews 12:7", "note": "God dealeth with you as with sons"},
                    {"ref": "Proverbs 29:17", "note": "Correct thy son, and he shall give thee rest"},
                ]
            },
            "Father's Role": {
                "description": "The father's responsibility",
                "verses": [
                    {"ref": "Ephesians 6:4", "note": "Fathers, provoke not your children to wrath"},
                    {"ref": "Colossians 3:21", "note": "Fathers, provoke not your children"},
                    {"ref": "1 Thessalonians 2:11-12", "note": "As a father doth his children"},
                    {"ref": "Proverbs 4:1-4", "note": "Father's instruction to his son"},
                ]
            },
            "Mother's Role": {
                "description": "The mother's influence",
                "verses": [
                    {"ref": "Proverbs 31:1", "note": "Prophecy that his mother taught him"},
                    {"ref": "Proverbs 31:26-28", "note": "Openeth her mouth with wisdom"},
                    {"ref": "2 Timothy 1:5", "note": "Faith that dwelt in thy mother"},
                    {"ref": "Proverbs 1:8", "note": "Forsake not the law of thy mother"},
                ]
            },
            "Children's Obedience": {
                "description": "Children honoring and obeying parents",
                "verses": [
                    {"ref": "Ephesians 6:1-3", "note": "Children, obey your parents"},
                    {"ref": "Colossians 3:20", "note": "Obey your parents in all things"},
                    {"ref": "Exodus 20:12", "note": "Honour thy father and thy mother"},
                    {"ref": "Proverbs 6:20", "note": "Keep thy father's commandment"},
                    {"ref": "Proverbs 23:22", "note": "Hearken unto thy father"},
                ]
            },
            "Love and Provision": {
                "description": "Caring for children's needs",
                "verses": [
                    {"ref": "Psalms 127:3", "note": "Children are an heritage of the LORD"},
                    {"ref": "Psalms 103:13", "note": "As a father pitieth his children"},
                    {"ref": "Matthew 7:11", "note": "Give good gifts unto your children"},
                    {"ref": "2 Corinthians 12:14", "note": "Children ought not to lay up for parents"},
                    {"ref": "1 Timothy 5:8", "note": "Provide for his own"},
                ]
            }
        }
    }
}


def get_all_topics():
    """Get all topics"""
    return TOPICS


def get_topic(topic_name: str):
    """Get a specific topic"""
    return TOPICS.get(topic_name)


def search_topics(query: str):
    """Search for topics by name or description"""
    query_lower = query.lower()
    results = []

    for topic_name, topic_data in TOPICS.items():
        if query_lower in topic_name.lower() or query_lower in topic_data.get("description", "").lower():
            results.append({
                "name": topic_name,
                "description": topic_data["description"],
                "subtopic_count": len(topic_data.get("subtopics", {}))
            })

    return results
