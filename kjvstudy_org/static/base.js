// Dark mode functionality
(function() {
  // Check for saved theme preference or default to light mode
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);
})();

function toggleDarkMode() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}

// Red letter toggle functionality
(function() {
  // Check for saved red letter preference or default to enabled
  const redLettersEnabled = localStorage.getItem('redLetters') !== 'disabled';
  if (!redLettersEnabled) {
    document.documentElement.setAttribute('data-red-letters', 'disabled');
  }
})();

function toggleRedLetters() {
  const currentState = document.documentElement.getAttribute('data-red-letters');
  const newState = currentState === 'disabled' ? 'enabled' : 'disabled';

  if (newState === 'disabled') {
    document.documentElement.setAttribute('data-red-letters', 'disabled');
    localStorage.setItem('redLetters', 'disabled');
  } else {
    document.documentElement.removeAttribute('data-red-letters');
    localStorage.removeItem('redLetters');
  }
}

// Sidebar collapse state persistence
(function() {
  var toggle = document.getElementById('sidebar-toggle');
  var savedState = localStorage.getItem('sidebarExpanded');
  var isMobile = window.innerWidth <= 768;

  // If user has explicitly set a preference, respect that
  if (savedState === 'false') {
    toggle.checked = false;
  } else if (savedState === 'true') {
    toggle.checked = true;
  } else {
    // No saved state - default to collapsed on mobile, expanded on desktop
    toggle.checked = !isMobile;
  }

  toggle.addEventListener('change', function() {
    localStorage.setItem('sidebarExpanded', toggle.checked ? 'true' : 'false');
  });
})();

// Details elements (subsections) collapse state persistence
(function() {
  // Get all details elements in sidebar
  var detailsElements = document.querySelectorAll('.nav-sidebar details');

  // Restore saved states
  detailsElements.forEach(function(details) {
    var id = details.id || details.querySelector('summary')?.textContent.trim();
    if (id) {
      var savedState = localStorage.getItem('sidebar-details-' + id);
      if (savedState === 'open') {
        details.open = true;
      } else if (savedState === 'closed') {
        details.open = false;
      }
    }
  });

  // Save state on toggle
  detailsElements.forEach(function(details) {
    details.addEventListener('toggle', function() {
      var id = this.id || this.querySelector('summary')?.textContent.trim();
      if (id) {
        localStorage.setItem('sidebar-details-' + id, this.open ? 'open' : 'closed');
      }
    });
  });
})();

