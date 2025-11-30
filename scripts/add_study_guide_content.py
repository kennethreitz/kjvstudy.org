#!/usr/bin/env python3
"""Add content for new study guides."""

import json

# Load existing study guides
with open('kjvstudy_org/data/study_guides.json', 'r') as f:
    data = json.load(f)

# Content for new study guides
new_content = {
    "baptism": {
        "title": "Baptism",
        "description": "Understanding Christian baptism",
        "sections": [
            {
                "title": "The Command to Be Baptized",
                "verses": ["Matthew 28:19", "Mark 16:16", "Acts 2:38"],
                "content": "Baptism is a command from Jesus Christ Himself. In the Great Commission, Jesus commanded His disciples to baptize all believers. This wasn't a suggestion but a clear directive for all who follow Him."
            },
            {
                "title": "The Meaning of Baptism",
                "verses": ["Romans 6:3-4", "Colossians 2:12"],
                "content": "Baptism symbolizes our death to sin and resurrection to new life in Christ. When we are immersed in water, it represents being buried with Christ. When we rise from the water, it represents being raised to walk in newness of life."
            },
            {
                "title": "Baptism as Public Declaration",
                "verses": ["Acts 8:36-38", "Acts 16:31-33"],
                "content": "Baptism is a public declaration of faith in Jesus Christ. It's an outward sign of an inward change. The Ethiopian eunuch and the Philippian jailer were both baptized immediately after believing, demonstrating their commitment publicly."
            },
            {
                "title": "The Mode of Baptism",
                "verses": ["Matthew 3:16", "John 3:23"],
                "content": "The Greek word 'baptizo' means to immerse or plunge under water. Jesus Himself was baptized by immersion, coming up out of the water. John baptized in locations where there was much water, indicating immersion was the practice."
            },
            {
                "title": "Who Should Be Baptized",
                "verses": ["Acts 2:38", "Acts 8:12", "Acts 18:8"],
                "content": "Baptism is for those who have believed in Jesus Christ. The pattern in Acts shows that people first heard the gospel, believed, and then were baptized. It follows faith and repentance, not precedes it."
            },
            {
                "title": "Baptism and Salvation",
                "verses": ["Ephesians 2:8-9", "1 Peter 3:21", "Titus 3:5"],
                "content": "Baptism does not save us—faith in Christ alone saves. However, baptism is the normal response of saving faith. Peter clarifies that baptism saves us as 'an answer of a good conscience toward God' through Christ's resurrection, not as a work that merits salvation."
            },
            {
                "title": "Unity in Baptism",
                "verses": ["Ephesians 4:4-6", "1 Corinthians 12:13"],
                "content": "There is one baptism for all believers, uniting us in the body of Christ. Whether Jew or Gentile, slave or free, all who believe are baptized by one Spirit into one body."
            },
            {
                "title": "The Urgency of Baptism",
                "verses": ["Acts 22:16", "Acts 8:36", "Acts 16:33"],
                "content": "The early church practice shows baptism followed belief without delay. When people believed, they were baptized the same day, even immediately. This demonstrates the importance and urgency of obeying Christ's command."
            }
        ]
    },
    "communion": {
        "title": "Holy Communion",
        "description": "The Lord's Supper and its meaning",
        "sections": [
            {
                "title": "Institution of the Lord's Supper",
                "verses": ["Matthew 26:26-28", "Mark 14:22-24", "Luke 22:19-20"],
                "content": "Jesus instituted the Lord's Supper on the night before His crucifixion. During the Passover meal, He took bread and wine, giving them new meaning as symbols of His body and blood about to be given for the sins of the world."
            },
            {
                "title": "Do This in Remembrance",
                "verses": ["1 Corinthians 11:23-25", "Luke 22:19"],
                "content": "Jesus commanded us to observe communion in remembrance of Him. It's not merely a ritual but a memorial feast where we actively remember Christ's sacrifice, His death on the cross for our sins, until He comes again."
            },
            {
                "title": "Proclaiming the Lord's Death",
                "verses": ["1 Corinthians 11:26"],
                "content": "When we partake of communion, we proclaim the Lord's death. It's a public declaration of the gospel—that Christ died for sinners. Every time we eat the bread and drink the cup, we're testifying to His sacrificial death."
            },
            {
                "title": "The Bread: Christ's Body",
                "verses": ["1 Corinthians 10:16-17", "John 6:51"],
                "content": "The bread represents Christ's body broken for us. Jesus is the bread of life who came down from heaven. When we eat the bread, we remember His physical suffering, His body pierced and broken on the cross for our redemption."
            },
            {
                "title": "The Cup: Christ's Blood",
                "verses": ["Matthew 26:28", "Hebrews 9:22", "1 Peter 1:18-19"],
                "content": "The cup represents Christ's blood shed for the forgiveness of sins. This is the blood of the new covenant, the precious blood that cleanses us from all sin. Without the shedding of blood, there is no remission of sin."
            },
            {
                "title": "Examining Ourselves",
                "verses": ["1 Corinthians 11:27-29"],
                "content": "We must not take communion in an unworthy manner. This means we should examine ourselves, confess our sins, and approach the table with reverence. Those who partake without discerning the Lord's body eat and drink judgment on themselves."
            },
            {
                "title": "Unity in the Body",
                "verses": ["1 Corinthians 10:17", "Acts 2:42"],
                "content": "Communion expresses our unity as believers. We who are many are one body, for we all partake of the one bread. The early church devoted themselves to the apostles' teaching, fellowship, breaking of bread, and prayer."
            },
            {
                "title": "Until He Comes",
                "verses": ["1 Corinthians 11:26", "Revelation 19:9"],
                "content": "We observe communion until Christ returns. It points backward to Calvary and forward to the marriage supper of the Lamb. Every celebration is a reminder that Jesus is coming again to receive His bride, the Church."
            }
        ]
    },
    "discipleship": {
        "title": "Discipleship",
        "description": "Following Jesus and making disciples",
        "sections": [
            {
                "title": "The Call to Discipleship",
                "verses": ["Matthew 4:19", "Luke 9:23", "John 1:43"],
                "content": "Jesus calls us to follow Him. Discipleship begins with a personal call from Christ—'Follow Me.' It's not a casual invitation but a life-changing summons to leave everything and follow the Master."
            },
            {
                "title": "Counting the Cost",
                "verses": ["Luke 14:26-33"],
                "content": "Jesus makes clear that discipleship costs everything. We must love Him more than family, carry our cross daily, and forsake all to follow Him. True discipleship requires total commitment and wholehearted surrender."
            },
            {
                "title": "Abiding in Christ",
                "verses": ["John 15:4-8", "John 8:31-32"],
                "content": "A disciple abides in Christ and in His Word. Just as a branch must remain connected to the vine to bear fruit, we must remain in Christ. Continuance in His Word is the mark of true discipleship."
            },
            {
                "title": "Love One Another",
                "verses": ["John 13:34-35", "1 John 4:20-21"],
                "content": "The identifying mark of disciples is love for one another. Jesus gave us a new commandment to love each other as He loved us. Our love for fellow believers shows the world that we are Christ's disciples."
            },
            {
                "title": "Denying Self",
                "verses": ["Matthew 16:24-25", "Galatians 2:20"],
                "content": "Discipleship requires self-denial. We must deny ourselves, take up our cross, and follow Jesus. It means dying to selfish desires and living for Christ. We are crucified with Christ, and He now lives in us."
            },
            {
                "title": "Making Disciples",
                "verses": ["Matthew 28:19-20", "2 Timothy 2:2"],
                "content": "Disciples make disciples. The Great Commission commands us to make disciples of all nations, teaching them to obey all that Jesus commanded. Paul instructed Timothy to entrust the gospel to faithful men who would teach others also."
            },
            {
                "title": "Learning from the Master",
                "verses": ["Matthew 11:29", "Luke 6:40"],
                "content": "A disciple is a learner who follows the teacher. Jesus invites us to learn from Him—He is gentle and humble in heart. When fully trained, a disciple becomes like their teacher, reflecting Christ's character."
            },
            {
                "title": "Bearing Fruit",
                "verses": ["John 15:16", "Galatians 5:22-23", "Colossians 1:10"],
                "content": "Disciples bear lasting fruit. Jesus chose us and appointed us to go and bear fruit that remains. This fruit includes the fruit of the Spirit, fruit in good works, and fruit in winning others to Christ."
            }
        ]
    },
    "evangelism": {
        "title": "Evangelism",
        "description": "Sharing the Gospel with others",
        "sections": [
            {
                "title": "The Great Commission",
                "verses": ["Matthew 28:18-20", "Mark 16:15"],
                "content": "Jesus commissioned all believers to go and make disciples of all nations. This is not optional but a direct command from our Lord. We are to go into all the world and preach the gospel to every creature."
            },
            {
                "title": "Power for Witness",
                "verses": ["Acts 1:8", "Acts 4:31"],
                "content": "We receive power when the Holy Spirit comes upon us to be witnesses for Christ. The Spirit empowers, emboldens, and equips us to testify about Jesus. The early disciples spoke God's Word with boldness after being filled with the Spirit."
            },
            {
                "title": "The Gospel We Proclaim",
                "verses": ["1 Corinthians 15:3-4", "Romans 1:16"],
                "content": "The gospel is the power of God for salvation. We preach Christ crucified, buried, and risen according to the Scriptures. This good news is for everyone who believes—it saves both Jew and Gentile."
            },
            {
                "title": "Ambassadors for Christ",
                "verses": ["2 Corinthians 5:18-20"],
                "content": "God has given us the ministry of reconciliation. We are ambassadors for Christ, as though God were making His appeal through us. We implore people on Christ's behalf: 'Be reconciled to God.'"
            },
            {
                "title": "Always Ready to Answer",
                "verses": ["1 Peter 3:15", "Colossians 4:5-6"],
                "content": "We must always be prepared to give an answer for the hope we have, doing so with gentleness and respect. We should be wise in how we act toward outsiders, making the most of every opportunity, speaking with grace."
            },
            {
                "title": "Sowing and Reaping",
                "verses": ["1 Corinthians 3:6-8", "Psalm 126:5-6"],
                "content": "In evangelism, one plants, another waters, but God gives the growth. Those who sow in tears will reap with songs of joy. We faithfully sow the seed of God's Word, trusting Him for the harvest."
            },
            {
                "title": "Not Ashamed of the Gospel",
                "verses": ["Romans 1:16", "2 Timothy 1:8", "Mark 8:38"],
                "content": "We must never be ashamed of the gospel of Christ. It is God's power for salvation. Those who are ashamed of Jesus and His words in this adulterous generation will find Christ ashamed of them when He comes in glory."
            },
            {
                "title": "Urgency of the Message",
                "verses": ["2 Corinthians 6:2", "Romans 10:13-15"],
                "content": "Now is the day of salvation! How can people call on Him they haven't believed in? And how can they believe without hearing? How can they hear without someone preaching? We must urgently share the gospel while it is still called today."
            }
        ]
    }
}

