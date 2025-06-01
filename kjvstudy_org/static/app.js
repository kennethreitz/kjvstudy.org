// KJV Study - Enhanced Bible Study Platform
// Main JavaScript functionality for interactive features

class KJVStudy {
    constructor() {
        this.preferences = this.loadPreferences();
        this.notes = this.loadNotes();
        this.highlights = this.loadHighlights();
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.applyPreferences();
        this.setupKeyboardShortcuts();
        this.initializeReadingProgress();
    }

    // Preferences Management
    loadPreferences() {
        const defaults = {
            fontSize: 18,
            lineHeight: 1.75,
            showVerseNumbers: true,
            theme: 'light',
            readingMode: 'normal'
        };
        
        const saved = localStorage.getItem('kjv-preferences');
        return saved ? { ...defaults, ...JSON.parse(saved) } : defaults;
    }

    savePreferences() {
        localStorage.setItem('kjv-preferences', JSON.stringify(this.preferences));
    }

    applyPreferences() {
        const versesContainer = document.getElementById('versesContainer');
        if (versesContainer) {
            versesContainer.style.fontSize = this.preferences.fontSize + 'px';
            
            const verses = document.querySelectorAll('.verse');
            verses.forEach(verse => {
                verse.style.lineHeight = this.preferences.lineHeight;
            });
            
            const verseNumbers = document.querySelectorAll('.verse-number');
            verseNumbers.forEach(number => {
                number.style.display = this.preferences.showVerseNumbers ? 'block' : 'none';
            });
        }
    }

    updatePreference(key, value) {
        this.preferences[key] = value;
        this.savePreferences();
        this.applyPreferences();
    }

    // Notes Management
    loadNotes() {
        const saved = localStorage.getItem('kjv-notes');
        return saved ? JSON.parse(saved) : {};
    }

    saveNotes() {
        localStorage.setItem('kjv-notes', JSON.stringify(this.notes));
    }

    addNote(book, chapter, verse, note) {
        const key = `${book}-${chapter}-${verse}`;
        this.notes[key] = {
            text: note,
            timestamp: Date.now(),
            book,
            chapter,
            verse
        };
        this.saveNotes();
        this.displayNoteIndicator(verse);
    }

    getNote(book, chapter, verse) {
        const key = `${book}-${chapter}-${verse}`;
        return this.notes[key];
    }

    displayNoteIndicator(verse) {
        const verseElement = document.getElementById(`verse-${verse}`);
        if (verseElement && !verseElement.querySelector('.note-indicator')) {
            const indicator = document.createElement('span');
            indicator.className = 'note-indicator';
            indicator.innerHTML = '📝';
            indicator.title = 'Has note';
            indicator.style.cssText = `
                margin-left: 0.5rem;
                color: var(--primary-color);
                cursor: pointer;
                font-size: 0.875rem;
            `;
            verseElement.querySelector('.verse-tools').appendChild(indicator);
        }
    }

    // Highlights Management
    loadHighlights() {
        const saved = localStorage.getItem('kjv-highlights');
        return saved ? JSON.parse(saved) : {};
    }

    saveHighlights() {
        localStorage.setItem('kjv-highlights', JSON.stringify(this.highlights));
    }

    toggleHighlight(book, chapter, verse) {
        const key = `${book}-${chapter}-${verse}`;
        const verseElement = document.getElementById(`verse-${verse}`);
        const verseText = verseElement.querySelector('.verse-text');
        
        if (this.highlights[key]) {
            delete this.highlights[key];
            verseText.classList.remove('verse-highlight');
            this.showToast('Highlight removed!');
        } else {
            this.highlights[key] = {
                timestamp: Date.now(),
                book,
                chapter,
                verse
            };
            verseText.classList.add('verse-highlight');
            this.showToast('Verse highlighted!');
        }
        
        this.saveHighlights();
    }

    applyHighlights(book, chapter) {
        Object.keys(this.highlights).forEach(key => {
            const highlight = this.highlights[key];
            if (highlight.book === book && highlight.chapter === chapter) {
                const verseElement = document.getElementById(`verse-${highlight.verse}`);
                if (verseElement) {
                    const verseText = verseElement.querySelector('.verse-text');
                    verseText.classList.add('verse-highlight');
                }
            }
        });
    }