// Universal search functionality with smart verse navigation
(function() {
  var searchInput = document.getElementById('sidebar-search-input');
  var dropdown = document.getElementById('search-results-dropdown');
  if (!searchInput || !dropdown) return;

  var searchTimeout = null;
  var selectedIndex = -1;
  var currentResults = [];

  // Book name mapping (same as homepage)
  var bookMap = {
    'genesis': 'Genesis', 'exodus': 'Exodus', 'leviticus': 'Leviticus', 'numbers': 'Numbers',
    'deuteronomy': 'Deuteronomy', 'joshua': 'Joshua', 'judges': 'Judges', 'ruth': 'Ruth',
    '1 samuel': '1 Samuel', '2 samuel': '2 Samuel', '1 kings': '1 Kings', '2 kings': '2 Kings',
    '1 chronicles': '1 Chronicles', '2 chronicles': '2 Chronicles', 'ezra': 'Ezra', 'nehemiah': 'Nehemiah',
    'esther': 'Esther', 'job': 'Job', 'psalms': 'Psalms', 'psalm': 'Psalms', 'proverbs': 'Proverbs',
    'ecclesiastes': 'Ecclesiastes', 'song of solomon': 'Song of Solomon', 'isaiah': 'Isaiah',
    'jeremiah': 'Jeremiah', 'lamentations': 'Lamentations', 'ezekiel': 'Ezekiel', 'daniel': 'Daniel',
    'hosea': 'Hosea', 'joel': 'Joel', 'amos': 'Amos', 'obadiah': 'Obadiah', 'jonah': 'Jonah',
    'micah': 'Micah', 'nahum': 'Nahum', 'habakkuk': 'Habakkuk', 'zephaniah': 'Zephaniah',
    'haggai': 'Haggai', 'zechariah': 'Zechariah', 'malachi': 'Malachi', 'matthew': 'Matthew',
    'mark': 'Mark', 'luke': 'Luke', 'john': 'John', 'acts': 'Acts', 'romans': 'Romans',
    '1 corinthians': '1 Corinthians', '2 corinthians': '2 Corinthians', 'galatians': 'Galatians',
    'ephesians': 'Ephesians', 'philippians': 'Philippians', 'colossians': 'Colossians',
    '1 thessalonians': '1 Thessalonians', '2 thessalonians': '2 Thessalonians',
    '1 timothy': '1 Timothy', '2 timothy': '2 Timothy', 'titus': 'Titus', 'philemon': 'Philemon',
    'hebrews': 'Hebrews', 'james': 'James', '1 peter': '1 Peter', '2 peter': '2 Peter',
    '1 john': '1 John', '2 john': '2 John', '3 john': '3 John', 'jude': 'Jude', 'revelation': 'Revelation',
    'gen': 'Genesis', 'ex': 'Exodus', 'lev': 'Leviticus', 'num': 'Numbers', 'deut': 'Deuteronomy',
    'josh': 'Joshua', 'judg': 'Judges', 'ru': 'Ruth', '1sam': '1 Samuel', '2sam': '2 Samuel',
    '1ki': '1 Kings', '2ki': '2 Kings', '1chr': '1 Chronicles', '2chr': '2 Chronicles',
    'neh': 'Nehemiah', 'est': 'Esther', 'ps': 'Psalms', 'prov': 'Proverbs', 'eccl': 'Ecclesiastes',
    'isa': 'Isaiah', 'jer': 'Jeremiah', 'lam': 'Lamentations', 'ezek': 'Ezekiel', 'dan': 'Daniel',
    'hos': 'Hosea', 'mic': 'Micah', 'hab': 'Habakkuk', 'zech': 'Zechariah', 'mal': 'Malachi',
    'matt': 'Matthew', 'mk': 'Mark', 'lk': 'Luke', 'jn': 'John', 'rom': 'Romans',
    '1cor': '1 Corinthians', '2cor': '2 Corinthians', 'gal': 'Galatians', 'eph': 'Ephesians',
    'phil': 'Philippians', 'col': 'Colossians', '1thess': '1 Thessalonians', '2thess': '2 Thessalonians',
    '1tim': '1 Timothy', '2tim': '2 Timothy', 'tit': 'Titus', 'heb': 'Hebrews', 'jas': 'James',
    '1pet': '1 Peter', '2pet': '2 Peter', '1jn': '1 John', '2jn': '2 John', '3jn': '3 John', 'rev': 'Revelation'
  };

  function capitalizeBook(name) {
    return bookMap[name.toLowerCase()] || name;
  }

  // Try to parse as verse reference and return URL, or null
  function parseVerseReference(input) {
    // Book Chapter:Verse
    var match = input.match(/^(.+)\s+(\d+):(\d+)$/i);
    if (match) {
      var book = capitalizeBook(match[1].trim());
      return '/book/' + encodeURIComponent(book) + '/chapter/' + match[2] + '/verse/' + match[3];
    }
    // Book Chapter
    match = input.match(/^(.+)\s+(\d+)$/i);
    if (match) {
      var book = capitalizeBook(match[1].trim());
      return '/book/' + encodeURIComponent(book) + '/chapter/' + match[2];
    }
    return null;
  }

  // Category labels
  var categoryLabels = {
    books: 'Books',
    verses: 'Verses',
    topics: 'Topics',
    resources: 'Resources',
    stories: 'Stories',
    plans: 'Reading Plans'
  };

  // Render search results
  function renderResults(data) {
    var results = data.results;
    var html = '';
    currentResults = [];

    // Check if query looks like a verse reference
    var verseUrl = parseVerseReference(data.query);
    if (verseUrl) {
      html += '<div class="search-results-category">';
      html += '<div class="search-results-category-title">Go to</div>';
      currentResults.push(verseUrl);
      html += '<a href="' + verseUrl + '" class="search-result-item selected">';
      html += '<span class="result-title">' + data.query + '</span>';
      html += '<span class="result-meta">Press Enter to navigate</span>';
      html += '</a></div>';
      selectedIndex = 0;
    }

    if (Object.keys(results).length === 0 && !verseUrl) {
      html = '<div class="search-no-results">No results found</div>';
    } else {
      // Render categories in specific order: books, topics, resources, stories, plans, verses
      var categoryOrder = ['books', 'topics', 'resources', 'stories', 'plans', 'verses'];
      categoryOrder.forEach(function(category) {
        if (results[category] && results[category].length > 0) {
          html += '<div class="search-results-category">';
          html += '<div class="search-results-category-title">' + (categoryLabels[category] || category) + '</div>';

          results[category].forEach(function(item) {
            var title = item.name || item.title || item.reference;
            var meta = '';
            if (item.text) meta = item.text;
            else if (item.category) meta = item.category;

            currentResults.push(item.url);
            html += '<a href="' + item.url + '" class="search-result-item">';
            html += '<span class="result-title">' + title + '</span>';
            if (meta) html += '<span class="result-meta">' + meta + '</span>';
            html += '</a>';
          });

          html += '</div>';
        }
      });

      // Add "View all results" link
      html += '<a href="/search?q=' + encodeURIComponent(data.query) + '" class="search-view-all">View all verse results →</a>';
    }

    dropdown.innerHTML = html;
    dropdown.classList.add('show');
    if (!verseUrl) selectedIndex = -1;
  }

  // Perform search
  function doSearch(query) {
    if (query.length < 2) {
      dropdown.classList.remove('show');
      return;
    }

    dropdown.innerHTML = '<div class="search-loading">Searching...</div>';
    dropdown.classList.add('show');

    fetch('/api/universal-search?q=' + encodeURIComponent(query) + '&limit=4')
      .then(function(r) { return r.json(); })
      .then(renderResults)
      .catch(function() {
        dropdown.innerHTML = '<div class="search-no-results">Search error</div>';
      });
  }

  // Input handler with debounce
  searchInput.addEventListener('input', function() {
    var query = this.value.trim();
    clearTimeout(searchTimeout);

    if (query.length < 2) {
      dropdown.classList.remove('show');
      return;
    }

    searchTimeout = setTimeout(function() {
      doSearch(query);
    }, 150);
  });

  // Keyboard navigation
  searchInput.addEventListener('keydown', function(e) {
    var items = dropdown.querySelectorAll('.search-result-item');

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      updateSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, -1);
      updateSelection(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && currentResults[selectedIndex]) {
        window.location.href = currentResults[selectedIndex];
      } else {
        // Try verse reference first, then search
        var verseUrl = parseVerseReference(this.value.trim());
        if (verseUrl) {
          window.location.href = verseUrl;
        } else if (this.value.trim()) {
          window.location.href = '/search?q=' + encodeURIComponent(this.value.trim());
        }
      }
    } else if (e.key === 'Escape') {
      dropdown.classList.remove('show');
      this.blur();
    }
  });

  function updateSelection(items) {
    items.forEach(function(item, i) {
      item.classList.toggle('selected', i === selectedIndex);
    });
  }

  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.sidebar-search')) {
      dropdown.classList.remove('show');
    }
  });

  // Reopen on focus if there's a query
  searchInput.addEventListener('focus', function() {
    if (this.value.trim().length >= 2) {
      doSearch(this.value.trim());
    }
  });
})();

