// KJV Study Service Worker - Offline Bible Access
const CACHE_VERSION = 'v2';
const STATIC_CACHE = 'kjvstudy-static-' + CACHE_VERSION;
const BIBLE_CACHE = 'kjvstudy-bible-' + CACHE_VERSION;
const PAGE_CACHE = 'kjvstudy-pages-' + CACHE_VERSION;

// Static assets to cache immediately on install
const STATIC_ASSETS = [
  '/',
  '/offline',
  '/static/tufte.css',
  '/static/style.css',
  '/static/app.js',
  '/static/manifest.json',
  '/static/verses-1769.json',
  '/books'
];

// All pages to pre-cache in background (185 pages)
const PAGES_TO_CACHE = [
  "/angels",
  "/apostles",
  "/biblical-timeline",
  "/book/1 Chronicles",
  "/book/1 Corinthians",
  "/book/1 John",
  "/book/1 Kings",
  "/book/1 Peter",
  "/book/1 Samuel",
  "/book/1 Thessalonians",
  "/book/1 Timothy",
  "/book/2 Chronicles",
  "/book/2 Corinthians",
  "/book/2 John",
  "/book/2 Kings",
  "/book/2 Peter",
  "/book/2 Samuel",
  "/book/2 Thessalonians",
  "/book/2 Timothy",
  "/book/3 John",
  "/book/Acts",
  "/book/Amos",
  "/book/Colossians",
  "/book/Daniel",
  "/book/Deuteronomy",
  "/book/Ecclesiastes",
  "/book/Ephesians",
  "/book/Esther",
  "/book/Exodus",
  "/book/Ezekiel",
  "/book/Ezra",
  "/book/Galatians",
  "/book/Genesis",
  "/book/Habakkuk",
  "/book/Haggai",
  "/book/Hebrews",
  "/book/Hosea",
  "/book/Isaiah",
  "/book/James",
  "/book/Jeremiah",
  "/book/Job",
  "/book/Joel",
  "/book/John",
  "/book/Jonah",
  "/book/Joshua",
  "/book/Jude",
  "/book/Judges",
  "/book/Lamentations",
  "/book/Leviticus",
  "/book/Luke",
  "/book/Malachi",
  "/book/Mark",
  "/book/Matthew",
  "/book/Micah",
  "/book/Nahum",
  "/book/Nehemiah",
  "/book/Numbers",
  "/book/Obadiah",
  "/book/Philemon",
  "/book/Philippians",
  "/book/Proverbs",
  "/book/Psalms",
  "/book/Revelation",
  "/book/Romans",
  "/book/Ruth",
  "/book/Song of Solomon",
  "/book/Titus",
  "/book/Zechariah",
  "/book/Zephaniah",
  "/covenants",
  "/family-tree",
  "/festivals",
  "/fruits-of-spirit",
  "/interlinear",
  "/names-of-god",
  "/parables",
  "/prophets",
  "/reading-plans",
  "/reading-plans/chronological",
  "/reading-plans/gospels-acts-30",
  "/reading-plans/nt-90-days",
  "/reading-plans/one-year",
  "/reading-plans/paul-epistles-30",
  "/reading-plans/psalms-proverbs",
  "/resources",
  "/search",
  "/stories",
  "/stories/kids",
  "/strongs",
  "/strongs/greek",
  "/strongs/hebrew",
  "/study-guides",
  "/study-guides/attributes-of-god",
  "/study-guides/biblical-marriage",
  "/study-guides/christian-living",
  "/study-guides/covenant-theology",
  "/study-guides/doctrine-of-scripture",
  "/study-guides/faith-and-works",
  "/study-guides/fruits-spirit",
  "/study-guides/gods-love",
  "/study-guides/gospel",
  "/study-guides/gospel-in-ot",
  "/study-guides/heaven-eternity",
  "/study-guides/hope-comfort",
  "/study-guides/law-and-christian",
  "/study-guides/money-stewardship",
  "/study-guides/new-believer",
  "/study-guides/prayer-faith",
  "/study-guides/problem-of-evil",
  "/study-guides/raising-children",
  "/study-guides/resurrection",
  "/study-guides/salvation",
  "/study-guides/scarlet-thread",
  "/study-guides/sovereignty-of-god",
  "/study-guides/spirits-demons",
  "/study-guides/trinity",
  "/study-guides/wisdom-guidance",
  "/topics",
  "/topics/anxiety",
  "/topics/baptism",
  "/topics/communion",
  "/topics/contentment",
  "/topics/faith",
  "/topics/fasting",
  "/topics/forgiveness",
  "/topics/generosity",
  "/topics/grace",
  "/topics/heaven",
  "/topics/holiness",
  "/topics/holy-spirit",
  "/topics/hope",
  "/topics/humility",
  "/topics/joy",
  "/topics/judgment",
  "/topics/love",
  "/topics/marriage",
  "/topics/mental-health",
  "/topics/obedience",
  "/topics/parenting",
  "/topics/patience",
  "/topics/peace",
  "/topics/prayer",
  "/topics/repentance",
  "/topics/rest",
  "/topics/salvation",
  "/topics/service",
  "/topics/spiritual-warfare",
  "/topics/stewardship",
  "/topics/suffering",
  "/topics/temptation",
  "/topics/the-church",
  "/topics/wisdom",
  "/topics/work",
  "/topics/worship",
  "/twelve-apostles",
  "/verse-of-the-day",
  "/women",
  "/christology",
  "/blood-in-scripture"
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Static assets cached');
        return self.skipWaiting();
      })
      .catch((err) => {
        console.error('[SW] Failed to cache static assets:', err);
      })
  );
});