    // Reading Progress
    initializeReadingProgress() {
        const progress = this.loadReadingProgress();
        this.updateReadingProgress();
    }

    loadReadingProgress() {
        const saved = localStorage.getItem('kjv-reading-progress');
        return saved ? JSON.parse(saved) : {};
    }

    saveReadingProgress(book, chapter) {
        const progress = this.loadReadingProgress();
        const key = `${book}-${chapter}`;
        progress[key] = {
            timestamp: Date.now(),
            book,
            chapter
        };
        localStorage.setItem('kjv-reading-progress', JSON.stringify(progress));
    }

    updateReadingProgress() {
        // Mark current chapter as read when user spends time on it
        const currentPath = window.location.pathname;
        const match = currentPath.match(/\/book\/([^\/]+)\/chapter\/(\d+)/);
        
        if (match) {
            const [, book, chapter] = match;
            setTimeout(() => {
                this.saveReadingProgress(book, parseInt(chapter));
            }, 30000); // Mark as read after 30 seconds
        }
    }

    // Search Functionality
    initializeSearch() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
        }
    }

    handleSearch(event) {
        const query = event.target.value.toLowerCase().trim();
        if (query.length < 3) return;

        // This would integrate with a search API in the future
        console.log('Searching for:', query);
        this.showToast('Search feature coming soon!');
    }

    // Keyboard Shortcuts
    setupKeyboardShortcuts() {
        // Enhanced device detection for iPad/tablet
        const isTablet = window.innerWidth >= 768 && window.innerWidth <= 1366;
        const isIPad = /iPad|iPhone|iPod/.test(navigator.userAgent) || 
                      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.getElementById('searchInput');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
            

            
            // Arrow keys for navigation with enhanced tablet support
            if (e.key === 'ArrowLeft' && (e.altKey || (isTablet && e.metaKey))) {
                e.preventDefault();
                const prevButton = document.querySelector('.nav-button[href*="chapter"]') ||
                                 document.querySelector('a[title*="Previous"]') ||
                                 document.querySelector('a:contains("←")');
                if (prevButton) prevButton.click();
            }
            
            if (e.key === 'ArrowRight' && (e.altKey || (isTablet && e.metaKey))) {
                e.preventDefault();
                const nextButton = document.querySelector('.nav-button[href*="chapter"]:last-of-type') ||
                                 document.querySelector('a[title*="Next"]') ||
                                 document.querySelector('a:contains("→")');
                if (nextButton) nextButton.click();
            }
            
            // Enhanced navigation for tablets
            if (isTablet || isIPad) {
                // Tab navigation improvements
                if (e.key === 'Tab') {
                    document.body.classList.add('keyboard-navigation');
                }
                
                // Sidebar navigation with arrow keys
                if (e.target.closest('.sidebar-nav')) {
                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        let next = e.target.nextElementSibling;
                        while (next && next.tagName !== 'A') {
                            next = next.nextElementSibling;
                        }
                        if (next) next.focus();
                    }
                    
                    if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        let prev = e.target.previousElementSibling;
                        while (prev && prev.tagName !== 'A') {
                            prev = prev.previousElementSibling;
                        }
                        if (prev) prev.focus();
                    }
                    
                    // Enter to activate link
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        e.target.click();
                    }
                }
                
                // Quick jump shortcuts for tablets
                if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '9') {
                    e.preventDefault();
                    const index = parseInt(e.key) - 1;
                    const navLinks = document.querySelectorAll('.sidebar-nav a');
                    if (navLinks[index]) {
                        navLinks[index].click();
                    }
                }
                
                // Home/End navigation in chapters
                if (e.key === 'Home' && e.ctrlKey) {
                    e.preventDefault();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
                
                if (e.key === 'End' && e.ctrlKey) {
                    e.preventDefault();
                    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
                }
            }
            
            // Escape to close modals/options
            if (e.key === 'Escape') {
                const readingOptions = document.getElementById('readingOptions');
                if (readingOptions && readingOptions.style.display !== 'none') {
                    readingOptions.style.display = 'none';
                }
                
                // Remove focus from sidebar if escape is pressed
                if (e.target.closest('.sidebar')) {
                    document.querySelector('.main-content').focus();
                }
            }
        });
        
        // Remove keyboard navigation class on mouse use
        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
        
        // Add focus management for better tablet experience
        document.addEventListener('focusin', (e) => {
            if (isTablet || isIPad) {
                // Ensure focused elements are visible
                if (e.target.closest('.sidebar-nav')) {
                    e.target.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                }
            }
        });
    }

    // Event Listeners
    setupEventListeners() {
        // Reading options
        const fontSizeInput = document.getElementById('fontSize');
        if (fontSizeInput) {
            fontSizeInput.addEventListener('change', (e) => {
                this.updatePreference('fontSize', parseInt(e.target.value));
                document.getElementById('fontSizeValue').textContent = e.target.value + 'px';
            });
        }

        const lineHeightInput = document.getElementById('lineHeight');
        if (lineHeightInput) {
            lineHeightInput.addEventListener('change', (e) => {
                this.updatePreference('lineHeight', parseFloat(e.target.value));
                document.getElementById('lineHeightValue').textContent = e.target.value;
            });
        }

        const showVerseNumbersInput = document.getElementById('showVerseNumbers');
        if (showVerseNumbersInput) {
            showVerseNumbersInput.addEventListener('change', (e) => {
                this.updatePreference('showVerseNumbers', e.target.checked);
            });
        }

        // Verse interactions
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('verse-tool')) {
                e.preventDefault();
                this.handleVerseToolClick(e.target);
            }
        });

        // Auto-save scroll position
        window.addEventListener('beforeunload', () => {
            const scrollPosition = window.pageYOffset;
            const path = window.location.pathname;
            localStorage.setItem(`scroll-${path}`, scrollPosition);
        });

        // Restore scroll position
        window.addEventListener('load', () => {
            const path = window.location.pathname;
            const savedPosition = localStorage.getItem(`scroll-${path}`);
            if (savedPosition) {
                window.scrollTo(0, parseInt(savedPosition));
            }
        });
    }

    handleVerseToolClick(tool) {
        const verse = tool.closest('.verse');
        const verseNumber = parseInt(verse.id.split('-')[1]);
        const currentPath = window.location.pathname;
        const match = currentPath.match(/\/book\/([^\/]+)\/chapter\/(\d+)/);
        
        if (!match) return;
        const [, book, chapter] = match;

        const title = tool.title;
        
        if (title.includes('Link')) {
            this.copyVerseLink(book, chapter, verseNumber);
        } else if (title.includes('note')) {
            this.showNoteDialog(book, chapter, verseNumber);
        } else if (title.includes('Highlight')) {
            this.toggleHighlight(book, chapter, verseNumber);
        }
    }

    copyVerseLink(book, chapter, verse) {
        const url = `${window.location.origin}/book/${book}/chapter/${chapter}#verse-${verse}`;
        navigator.clipboard.writeText(url).then(() => {
            this.showToast('Verse link copied to clipboard!');
        }).catch(() => {
            this.showToast('Could not copy link');
        });
    }

    showNoteDialog(book, chapter, verse) {
        const existingNote = this.getNote(book, chapter, verse);
        const noteText = prompt('Add a note for this verse:', existingNote ? existingNote.text : '');
        
        if (noteText !== null) {
            if (noteText.trim()) {
                this.addNote(book, chapter, verse, noteText.trim());
                this.showToast('Note saved!');
            } else if (existingNote) {
                // Remove note if empty
                const key = `${book}-${chapter}-${verse}`;
                delete this.notes[key];
                this.saveNotes();
                const indicator = document.querySelector(`#verse-${verse} .note-indicator`);
                if (indicator) indicator.remove();
                this.showToast('Note removed!');
            }
        }
    }



    // Utility Functions
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.className = `toast toast-${type}`;
        toast.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            background: var(--primary-color);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-md);
            z-index: 1000;
            font-size: 0.875rem;
            box-shadow: var(--shadow-lg);
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;
        
        if (type === 'error') {
            toast.style.background = '#dc2626';
        } else if (type === 'success') {
            toast.style.background = '#059669';
        }
        
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Public API for template functions
    static getInstance() {
        if (!window.kjvStudyInstance) {
            window.kjvStudyInstance = new KJVStudy();
        }
        return window.kjvStudyInstance;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const app = KJVStudy.getInstance();
    
    // Apply highlights and notes to current chapter
    const currentPath = window.location.pathname;
    const match = currentPath.match(/\/book\/([^\/]+)\/chapter\/(\d+)/);
    if (match) {
        const [, book, chapter] = match;
        app.applyHighlights(book, parseInt(chapter));
        
        // Display note indicators
        Object.keys(app.notes).forEach(key => {
            const note = app.notes[key];
            if (note.book === book && note.chapter === parseInt(chapter)) {
                app.displayNoteIndicator(note.verse);
            }
        });
    }
});