// Global viewport helpers for keyboard navigation
window.KJVNav = {
  isInViewport: function(el) {
    if (!el) return false;
    var rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
  },
  findFirstVisibleIndex: function(elements) {
    for (var i = 0; i < elements.length; i++) {
      if (this.isInViewport(elements[i])) return i;
    }
    return 0;
  },
  isSelectionOffScreen: function(elements, selectedIndex) {
    if (selectedIndex < 0) return true;
    if (selectedIndex >= elements.length) return true;
    return !this.isInViewport(elements[selectedIndex]);
  },
  // Sidebar navigation state
  sidebarActive: false,
  sidebarIndex: -1,
  sidebarLinks: [],
  currentPageNav: null,

  // Activate sidebar navigation with 'n' key
  initSidebarNav: function() {
    var self = this;
    var sidebar = document.querySelector('.nav-sidebar');
    if (!sidebar) return;

    // Get all navigable links in sidebar
    self.sidebarLinks = Array.from(sidebar.querySelectorAll('a'));

    function clearSidebarSelection() {
      self.sidebarLinks.forEach(function(link) {
        link.style.outline = '';
        link.style.background = '';
      });
    }

    function selectSidebarLink(index) {
      clearSidebarSelection();
      if (self.sidebarLinks.length === 0) return;
      self.sidebarIndex = Math.max(0, Math.min(index, self.sidebarLinks.length - 1));
      var link = self.sidebarLinks[self.sidebarIndex];
      link.style.outline = '2px solid #4a7c59';
      link.style.background = 'rgba(74, 124, 89, 0.1)';
      link.scrollIntoView({ behavior: 'auto', block: 'center' });

      // Expand parent details if collapsed
      var details = link.closest('details');
      if (details && !details.open) {
        details.open = true;
      }
    }

    function exitSidebar() {
      clearSidebarSelection();
      self.sidebarActive = false;
      self.sidebarIndex = -1;
      // Close sidebar on mobile when exiting nav mode
      var sidebarToggle = document.getElementById('sidebar-toggle');
      if (sidebarToggle && sidebarToggle.checked) {
        sidebarToggle.checked = false;
      }
      // Clear page nav selection if exists
      if (self.currentPageNav && self.currentPageNav.clearSelection) {
        self.currentPageNav.clearSelection();
      }
    }

    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      // 'n' to enter sidebar nav mode
      if (e.key === 'n' && !self.sidebarActive) {
        e.preventDefault();
        // Open sidebar if it's not visible (mobile/collapsed state)
        var sidebarToggle = document.getElementById('sidebar-toggle');
        if (sidebarToggle && !sidebarToggle.checked) {
          sidebarToggle.checked = true;
        }
        self.sidebarActive = true;
        // Clear any page content selection
        if (self.currentPageNav && self.currentPageNav.clearSelection) {
          self.currentPageNav.clearSelection();
        }
        // Start at first link or current page link
        var currentLink = sidebar.querySelector('a.current');
        var startIndex = currentLink ? self.sidebarLinks.indexOf(currentLink) : 0;
        selectSidebarLink(startIndex >= 0 ? startIndex : 0);
        return;
      }

      // Handle sidebar navigation when active
      if (self.sidebarActive) {
        if (e.key === 'ArrowDown' || e.key === 'j') {
          e.preventDefault();
          selectSidebarLink(self.sidebarIndex + 1);
        } else if (e.key === 'ArrowUp' || e.key === 'k') {
          e.preventDefault();
          selectSidebarLink(self.sidebarIndex - 1);
        } else if (e.key === 'Enter') {
          e.preventDefault();
          if (self.sidebarIndex >= 0 && self.sidebarLinks[self.sidebarIndex]) {
            window.location.href = self.sidebarLinks[self.sidebarIndex].href;
          }
        } else if (e.key === 'Escape') {
          e.preventDefault();
          exitSidebar();
        } else if (e.key === 'ArrowRight' || e.key === 'l') {
          // Expand details or go to link
          e.preventDefault();
          if (self.sidebarIndex >= 0) {
            var link = self.sidebarLinks[self.sidebarIndex];
            var details = link.closest('details');
            var summary = link.closest('summary');
            if (summary && details && !details.open) {
              details.open = true;
            } else {
              window.location.href = link.href;
            }
          }
        } else if (e.key === 'ArrowLeft' || e.key === 'h') {
          // Collapse details or exit sidebar
          e.preventDefault();
          if (self.sidebarIndex >= 0) {
            var link = self.sidebarLinks[self.sidebarIndex];
            var details = link.closest('details');
            if (details && details.open) {
              details.open = false;
            } else {
              exitSidebar();
            }
          } else {
            exitSidebar();
          }
        }
      }
    });
  },

  // Simple linear keyboard navigation - just pass a CSS selector
  initSimpleNav: function(selector, options) {
    options = options || {};
    var elements = Array.from(document.querySelectorAll(selector));
    var selectedIndex = -1;
    var pdfSelector = options.pdfSelector || '[class*="-download-btn"]';
    var self = this;

    function clearSelection() {
      if (selectedIndex >= 0 && selectedIndex < elements.length) {
        elements[selectedIndex].style.outline = '';
        elements[selectedIndex].style.outlineOffset = '';
        elements[selectedIndex].classList.remove('selected');
      }
    }

    function selectElement(index) {
      // Exit sidebar mode if active
      if (self.sidebarActive) {
        self.sidebarActive = false;
        self.sidebarIndex = -1;
        document.querySelectorAll('.nav-sidebar a').forEach(function(link) {
          link.style.outline = '';
          link.style.background = '';
        });
      }
      clearSelection();
      if (elements.length === 0) return;
      selectedIndex = Math.max(0, Math.min(index, elements.length - 1));
      elements[selectedIndex].style.outline = '2px solid #4a7c59';
      elements[selectedIndex].style.outlineOffset = '8px';
      elements[selectedIndex].classList.add('selected');
      elements[selectedIndex].scrollIntoView({ behavior: 'auto', block: 'center' });
    }

    // Store reference for sidebar to clear
    var navInstance = { elements: elements, selectElement: selectElement, clearSelection: clearSelection };
    self.currentPageNav = navInstance;

    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      // Don't handle if sidebar is active (except 'n' is handled above)
      if (self.sidebarActive) return;

      if (e.key === 'ArrowDown' || e.key === 'j') {
        e.preventDefault();
        if (selectedIndex < 0 || KJVNav.isSelectionOffScreen(elements, selectedIndex)) {
          selectElement(KJVNav.findFirstVisibleIndex(elements));
        } else {
          selectElement(selectedIndex + 1);
        }
      } else if (e.key === 'ArrowUp' || e.key === 'k') {
        e.preventDefault();
        if (selectedIndex < 0 || KJVNav.isSelectionOffScreen(elements, selectedIndex)) {
          selectElement(KJVNav.findFirstVisibleIndex(elements));
        } else {
          selectElement(selectedIndex - 1);
        }
      } else if (e.key === 'ArrowLeft' || e.key === 'h') {
        e.preventDefault();
        history.back();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIndex >= 0) {
          var el = elements[selectedIndex];
          var link = el.tagName === 'A' ? el : el.querySelector('a');
          if (link) window.location.href = link.href;
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        clearSelection();
        selectedIndex = -1;
      } else if (e.key === 'p') {
        e.preventDefault();
        var pdfBtn = document.querySelector(pdfSelector);
        if (pdfBtn) window.location.href = pdfBtn.href;
      } else if (e.key === ' ') {
        e.preventDefault();
        if (selectedIndex >= 0 && window.KJVSpeech) {
          var text = elements[selectedIndex].textContent || elements[selectedIndex].innerText;
          KJVSpeech.speak(text);
        }
      }
    });

    return navInstance;
  },

  // 2D Grid navigation for card grids - handles up/down by row, left/right within row
  initGridNav: function(selector, options) {
    options = options || {};
    var gridSelector = options.gridSelector || '.book-grid, .topic-grid, .resource-grid, .story-grid, .card-grid';
    var elements = Array.from(document.querySelectorAll(selector));
    var selectedIndex = -1;
    var self = this;

    function getGridColumns() {
      var grid = document.querySelector(gridSelector);
      if (!grid) return 1;
      var style = getComputedStyle(grid);
      var cols = style.gridTemplateColumns.split(' ').length;
      return cols || 1;
    }

    function clearSelection() {
      if (selectedIndex >= 0 && selectedIndex < elements.length) {
        elements[selectedIndex].style.outline = '';
        elements[selectedIndex].style.outlineOffset = '';
        elements[selectedIndex].classList.remove('selected');
      }
    }

    function selectElement(index) {
      // Exit sidebar mode if active
      if (self.sidebarActive) {
        self.sidebarActive = false;
        self.sidebarIndex = -1;
        document.querySelectorAll('.nav-sidebar a').forEach(function(link) {
          link.style.outline = '';
          link.style.background = '';
        });
      }
      clearSelection();
      if (elements.length === 0) return;
      selectedIndex = Math.max(0, Math.min(index, elements.length - 1));
      elements[selectedIndex].style.outline = '2px solid #4a7c59';
      elements[selectedIndex].style.outlineOffset = '4px';
      elements[selectedIndex].classList.add('selected');
      elements[selectedIndex].scrollIntoView({ behavior: 'auto', block: 'center' });
    }

    // Store reference for sidebar to clear
    var navInstance = { elements: elements, selectElement: selectElement, clearSelection: clearSelection };
    self.currentPageNav = navInstance;

    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (self.sidebarActive) return;

      var cols = getGridColumns();

      if (e.key === 'ArrowDown' || e.key === 'j') {
        e.preventDefault();
        if (selectedIndex < 0) {
          selectElement(0);
        } else {
          selectElement(selectedIndex + cols);
        }
      } else if (e.key === 'ArrowUp' || e.key === 'k') {
        e.preventDefault();
        if (selectedIndex < 0) {
          selectElement(0);
        } else if (selectedIndex - cols >= 0) {
          selectElement(selectedIndex - cols);
        }
      } else if (e.key === 'ArrowRight' || e.key === 'l') {
        e.preventDefault();
        if (selectedIndex < 0) {
          selectElement(0);
        } else {
          selectElement(selectedIndex + 1);
        }
      } else if (e.key === 'ArrowLeft' || e.key === 'h') {
        e.preventDefault();
        if (selectedIndex <= 0) {
          history.back();
        } else {
          selectElement(selectedIndex - 1);
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIndex >= 0) {
          var el = elements[selectedIndex];
          var link = el.tagName === 'A' ? el : el.querySelector('a');
          if (link) window.location.href = link.href;
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        clearSelection();
        selectedIndex = -1;
      } else if (e.key === ' ') {
        e.preventDefault();
        if (selectedIndex >= 0 && window.KJVSpeech) {
          var text = elements[selectedIndex].textContent || elements[selectedIndex].innerText;
          KJVSpeech.speak(text);
        }
      }
    });

    return navInstance;
  }
};

