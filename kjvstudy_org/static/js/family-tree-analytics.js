/**
 * Family Tree Analytics and Statistics System for KJV Study
 * Provides comprehensive statistical analysis and insights with interactive charts
 */

class FamilyTreeAnalytics {
    constructor(familyData) {
        this.familyData = familyData;
        this.chartInstances = {};
        this.analysisCache = {};
        
        this.initializeAnalytics();
        this.calculateStatistics();
    }

    initializeAnalytics() {
        this.createAnalyticsInterface();
        this.setupEventListeners();
    }

    createAnalyticsInterface() {
        const analyticsContainer = document.createElement('div');
        analyticsContainer.className = 'family-analytics-container';
        analyticsContainer.innerHTML = `
            <div class="analytics-header">
                <h3><i class="fas fa-chart-bar"></i> Family Tree Analytics</h3>
                <div class="analytics-controls">
                    <button id="refresh-analytics" class="analytics-btn" title="Refresh statistics">
                        <i class="fas fa-sync-alt"></i> Refresh
                    </button>
                    <button id="export-analytics" class="analytics-btn" title="Export analytics report">
                        <i class="fas fa-download"></i> Export Report
                    </button>
                    <button id="toggle-analytics" class="analytics-btn" title="Toggle analytics panel">
                        <i class="fas fa-eye"></i> Toggle
                    </button>
                </div>
            </div>
            
            <div class="analytics-content">
                <!-- Overview Statistics -->
                <div class="stats-overview">
                    <div class="stat-card total-persons">
                        <div class="stat-icon"><i class="fas fa-users"></i></div>
                        <div class="stat-info">
                            <div class="stat-number" id="total-persons">0</div>
                            <div class="stat-label">Total Persons</div>
                        </div>
                    </div>
                    
                    <div class="stat-card male-count">
                        <div class="stat-icon"><i class="fas fa-male"></i></div>
                        <div class="stat-info">
                            <div class="stat-number" id="male-count">0</div>
                            <div class="stat-label">Male</div>
                        </div>
                    </div>
                    
                    <div class="stat-card female-count">
                        <div class="stat-icon"><i class="fas fa-female"></i></div>
                        <div class="stat-info">
                            <div class="stat-number" id="female-count">0</div>
                            <div class="stat-label">Female</div>
                        </div>
                    </div>
                    
                    <div class="stat-card generations-count">
                        <div class="stat-icon"><i class="fas fa-layer-group"></i></div>
                        <div class="stat-info">
                            <div class="stat-number" id="generations-count">0</div>
                            <div class="stat-label">Generations</div>
                        </div>
                    </div>
                    
                    <div class="stat-card families-count">
                        <div class="stat-icon"><i class="fas fa-home"></i></div>
                        <div class="stat-info">
                            <div class="stat-number" id="families-count">0</div>
                            <div class="stat-label">Families</div>
                        </div>
                    </div>
                    
                    <div class="stat-card avg-children">
                        <div class="stat-icon"><i class="fas fa-baby"></i></div>
                        <div class="stat-info">
                            <div class="stat-number" id="avg-children">0</div>
                            <div class="stat-label">Avg Children</div>
                        </div>
                    </div>
                </div>

                <!-- Chart Tabs -->
                <div class="chart-tabs">
                    <button class="tab-btn active" data-tab="demographic">Demographics</button>
                    <button class="tab-btn" data-tab="generational">Generations</button>
                    <button class="tab-btn" data-tab="relationships">Relationships</button>
                    <button class="tab-btn" data-tab="timeline">Timeline</button>
                    <button class="tab-btn" data-tab="longevity">Longevity</button>
                </div>

                <!-- Chart Panels -->
                <div class="chart-panels">
                    <!-- Demographics Panel -->
                    <div class="chart-panel active" id="demographic-panel">
                        <div class="panel-header">
                            <h4>Demographic Analysis</h4>
                            <div class="chart-options">
                                <select id="demographic-chart-type">
                                    <option value="pie">Pie Chart</option>
                                    <option value="bar">Bar Chart</option>
                                    <option value="doughnut">Doughnut Chart</option>
                                </select>
                            </div>
                        </div>
                        <div class="chart-container">
                            <canvas id="demographic-chart"></canvas>
                        </div>
                        <div class="chart-insights">
                            <div class="insight-item">
                                <strong>Gender Ratio:</strong> <span id="gender-ratio">Loading...</span>
                            </div>
                            <div class="insight-item">
                                <strong>Most Common Names:</strong> <span id="common-names">Loading...</span>
                            </div>
                        </div>
                    </div>

                    <!-- Generational Panel -->
                    <div class="chart-panel" id="generational-panel">
                        <div class="panel-header">
                            <h4>Generational Distribution</h4>
                            <div class="chart-options">
                                <select id="generational-metric">
                                    <option value="count">Person Count</option>
                                    <option value="lifespan">Average Lifespan</option>
                                    <option value="children">Children per Generation</option>
                                </select>
                            </div>
                        </div>
                        <div class="chart-container">
                            <canvas id="generational-chart"></canvas>
                        </div>
                        <div class="generation-details">
                            <div id="generation-breakdown"></div>
                        </div>
                    </div>

                    <!-- Relationships Panel -->
                    <div class="chart-panel" id="relationships-panel">
                        <div class="panel-header">
                            <h4>Family Relationships</h4>
                        </div>
                        <div class="relationship-metrics">
                            <div class="metric-grid">
                                <div class="metric-item">
                                    <div class="metric-value" id="married-couples">0</div>
                                    <div class="metric-label">Married Couples</div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-value" id="single-parents">0</div>
                                    <div class="metric-label">Single Parents</div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-value" id="childless-couples">0</div>
                                    <div class="metric-label">Childless Couples</div>
                                </div>
                                <div class="metric-item">
                                    <div class="metric-value" id="largest-family">0</div>
                                    <div class="metric-label">Largest Family</div>
                                </div>
                            </div>
                        </div>
                        <div class="chart-container">
                            <canvas id="relationships-chart"></canvas>
                        </div>
                    </div>

                    <!-- Timeline Panel -->
                    <div class="chart-panel" id="timeline-panel">
                        <div class="panel-header">
                            <h4>Biblical Timeline Analysis</h4>
                            <div class="chart-options">
                                <select id="timeline-view">
                                    <option value="births">Birth Timeline</option>
                                    <option value="lifespans">Lifespan Overview</option>
                                    <option value="generations">Generation Overlap</option>
                                </select>
                            </div>
                        </div>
                        <div class="chart-container timeline-container">
                            <canvas id="timeline-chart"></canvas>
                        </div>
                        <div class="timeline-insights">
                            <div class="insight-grid">
                                <div class="insight-card">
                                    <h5>Longest Lifespan</h5>
                                    <div id="longest-lived">Loading...</div>
                                </div>
                                <div class="insight-card">
                                    <h5>Shortest Lifespan</h5>
                                    <div id="shortest-lived">Loading...</div>
                                </div>
                                <div class="insight-card">
                                    <h5>Average Lifespan</h5>
                                    <div id="average-lifespan">Loading...</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Longevity Panel -->
                    <div class="chart-panel" id="longevity-panel">
                        <div class="panel-header">
                            <h4>Longevity Analysis</h4>
                        </div>
                        <div class="chart-container">
                            <canvas id="longevity-chart"></canvas>
                        </div>
                        <div class="longevity-trends">
                            <div id="longevity-trends-content"></div>
                        </div>
                    </div>
                </div>

                <!-- Detailed Insights Section -->
                <div class="detailed-insights">
                    <h4>Detailed Insights</h4>
                    <div class="insights-grid">
                        <div class="insight-section">
                            <h5>Family Patterns</h5>
                            <ul id="family-patterns"></ul>
                        </div>
                        <div class="insight-section">
                            <h5>Notable Statistics</h5>
                            <ul id="notable-stats"></ul>
                        </div>
                        <div class="insight-section">
                            <h5>Genealogical Insights</h5>
                            <ul id="genealogical-insights"></ul>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Insert analytics container into the page
        const familyViewer = document.querySelector('.family-viewer');
        if (familyViewer) {
            familyViewer.appendChild(analyticsContainer);
        }
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Chart type changes
        document.getElementById('demographic-chart-type')?.addEventListener('change', (e) => {
            this.updateDemographicChart(e.target.value);
        });

        document.getElementById('generational-metric')?.addEventListener('change', (e) => {
            this.updateGenerationalChart(e.target.value);
        });

        document.getElementById('timeline-view')?.addEventListener('change', (e) => {
            this.updateTimelineChart(e.target.value);
        });

        // Control buttons
        document.getElementById('refresh-analytics')?.addEventListener('click', () => {
            this.refreshAnalytics();
        });

        document.getElementById('export-analytics')?.addEventListener('click', () => {
            this.exportAnalyticsReport();
        });

        document.getElementById('toggle-analytics')?.addEventListener('click', () => {
            this.toggleAnalyticsPanel();
        });
    }

    calculateStatistics() {
        this.stats = {
            totalPersons: Object.keys(this.familyData).length,
            genderDistribution: this.calculateGenderDistribution(),
            generationData: this.calculateGenerationData(),
            familyStructure: this.calculateFamilyStructure(),
            lifespanData: this.calculateLifespanData(),
            relationshipMetrics: this.calculateRelationshipMetrics(),
            nameAnalysis: this.calculateNameAnalysis(),
            biblicalTimeline: this.calculateBiblicalTimeline()
        };

        this.updateOverviewStats();
        this.generateInsights();
        this.createCharts();
    }

    calculateGenderDistribution() {
        const genders = { male: 0, female: 0, unknown: 0 };
        
        Object.values(this.familyData).forEach(person => {
            const gender = this.determineGender(person);
            genders[gender]++;
        });

        return genders;
    }

    calculateGenerationData() {
        const generations = {};
        const visited = new Set();

        const mapGeneration = (personId, generation = 0) => {
            if (visited.has(personId)) return;
            visited.add(personId);

            const person = this.familyData[personId];
            if (!person) return;

            if (!generations[generation]) {
                generations[generation] = {
                    count: 0,
                    persons: [],
                    totalLifespan: 0,
                    lifespanCount: 0,
                    totalChildren: 0
                };
            }

            generations[generation].count++;
            generations[generation].persons.push(personId);
            generations[generation].totalChildren += (person.children?.length || 0);

            // Calculate lifespan if available
            const lifespan = this.calculateLifespan(person);
            if (lifespan > 0) {
                generations[generation].totalLifespan += lifespan;
                generations[generation].lifespanCount++;
            }

            // Map children to next generation
            if (person.children) {
                person.children.forEach(childId => {
                    mapGeneration(childId, generation + 1);
                });
            }
        };

        // Start with root figures (those without parents)
        Object.entries(this.familyData).forEach(([id, person]) => {
            if (!person.parents || person.parents.length === 0) {
                mapGeneration(id, 0);
            }
        });

        return generations;
    }

    calculateFamilyStructure() {
        let marriedCouples = 0;
        let singleParents = 0;
        let childlessCouples = 0;
        let largestFamily = 0;
        const familySizes = [];

        Object.values(this.familyData).forEach(person => {
            const childrenCount = person.children?.length || 0;
            
            if (childrenCount > 0) {
                familySizes.push(childrenCount);
                largestFamily = Math.max(largestFamily, childrenCount);
                
                if (person.spouse) {
                    marriedCouples++;
                } else {
                    singleParents++;
                }
            } else if (person.spouse) {
                childlessCouples++;
            }
        });

        return {
            marriedCouples: Math.floor(marriedCouples / 2), // Avoid double counting
            singleParents,
            childlessCouples: Math.floor(childlessCouples / 2),
            largestFamily,
            familySizes,
            averageChildren: familySizes.length > 0 ? 
                (familySizes.reduce((a, b) => a + b, 0) / familySizes.length).toFixed(1) : 0
        };
    }

    calculateLifespanData() {
        const lifespans = [];
        let totalLifespan = 0;
        let lifespanCount = 0;
        let longestLived = { name: '', years: 0 };
        let shortestLived = { name: '', years: Infinity };

        Object.values(this.familyData).forEach(person => {
            const lifespan = this.calculateLifespan(person);
            if (lifespan > 0) {
                lifespans.push({ name: person.name, years: lifespan });
                totalLifespan += lifespan;
                lifespanCount++;

                if (lifespan > longestLived.years) {
                    longestLived = { name: person.name, years: lifespan };
                }
                if (lifespan < shortestLived.years) {
                    shortestLived = { name: person.name, years: lifespan };
                }
            }
        });

        return {
            lifespans,
            averageLifespan: lifespanCount > 0 ? (totalLifespan / lifespanCount).toFixed(1) : 0,
            longestLived: longestLived.years > 0 ? longestLived : null,
            shortestLived: shortestLived.years < Infinity ? shortestLived : null
        };
    }

    calculateRelationshipMetrics() {
        const relationships = {
            parentChild: 0,
            spouses: 0,
            siblings: 0
        };

        Object.values(this.familyData).forEach(person => {
            relationships.parentChild += person.children?.length || 0;
            if (person.spouse) relationships.spouses++;
        });

        relationships.spouses = Math.floor(relationships.spouses / 2); // Avoid double counting

        return relationships;
    }

    calculateNameAnalysis() {
        const nameFrequency = {};
        const nameComponents = {};

        Object.values(this.familyData).forEach(person => {
            const name = person.name.toLowerCase();
            nameFrequency[name] = (nameFrequency[name] || 0) + 1;

            // Analyze name components
            const parts = name.split(' ');
            parts.forEach(part => {
                if (part.length > 2) {
                    nameComponents[part] = (nameComponents[part] || 0) + 1;
                }
            });
        });

        const commonNames = Object.entries(nameFrequency)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5)
            .map(([name, count]) => ({ name, count }));

        return { nameFrequency, nameComponents, commonNames };
    }

    calculateBiblicalTimeline() {
        const timeline = [];
        
        Object.values(this.familyData).forEach(person => {
            const birthYear = this.parseBiblicalYear(person.birth_year);
            const deathYear = this.parseBiblicalYear(person.death_year);
            
            if (birthYear) {
                timeline.push({
                    name: person.name,
                    birthYear,
                    deathYear,
                    lifespan: deathYear ? deathYear - birthYear : null
                });
            }
        });

        return timeline.sort((a, b) => (b.birthYear || 0) - (a.birthYear || 0));
    }

    updateOverviewStats() {
        document.getElementById('total-persons').textContent = this.stats.totalPersons;
        document.getElementById('male-count').textContent = this.stats.genderDistribution.male;
        document.getElementById('female-count').textContent = this.stats.genderDistribution.female;
        document.getElementById('generations-count').textContent = Object.keys(this.stats.generationData).length;
        document.getElementById('families-count').textContent = this.stats.familyStructure.marriedCouples;
        document.getElementById('avg-children').textContent = this.stats.familyStructure.averageChildren;
    }

    createCharts() {
        this.createDemographicChart();
        this.createGenerationalChart();
        this.createRelationshipsChart();
        this.createTimelineChart();
        this.createLongevityChart();
    }

    createDemographicChart(type = 'pie') {
        const ctx = document.getElementById('demographic-chart');
        if (!ctx) return;

        if (this.chartInstances.demographic) {
            this.chartInstances.demographic.destroy();
        }

        const data = {
            labels: ['Male', 'Female', 'Unknown'],
            datasets: [{
                data: [
                    this.stats.genderDistribution.male,
                    this.stats.genderDistribution.female,
                    this.stats.genderDistribution.unknown
                ],
                backgroundColor: ['#2196F3', '#E91E63', '#9E9E9E'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        };

        this.chartInstances.demographic = new Chart(ctx, {
            type: type,
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Gender Distribution'
                    }
                }
            }
        });

        this.updateDemographicInsights();
    }

    createGenerationalChart(metric = 'count') {
        const ctx = document.getElementById('generational-chart');
        if (!ctx) return;

        if (this.chartInstances.generational) {
            this.chartInstances.generational.destroy();
        }

        const generations = this.stats.generationData;
        const labels = Object.keys(generations).map(gen => `Generation ${gen}`);
        let dataValues = [];
        let label = '';

        switch(metric) {
            case 'count':
                dataValues = Object.values(generations).map(gen => gen.count);
                label = 'Number of Persons';
                break;
            case 'lifespan':
                dataValues = Object.values(generations).map(gen => 
                    gen.lifespanCount > 0 ? (gen.totalLifespan / gen.lifespanCount).toFixed(1) : 0
                );
                label = 'Average Lifespan (years)';
                break;
            case 'children':
                dataValues = Object.values(generations).map(gen => 
                    gen.count > 0 ? (gen.totalChildren / gen.count).toFixed(1) : 0
                );
                label = 'Average Children per Person';
                break;
        }

        this.chartInstances.generational = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: dataValues,
                    backgroundColor: '#4CAF50',
                    borderColor: '#388E3C',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: `Generational Analysis - ${label}`
                    }
                }
            }
        });

        this.updateGenerationBreakdown();
    }

    createRelationshipsChart() {
        const ctx = document.getElementById('relationships-chart');
        if (!ctx) return;

        if (this.chartInstances.relationships) {
            this.chartInstances.relationships.destroy();
        }

        const familySizes = this.stats.familyStructure.familySizes;
        const distribution = {};
        
        familySizes.forEach(size => {
            const key = size > 10 ? '10+' : size.toString();
            distribution[key] = (distribution[key] || 0) + 1;
        });

        this.chartInstances.relationships = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(distribution).sort((a, b) => {
                    if (a === '10+') return 1;
                    if (b === '10+') return -1;
                    return parseInt(a) - parseInt(b);
                }),
                datasets: [{
                    label: 'Number of Families',
                    data: Object.values(distribution),
                    backgroundColor: '#FF9800',
                    borderColor: '#F57C00',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Number of Children'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Families'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Family Size Distribution'
                    }
                }
            }
        });

        this.updateRelationshipMetrics();
    }

    createTimelineChart(view = 'births') {
        const ctx = document.getElementById('timeline-chart');
        if (!ctx) return;

        if (this.chartInstances.timeline) {
            this.chartInstances.timeline.destroy();
        }

        const timeline = this.stats.biblicalTimeline.filter(person => person.birthYear);
        
        if (timeline.length === 0) {
            ctx.getContext('2d').clearRect(0, 0, ctx.width, ctx.height);
            return;
        }

        let chartData = {};

        switch(view) {
            case 'births':
                chartData = this.createBirthTimelineData(timeline);
                break;
            case 'lifespans':
                chartData = this.createLifespanTimelineData(timeline);
                break;
            case 'generations':
                chartData = this.createGenerationOverlapData(timeline);
                break;
        }

        this.chartInstances.timeline = new Chart(ctx, chartData);
        this.updateTimelineInsights();
    }

    createLongevityChart() {
        const ctx = document.getElementById('longevity-chart');
        if (!ctx) return;

        if (this.chartInstances.longevity) {
            this.chartInstances.longevity.destroy();
        }

        const lifespans = this.stats.lifespanData.lifespans;
        if (lifespans.length === 0) return;

        // Create age groups
        const ageGroups = {
            '0-100': 0, '101-200': 0, '201-300': 0, '301-400': 0,
            '401-500': 0, '501-600': 0, '601-700': 0, '700+': 0
        };

        lifespans.forEach(person => {
            const age = person.years;
            if (age <= 100) ageGroups['0-100']++;
            else if (age <= 200) ageGroups['101-200']++;
            else if (age <= 300) ageGroups['201-300']++;
            else if (age <= 400) ageGroups['301-400']++;
            else if (age <= 500) ageGroups['401-500']++;
            else if (age <= 600) ageGroups['501-600']++;
            else if (age <= 700) ageGroups['601-700']++;
            else ageGroups['700+']++;
        });

        this.chartInstances.longevity = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(ageGroups),
                datasets: [{
                    data: Object.values(ageGroups),
                    backgroundColor: [
                        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
                        '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Longevity Distribution (Years)'
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        this.updateLongevityTrends();
    }

    // Helper Methods

    determineGender(person) {
        const name = person.name.toLowerCase();
        const femaleNames = [
            'eve', 'sarah', 'sarai', 'rebekah', 'rebecca', 'rachel', 'leah', 'dinah',
            'tamar', 'miriam', 'deborah', 'ruth', 'naomi', 'bathsheba', 'abigail',
            'esther', 'mary', 'elizabeth', 'anna', 'hannah', 'martha'
        ];
        
        if (femaleNames.some(femName => name.includes(femName))) {
            return 'female';
        }
        
        // Check title/description for gender clues
        const description = (person.description || '').toLowerCase();
        const title = (person.title || '').toLowerCase();
        
        if (description.includes('wife') || title.includes('wife') || 
            description.includes('mother') || title.includes('mother')) {
            return 'female';
        }
        
        return 'male'; // Default for biblical genealogies
    }

    calculateLifespan(person) {
        const birthYear = this.parseBiblicalYear(person.birth_year);
        const deathYear = this.parseBiblicalYear(person.death_year);
        
        if (birthYear && deathYear && deathYear > birthYear) {
            return deathYear - birthYear;
        }
        
        // Try to extract from age_at_death
        if (person.age_at_death && person.age_at_death !== "Unknown") {
            const match = person.age_at_death.match(/(\d+)/);
            if (match) {
                return parseInt(match[1]);
            }
        }
        
        return 0;
    }

    parseBiblicalYear(yearString) {
        if (!yearString || yearString === "Unknown") return null;
        
        const match = yearString.match(/(\d+)/);
        return match ? parseInt(match[1]) : null;
    }

    // UI Update Methods

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update panels
        document.querySelectorAll('.chart-panel').forEach(panel => {
            panel.classList.toggle('active', panel.id === `${tabName}-panel`);
        });
    }

    updateDemographicChart(type) {
        this.createDemographicChart(type);
    }

    updateGenerationalChart(metric) {
        this.createGenerationalChart(metric);
    }

    updateTimelineChart(view) {
        this.createTimelineChart(view);
    }

    updateDemographicInsights() {
        const total = this.stats.genderDistribution.male + this.stats.genderDistribution.female;
        const ratio = total > 0 ? 
            `${(this.stats.genderDistribution.male / total * 100).toFixed(1)}% Male, ${(this.stats.genderDistribution.female / total * 100).toFixed(1)}% Female` : 
            'No data';
        
        document.getElementById('gender-ratio').textContent = ratio;
        
        const commonNames = this.stats.nameAnalysis.commonNames
            .slice(0, 3)
            .map(item => item.name)
            .join(', ');
        
        document.getElementById('