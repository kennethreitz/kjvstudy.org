#!/usr/bin/env python3
"""Add new study guides to the catalog."""

import json

# Load existing study guides
with open('kjvstudy_org/data/study_guides.json', 'r') as f:
    data = json.load(f)

# New study guides to add
new_guides = {
    "Foundational Studies": [
        {
            "title": "Baptism",
            "description": "Understanding Christian baptism",
            "slug": "baptism",
            "verses": [
                "Matthew 28:19",
                "Acts 2:38",
                "Romans 6:3-4",
                "Colossians 2:12",
                "1 Peter 3:21",
                "Mark 16:16",
                "Acts 8:36-38",
                "Acts 22:16"
            ]
        },
        {
            "title": "Holy Communion",
            "description": "The Lord's Supper and its meaning",
            "slug": "communion",
            "verses": [
                "1 Corinthians 11:23-26",
                "Matthew 26:26-28",
                "Luke 22:19-20",
                "John 6:53-56",
                "1 Corinthians 10:16-17",
                "Acts 2:42"
            ]
        }
    ],
    "Character & Living": [
        {
            "title": "Discipleship",
            "description": "Following Jesus and making disciples",
            "slug": "discipleship",
            "verses": [
                "Matthew 28:19-20",
                "Luke 9:23",
                "John 8:31-32",
                "Luke 14:27",
                "John 13:34-35",
                "2 Timothy 2:2",
                "Matthew 16:24"
            ]
        },
        {
            "title": "Evangelism",
            "description": "Sharing the Gospel with others",
            "slug": "evangelism",
            "verses": [
                "Matthew 28:18-20",
                "Acts 1:8",
                "Romans 1:16",
                "2 Corinthians 5:20",
                "1 Peter 3:15",
                "Mark 16:15",
                "Romans 10:14-15"
            ]
        },
        {
            "title": "Suffering & Persecution",
            "description": "Enduring trials for Christ",
            "slug": "suffering-persecution",
            "verses": [
                "1 Peter 4:12-13",
                "2 Timothy 3:12",
                "Matthew 5:10-12",
                "Romans 8:17-18",
                "James 1:2-4",
                "2 Corinthians 4:17",
                "Philippians 1:29"
            ]
        }
    ],
    "Biblical Themes": [
        {
            "title": "Parables of Jesus",
            "description": "Understanding Christ's teaching stories",
            "slug": "parables",
            "verses": [
                "Matthew 13:3-9",
                "Luke 15:11-32",
                "Matthew 13:44-46",
                "Luke 10:30-37",
                "Matthew 25:14-30",
                "Luke 15:3-7",
                "Matthew 13:24-30"
            ]
        },
        {
            "title": "Miracles of Jesus",
            "description": "Signs and wonders of the Messiah",
            "slug": "miracles",
            "verses": [
                "John 2:11",
                "Mark 4:39-41",
                "John 11:43-44",
                "Matthew 14:25",
                "Mark 5:41-42",
                "John 6:11-13",
                "Matthew 8:2-3"
            ]
        }
    ],
    "Doctrinal Studies": [
        {
            "title": "End Times & Eschatology",
            "description": "Biblical prophecy and Christ's return",
            "slug": "end-times",
            "verses": [
                "1 Thessalonians 4:16-17",
                "Revelation 20:1-6",
                "Matthew 24:30-31",
                "2 Peter 3:10",
                "Revelation 21:1-4",
                "1 Corinthians 15:51-52",
                "Revelation 22:20"
            ]
        },
        {
            "title": "Spiritual Warfare",
            "description": "Fighting the good fight of faith",
            "slug": "spiritual-warfare",
            "verses": [
                "Ephesians 6:10-18",
                "2 Corinthians 10:4-5",
                "1 Peter 5:8-9",
                "James 4:7",
                "Revelation 12:11",
                "1 John 4:4",
                "Romans 8:37"
            ]
        },
        {
            "title": "Spiritual Gifts",
            "description": "Gifts of the Holy Spirit for ministry",
            "slug": "spiritual-gifts",
            "verses": [
                "1 Corinthians 12:4-11",
                "Romans 12:6-8",
                "1 Peter 4:10-11",
                "Ephesians 4:11-13",
                "1 Corinthians 14:1",
                "1 Timothy 4:14",
                "2 Timothy 1:6"
            ]
        },
        {
            "title": "The Church",
            "description": "The body of Christ and its mission",
            "slug": "the-church",
            "verses": [
                "Matthew 16:18",
                "1 Corinthians 12:27",
                "Ephesians 5:25-27",
                "Acts 2:42-47",
                "Ephesians 4:11-16",
                "Hebrews 10:24-25",
                "1 Timothy 3:15"
            ]
        }
    ]
}

# Add new guides to existing categories
for category, guides in new_guides.items():
    if category in data['catalog']:
        # Extend existing category
        existing_slugs = {g['slug'] for g in data['catalog'][category]}
        for guide in guides:
            if guide['slug'] not in existing_slugs:
                data['catalog'][category].append(guide)
                print(f"Added: {guide['title']} to {category}")
    else:
        # Create new category
        data['catalog'][category] = guides
        print(f"Created category: {category} with {len(guides)} guides")

# Save updated data
with open('kjvstudy_org/data/study_guides.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nTotal guides now: {sum(len(guides) for guides in data['catalog'].values())}")