// Initialize sidebar navigation globally
document.addEventListener('DOMContentLoaded', function() {
  KJVNav.initSidebarNav();
});

// Text-to-speech for any selected content
window.KJVSpeech = {
  utterance: null,
  speaking: false,

  speak: function(text) {
    if (!('speechSynthesis' in window)) {
      console.log('Speech synthesis not supported');
      return;
    }

    // Stop any current speech
    this.stop();

    // Clean up the text - remove verse numbers at start, collapse whitespace
    text = text.replace(/^\s*\d+\s*/, '').replace(/\s+/g, ' ').trim();

    if (!text) return;

    this.utterance = new SpeechSynthesisUtterance(text);
    this.utterance.rate = 0.9;
    this.utterance.pitch = 1;

    // Try to use a good English voice
    var voices = speechSynthesis.getVoices();
    var englishVoice = voices.find(function(v) {
      return v.lang.startsWith('en') && v.name.includes('Daniel');
    }) || voices.find(function(v) {
      return v.lang.startsWith('en-GB');
    }) || voices.find(function(v) {
      return v.lang.startsWith('en');
    });

    if (englishVoice) {
      this.utterance.voice = englishVoice;
    }

    this.speaking = true;

    this.utterance.onend = function() {
      KJVSpeech.speaking = false;
    };

    this.utterance.onerror = function() {
      KJVSpeech.speaking = false;
    };

    speechSynthesis.speak(this.utterance);
  },

  stop: function() {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel();
    }
    this.speaking = false;
  },

  toggle: function(text) {
    if (this.speaking) {
      this.stop();
    } else {
      this.speak(text);
    }
  },

  // Get text from the currently selected element (green box)
  getSelectedText: function() {
    // Find element with our green selection outline
    var selected = document.querySelector('[style*="outline: 2px solid"]') ||
                   document.querySelector('[style*="outline:2px solid"]');

    if (selected) {
      return selected.textContent || selected.innerText;
    }

    // Fallback: Try specific verse selectors
    var verseEl = document.querySelector('.verse-text-content') ||
                  document.querySelector('.verse-display .text') ||
                  document.querySelector('.verse-text') ||
                  document.querySelector('[data-verse-text]');

    if (verseEl) {
      return verseEl.textContent || verseEl.innerText;
    }

    return null;
  }
};

// Simple resource reader state (for resource pages)
window.KJVResourceSpeech = {
  speaking: false,
  utterance: null,
  suppressSpace: false
};

// Load voices (they may not be available immediately)
if ('speechSynthesis' in window) {
  speechSynthesis.getVoices();
  speechSynthesis.onvoiceschanged = function() {
    speechSynthesis.getVoices();
  };
}