// Global functions for template compatibility
function toggleReadingOptions() {
    const options = document.getElementById('readingOptions');
    options.style.display = options.style.display === 'none' ? 'block' : 'none';
}

function updateFontSize(value) {
    KJVStudy.getInstance().updatePreference('fontSize', parseInt(value));
    document.getElementById('fontSizeValue').textContent = value + 'px';
}

function updateLineHeight(value) {
    KJVStudy.getInstance().updatePreference('lineHeight', parseFloat(value));
    document.getElementById('lineHeightValue').textContent = value;
}

function toggleVerseNumbers(show) {
    KJVStudy.getInstance().updatePreference('showVerseNumbers', show);
}

function copyVerseLink(verseNumber) {
    const currentPath = window.location.pathname;
    const match = currentPath.match(/\/book\/([^\/]+)\/chapter\/(\d+)/);
    if (match) {
        const [, book, chapter] = match;
        KJVStudy.getInstance().copyVerseLink(book, parseInt(chapter), verseNumber);
    }
}

function addNote(verseNumber) {
    const currentPath = window.location.pathname;
    const match = currentPath.match(/\/book\/([^\/]+)\/chapter\/(\d+)/);
    if (match) {
        const [, book, chapter] = match;
        KJVStudy.getInstance().showNoteDialog(book, parseInt(chapter), verseNumber);
    }
}

