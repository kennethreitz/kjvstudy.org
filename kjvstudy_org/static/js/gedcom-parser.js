/**
 * JavaScript GEDCOM Parser for KJV Study Family Tree
 * Parses GEDCOM files directly in the browser without server dependency
 */

class GedcomParser {
    constructor() {
        this.individuals = new Map();
        this.families = new Map();
        this.notes = new Map();
        this.sources = new Map();
        this.rawData = '';
        this.lines = [];
        this.currentIndex = 0;
    }

    /**
     * Parse GEDCOM content from string
     */
    parse(gedcomContent) {
        this.rawData = gedcomContent;
        this.lines = this.preprocessLines(gedcomContent);
        this.currentIndex = 0;
        
        // Clear previous data
        this.individuals.clear();
        this.families.clear();
        this.notes.clear();
        this.sources.clear();

        // Parse all records
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            
            if (line.level === 0) {
                this.parseRecord(line);
            } else {
                this.currentIndex++;
            }
        }

        // Build relationships
        this.buildRelationships();

        return this.buildFamilyTreeData();
    }

    /**
     * Preprocess GEDCOM lines into structured format
     */
    preprocessLines(content) {
        const lines = content.split('\n').map(line => line.trim()).filter(line => line);
        const processed = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const match = line.match(/^(\d+)\s+(@?\w*@?)\s*(.*)/);
            
            if (match) {
                const [, level, tag, value] = match;
                processed.push({
                    level: parseInt(level),
                    tag: tag.replace(/@/g, ''),
                    value: value.trim(),
                    originalLine: line,
                    lineNumber: i + 1
                });
            }
        }

        return processed;
    }

    /**
     * Parse a top-level record
     */
    parseRecord(line) {
        const { tag, value } = line;
        
        switch (value) {
            case 'INDI':
                this.parseIndividual(tag);
                break;
            case 'FAM':
                this.parseFamily(tag);
                break;
            case 'NOTE':
                this.parseNote(tag);
                break;
            case 'SOUR':
                this.parseSource(tag);
                break;
            default:
                this.skipRecord();
                break;
        }
    }

    /**
     * Parse individual record
     */
    parseIndividual(id) {
        const individual = {
            id: id,
            name: '',
            givenName: '',
            surname: '',
            sex: 'U',
            birthDate: '',
            birthPlace: '',
            deathDate: '',
            deathPlace: '',
            occupation: '',
            notes: [],
            sources: [],
            families: {
                spouse: [],
                child: []
            },
            events: []
        };

        this.currentIndex++;
        
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            
            if (line.level === 0) {
                break;
            }

            if (line.level === 1) {
                switch (line.tag) {
                    case 'NAME':
                        this.parseName(individual, line);
                        break;
                    case 'SEX':
                        individual.sex = line.value;
                        break;
                    case 'BIRT':
                        this.parseEvent(individual, 'birth');
                        break;
                    case 'DEAT':
                        this.parseEvent(individual, 'death');
                        break;
                    case 'OCCU':
                        individual.occupation = line.value;
                        break;
                    case 'NOTE':
                        this.parseNoteReference(individual, line);
                        break;
                    case 'FAMS':
                        individual.families.spouse.push(line.value);
                        break;
                    case 'FAMC':
                        individual.families.child.push(line.value);
                        break;
                    default:
                        this.skipSubRecord();
                        continue;
                }
            }
            
            this.currentIndex++;
        }

        this.individuals.set(id, individual);
    }

    /**
     * Parse family record
     */
    parseFamily(id) {
        const family = {
            id: id,
            husband: '',
            wife: '',
            children: [],
            marriageDate: '',
            marriagePlace: '',
            divorceDate: '',
            notes: []
        };

        this.currentIndex++;
        
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            
            if (line.level === 0) {
                break;
            }

            if (line.level === 1) {
                switch (line.tag) {
                    case 'HUSB':
                        family.husband = line.value;
                        break;
                    case 'WIFE':
                        family.wife = line.value;
                        break;
                    case 'CHIL':
                        family.children.push(line.value);
                        break;
                    case 'MARR':
                        this.parseMarriageEvent(family);
                        break;
                    case 'DIV':
                        this.parseDivorceEvent(family);
                        break;
                    case 'NOTE':
                        this.parseNoteReference(family, line);
                        break;
                    default:
                        this.skipSubRecord();
                        continue;
                }
            }
            
            this.currentIndex++;
        }

        this.families.set(id, family);
    }

    /**
     * Parse name field
     */
    parseName(individual, line) {
        let name = line.value;
        
        // Handle GEDCOM name format: "Given /Surname/"
        const nameMatch = name.match(/(.+?)\s*\/(.+?)\//);
        if (nameMatch) {
            individual.givenName = nameMatch[1].trim();
            individual.surname = nameMatch[2].trim();
            individual.name = `${individual.givenName} ${individual.surname}`.trim();
        } else {
            individual.name = name.replace(/\//g, '').trim();
            const nameParts = individual.name.split(' ');
            if (nameParts.length > 1) {
                individual.givenName = nameParts[0];
                individual.surname = nameParts.slice(1).join(' ');
            } else {
                individual.givenName = individual.name;
            }
        }

        // Parse additional name parts
        this.currentIndex++;
        while (this.currentIndex < this.lines.length) {
            const subLine = this.lines[this.currentIndex];
            if (subLine.level <= 1) {
                this.currentIndex--;
                break;
            }

            if (subLine.level === 2) {
                switch (subLine.tag) {
                    case 'GIVN':
                        individual.givenName = subLine.value;
                        break;
                    case 'SURN':
                        individual.surname = subLine.value;
                        break;
                }
            }
            this.currentIndex++;
        }

        // Rebuild full name if parts were specified
        if (individual.givenName && individual.surname) {
            individual.name = `${individual.givenName} ${individual.surname}`;
        }
    }

    /**
     * Parse event (birth, death, etc.)
     */
    parseEvent(individual, eventType) {
        const event = {
            type: eventType,
            date: '',
            place: '',
            description: ''
        };

        this.currentIndex++;
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            if (line.level <= 1) {
                this.currentIndex--;
                break;
            }

            if (line.level === 2) {
                switch (line.tag) {
                    case 'DATE':
                        event.date = line.value;
                        if (eventType === 'birth') {
                            individual.birthDate = line.value;
                        } else if (eventType === 'death') {
                            individual.deathDate = line.value;
                        }
                        break;
                    case 'PLAC':
                        event.place = line.value;
                        if (eventType === 'birth') {
                            individual.birthPlace = line.value;
                        } else if (eventType === 'death') {
                            individual.deathPlace = line.value;
                        }
                        break;
                }
            }
            this.currentIndex++;
        }

        individual.events.push(event);
    }

    /**
     * Parse marriage event
     */
    parseMarriageEvent(family) {
        this.currentIndex++;
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            if (line.level <= 1) {
                this.currentIndex--;
                break;
            }

            if (line.level === 2) {
                switch (line.tag) {
                    case 'DATE':
                        family.marriageDate = line.value;
                        break;
                    case 'PLAC':
                        family.marriagePlace = line.value;
                        break;
                }
            }
            this.currentIndex++;
        }
    }

    /**
     * Parse divorce event
     */
    parseDivorceEvent(family) {
        this.currentIndex++;
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            if (line.level <= 1) {
                this.currentIndex--;
                break;
            }

            if (line.level === 2) {
                if (line.tag === 'DATE') {
                    family.divorceDate = line.value;
                }
            }
            this.currentIndex++;
        }
    }

    /**
     * Parse note record
     */
    parseNote(id) {
        let noteText = '';
        this.currentIndex++;
        
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            
            if (line.level === 0) {
                break;
            }

            if (line.level === 1 && line.tag === 'CONT') {
                noteText += '\n' + line.value;
            } else if (line.level === 1 && line.tag === 'CONC') {
                noteText += line.value;
            }
            
            this.currentIndex++;
        }

        this.notes.set(id, noteText.trim());
    }

    /**
     * Parse source record
     */
    parseSource(id) {
        const source = {
            id: id,
            title: '',
            author: '',
            publication: ''
        };

        this.currentIndex++;
        
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            
            if (line.level === 0) {
                break;
            }

            if (line.level === 1) {
                switch (line.tag) {
                    case 'TITL':
                        source.title = line.value;
                        break;
                    case 'AUTH':
                        source.author = line.value;
                        break;
                    case 'PUBL':
                        source.publication = line.value;
                        break;
                }
            }
            
            this.currentIndex++;
        }

        this.sources.set(id, source);
    }

    /**
     * Parse note reference
     */
    parseNoteReference(record, line) {
        if (line.value.startsWith('@') && line.value.endsWith('@')) {
            // Reference to a note record
            const noteId = line.value.replace(/@/g, '');
            record.notes.push(noteId);
        } else {
            // Inline note
            record.notes.push(line.value);
        }
    }

    /**
     * Skip unknown record
     */
    skipRecord() {
        this.currentIndex++;
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            if (line.level === 0) {
                break;
            }
            this.currentIndex++;
        }
    }

    /**
     * Skip unknown sub-record
     */
    skipSubRecord() {
        const currentLevel = this.lines[this.currentIndex].level;
        this.currentIndex++;
        
        while (this.currentIndex < this.lines.length) {
            const line = this.lines[this.currentIndex];
            if (line.level <= currentLevel) {
                this.currentIndex--;
                break;
            }
            this.currentIndex++;
        }
    }

    /**
     * Build relationships between individuals
     */
    buildRelationships() {
        // Process families to establish relationships
        for (const [familyId, family] of this.families) {
            const husband = this.individuals.get(family.husband);
            const wife = this.individuals.get(family.wife);

            // Set spouse relationships
            if (husband && wife) {
                husband.spouse = wife.name;
                wife.spouse = husband.name;
            }

            // Set parent-child relationships
            for (const childId of family.children) {
                const child = this.individuals.get(childId);
                if (child) {
                    child.parents = [];
                    child.children = child.children || [];

                    // Add parents
                    if (husband) {
                        child.parents.push(family.husband);
                        husband.children = husband.children || [];
                        if (!husband.children.includes(childId)) {
                            husband.children.push(childId);
                        }
                    }
                    if (wife) {
                        child.parents.push(family.wife);
                        wife.children = wife.children || [];
                        if (!wife.children.includes(childId)) {
                            wife.children.push(childId);
                        }
                    }
                }
            }
        }
    }

    /**
     * Build family tree data compatible with existing viewer
     */
    buildFamilyTreeData() {
        const familyTreeData = {};

        for (const [id, individual] of this.individuals) {
            // Filter out non-biblical names
            if (!this.isBiblicalName(individual.name)) {
                continue;
            }
            // Convert birth/death dates to years for compatibility
            const birthYear = this.extractYear(individual.birthDate);
            const deathYear = this.extractYear(individual.deathDate);
            
            // Calculate age at death
            let ageAtDeath = 'Unknown';
            if (birthYear && deathYear) {
                const age = deathYear - birthYear;
                if (age > 0) {
                    ageAtDeath = `${age} years`;
                }
            }

            // Build biblical verses (placeholder)
            const verses = this.getBiblicalVerses(individual.name);

            familyTreeData[id] = {
                name: individual.name || 'Unknown',
                title: individual.occupation || 'Biblical Figure',
                description: this.buildDescription(individual),
                children: individual.children || [],
                parents: individual.parents || [],
                spouse: individual.spouse || null,
                birth_year: individual.birthDate || 'Unknown',
                death_year: individual.deathDate || 'Unknown',
                age_at_death: ageAtDeath,
                verses: verses,
                
                // Additional data for enhanced features
                givenName: individual.givenName,
                surname: individual.surname,
                sex: individual.sex,
                birthPlace: individual.birthPlace,
                deathPlace: individual.deathPlace,
                events: individual.events,
                notes: this.resolveNotes(individual.notes)
            };
        }

        return familyTreeData;
    }

    /**
     * Extract year from date string
     */
    extractYear(dateString) {
        if (!dateString || dateString === 'Unknown') return null;
        
        // Try to match various date formats
        const yearMatch = dateString.match(/(\d{3,4})/);
        if (yearMatch) {
            return parseInt(yearMatch[1]);
        }
        
        return null;
    }

    /**
     * Build description from individual data
     */
    buildDescription(individual) {
        let description = `Biblical figure`;
        
        if (individual.occupation) {
            description += `, ${individual.occupation.toLowerCase()}`;
        }
        
        if (individual.birthPlace) {
            description += ` from ${individual.birthPlace}`;
        }
        
        return description + '.';
    }

    /**
     * Get biblical verses for a person (placeholder implementation)
     */
    getBiblicalVerses(name) {
        // This is a simplified implementation
        // In a real app, you'd have a database of biblical references
        const commonVerses = {
            'adam': [
                { reference: 'Genesis 2:7', text: 'And the LORD God formed man of the dust of the ground...' },
                { reference: 'Genesis 5:5', text: 'And all the days that Adam lived were nine hundred and thirty years...' }
            ],
            'eve': [
                { reference: 'Genesis 2:22', text: 'And the rib, which the LORD God had taken from man, made he a woman...' },
                { reference: 'Genesis 3:20', text: 'And Adam called his wife\'s name Eve; because she was the mother of all living.' }
            ],
            'noah': [
                { reference: 'Genesis 6:9', text: 'Noah was a just man and perfect in his generations...' },
                { reference: 'Genesis 7:1', text: 'Come thou and all thy house into the ark...' }
            ],
            'abraham': [
                { reference: 'Genesis 12:1', text: 'Now the LORD had said unto Abram, Get thee out of thy country...' },
                { reference: 'Genesis 22:2', text: 'Take now thy son, thine only son Isaac, whom thou lovest...' }
            ]
        };

        const key = name.toLowerCase();
        return commonVerses[key] || [];
    }

    /**
     * Resolve note references to actual note text
     */
    resolveNotes(noteRefs) {
        const resolvedNotes = [];
        
        for (const noteRef of noteRefs) {
            if (this.notes.has(noteRef)) {
                resolvedNotes.push(this.notes.get(noteRef));
            } else {
                resolvedNotes.push(noteRef); // Inline note
            }
        }
        
        return resolvedNotes;
    }

    /**
     * Get statistics about the parsed data
     */
    getStatistics() {
        const stats = {
            individuals: this.individuals.size,
            families: this.families.size,
            males: 0,
            females: 0,
            unknown: 0,
            generations: new Set()
        };

        for (const individual of this.individuals.values()) {
            switch (individual.sex) {
                case 'M':
                    stats.males++;
                    break;
                case 'F':
                    stats.females++;
                    break;
                default:
                    stats.unknown++;
                    break;
            }
        }

        return stats;
    }

    /**
     * Find root individuals (those without parents)
     */
    findRoots() {
        const roots = [];
        
        for (const [id, individual] of this.individuals) {
            if (!individual.parents || individual.parents.length === 0) {
                roots.push({ id, individual });
            }
        }
        
        return roots;
    }

    /**
     * Validate the parsed data
     */
    validate() {
        const errors = [];
        const warnings = [];

        // Check for missing individuals referenced in families
        for (const family of this.families.values()) {
            if (family.husband && !this.individuals.has(family.husband)) {
                errors.push(`Missing husband individual: ${family.husband}`);
            }
            if (family.wife && !this.individuals.has(family.wife)) {
                errors.push(`Missing wife individual: ${family.wife}`);
            }
            for (const child of family.children) {
                if (!this.individuals.has(child)) {
                    errors.push(`Missing child individual: ${child}`);
                }
            }
        }

        // Check for individuals without names
        for (const [id, individual] of this.individuals) {
            if (!individual.name) {
                warnings.push(`Individual ${id} has no name`);
            }
        }

        return { errors, warnings };
    }

    /**
     * Check if a name is a biblical figure
     */
    isBiblicalName(name) {
        if (!name || name === 'Unknown') return false;
        
        const nameLower = name.toLowerCase();
        
        // Known non-biblical patterns to exclude
        const nonBiblicalPatterns = [
            /^page\s/i,
            /^mr\./i,
            /^mrs\./i,
            /^dr\./i,
            /robert/i,
            /smith/i,
            /johnson/i,
            /brown/i,
            /williams/i,
            /jones/i,
            /garcia/i,
            /miller/i,
            /davis/i,
            /wilson/i,
            /moore/i,
            /taylor/i,
            /anderson/i,
            /thomas/i,
            /jackson/i,
            /white/i,
            /harris/i,
            /martin/i,
            /thompson/i,
            /young/i,
            /allen/i,
            /king/i,
            /wright/i,
            /lopez/i,
            /hill/i,
            /scott/i,
            /green/i,
            /adams/i,
            /baker/i,
            /gonzalez/i,
            /nelson/i,
            /carter/i,
            /mitchell/i,
            /perez/i,
            /roberts/i,
            /turner/i,
            /phillips/i,
            /campbell/i,
            /parker/i,
            /evans/i,
            /edwards/i,
            /collins/i,
            /stewart/i,
            /sanchez/i,
            /morris/i,
            /rogers/i,
            /reed/i,
            /cook/i,
            /morgan/i,
            /bell/i,
            /murphy/i,
            /bailey/i,
            /rivera/i,
            /cooper/i,
            /richardson/i,
            /cox/i,
            /howard/i,
            /ward/i,
            /torres/i,
            /peterson/i,
            /gray/i,
            /ramirez/i,
            /james/i,
            /watson/i,
            /brooks/i,
            /kelly/i,
            /sanders/i,
            /price/i,
            /bennett/i,
            /wood/i,
            /barnes/i,
            /ross/i,
            /henderson/i,
            /coleman/i,
            /jenkins/i,
            /perry/i,
            /powell/i,
            /long/i,
            /patterson/i,
            /hughes/i,
            /flores/i,
            /washington/i,
            /butler/i,
            /simmons/i,
            /foster/i,
            /gonzales/i,
            /bryant/i,
            /alexander/i,
            /russell/i,
            /griffin/i,
            /diaz/i,
            /hayes/i
        ];
        
        // Check if name matches any non-biblical pattern
        if (nonBiblicalPatterns.some(pattern => pattern.test(name))) {
            return false;
        }
        
        // Known biblical names (comprehensive list)
        const biblicalNames = [
            'adam', 'eve', 'cain', 'abel', 'seth', 'enos', 'cainan', 'mahalaleel',
            'jared', 'enoch', 'methuselah', 'lamech', 'noah', 'shem', 'ham', 'japheth',
            'abraham', 'isaac', 'jacob', 'joseph', 'moses', 'aaron', 'miriam',
            'joshua', 'caleb', 'david', 'solomon', 'samuel', 'saul', 'jonathan',
            'daniel', 'ezekiel', 'jeremiah', 'isaiah', 'hosea', 'joel', 'amos',
            'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai',
            'zechariah', 'malachi', 'matthew', 'mark', 'luke', 'john', 'paul',
            'peter', 'james', 'andrew', 'philip', 'bartholomew', 'thomas', 'simon',
            'thaddeus', 'judas', 'matthias', 'stephen', 'barnabas', 'timothy',
            'titus', 'philemon', 'mary', 'martha', 'elizabeth', 'anna', 'sarah',
            'rebekah', 'rachel', 'leah', 'dinah', 'tamar', 'ruth', 'naomi',
            'esther', 'judith', 'deborah', 'jael', 'huldah', 'abigail', 'bathsheba',
            'gomer', 'rahab', 'dorcas', 'lydia', 'priscilla', 'phoebe', 'eunice',
            'lois', 'claudia', 'tryphena', 'tryphosa', 'persis', 'julia', 'nereus',
            'olympas', 'reuben', 'simeon', 'levi', 'judah', 'zebulun', 'issachar',
            'dan', 'gad', 'asher', 'naphtali', 'benjamin', 'manasseh', 'ephraim',
            'gideon', 'samson', 'eli', 'hannah', 'ruth', 'boaz', 'obed', 'jesse',
            'goliath', 'abner', 'joab', 'uriah', 'nathan', 'zadok', 'benaiah',
            'ahithophel', 'hushai', 'shimei', 'mephibosheth', 'ziba', 'barzillai',
            'elijah', 'elisha', 'gehazi', 'naaman', 'hazael', 'jehu', 'athaliah',
            'joash', 'amaziah', 'uzziah', 'jotham', 'ahaz', 'hezekiah', 'manasseh',
            'amon', 'josiah', 'jehoahaz', 'jehoiakim', 'jehoiachin', 'zedekiah',
            'ezra', 'nehemiah', 'esther', 'mordecai', 'haman', 'vashti', 'zerubbabel',
            'haggai', 'zechariah', 'malachi', 'job', 'bildad', 'eliphaz', 'zophar',
            'elihu', 'cyrus', 'darius', 'artaxerxes', 'ahasuerus', 'nebuchadnezzar',
            'belshazzar', 'shadrach', 'meshach', 'abednego', 'arioch', 'ashpenaz',
            'melzar', 'gabriel', 'michael', 'raphael', 'uriel', 'lucifer', 'satan',
            'beelzebub', 'apollyon', 'abaddon', 'jesus', 'christ', 'emmanuel',
            'immanuel', 'messiah', 'mary', 'joseph', 'zechariah', 'elisabeth',
            'john', 'andrew', 'peter', 'philip', 'bartholomew', 'matthew', 'thomas',
            'james', 'simon', 'judas', 'matthias', 'paul', 'saul', 'barnabas',
            'mark', 'luke', 'timothy', 'titus', 'philemon', 'onesimus', 'epaphras',
            'epaphroditus', 'silas', 'aquila', 'priscilla', 'apollos', 'cephas',
            'stephanas', 'fortunatus', 'achaicus', 'erastus', 'trophimus', 'tychicus',
            'artemas', 'zenas', 'crescens', 'demas', 'hermogenes', 'phygellus',
            'onesiphorus', 'hymenaeus', 'alexander', 'philetus', 'jannes', 'jambres',
            'diotrephes', 'gaius', 'demetrius', 'archippus', 'nympha', 'laodicea',
            'philadelphia', 'sardis', 'thyatira', 'pergamos', 'smyrna', 'ephesus',
            'patmos', 'nicolaitanes', 'balaam', 'balak', 'jezebel', 'ahab', 'elijah',
            'elisha', 'gehazi', 'naaman', 'syria', 'jordan', 'gilead', 'bashan',
            'aroer', 'arnon', 'jabbok', 'peniel', 'mahanaim', 'succoth', 'shechem',
            'bethel', 'ai', 'jericho', 'gilgal', 'shiloh', 'mizpah', 'ramah',
            'gibeah', 'jerusalem', 'zion', 'moriah', 'olivet', 'gethsemane',
            'calvary', 'golgotha', 'bethany', 'bethphage', 'emmaus', 'joppa',
            'lydda', 'caesarea', 'antioch', 'damascus', 'tarsus', 'derbe', 'lystra',
            'iconium', 'pisidian', 'perga', 'attalia', 'salamis', 'paphos', 'cyprus',
            'crete', 'fair', 'havens', 'lasea', 'phoenix', 'clauda', 'melita',
            'malta', 'syracuse', 'rhegium', 'puteoli', 'appii', 'forum', 'rome',
            'spanish', 'illyricum', 'macedonia', 'achaia', 'corinth', 'cenchrea',
            'athens', 'berea', 'thessalonica', 'philippi', 'neapolis', 'samothrace',
            'troas', 'assos', 'mitylene', 'chios', 'samos', 'miletus', 'cos',
            'rhodes', 'patara', 'myra', 'cnidus', 'salmone', 'phenice', 'lasea',
            'melita', 'sicily', 'regium', 'puteoli', 'brundusium', 'appian', 'way',
            'three', 'taverns', 'market', 'appius', 'forum', 'rome', 'palatine',
            'aventine', 'capitoline', 'caelian', 'esquiline', 'quirinal', 'viminal',
            'arphaxad', 'shelah', 'eber', 'peleg', 'reu', 'serug', 'nahor', 'terah',
            'abram', 'lot', 'melchizedek', 'hagar', 'ishmael', 'keturah', 'zimran',
            'jokshan', 'medan', 'midian', 'ishbak', 'shuah', 'sheba', 'dedan',
            'asshurim', 'letushim', 'leummim', 'ephah', 'epher', 'hanoch', 'abida',
            'eldaah', 'esau', 'edom', 'eliphaz', 'reuel', 'jeush', 'jaalam', 'korah',
            'teman', 'omar', 'zepho', 'gatam', 'kenaz', 'timna', 'amalek', 'nahath',
            'zerah', 'shammah', 'mizzah', 'magdiel', 'iram', 'lotan', 'shobal',
            'zibeon', 'anah', 'dishon', 'ezer', 'dishan', 'hori', 'homam', 'alvan',
            'manahath', 'ebal', 'shepho', 'onam', 'ajah', 'dishon', 'hemdan',
            'eshban', 'ithran', 'cheran', 'bilhan', 'zaavan', 'akan', 'uz', 'aran'
        ];
        
        // Check if name (or part of name) is biblical
        const nameWords = nameLower.split(/\s+/);
        const hasKnownBiblicalName = nameWords.some(word => 
            biblicalNames.some(biblical => 
                word.includes(biblical) || biblical.includes(word)
            )
        );
        
        // Check if it has biblical patterns
        const hasHebrewPattern = /^[a-z]*(?:ah|iah|el|ai|im|an|on|ur|ar|am|ab|ad|ag|ak|al|ap|as|at|av|az|ba|be|da|ga|ha|ja|ka|ma|na|ra|sa|ta|za)$/i.test(nameLower);
        
        // Accept if it matches known biblical names or has Hebrew naming patterns
        return hasKnownBiblicalName || (hasHebrewPattern && name.length >= 3);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GedcomParser;
} else if (typeof window !== 'undefined') {
    window.GedcomParser = GedcomParser;
}