// Default resource reader unless explicitly disabled
document.addEventListener('DOMContentLoaded', function() {
  if (document.body && !document.body.dataset.resourceReader) {
    document.body.dataset.resourceReader = 'true';
  }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Don't trigger if user is typing in an input field
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
    // Allow Escape to clear focus
    if (e.key === 'Escape') {
      e.target.blur();
    }
    return;
  }

  // Cmd/Ctrl + D: Toggle dark mode
  if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
    e.preventDefault();
    toggleDarkMode();
  }

  // Cmd/Ctrl + B: Toggle sidebar
  if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
    e.preventDefault();
    var toggle = document.getElementById('sidebar-toggle');
    if (toggle) {
      toggle.checked = !toggle.checked;
      toggle.dispatchEvent(new Event('change'));
    }
  }

  // Cmd/Ctrl + K or /: Focus search
  if (((e.metaKey || e.ctrlKey) && e.key === 'k') || e.key === '/') {
    e.preventDefault();
    window.location.href = '/search';
  }

  // Single key shortcuts for navigation (only work without modifiers)
  if (!e.metaKey && !e.ctrlKey && !e.altKey) {
    switch(e.key) {
      case '0':
        e.preventDefault();
        window.location.href = '/';
        break;
      case '1':
        e.preventDefault();
        window.location.href = '/book/Genesis';
        break;
      case '2':
        e.preventDefault();
        window.location.href = '/book/Matthew';
        break;
      case '3':
        e.preventDefault();
        window.location.href = '/book/John';
        break;
      case '4':
        e.preventDefault();
        window.location.href = '/book/Romans';
        break;
      case '7':
        e.preventDefault();
        window.location.href = '/book/Psalms';
        break;
      case '8':
        e.preventDefault();
        window.location.href = '/book/Proverbs';
        break;
      case '9':
        e.preventDefault();
        window.location.href = '/book/Revelation';
        break;
      case '`':
        e.preventDefault();
        var toggle = document.getElementById('sidebar-toggle');
        if (toggle) {
          toggle.checked = !toggle.checked;
          toggle.dispatchEvent(new Event('change'));
        }
        break;
      case 'g':
        e.preventDefault();
        showVerseLookup();
        break;
      case 'r':
        e.preventDefault();
        window.location.href = '/resources';
        break;
      case 'b':
        e.preventDefault();
        window.location.href = '/books';
        break;
      case 's':
        e.preventDefault();
        window.location.href = '/stories';
        break;
      case '/':
        e.preventDefault();
        window.location.href = '/search';
        break;
      case 't':
        e.preventDefault();
        window.location.href = '/topics';
        break;
      case 'p':
        e.preventDefault();
        var pdfBtn = document.querySelector('.pdf-btn, a[href$="/pdf"]');
        if (pdfBtn) window.location.href = pdfBtn.href;
        break;
      case 'f':
        e.preventDefault();
        window.location.href = '/family-tree';
        break;
      case 'c':
        e.preventDefault();
        window.location.href = '/strongs';
        break;
      case 'v':
        e.preventDefault();
        window.location.href = '/verse-of-the-day';
        break;
      case '.':
        e.preventDefault();
        window.location.href = '/random-verse';
        break;
      case '?':
        showKeyboardHelp();
        break;
      case 'R':
        e.preventDefault();
        toggleRedLetters();
        break;
      case ' ':
        // Space: Read aloud selected text (with optional resource-reader handling)
        if (document.body && document.body.dataset && document.body.dataset.resourceReader === 'false') {
          // explicitly disabled
        } else if (document.body) {
          e.preventDefault();
          if (window.KJVResourceSpeech.suppressSpace) return;
          if (!('speechSynthesis' in window)) return;
          // If something is currently speaking or queued, stop it instead of starting a new read
          if (window.KJVResourceSpeech.utterance && (speechSynthesis.speaking || speechSynthesis.pending || speechSynthesis.paused)) {
            speechSynthesis.cancel();
            window.KJVResourceSpeech.speaking = false;
            window.KJVResourceSpeech.utterance = null;
            window.KJVResourceSpeech.suppressSpace = true;
            return;
          }
          if (window.KJVResourceSpeech.speaking) {
            speechSynthesis.cancel();
            window.KJVResourceSpeech.speaking = false;
            window.KJVResourceSpeech.utterance = null;
            window.KJVResourceSpeech.suppressSpace = true;
            return;
          }
          var highlighted = document.querySelector('[style*=\"outline: 2px solid\"]:not(.toc):not(.breadcrumb):not(.chapters-section)') ||
                            document.querySelector('[style*=\"outline:2px solid\"]:not(.toc):not(.breadcrumb):not(.chapters-section)') ||
                            document.querySelector('.selected:not(.toc):not(.breadcrumb):not(.chapters-section)');
          var combined = '';
          if (highlighted) {
            var hclone = highlighted.cloneNode(true);
            hclone.querySelectorAll('.sidenote, .marginnote, .sidenote-number, .margin-toggle, .breadcrumb, .toc, .chapters-section, script, style').forEach(function(el) { el.remove(); });
            combined = (hclone.textContent || hclone.innerText || '').trim();
          } else {
            var article = document.querySelector('article');
            if (article) {
              // If this is a card grid, concatenate the highlighted or first card
              var selectedCard = article.querySelector('.resource-card[style*=\"outline\"]') || article.querySelector('.resource-card');
              if (selectedCard) {
                var cclone = selectedCard.cloneNode(true);
                cclone.querySelectorAll('.sidenote, .marginnote, .sidenote-number, .margin-toggle, .breadcrumb, .toc, .chapters-section, script, style').forEach(function(el) { el.remove(); });
                combined = (cclone.textContent || cclone.innerText || '').trim();
              } else {
                // Prefer reading substantive text blocks instead of the whole article
                var textBlocks = Array.from(article.querySelectorAll('h1, h2, h3, p, li, blockquote, .intro-text, .verse-text, .resource-description, .resource-description-body, .resource-item-description, .parable-description, .angel-description, .covenant-description, .festival-description, .prophet-description, .fruit-description, .name-description, .woman-description, .apostle-description'))
                  .filter(function(el) {
                    if (el.closest('.toc') || el.closest('.chapters-section') || el.closest('.breadcrumb')) return false;
                    var txt = (el.textContent || el.innerText || '').trim();
                    return txt.length > 120;
                  })
                  .map(function(el) {
                    var clone = el.cloneNode(true);
                    clone.querySelectorAll('.sidenote, .marginnote, .sidenote-number, .margin-toggle, .breadcrumb, .toc, .chapters-section, script, style').forEach(function(x) { x.remove(); });
                    return (clone.textContent || clone.innerText || '').trim();
                  })
                  .filter(Boolean);
                if (textBlocks.length > 0) {
                  combined = textBlocks.join('\\n\\n');
                } else {
                  var aclone = article.cloneNode(true);
                  aclone.querySelectorAll('.sidenote, .marginnote, .sidenote-number, .margin-toggle, .breadcrumb, .toc, .chapters-section, script, style').forEach(function(el) { el.remove(); });
                  combined = (aclone.textContent || aclone.innerText || '').trim();
                }
              }
            }
          }
          if (combined) {
            var utter = new SpeechSynthesisUtterance(combined);
            var voices = speechSynthesis.getVoices();
            var englishVoice = voices.find(function(v) { return v.lang && v.lang.toLowerCase().startsWith('en') && v.name.includes('Daniel'); }) ||
                               voices.find(function(v) { return v.lang && v.lang.toLowerCase().startsWith('en-gb'); }) ||
                               voices.find(function(v) { return v.lang && v.lang.toLowerCase().startsWith('en'); });
            if (englishVoice) utter.voice = englishVoice;
            utter.onend = function() {
              window.KJVResourceSpeech.speaking = false;
              window.KJVResourceSpeech.utterance = null;
            };
            utter.onerror = function() {
              window.KJVResourceSpeech.speaking = false;
              window.KJVResourceSpeech.utterance = null;
            };
            window.KJVResourceSpeech.speaking = true;
            window.KJVResourceSpeech.utterance = utter;
            window.KJVResourceSpeech.suppressSpace = false;
            speechSynthesis.cancel();
            speechSynthesis.speak(utter);
          }
        } else {
          var selectedText = KJVSpeech.getSelectedText();
          if (selectedText) {
            e.preventDefault();
            KJVSpeech.toggle(selectedText);
          }
        }
        break;
    }
  }
});