// Activate event - clean up old caches and start background caching
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            // Delete old version caches
            if (cacheName.startsWith('kjvstudy-') &&
                cacheName !== STATIC_CACHE &&
                cacheName !== BIBLE_CACHE &&
                cacheName !== PAGE_CACHE) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] Service worker activated');
        return self.clients.claim();
      })
      .then(() => {
        // Start background pre-caching after activation
        startBackgroundCaching();
      })
  );
});

// Background pre-caching - cache all pages gradually
let cachingInProgress = false;
let cachedCount = 0;

async function startBackgroundCaching() {
  if (cachingInProgress) return;
  cachingInProgress = true;

  console.log('[SW] Starting background pre-cache of', PAGES_TO_CACHE.length, 'pages...');

  const cache = await caches.open(PAGE_CACHE);

  // Check which pages are already cached
  const uncachedPages = [];
  for (const url of PAGES_TO_CACHE) {
    const cached = await cache.match(url);
    if (!cached) {
      uncachedPages.push(url);
    }
  }

  console.log('[SW] Need to cache', uncachedPages.length, 'pages');

  // Cache pages in batches with delay to avoid overwhelming the server
  const BATCH_SIZE = 5;
  const BATCH_DELAY = 1000; // 1 second between batches

  for (let i = 0; i < uncachedPages.length; i += BATCH_SIZE) {
    const batch = uncachedPages.slice(i, i + BATCH_SIZE);

    await Promise.all(
      batch.map(async (url) => {
        try {
          const response = await fetch(url);
          if (response.ok) {
            await cache.put(url, response);
            cachedCount++;
            // Notify clients of progress
            notifyClients({
              type: 'CACHE_PROGRESS',
              cached: cachedCount,
              total: uncachedPages.length
            });
          }
        } catch (err) {
          console.log('[SW] Failed to cache:', url);
        }
      })
    );

    // Wait between batches
    if (i + BATCH_SIZE < uncachedPages.length) {
      await new Promise(resolve => setTimeout(resolve, BATCH_DELAY));
    }
  }

  console.log('[SW] Background caching complete!', cachedCount, 'pages cached');
  cachingInProgress = false;

  // Notify clients that caching is complete
  notifyClients({ type: 'CACHE_COMPLETE', total: cachedCount });
}

// Notify all clients of caching progress
async function notifyClients(message) {
  const clients = await self.clients.matchAll();
  clients.forEach(client => client.postMessage(message));
}

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Only handle same-origin requests
  if (url.origin !== location.origin) {
    return;
  }

  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip API requests (they need fresh data)
  if (url.pathname.startsWith('/api/')) {
    // For API requests, try network first, then cache for offline
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache successful API responses for offline use
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(PAGE_CACHE).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Offline - try to serve from cache
          return caches.match(event.request);
        })
    );
    return;
  }

  // Static assets - cache first
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(event.request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(event.request).then((response) => {
            if (response.ok) {
              const responseClone = response.clone();
              caches.open(STATIC_CACHE).then((cache) => {
                cache.put(event.request, responseClone);
              });
            }
            return response;
          });
        })
    );
    return;
  }

  // Bible pages (book, chapter, verse) - network first, cache fallback
  if (url.pathname.startsWith('/book/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(BIBLE_CACHE).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Redirect to offline reader with book/chapter info
            const pathMatch = url.pathname.match(/\/book\/([^\/]+)(?:\/chapter\/(\d+))?/);
            if (pathMatch) {
              const book = decodeURIComponent(pathMatch[1]);
              const chapter = pathMatch[2] || '1';
              return Response.redirect('/offline?book=' + encodeURIComponent(book) + '&chapter=' + chapter, 302);
            }
            return caches.match('/offline');
          });
        })
    );
    return;
  }

  // Other pages - network first with cache fallback
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(PAGE_CACHE).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // For HTML pages, return the cached homepage as fallback
          if (event.request.headers.get('Accept')?.includes('text/html')) {
            return caches.match('/');
          }
        });
      })
  );
});

// Handle messages from the main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  // Pre-cache specific book/chapter on demand
  if (event.data && event.data.type === 'CACHE_CHAPTER') {
    const { book, chapter } = event.data;
    const url = `/book/${encodeURIComponent(book)}/chapter/${chapter}`;
    caches.open(BIBLE_CACHE).then((cache) => {
      fetch(url).then((response) => {
        if (response.ok) {
          cache.put(url, response);
        }
      });
    });
  }
});
