/**
 * Advanced Search and Navigation System for KJV Study Family Tree
 * Provides comprehensive search capabilities with tree highlighting and breadcrumb navigation
 */

class FamilyTreeSearch {
    constructor(familyData, treeVisualization) {
        this.familyData = familyData;
        this.treeVisualization = treeVisualization;
        this.searchResults = [];
        this.currentHighlights = [];
        this.searchHistory = [];
        this.bookmarks = JSON.parse(localStorage.getItem('familyTreeBookmarks')) || [];
        this.breadcrumbs = [];
        
        this.initializeSearch();
        this.initializeNavigation();
        this.loadBookmarks();
    }

    initializeSearch() {
        // Create search interface
        this.createSearchInterface();
        this.setupSearchEventListeners();
        this.buildSearchIndex();
    }

    createSearchInterface() {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'family-search-container';
        searchContainer.innerHTML = `
            <div class="search-bar-container">
                <div class="search-input-wrapper">
                    <input type="text" id="family-search-input" class="search-input" 
                           placeholder="Search by name, title, or relationship...">
                    <button id="search-clear-btn" class="search-clear-btn" title="Clear search">
                        <i class="fas fa-times"></i>
                    </button>
                    <button id="advanced-search-toggle" class="advanced-search-toggle" title="Advanced search options">
                        <i class="fas fa-cog"></i>
                    </button>
                </div>
                
                <div class="search-filters">
                    <div class="filter-group">
                        <label>Search in:</label>
                        <label><input type="checkbox" name="searchFields" value="name" checked> Names</label>
                        <label><input type="checkbox" name="searchFields" value="title" checked> Titles</label>
                        <label><input type="checkbox" name="searchFields" value="description"> Descriptions</label>
                        <label><input type="checkbox" name="searchFields" value="verses"> Scripture References</label>
                    </div>
                    
                    <div class="filter-group">
                        <label>Gender:</label>
                        <label><input type="radio" name="genderFilter" value="all" checked> All</label>
                        <label><input type="radio" name="genderFilter" value="male"> Male</label>
                        <label><input type="radio" name="genderFilter" value="female"> Female</label>
                    </div>
                    
                    <div class="filter-group">
                        <label>Generation:</label>
                        <select id="generation-filter">
                            <option value="all">All Generations</option>
                            <option value="ancestors">Ancestors Only</option>
                            <option value="descendants">Descendants Only</option>
                            <option value="same">Same Generation</option>
                        </select>
                    </div>
                </div>
                
                <div class="search-results-container">
                    <div class="search-results-header">
                        <span class="results-count">0 results</span>
                        <div class="result-actions">
                            <button id="highlight-all-btn" class="action-btn" title="Highlight all results in tree">
                                <i class="fas fa-highlighter"></i> Highlight All
                            </button>
                            <button id="export-results-btn" class="action-btn" title="Export search results">
                                <i class="fas fa-download"></i> Export
                            </button>
                        </div>
                    </div>
                    <div id="search-results-list" class="search-results-list"></div>
                </div>
            </div>
            
            <div class="navigation-container">
                <div class="breadcrumb-navigation">
                    <div class="breadcrumb-header">
                        <h4>Navigation Path</h4>
                        <button id="clear-breadcrumbs" class="clear-btn" title="Clear navigation history">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    <div id="breadcrumb-trail" class="breadcrumb-trail"></div>
                </div>
                
                <div class="quick-navigation">
                    <div class="nav-section">
                        <h4>Quick Access</h4>
                        <div class="quick-nav-buttons">
                            <button id="nav-root" class="nav-btn" title="Go to tree root">
                                <i class="fas fa-home"></i> Root
                            </button>
                            <button id="nav-back" class="nav-btn" title="Go back">
                                <i class="fas fa-arrow-left"></i> Back
                            </button>
                            <button id="nav-forward" class="nav-btn" title="Go forward">
                                <i class="fas fa-arrow-right"></i> Forward
                            </button>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <h4>Bookmarks</h4>
                        <div class="bookmark-controls">
                            <button id="add-bookmark" class="bookmark-btn" title="Bookmark current person">
                                <i class="fas fa-bookmark"></i> Add
                            </button>
                            <button id="manage-bookmarks" class="bookmark-btn" title="Manage bookmarks">
                                <i class="fas fa-cog"></i> Manage
                            </button>
                        </div>
                        <div id="bookmarks-list" class="bookmarks-list"></div>
                    </div>
                </div>
            </div>
        `;

        // Insert search container into the page
        const familyViewer = document.querySelector('.family-viewer');
        if (familyViewer) {
            familyViewer.insertBefore(searchContainer, familyViewer.firstChild);
        }
    }