// Clear suppression after spacebar is released
document.addEventListener('keyup', function(e) {
  if (e.key === ' ') {
    window.KJVResourceSpeech.suppressSpace = false;
  }
});

// Quick verse lookup
function showVerseLookup() {
  var reference = prompt('Enter verse reference (e.g., John 3:16, Psalm 23, Genesis 1):');
  if (!reference) return;

  reference = reference.trim();

  // Try to match: Book Chapter:Verse
  var match = reference.match(/^(.+?)\s+(\d+):(\d+)$/i);
  if (match) {
    var book = match[1].trim();
    var chapter = match[2];
    var verse = match[3];
    window.location.href = '/book/' + encodeURIComponent(book) + '/chapter/' + chapter + '/verse/' + verse;
    return;
  }

  // Try to match: Book Chapter
  match = reference.match(/^(.+?)\s+(\d+)$/i);
  if (match) {
    var book = match[1].trim();
    var chapter = match[2];
    window.location.href = '/book/' + encodeURIComponent(book) + '/chapter/' + chapter;
    return;
  }

  // Try to match: Book
  match = reference.match(/^(.+)$/i);
  if (match) {
    var book = match[1].trim();
    window.location.href = '/book/' + encodeURIComponent(book);
    return;
  }
}

// Keyboard shortcuts help modal
function showKeyboardHelp() {
  // Remove existing modal if present
  var existingModal = document.getElementById('keyboard-help-modal');
  if (existingModal) {
    existingModal.remove();
    return;
  }

  var modal = document.createElement('div');
  modal.id = 'keyboard-help-modal';
  modal.innerHTML =
    '<div class="keyboard-help-backdrop"></div>' +
    '<div class="keyboard-help-content">' +
      '<button class="keyboard-help-close" aria-label="Close">&times;</button>' +
      '<h2>Keyboard Shortcuts</h2>' +
      '<div class="keyboard-help-columns">' +
        '<div class="keyboard-help-section">' +
          '<h3>Navigation</h3>' +
          '<div class="shortcut"><kbd>0</kbd><span>Homepage</span></div>' +
          '<div class="shortcut"><kbd>1</kbd><span>Genesis (OT)</span></div>' +
          '<div class="shortcut"><kbd>2</kbd><span>Matthew (NT)</span></div>' +
          '<div class="shortcut"><kbd>3</kbd><span>John</span></div>' +
          '<div class="shortcut"><kbd>4</kbd><span>Romans</span></div>' +
          '<div class="shortcut"><kbd>7</kbd><span>Psalms</span></div>' +
          '<div class="shortcut"><kbd>8</kbd><span>Proverbs</span></div>' +
          '<div class="shortcut"><kbd>9</kbd><span>Revelation</span></div>' +
          '<div class="shortcut"><kbd>b</kbd><span>Books</span></div>' +
          '<div class="shortcut"><kbd>s</kbd><span>Stories</span></div>' +
          '<div class="shortcut"><kbd>r</kbd><span>Resources</span></div>' +
          '<div class="shortcut"><kbd>t</kbd><span>Topics</span></div>' +
          '<div class="shortcut"><kbd>p</kbd><span>PDF (when available)</span></div>' +
          '<div class="shortcut"><kbd>f</kbd><span>Family Tree</span></div>' +
          '<div class="shortcut"><kbd>c</kbd><span>Strong\'s Concordance</span></div>' +
          '<div class="shortcut"><kbd>v</kbd><span>Verse of the Day</span></div>' +
          '<div class="shortcut"><kbd>.</kbd><span>Random Verse</span></div>' +
          '<div class="shortcut"><kbd>g</kbd><span>Quick verse lookup</span></div>' +
        '</div>' +
        '<div class="keyboard-help-section">' +
          '<h3>Page Navigation</h3>' +
          '<div class="shortcut"><kbd>↑</kbd> / <kbd>k</kbd><span>Previous item</span></div>' +
          '<div class="shortcut"><kbd>↓</kbd> / <kbd>j</kbd><span>Next item</span></div>' +
          '<div class="shortcut"><kbd>←</kbd> / <kbd>h</kbd><span>Go back</span></div>' +
          '<div class="shortcut"><kbd>→</kbd> / <kbd>l</kbd><span>Next page</span></div>' +
          '<div class="shortcut"><kbd>Enter</kbd><span>Select / Open</span></div>' +
        '</div>' +
        '<div class="keyboard-help-section">' +
          '<h3>Other</h3>' +
          '<div class="shortcut"><kbd>Space</kbd><span>Read aloud</span></div>' +
          '<div class="shortcut"><kbd>`</kbd><span>Toggle sidebar</span></div>' +
          '<div class="shortcut"><kbd>⌘</kbd>+<kbd>D</kbd><span>Toggle dark mode</span></div>' +
          '<div class="shortcut"><kbd>R</kbd><span>Toggle red letters</span></div>' +
          '<div class="shortcut"><kbd>/</kbd><span>Search</span></div>' +
          '<div class="shortcut"><kbd>?</kbd><span>Show this help</span></div>' +
          '<div class="shortcut"><kbd>Esc</kbd><span>Close / Clear focus</span></div>' +
        '</div>' +
      '</div>' +
    '</div>';

  // Add styles
  var style = document.createElement('style');
  style.textContent =
    '#keyboard-help-modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 10000; display: flex; align-items: center; justify-content: center; }' +
    '.keyboard-help-backdrop { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); }' +
    '.keyboard-help-content { position: relative; background: var(--bg-color); border-radius: 8px; padding: 1.5rem 2rem; max-width: 700px; max-height: 90vh; overflow-y: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }' +
    '.keyboard-help-content h2 { margin: 0 0 1rem 0; font-size: 1.4rem; font-weight: 600; }' +
    '.keyboard-help-close { position: absolute; top: 0.75rem; right: 0.75rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-secondary); padding: 0.25rem 0.5rem; line-height: 1; }' +
    '.keyboard-help-close:hover { color: var(--text-color); }' +
    '.keyboard-help-columns { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }' +
    '.keyboard-help-section h3 { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin: 0 0 0.75rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border-color); }' +
    '.shortcut { display: flex; align-items: center; gap: 0.5rem; margin: 0.4rem 0; font-size: 0.9rem; }' +
    '.shortcut kbd { display: inline-block; padding: 0.15rem 0.4rem; font-family: inherit; font-size: 0.8rem; background: var(--code-bg); border: 1px solid var(--border-color-darker); border-radius: 3px; min-width: 1.5rem; text-align: center; }' +
    '.shortcut span { color: var(--text-secondary); }' +
    '@media (max-width: 700px) { .keyboard-help-columns { grid-template-columns: 1fr; } .keyboard-help-content { margin: 1rem; padding: 1rem 1.5rem; } }';
  modal.appendChild(style);

  document.body.appendChild(modal);

  // Close handlers
  modal.querySelector('.keyboard-help-backdrop').addEventListener('click', function() {
    modal.remove();
  });
  modal.querySelector('.keyboard-help-close').addEventListener('click', function() {
    modal.remove();
  });
  document.addEventListener('keydown', function closeOnEsc(e) {
    if (e.key === 'Escape') {
      modal.remove();
      document.removeEventListener('keydown', closeOnEsc);
    }
  });
}