# Add more content...
more_content = {
    "suffering-persecution": {
        "title": "Suffering & Persecution",
        "description": "Enduring trials for Christ",
        "sections": [
            {
                "title": "Expected Suffering",
                "verses": ["John 15:18-20", "2 Timothy 3:12"],
                "content": "Jesus warned that the world would hate His followers. If they persecuted Him, they will persecute us. All who desire to live godly in Christ Jesus will suffer persecution. It's not a matter of 'if' but 'when.'"
            },
            {
                "title": "Blessed Are the Persecuted",
                "verses": ["Matthew 5:10-12", "Luke 6:22-23"],
                "content": "Jesus declared blessed those persecuted for righteousness' sake. When people revile and persecute you falsely for Christ's sake, rejoice! Your reward in heaven is great. The prophets before you were persecuted the same way."
            },
            {
                "title": "Sharing Christ's Sufferings",
                "verses": ["1 Peter 4:12-13", "Philippians 3:10", "Romans 8:17"],
                "content": "Don't be surprised at trials—they test your faith. Instead, rejoice that you share Christ's sufferings. Paul desired to know Christ and the fellowship of His sufferings. If we suffer with Him, we will also be glorified with Him."
            },
            {
                "title": "Present Suffering, Future Glory",
                "verses": ["Romans 8:18", "2 Corinthians 4:17"],
                "content": "Our present sufferings are not worth comparing with the glory that will be revealed. Our light and momentary troubles are achieving for us an eternal glory that far outweighs them all. Suffering is temporary; glory is eternal."
            },
            {
                "title": "Trials Produce Perseverance",
                "verses": ["James 1:2-4", "Romans 5:3-5", "1 Peter 1:6-7"],
                "content": "Consider it joy when you face trials, because testing produces perseverance. Suffering produces endurance, endurance produces character, and character produces hope. These trials prove your faith genuine and will result in praise and glory."
            },
            {
                "title": "Suffering for Doing Good",
                "verses": ["1 Peter 3:13-17", "1 Peter 2:20-21"],
                "content": "Better to suffer for doing good than for doing evil. Christ also suffered for you, leaving an example that you should follow in His steps. He committed no sin, yet endured suffering unjustly, entrusting Himself to God."
            },
            {
                "title": "God's Comfort in Suffering",
                "verses": ["2 Corinthians 1:3-7", "Psalm 34:18"],
                "content": "God is the Father of compassion and God of all comfort. He comforts us in all our troubles so we can comfort others. The Lord is close to the brokenhearted and saves those crushed in spirit."
            },
            {
                "title": "Counted Worthy to Suffer",
                "verses": ["Acts 5:41", "Philippians 1:29"],
                "content": "The apostles rejoiced that they were counted worthy to suffer shame for Christ's name. It has been granted to you not only to believe in Christ but also to suffer for Him. Suffering for Christ is a privilege and honor."
            }
        ]
    },
    "parables": {
        "title": "Parables of Jesus",
        "description": "Understanding Christ's teaching stories",
        "sections": [
            {
                "title": "Why Jesus Taught in Parables",
                "verses": ["Matthew 13:10-17", "Mark 4:11-12"],
                "content": "Jesus used parables to reveal truth to believers while concealing it from the hard-hearted. To those with ears to hear, the mysteries of the kingdom are revealed. Parables illustrate spiritual truths through earthly stories."
            },
            {
                "title": "The Sower and the Seed",
                "verses": ["Matthew 13:3-9", "Matthew 13:18-23"],
                "content": "The parable of the sower teaches about different responses to God's Word. The seed is the Word of God sown in human hearts. Some reject it immediately, others receive it with joy but fall away, and still others produce abundant fruit."
            },
            {
                "title": "The Good Samaritan",
                "verses": ["Luke 10:30-37"],
                "content": "This parable defines true neighborly love. While the priest and Levite passed by, the Samaritan showed mercy to the wounded man. Jesus teaches us to show compassion to all people, even those different from us."
            },
            {
                "title": "The Prodigal Son",
                "verses": ["Luke 15:11-32"],
                "content": "Perhaps the greatest story of redemption, this parable shows God's heart for the lost. The wayward son's return and the father's celebration illustrate God's love for repentant sinners. The elder brother's resentment warns against self-righteousness."
            },
            {
                "title": "The Pearl of Great Price",
                "verses": ["Matthew 13:45-46"],
                "content": "The kingdom of heaven is like a merchant seeking fine pearls. When he found one of great value, he sold everything to obtain it. This teaches that the kingdom is worth any sacrifice—nothing compares to its value."
            },
            {
                "title": "The Talents",
                "verses": ["Matthew 25:14-30"],
                "content": "This parable teaches faithful stewardship of what God has entrusted to us. The master rewarded those who used their talents wisely but condemned the one who buried his talent. We must use our gifts for God's glory."
            },
            {
                "title": "The Wheat and the Tares",
                "verses": ["Matthew 13:24-30", "Matthew 13:36-43"],
                "content": "The kingdom contains both true believers (wheat) and false professors (tares). They grow together until harvest (judgment day) when God will separate them. This teaches patience with visible mixture in the church until Christ returns."
            },
            {
                "title": "The Lost Sheep",
                "verses": ["Luke 15:3-7", "Matthew 18:12-14"],
                "content": "God pursues the lost with relentless love. The shepherd leaves ninety-nine sheep to find the one that strayed. There is more joy in heaven over one sinner who repents than over ninety-nine who need no repentance."
            }
        ]
    },
    "miracles": {
        "title": "Miracles of Jesus",
        "description": "Signs and wonders of the Messiah",
        "sections": [
            {
                "title": "Purpose of Miracles",
                "verses": ["John 20:30-31", "John 2:11"],
                "content": "Jesus performed many signs in the presence of His disciples. These were written that we might believe Jesus is the Christ, the Son of God, and have life in His name. Miracles revealed His glory and authenticated His divine mission."
            },
            {
                "title": "Power Over Nature",
                "verses": ["Mark 4:39-41", "Matthew 14:25"],
                "content": "Jesus demonstrated authority over creation by calming the storm with a word and walking on water. The disciples marveled, 'What manner of man is this, that even the winds and sea obey Him?' These miracles show He is Creator and Lord."
            },
            {
                "title": "Power Over Disease",
                "verses": ["Matthew 8:2-3", "Mark 1:40-42"],
                "content": "Jesus healed all manner of sickness with a word or touch. He healed the leper, the blind, the deaf, and the paralyzed. No disease was too difficult for Him. These healings fulfilled Isaiah's prophecy that Messiah would bear our infirmities."
            },
            {
                "title": "Power Over Death",
                "verses": ["John 11:43-44", "Luke 7:14-15", "Mark 5:41-42"],
                "content": "Jesus raised the dead on multiple occasions: Jairus' daughter, the widow's son, and Lazarus. These miracles demonstrated His power over death itself and foreshadowed His own resurrection. He is the resurrection and the life."
            },
            {
                "title": "Power Over Demons",
                "verses": ["Mark 5:1-13", "Luke 4:35-36"],
                "content": "Jesus cast out demons with authority. Even the evil spirits recognized Him as the Son of God and obeyed His commands. These exorcisms demonstrated His victory over Satan and His power to set captives free."
            },
            {
                "title": "The First Sign: Water to Wine",
                "verses": ["John 2:1-11"],
                "content": "At Cana, Jesus turned water into wine, manifesting His glory. This first miracle showed His creative power and His care for human needs. The new wine symbolizes the superior joy and abundance of the new covenant He brings."
            },
            {
                "title": "Feeding the Multitudes",
                "verses": ["John 6:1-13", "Matthew 14:15-21"],
                "content": "Jesus fed five thousand men (plus women and children) with five loaves and two fish. This miracle revealed Him as the Bread of Life who satisfies spiritual hunger. It demonstrated His compassion and His power to provide abundantly."
            },
            {
                "title": "The Ultimate Miracle: Resurrection",
                "verses": ["Matthew 28:5-6", "1 Corinthians 15:20"],
                "content": "The greatest miracle was Jesus' own resurrection. He conquered death and rose on the third day, becoming the firstfruits of those who sleep. His resurrection proves His deity, validates His sacrifice, and guarantees our future resurrection."
            }
        ]
    }
}