    setupSearchEventListeners() {
        const searchInput = document.getElementById('family-search-input');
        const clearBtn = document.getElementById('search-clear-btn');
        const advancedToggle = document.getElementById('advanced-search-toggle');
        const highlightBtn = document.getElementById('highlight-all-btn');
        const exportBtn = document.getElementById('export-results-btn');

        // Search input with debouncing
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.performSearch(e.target.value);
            }, 300);
        });

        // Clear search
        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            this.clearSearch();
        });

        // Toggle advanced filters
        advancedToggle.addEventListener('click', () => {
            const filters = document.querySelector('.search-filters');
            filters.classList.toggle('visible');
        });

        // Filter change events
        document.querySelectorAll('input[name="searchFields"], input[name="genderFilter"]').forEach(input => {
            input.addEventListener('change', () => {
                if (searchInput.value) {
                    this.performSearch(searchInput.value);
                }
            });
        });

        document.getElementById('generation-filter').addEventListener('change', () => {
            if (searchInput.value) {
                this.performSearch(searchInput.value);
            }
        });

        // Result actions
        highlightBtn.addEventListener('click', () => this.highlightAllResults());
        exportBtn.addEventListener('click', () => this.exportSearchResults());
    }

    buildSearchIndex() {
        this.searchIndex = {};
        Object.entries(this.familyData).forEach(([id, person]) => {
            this.searchIndex[id] = {
                id: id,
                name: person.name.toLowerCase(),
                title: (person.title || '').toLowerCase(),
                description: (person.description || '').toLowerCase(),
                verses: this.extractVerseText(person.verses || []).toLowerCase(),
                gender: this.determineGender(person),
                searchText: [
                    person.name,
                    person.title || '',
                    person.description || '',
                    this.extractVerseText(person.verses || [])
                ].join(' ').toLowerCase()
            };
        });
    }

    performSearch(query) {
        if (!query.trim()) {
            this.clearSearch();
            return;
        }

        const searchFields = this.getSelectedSearchFields();
        const genderFilter = this.getSelectedGenderFilter();
        const generationFilter = this.getGenerationFilter();
        
        this.searchResults = this.executeSearch(query, searchFields, genderFilter, generationFilter);
        this.displaySearchResults();
        this.updateResultsCount();
        
        // Add to search history
        this.addToSearchHistory(query);
    }

    executeSearch(query, searchFields, genderFilter, generationFilter) {
        const queryLower = query.toLowerCase();
        const queryTerms = queryLower.split(/\s+/).filter(term => term.length > 0);
        
        return Object.values(this.searchIndex).filter(person => {
            // Gender filter
            if (genderFilter !== 'all' && person.gender !== genderFilter) {
                return false;
            }

            // Generation filter (would need current person context)
            if (generationFilter !== 'all') {
                // Implementation depends on current tree state
                // This is a placeholder for generation-based filtering
            }

            // Text search
            const matchScore = this.calculateMatchScore(person, queryTerms, searchFields);
            return matchScore > 0;
        }).sort((a, b) => {
            // Sort by relevance score
            const scoreA = this.calculateMatchScore(a, queryTerms, searchFields);
            const scoreB = this.calculateMatchScore(b, queryTerms, searchFields);
            return scoreB - scoreA;
        });
    }

    calculateMatchScore(person, queryTerms, searchFields) {
        let score = 0;
        
        queryTerms.forEach(term => {
            searchFields.forEach(field => {
                const fieldValue = person[field] || '';
                if (fieldValue.includes(term)) {
                    // Exact name matches get highest score
                    if (field === 'name' && fieldValue === term) {
                        score += 10;
                    }
                    // Name contains term gets high score
                    else if (field === 'name') {
                        score += 5;
                    }
                    // Other fields get standard score
                    else {
                        score += 1;
                    }
                }
            });
        });

        return score;
    }

    displaySearchResults() {
        const resultsList = document.getElementById('search-results-list');
        resultsList.innerHTML = '';

        if (this.searchResults.length === 0) {
            resultsList.innerHTML = '<div class="no-results">No results found</div>';
            return;
        }

        this.searchResults.forEach((result, index) => {
            const person = this.familyData[result.id];
            const resultElement = document.createElement('div');
            resultElement.className = 'search-result-item';
            resultElement.innerHTML = `
                <div class="result-info">
                    <div class="result-name">${person.name}</div>
                    <div class="result-title">${person.title || 'Biblical Figure'}</div>
                    <div class="result-snippet">${this.createSearchSnippet(person)}</div>
                </div>
                <div class="result-actions">
                    <button class="select-person-btn" data-person-id="${result.id}" title="View this person">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="highlight-person-btn" data-person-id="${result.id}" title="Highlight in tree">
                        <i class="fas fa-highlighter"></i>
                    </button>
                    <button class="bookmark-person-btn" data-person-id="${result.id}" title="Bookmark this person">
                        <i class="fas fa-bookmark"></i>
                    </button>
                </div>
            `;

            // Add event listeners
            resultElement.querySelector('.select-person-btn').addEventListener('click', () => {
                this.selectPerson(result.id);
            });

            resultElement.querySelector('.highlight-person-btn').addEventListener('click', () => {
                this.highlightPersonInTree(result.id);
            });

            resultElement.querySelector('.bookmark-person-btn').addEventListener('click', () => {
                this.addBookmark(result.id);
            });

            resultsList.appendChild(resultElement);
        });
    }

    createSearchSnippet(person) {
        const snippetLength = 100;
        let snippet = person.description || '';
        
        if (snippet.length > snippetLength) {
            snippet = snippet.substring(0, snippetLength) + '...';
        }
        
        return snippet || 'Biblical figure in genealogy';
    }

    // Navigation Methods

    initializeNavigation() {
        this.navigationHistory = [];
        this.navigationIndex = -1;
        this.setupNavigationEventListeners();
    }

    setupNavigationEventListeners() {
        document.getElementById('nav-root').addEventListener('click', () => this.navigateToRoot());
        document.getElementById('nav-back').addEventListener('click', () => this.navigateBack());
        document.getElementById('nav-forward').addEventListener('click', () => this.navigateForward());
        document.getElementById('clear-breadcrumbs').addEventListener('click', () => this.clearBreadcrumbs());
        document.getElementById('add-bookmark').addEventListener('click', () => this.addCurrentBookmark());
        document.getElementById('manage-bookmarks').addEventListener('click', () => this.openBookmarkManager());
    }

    addToBreadcrumbs(personId) {
        const person = this.familyData[personId];
        if (!person) return;

        // Avoid duplicate consecutive entries
        if (this.breadcrumbs.length > 0 && this.breadcrumbs[this.breadcrumbs.length - 1].id === personId) {
            return;
        }

        this.breadcrumbs.push({
            id: personId,
            name: person.name,
            timestamp: Date.now()
        });

        // Limit breadcrumb history
        if (this.breadcrumbs.length > 10) {
            this.breadcrumbs.shift();
        }

        this.updateBreadcrumbDisplay();
    }

    updateBreadcrumbDisplay() {
        const breadcrumbTrail = document.getElementById('breadcrumb-trail');
        breadcrumbTrail.innerHTML = '';

        this.breadcrumbs.forEach((crumb, index) => {
            const crumbElement = document.createElement('div');
            crumbElement.className = 'breadcrumb-item';
            crumbElement.innerHTML = `
                <span class="breadcrumb-name">${crumb.name}</span>
                <button class="breadcrumb-select" data-person-id="${crumb.id}" title="Go to ${crumb.name}">
                    <i class="fas fa-arrow-right"></i>
                </button>
            `;

            crumbElement.querySelector('.breadcrumb-select').addEventListener('click', () => {
                this.selectPerson(crumb.id);
            });

            breadcrumbTrail.appendChild(crumbElement);

            // Add separator
            if (index < this.breadcrumbs.length - 1) {
                const separator = document.createElement('span');
                separator.className = 'breadcrumb-separator';
                separator.textContent = '→';
                breadcrumbTrail.appendChild(separator);
            }
        });
    }

    // Bookmark Management

    addBookmark(personId) {
        const person = this.familyData[personId];
        if (!person) return;

        const bookmark = {
            id: personId,
            name: person.name,
            title: person.title || 'Biblical Figure',
            timestamp: Date.now()
        };

        // Check if already bookmarked
        if (!this.bookmarks.find(b => b.id === personId)) {
            this.bookmarks.push(bookmark);
            this.saveBookmarks();
            this.updateBookmarksDisplay();
            this.showNotification(`${person.name} added to bookmarks`);
        } else {
            this.showNotification(`${person.name} is already bookmarked`);
        }
    }

    removeBookmark(personId) {
        this.bookmarks = this.bookmarks.filter(b => b.id !== personId);
        this.saveBookmarks();
        this.updateBookmarksDisplay();
    }

    saveBookmarks() {
        localStorage.setItem('familyTreeBookmarks', JSON.stringify(this.bookmarks));
    }

    loadBookmarks() {
        this.updateBookmarksDisplay();
    }

    updateBookmarksDisplay() {
        const bookmarksList = document.getElementById('bookmarks-list');
        bookmarksList.innerHTML = '';

        if (this.bookmarks.length === 0) {
            bookmarksList.innerHTML = '<div class="no-bookmarks">No bookmarks yet</div>';
            return;
        }

        this.bookmarks.forEach(bookmark => {
            const bookmarkElement = document.createElement('div');
            bookmarkElement.className = 'bookmark-item';
            bookmarkElement.innerHTML = `
                <div class="bookmark-info">
                    <div class="bookmark-name">${bookmark.name}</div>
                    <div class="bookmark-title">${bookmark.title}</div>
                </div>
                <div class="bookmark-actions">
                    <button class="bookmark-select" data-person-id="${bookmark.id}" title="Go to ${bookmark.name}">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="bookmark-remove" data-person-id="${bookmark.id}" title="Remove bookmark">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;

            bookmarkElement.querySelector('.bookmark-select').addEventListener('click', () => {
                this.selectPerson(bookmark.id);
            });

            bookmarkElement.querySelector('.bookmark-remove').addEventListener('click', () => {
                this.removeBookmark(bookmark.id);
            });

            bookmarksList.appendChild(bookmarkElement);
        });
    }

    // Tree Highlighting

    highlightPersonInTree(personId) {
        // Remove existing highlights
        this.clearHighlights();

        // Add new highlight
        this.currentHighlights.push(personId);
        
        // Update tree visualization
        if (this.treeVisualization && this.treeVisualization.highlightNode) {
            this.treeVisualization.highlightNode(personId);
        }
    }

    highlightAllResults() {
        this.clearHighlights();
        
        this.currentHighlights = this.searchResults.map(result => result.id);
        
        if (this.treeVisualization && this.treeVisualization.highlightNodes) {
            this.treeVisualization.highlightNodes(this.currentHighlights);
        }
    }

    clearHighlights() {
        this.currentHighlights = [];
        
        if (this.treeVisualization && this.treeVisualization.clearHighlights) {
            this.treeVisualization.clearHighlights();
        }
    }

    // Utility Methods

    getSelectedSearchFields() {
        const checkboxes = document.querySelectorAll('input[name="searchFields"]:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    getSelectedGenderFilter() {
        const radio = document.querySelector('input[name="genderFilter"]:checked');
        return radio ? radio.value : 'all';
    }

    getGenerationFilter() {
        const select = document.getElementById('generation-filter');
        return select ? select.value : 'all';
    }

    extractVerseText(verses) {
        if (!Array.isArray(verses)) return '';
        return verses.map(verse => verse.text || '').join(' ');
    }

    determineGender(person) {
        const name = person.name.toLowerCase();
        const femaleNames = ['eve', 'sarah', 'rebekah', 'rachel', 'leah', 'mary', 'elizabeth'];
        return femaleNames.includes(name) ? 'female' : 'male';
    }

    updateResultsCount() {
        const countElement = document.querySelector('.results-count');
        if (countElement) {
            countElement.textContent = `${this.searchResults.length} result${this.searchResults.length !== 1 ? 's' : ''}`;
        }
    }

    clearSearch() {
        this.searchResults = [];
        this.displaySearchResults();
        this.updateResultsCount();
        this.clearHighlights();
    }

    addToSearchHistory(query) {
        if (!this.searchHistory.includes(query)) {
            this.searchHistory.unshift(query);
            if (this.searchHistory.length > 20) {
                this.searchHistory.pop();
            }
        }
    }

    showNotification(message) {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = 'search-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    exportSearchResults() {
        if (this.searchResults.length === 0) {
            this.showNotification('No search results to export');
            return;
        }

        const csvContent = this.generateSearchResultsCSV();
        this.downloadCSV(csvContent, 'family_tree_search_results.csv');
    }

    generateSearchResultsCSV() {
        const headers = ['Name', 'Title', 'Description', 'Birth Year', 'Death Year'];
        const rows = [headers];

        this.searchResults.forEach(result => {
            const person = this.familyData[result.id];
            rows.push([
                person.name,
                person.title || '',
                person.description || '',
                person.birth_year || '',
                person.death_year || ''
            ]);
        });

        return rows.map(row => row.map(field => `"${field}"`).join(',')).join('\n');
    }

    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Public API

    selectPerson(personId) {
        this.addToBreadcrumbs(personId);
        
        // Call the external select person function
        if (window.selectPerson) {
            window.selectPerson(personId);
        }
    }

    getCurrentHighlights() {
        return [...this.currentHighlights];
    }

    getSearchResults() {
        return [...this.searchResults];
    }

    setTreeVisualization(treeViz) {
        this.treeVisualization = treeViz;
    }
}

// CSS Styles for Search Interface
const searchStyles = `
<style>
.family-search-container {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.search-bar-container {
    margin-bottom: 20px;
}

.search-input-wrapper {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.search-input {
    flex: 1;
    padding: 10px 15px;
    border: 2px solid #dee2e6;
    border-radius: 25px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.3s;
}

.search-input:focus {
    border-color: #007bff;
}

.search-clear-btn, .advanced-search-toggle {
    margin-left: 10px;
    padding: 10px;
    border: none;
    background: #6c757d;
    color: white;
    border-radius: 50%;
    cursor: pointer;
    transition: background-color 0.3s;
}

.search-clear-btn:hover, .advanced-search-toggle:hover {
    background: #5a6268;
}

.search-filters {
    display: none;
    background: white;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    margin-bottom: 15px;
}

.search-filters.visible {
    display: block;
}

.filter-group {
    margin-bottom: 15px;
}

.filter-group label {
    margin-right: 15px;
    font-size: 13px;
}

.search-results-container {
    background: white;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.search-results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #dee2e6;
    background: #f8f9fa;
}

.search-results-list {
    max-height: 300px;
    overflow-y: auto;
}

.search-result-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #f1f3f4;
    transition: background-color 0.3s;
}

.search-result-item:hover {
    background: #f8f9fa;
}

.result-name {
    font-weight: bold;
    color: #007bff;
}

.result-title {
    font-size: 13px;
    color: #6c757d;
}

.result-snippet {
    font-size: 12px;
    color: #6c757d;
    margin-top: 5px;
}

.result-actions {
    display: flex;
    gap: 5px;
}

.result-actions button {
    padding: 8px;
    border: none;
    background: #6c757d;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.result-actions button:hover {
    background: #5a6268;
}

.navigation-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 20px;
}

.breadcrumb-navigation, .quick-navigation {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 15px;
}

.breadcrumb-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.breadcrumb-trail {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 5px;
}

.breadcrumb-item {
    display: flex;
    align-items: center;
    padding: 5px 10px;
    background: #f8f9fa;
    border-radius: 15px;
    font-size: 12px;
}

.nav-section {
    margin-bottom: 20px;
}

.nav-section h4 {
    margin-bottom: 10px;
    color: #495057;
}

.quick-nav-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
}

.nav-btn, .bookmark-btn {
    padding: 8px 12px;
    border: 1px solid #dee2e6;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.3s;
}

.nav-btn:hover, .bookmark-btn:hover {
    background: #f8f9fa;
    border-color: #007bff;
}

.bookmarks-list {
    max-height: 200px;
    overflow-y: auto;
}

.bookmark-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #f1f3f4;
}

.bookmark-name {
    font-weight: bold;
    font-size: 13px;
}

.bookmark-title {
    font-size: 11px;
    color: #6c757d;
}

.search-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #28a745;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    font-size: 14px;
    z-index: 1000;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}

@media (max-width: 768px) {
    .navigation-container {
        grid-template-columns: 1fr;
    }
    
    .search-filters {
        padding: 10px;
    }
    
    .filter-group {
        margin-bottom: 10px;
    }
    
    .breadcrumb-trail {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', searchStyles);

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FamilyTreeSearch;
}