// Verse tooltip functionality
(function() {
  // Remove any existing tooltip (handles bfcache restoration)
  var existingTooltip = document.querySelector('.verse-tooltip');
  if (existingTooltip) {
    existingTooltip.remove();
  }

  // Create tooltip element
  var tooltip = document.createElement('div');
  tooltip.className = 'verse-tooltip';
  document.body.appendChild(tooltip);

  // Cache for fetched verses
  var verseCache = {};

  // Parse verse URL to extract book, chapter, and verse
  function parseVerseUrl(url) {
    // Try to match single verse URL (old format): /book/John/chapter/3/verse/16
    var match = url.match(/\/book\/([^\/]+)\/chapter\/(\d+)\/verse\/(\d+)/);
    if (match) {
      return {
        book: decodeURIComponent(match[1]),
        chapter: match[2],
        verse: match[3],
        verseEnd: null,
        cacheKey: match[1] + '_' + match[2] + '_' + match[3],
        isRange: false
      };
    }

    // Try to match verse range URL: /book/Proverbs/chapter/31#verse-26-28
    match = url.match(/\/book\/([^\/]+)\/chapter\/(\d+)#verse-(\d+)-(\d+)/);
    if (match) {
      return {
        book: decodeURIComponent(match[1]),
        chapter: match[2],
        verse: match[3],
        verseEnd: match[4],
        cacheKey: match[1] + '_' + match[2] + '_' + match[3] + '-' + match[4],
        isRange: true
      };
    }

    // Try to match single verse anchor URL (new format): /book/John/chapter/3#verse-16
    match = url.match(/\/book\/([^\/]+)\/chapter\/(\d+)#verse-(\d+)$/);
    if (match) {
      return {
        book: decodeURIComponent(match[1]),
        chapter: match[2],
        verse: match[3],
        verseEnd: null,
        cacheKey: match[1] + '_' + match[2] + '_' + match[3],
        isRange: false
      };
    }

    return null;
  }

  // Fetch verse text from server using API
  async function fetchVerseText(book, chapter, verse, verseEnd, cacheKey) {
    // Check cache first
    if (verseCache[cacheKey]) {
      return verseCache[cacheKey];
    }

    try {
      var url;

      if (verseEnd) {
        // Use verse range API endpoint
        url = '/api/verse-range/' + encodeURIComponent(book) + '/' + chapter + '/' + verse + '/' + verseEnd;
      } else {
        // Use single verse API endpoint
        url = '/api/verse/' + encodeURIComponent(book) + '/' + chapter + '/' + verse;
      }

      var response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch verse');

      var data = await response.json();

      // Cache the result
      verseCache[cacheKey] = {
        reference: data.reference,
        text: data.text
      };

      return verseCache[cacheKey];
    } catch (error) {
      console.error('Error fetching verse:', error);
      return {
        reference: verseEnd ? book + ' ' + chapter + ':' + verse + '-' + verseEnd : book + ' ' + chapter + ':' + verse,
        text: 'Error loading verse'
      };
    }
  }

  // Show tooltip
  function showTooltip(verseData, mouseX, mouseY) {
    tooltip.innerHTML =
      '<span class="verse-tooltip-reference">' + verseData.reference + '</span>' +
      '<span class="verse-tooltip-text">' + verseData.text + '</span>';

    // Position tooltip
    var tooltipRect = tooltip.getBoundingClientRect();
    var x = mouseX + 15;
    var y = mouseY + 15;

    // Adjust if tooltip goes off right edge
    if (x + tooltipRect.width > window.innerWidth) {
      x = mouseX - tooltipRect.width - 15;
    }

    // Adjust if tooltip goes off bottom edge
    if (y + tooltipRect.height > window.innerHeight) {
      y = mouseY - tooltipRect.height - 15;
    }

    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
    tooltip.classList.add('show');
  }

  // Hide tooltip
  function hideTooltip() {
    tooltip.classList.remove('show');
  }

  // Event delegation for verse links
  document.addEventListener('mouseover', function(e) {
    var target = e.target;

    // Check if target is a link or inside a link
    if (target.tagName !== 'A') {
      target = target.closest('a');
    }

    if (!target || !target.href) return;

    // Skip if this is a cross-reference link (has its own tooltip system)
    if (target.classList.contains('cross-ref-link')) return;

    // Skip if this is a verse number link (the number at the start of each verse)
    if (target.classList.contains('verse-number-link')) return;

    // Skip links in search dropdowns
    if (target.closest('.search-results-dropdown') || target.closest('.search-dropdown') ||
        target.closest('.lookup-results-dropdown') || target.closest('.story-search-dropdown')) return;

    // Skip links in concordance results (verse text already shown inline)
    if (target.closest('.occurrence-reference') || target.closest('.occurrence')) return;

    // Skip links in cross-references section (has its own CSS tooltip system)
    if (target.closest('.cross-references-section')) return;

    // Skip links in navigation, buttons, actions, headers, and non-content areas
    if (target.closest('nav') || target.closest('header') || target.closest('footer') ||
        target.closest('.toc') || target.closest('.breadcrumb') ||
        target.closest('button') || target.closest('[class*="-btn"]') || target.closest('[class*="-actions"]') ||
        target.closest('[class*="download"]') || target.closest('[class*="print"]') ||
        target.closest('.share-container') || target.closest('.share-buttons') ||
        target.closest('.chapter-nav') || target.closest('.verse-nav') ||
        target.closest('h1') || target.closest('h2') || target.closest('h3')) return;

    // Only show tooltips for links inside content paragraphs, sections, or article content
    if (!target.closest('p') && !target.closest('section') && !target.closest('article') &&
        !target.closest('.verse-item') && !target.closest('.verse-text') &&
        !target.closest('.intro-text') && !target.closest('.description') &&
        !target.closest('.sidenote') && !target.closest('.marginnote') &&
        !target.closest('li')) return;

    var verseInfo = parseVerseUrl(target.pathname + target.hash);
    if (!verseInfo) return;

    // Show loading state
    tooltip.innerHTML = '<span class="verse-tooltip-loading">Loading...</span>';
    tooltip.style.left = (e.pageX + 15) + 'px';
    tooltip.style.top = (e.pageY + 15) + 'px';
    tooltip.classList.add('show');

    // Fetch and display verse
    fetchVerseText(verseInfo.book, verseInfo.chapter, verseInfo.verse, verseInfo.verseEnd, verseInfo.cacheKey)
      .then(function(verseData) {
        // Only show if still hovering
        if (target.matches(':hover')) {
          showTooltip(verseData, e.pageX, e.pageY);
        }
      });

    // Track mouse movement for tooltip positioning
    var mouseMoveHandler = function(e) {
      if (tooltip.classList.contains('show')) {
        var x = e.pageX + 15;
        var y = e.pageY + 15;
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
      }
    };

    target.addEventListener('mousemove', mouseMoveHandler);

    // Hide tooltip on mouse leave
    target.addEventListener('mouseleave', function() {
      hideTooltip();
      target.removeEventListener('mousemove', mouseMoveHandler);
    }, { once: true });
  });

  // Hide tooltip on page restore from bfcache (Safari fix)
  window.addEventListener('pageshow', function() {
    hideTooltip();
    setTimeout(hideTooltip, 0);
    setTimeout(hideTooltip, 100);
  });
})();

// Site-wide verse linking
(function() {
  function linkVerseReferences(element) {
    if (!element) return;

    // Get all text nodes, but skip those inside anchors (already linked)
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, {
      acceptNode: function(node) {
        // Skip text nodes that are inside anchor tags (already linked)
        if (node.parentNode && node.parentNode.tagName === 'A') {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    }, false);
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
      textNodes.push(node);
    }

    textNodes.forEach(function(textNode) {
      let text = textNode.textContent;
      let changed = false;

      // First, handle comma-separated verse lists like "Psalms 7:17, 9:2, 18:13"
      text = text.replace(/\b(\d?\s?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+((?:\d+:\d+(?:-\d+)?(?:\s*,\s*)?)+)/g, function(match, book, verseList) {
        book = book.trim();

        if (!verseList.includes(',')) {
          return match;
        }

        changed = true;

        var verses = verseList.split(/\s*,\s*/);
        var links = verses.map(function(verseRef) {
          verseRef = verseRef.trim();
          var parts = verseRef.match(/^(\d+):(\d+)(?:-(\d+))?$/);
          if (parts) {
            var chapter = parts[1];
            var verseStart = parts[2];
            var verseEnd = parts[3];

            if (verseEnd) {
              return '<a href="/book/' + book + '/chapter/' + chapter + '#verse-' + verseStart + '-' + verseEnd + '">' + book + ' ' + chapter + ':' + verseStart + '-' + verseEnd + '</a>';
            } else {
              return '<a href="/book/' + book + '/chapter/' + chapter + '/verse/' + verseStart + '">' + book + ' ' + chapter + ':' + verseStart + '</a>';
            }
          }
          return verseRef;
        });

        return links.join(', ');
      });

      // Then handle individual verse references like "John 3:16" or "Romans 8:28-29"
      text = text.replace(/\b(\d?\s?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(\d+):(\d+)(?:-(\d+))?\b/g, function(match, book, chapter, verseStart, verseEnd) {
        changed = true;
        book = book.trim();
        if (verseEnd) {
          return '<a href="/book/' + book + '/chapter/' + chapter + '#verse-' + verseStart + '-' + verseEnd + '">' + match + '</a>';
        } else {
          return '<a href="/book/' + book + '/chapter/' + chapter + '/verse/' + verseStart + '">' + match + '</a>';
        }
      });

      if (changed) {
        const span = document.createElement('span');
        span.innerHTML = text;
        textNode.parentNode.replaceChild(span, textNode);
        while (span.firstChild) {
          span.parentNode.insertBefore(span.firstChild, span);
        }
        span.parentNode.removeChild(span);
      }
    });
  }

  // Link verses in common content areas
  document.querySelectorAll('.intro-text, .prophet-description, .angel-description, .covenant-description, p, li').forEach(function(element) {
    // Skip if already processed or if it's in the sidebar
    if (element.closest('.nav-sidebar') || element.dataset.verseLinked) {
      return;
    }
    element.dataset.verseLinked = 'true';
    linkVerseReferences(element);
  });
})();