function highlightVerse(verseNumber) {
    const currentPath = window.location.pathname;
    const match = currentPath.match(/\/book\/([^\/]+)\/chapter\/(\d+)/);
    if (match) {
        const [, book, chapter] = match;
        KJVStudy.getInstance().toggleHighlight(book, parseInt(chapter), verseNumber);
    }
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}



// Fix background color issues in browsers
function fixBackgroundColors() {
    const bgColor = getComputedStyle(document.documentElement).getPropertyValue('--background-color').trim();
    const surfaceColor = getComputedStyle(document.documentElement).getPropertyValue('--surface-color').trim();
    
    // Create a fixed background element to ensure full coverage
    const fixedBg = document.createElement('div');
    fixedBg.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: ${bgColor};
        z-index: -999;
        pointer-events: none;
    `;
    document.body.appendChild(fixedBg);
    
    // Apply background color to main elements
    document.body.style.backgroundColor = bgColor;
    document.documentElement.style.backgroundColor = bgColor;
    
    // Apply to main content areas
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.backgroundColor = bgColor;
    }
    
    // Apply to containers
    const containers = document.querySelectorAll('.container, .narrow-container, .commentary-container');
    containers.forEach(container => {
        container.style.backgroundColor = bgColor;
    });
    
    // Apply to cards and content areas
    const surfaceElements = document.querySelectorAll('.verse-card, .commentary-section, .chapter-overview, .verse-text');
    surfaceElements.forEach(element => {
        element.style.backgroundColor = surfaceColor;
    });
    
    // Force the layout to repaint by triggering a reflow
    document.body.offsetHeight;
}

// Run background fix on page load
document.addEventListener('DOMContentLoaded', function() {
    fixBackgroundColors();
    
    // Run again after a slight delay to catch any dynamic content
    setTimeout(fixBackgroundColors, 100);
    
    // Keep applying the fix periodically for the first few seconds
    setTimeout(fixBackgroundColors, 500);
    setTimeout(fixBackgroundColors, 1000);
    setTimeout(fixBackgroundColors, 2000);
    
    // Fix again on window resize
    window.addEventListener('resize', function() {
        fixBackgroundColors();
    });
});