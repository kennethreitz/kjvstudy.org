// KJV Study Service Worker - Offline Bible Access
const CACHE_VERSION = 'v6';
const STATIC_CACHE = 'kjvstudy-static-' + CACHE_VERSION;
const PAGE_CACHE = 'kjvstudy-pages-' + CACHE_VERSION;

// Static assets to cache immediately on install
const STATIC_ASSETS = [
  '/',
  '/offline',
  '/static/tufte.css',
  '/static/style.css',
  '/static/manifest.json',
  '/static/verses-1769.json',
  '/books'
];

// Install event - cache static assets only
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

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName.startsWith('kjvstudy-') &&
                cacheName !== STATIC_CACHE &&
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
  );
});

// Parse sitemap XML and extract URLs
async function parseSitemap(url) {
  try {
    const response = await fetch(url);
    const text = await response.text();
    const urls = [];

    // Extract URLs from <loc> tags
    const locRegex = /<loc>([^<]+)<\/loc>/g;
    let match;
    while ((match = locRegex.exec(text)) !== null) {
      // Convert absolute URL to relative path
      let path = match[1].replace(/^https?:\/\/[^\/]+/, '');
      if (path) urls.push(path);
    }

    return urls;
  } catch (err) {
    console.error('[SW] Failed to parse sitemap:', url, err);
    return [];
  }
}

// Get all URLs from sitemaps
async function getAllUrlsFromSitemaps() {
  const allUrls = new Set();

  // First, fetch the sitemap index
  try {
    const indexResponse = await fetch('/sitemap.xml');
    const indexText = await indexResponse.text();

    // Check if it's a sitemap index (has <sitemapindex>)
    if (indexText.includes('<sitemapindex')) {
      // Extract child sitemap URLs
      const sitemapUrls = [];
      const locRegex = /<loc>([^<]+)<\/loc>/g;
      let match;
      while ((match = locRegex.exec(indexText)) !== null) {
        let sitemapUrl = match[1].replace(/^https?:\/\/[^\/]+/, '');
        sitemapUrls.push(sitemapUrl);
      }

      // Fetch each child sitemap
      for (const sitemapUrl of sitemapUrls) {
        const urls = await parseSitemap(sitemapUrl);
        urls.forEach(url => allUrls.add(url));
      }
    } else {
      // It's a regular sitemap
      const urls = await parseSitemap('/sitemap.xml');
      urls.forEach(url => allUrls.add(url));
    }
  } catch (err) {
    console.error('[SW] Failed to fetch sitemap index:', err);
  }

  return Array.from(allUrls);
}

// Background pre-caching - only triggered when user requests it
let cachingInProgress = false;
let cachedCount = 0;
let totalToCache = 0;

async function startBackgroundCaching() {
  if (cachingInProgress) return;
  cachingInProgress = true;
  cachedCount = 0;

  console.log('[SW] Fetching URLs from sitemaps...');
  notifyClients({ type: 'CACHE_STATUS', status: 'Fetching page list from sitemaps...' });

  // Get all URLs from sitemaps
  const allUrls = await getAllUrlsFromSitemaps();

  console.log('[SW] Found', allUrls.length, 'URLs in sitemaps');

  if (allUrls.length === 0) {
    notifyClients({ type: 'CACHE_ERROR', error: 'No URLs found in sitemaps' });
    cachingInProgress = false;
    return;
  }

  const cache = await caches.open(PAGE_CACHE);

  // Check which pages are already cached
  const uncachedPages = [];
  for (const url of allUrls) {
    const cached = await cache.match(url);
    if (!cached) {
      uncachedPages.push(url);
    }
  }

  totalToCache = uncachedPages.length;
  console.log('[SW] Need to cache', totalToCache, 'pages');

  if (totalToCache === 0) {
    notifyClients({ type: 'CACHE_COMPLETE', total: allUrls.length });
    cachingInProgress = false;
    return;
  }

  notifyClients({
    type: 'CACHE_PROGRESS',
    cached: 0,
    total: totalToCache,
    status: `Downloading ${totalToCache.toLocaleString()} pages...`
  });

  // Concurrent pool - keep N requests in flight at all times
  const CONCURRENCY = 80; // Number of concurrent requests
  const PROGRESS_INTERVAL = 200; // Notify every N completions

  let nextIndex = 0;
  let lastNotified = 0;

  async function cacheUrl(url) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        await cache.put(url, response);
        cachedCount++;

        // Notify progress periodically
        if (cachedCount - lastNotified >= PROGRESS_INTERVAL) {
          lastNotified = cachedCount;
          notifyClients({
            type: 'CACHE_PROGRESS',
            cached: cachedCount,
            total: totalToCache
          });
        }
      }
    } catch (err) {
      // Silent fail for individual pages
    }
  }

  async function worker() {
    while (nextIndex < uncachedPages.length) {
      const url = uncachedPages[nextIndex++];
      await cacheUrl(url);
    }
  }

  // Start concurrent workers
  const workers = [];
  for (let i = 0; i < Math.min(CONCURRENCY, uncachedPages.length); i++) {
    workers.push(worker());
  }

  // Wait for all workers to complete
  await Promise.all(workers);

  console.log('[SW] Background caching complete!', cachedCount, 'pages cached');
  cachingInProgress = false;

  notifyClients({ type: 'CACHE_COMPLETE', total: allUrls.length });
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

  // Skip API requests - network first with cache fallback
  if (url.pathname.startsWith('/api/')) {
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
        .catch(() => caches.match(event.request))
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

  // All other requests - network first, cache fallback, offline reader as last resort
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

          // For HTML pages, try to redirect to offline reader with context
          if (event.request.headers.get('Accept')?.includes('text/html')) {
            // Try to extract book/chapter from various URL patterns
            const bookChapterMatch = url.pathname.match(/\/(?:book|interlinear)\/([^\/]+)(?:\/(?:chapter\/)?(\d+))?/);
            if (bookChapterMatch) {
              const book = decodeURIComponent(bookChapterMatch[1]);
              const chapter = bookChapterMatch[2] || '1';
              return Response.redirect('/offline?book=' + encodeURIComponent(book) + '&chapter=' + chapter, 302);
            }

            // Default to offline page
            return caches.match('/offline');
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

  if (event.data && event.data.type === 'START_CACHING') {
    console.log('[SW] Received START_CACHING request');
    startBackgroundCaching();
  }

  // Report current caching status
  if (event.data && event.data.type === 'GET_CACHE_STATUS') {
    if (cachingInProgress) {
      event.source.postMessage({
        type: 'CACHE_PROGRESS',
        cached: cachedCount,
        total: totalToCache,
        inProgress: true
      });
    } else {
      event.source.postMessage({
        type: 'CACHE_IDLE',
        inProgress: false
      });
    }
  }
});