new_content.update(more_content)

# Add final set of content
final_content = {
    "end-times": {
        "title": "End Times & Eschatology",
        "description": "Biblical prophecy and Christ's return",
        "sections": [
            {
                "title": "The Promise of Christ's Return",
                "verses": ["John 14:2-3", "Acts 1:11", "Revelation 22:20"],
                "content": "Jesus promised to return for His own. He has gone to prepare a place for us and will come again to receive us. The angels declared that He will return in the same way He ascended. He affirms, 'Surely I am coming quickly.'"
            },
            {
                "title": "The Rapture of the Church",
                "verses": ["1 Thessalonians 4:16-17", "1 Corinthians 15:51-52"],
                "content": "At the rapture, the Lord will descend from heaven with a shout. The dead in Christ will rise first, then living believers will be caught up together with them in the clouds. This happens in a moment, in the twinkling of an eye."
            },
            {
                "title": "The Tribulation",
                "verses": ["Matthew 24:21", "Revelation 7:14", "Daniel 9:27"],
                "content": "The tribulation will be a time of great distress unequaled from the beginning of the world. It refers to a seven-year period of God's judgment on earth. Many believe the church will be raptured before this time of trouble."
            },
            {
                "title": "The Second Coming",
                "verses": ["Matthew 24:30-31", "Revelation 19:11-16", "Zechariah 14:4"],
                "content": "Christ will return in power and glory with His angels. Every eye will see Him. He comes as King of Kings and Lord of Lords to judge the earth and establish His kingdom. His feet will stand on the Mount of Olives."
            },
            {
                "title": "The Millennium",
                "verses": ["Revelation 20:1-6", "Isaiah 11:6-9"],
                "content": "Christ will reign on earth for a thousand years. Satan will be bound during this time. The martyred saints will be resurrected to reign with Christ. Peace will cover the earth as the waters cover the sea."
            },
            {
                "title": "The Final Judgment",
                "verses": ["Revelation 20:11-15", "2 Corinthians 5:10", "Romans 14:10-12"],
                "content": "All will stand before God's judgment seat. The unsaved will face the great white throne judgment and be cast into the lake of fire. Believers will give account of their works, though they are saved by grace through faith."
            },
            {
                "title": "New Heaven and New Earth",
                "verses": ["Revelation 21:1-4", "2 Peter 3:13", "Isaiah 65:17"],
                "content": "God will create new heavens and a new earth where righteousness dwells. The New Jerusalem will descend from heaven. God will dwell with His people, wiping away every tear. Death, sorrow, and pain will be no more."
            },
            {
                "title": "Living in Light of His Return",
                "verses": ["1 John 3:2-3", "Titus 2:13", "2 Peter 3:11-14"],
                "content": "We are to purify ourselves as we await Christ's appearing. We look for the blessed hope and glorious appearing of our great God and Savior. Since all will be destroyed, we should live holy and godly lives as we look forward to His coming."
            }
        ]
    },
    "spiritual-warfare": {
        "title": "Spiritual Warfare",
        "description": "Fighting the good fight of faith",
        "sections": [
            {
                "title": "Our Real Enemy",
                "verses": ["Ephesians 6:12", "2 Corinthians 10:3-4"],
                "content": "We wrestle not against flesh and blood, but against principalities, powers, and spiritual wickedness in high places. Our warfare is not carnal but spiritual. We must recognize our true enemy is Satan and his demonic forces."
            },
            {
                "title": "The Armor of God",
                "verses": ["Ephesians 6:13-18"],
                "content": "God provides spiritual armor for battle: the belt of truth, breastplate of righteousness, shoes of the gospel of peace, shield of faith, helmet of salvation, and sword of the Spirit. We must take up the full armor to stand against the devil's schemes."
            },
            {
                "title": "The Enemy's Schemes",
                "verses": ["1 Peter 5:8", "2 Corinthians 11:14", "John 8:44"],
                "content": "Our adversary the devil prowls like a roaring lion seeking whom he may devour. He masquerades as an angel of light. He is a liar and the father of lies, seeking to deceive and destroy God's people."
            },
            {
                "title": "Weapons of Our Warfare",
                "verses": ["2 Corinthians 10:4-5", "Hebrews 4:12", "Ephesians 6:17"],
                "content": "Our weapons are divinely powerful for pulling down strongholds. We demolish arguments and pretensions raised against God's knowledge. The Word of God is living and active, sharper than any two-edged sword, our primary offensive weapon."
            },
            {
                "title": "Resisting the Devil",
                "verses": ["James 4:7", "1 Peter 5:9", "Luke 4:8"],
                "content": "Submit to God and resist the devil, and he will flee. Stand firm against him, solid in your faith. Jesus modeled resistance by quoting Scripture when tempted. The Word of God is our defense against Satan's attacks."
            },
            {
                "title": "Victory in Christ",
                "verses": ["1 John 4:4", "Romans 8:37", "Revelation 12:11"],
                "content": "Greater is He who is in us than he who is in the world. We are more than conquerors through Christ who loved us. They overcame Satan by the blood of the Lamb and the word of their testimony. Victory is assured in Christ."
            },
            {
                "title": "Authority Over Evil",
                "verses": ["Luke 10:19", "Mark 16:17", "James 4:7"],
                "content": "Jesus gave us authority to trample on serpents and scorpions and over all the power of the enemy. In His name, we cast out demons. When we resist the devil in Jesus' name, he must flee. We operate in Christ's delegated authority."
            },
            {
                "title": "Prayer: Our Primary Weapon",
                "verses": ["Ephesians 6:18", "Matthew 26:41", "1 Thessalonians 5:17"],
                "content": "We are to pray at all times in the Spirit, with all prayer and supplication. Watch and pray lest you enter into temptation. Pray without ceasing. Prayer is essential in spiritual warfare—it's our communication with our Commander."
            }
        ]
    },
    "spiritual-gifts": {
        "title": "Spiritual Gifts",
        "description": "Gifts of the Holy Spirit for ministry",
        "sections": [
            {
                "title": "Diversity of Gifts",
                "verses": ["1 Corinthians 12:4-6", "Romans 12:6"],
                "content": "There are varieties of gifts, but the same Spirit. There are varieties of service, but the same Lord. God distributes gifts differently to each believer, but all come from the one Spirit for the common good."
            },
            {
                "title": "Gifts for the Common Good",
                "verses": ["1 Corinthians 12:7", "1 Peter 4:10"],
                "content": "Each is given the manifestation of the Spirit for the common good. As good stewards of God's varied grace, we are to use our gifts to serve one another. Gifts aren't for personal glory but for building up the body of Christ."
            },
            {
                "title": "The Motivational Gifts",
                "verses": ["Romans 12:6-8"],
                "content": "Paul lists seven motivational gifts: prophecy, serving, teaching, encouraging, giving, leading, and showing mercy. Each should be exercised according to the measure of faith God has given, with sincerity and diligence."
            },
            {
                "title": "The Ministry Gifts",
                "verses": ["Ephesians 4:11-13"],
                "content": "Christ gave some to be apostles, prophets, evangelists, pastors, and teachers. These equip the saints for the work of ministry, for building up the body of Christ, until we all reach unity in the faith and maturity in Christ."
            },
            {
                "title": "The Manifestation Gifts",
                "verses": ["1 Corinthians 12:8-10"],
                "content": "The Spirit manifests through gifts of wisdom, knowledge, faith, healing, miracles, prophecy, discerning of spirits, tongues, and interpretation of tongues. These supernatural gifts demonstrate God's power and build up the church."
            },
            {
                "title": "Desire the Greater Gifts",
                "verses": ["1 Corinthians 12:31", "1 Corinthians 14:1"],
                "content": "We should eagerly desire the greater gifts, especially prophecy which edifies the church. Paul encourages us to pursue love and earnestly desire spiritual gifts. We should seek gifts that most benefit others and glorify God."
            },
            {
                "title": "Gifts Must Operate in Love",
                "verses": ["1 Corinthians 13:1-3", "1 Corinthians 13:13"],
                "content": "Without love, even the greatest gifts are worthless. Speaking in tongues without love is just noise. Prophecy and knowledge without love profit nothing. Faith, hope, and love remain—but the greatest of these is love."
            },
            {
                "title": "Stewardship of Gifts",
                "verses": ["1 Peter 4:10-11", "Matthew 25:14-30", "1 Timothy 4:14"],
                "content": "We must faithfully steward the gifts God has given. Don't neglect your gift—fan it into flame. Use it to serve others as good stewards of God's grace. We will give account for how we used what He entrusted to us."
            }
        ]
    },
    "the-church": {
        "title": "The Church",
        "description": "The body of Christ and its mission",
        "sections": [
            {
                "title": "Christ Builds His Church",
                "verses": ["Matthew 16:18", "1 Corinthians 3:11"],
                "content": "Jesus declared, 'I will build My church, and the gates of hell shall not prevail against it.' Christ is the foundation—no one can lay another. He is the head, and the church is His body which He purchased with His own blood."
            },
            {
                "title": "The Body of Christ",
                "verses": ["1 Corinthians 12:27", "Ephesians 1:22-23", "Colossians 1:18"],
                "content": "We are the body of Christ, and individually members of it. The church is His body, the fullness of Him who fills all in all. Christ is the head of the body, the beginning, the firstborn from the dead, having preeminence in all things."
            },
            {
                "title": "The Bride of Christ",
                "verses": ["Ephesians 5:25-27", "Revelation 19:7-9"],
                "content": "Christ loved the church and gave Himself for her to make her holy, presenting her to Himself as a radiant bride without spot or wrinkle. The marriage supper of the Lamb is coming when Christ will be united with His bride forever."
            },
            {
                "title": "The Early Church's Devotion",
                "verses": ["Acts 2:42-47"],
                "content": "The early church devoted themselves to the apostles' teaching, fellowship, breaking of bread, and prayer. They had all things in common, sold possessions to help those in need, and met daily with glad and sincere hearts, praising God."
            },
            {
                "title": "Unity in the Body",
                "verses": ["Ephesians 4:3-6", "1 Corinthians 1:10"],
                "content": "We must endeavor to keep the unity of the Spirit in the bond of peace. There is one body, one Spirit, one hope, one Lord, one faith, one baptism, one God and Father of all. We should be perfectly joined together in mind and judgment."
            },
            {
                "title": "The Church's Mission",
                "verses": ["Matthew 28:19-20", "Acts 1:8", "Mark 16:15"],
                "content": "The church's mission is to make disciples of all nations, baptizing and teaching them to obey Christ's commands. We are to be His witnesses to the ends of the earth, preaching the gospel to every creature."
            },
            {
                "title": "Not Forsaking Assembly",
                "verses": ["Hebrews 10:24-25", "Acts 2:46"],
                "content": "We must not forsake assembling together as is the habit of some. Instead, we should encourage one another daily, especially as we see the Day approaching. The early church met daily in homes and the temple, devoted to fellowship and worship."
            },
            {
                "title": "Pillar and Ground of Truth",
                "verses": ["1 Timothy 3:15", "Matthew 5:14-16", "Philippians 2:15"],
                "content": "The church is the pillar and ground of the truth, the household of the living God. We are the light of the world, a city set on a hill that cannot be hidden. We shine as lights in a crooked generation, holding forth the word of life."
            }
        ]
    }
}

new_content.update(final_content)

# Add all content
for slug, content in new_content.items():
    if slug not in data['content']:
        data['content'][slug] = content
        print(f"Added content for: {content['title']}")
    else:
        print(f"Skipped (already exists): {content['title']}")

# Save updated data
with open('kjvstudy_org/data/study_guides.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nTotal content entries: {len(data['content'])}")
print(f"Total catalog entries: {sum(len(guides) for guides in data['catalog'].values())}")
