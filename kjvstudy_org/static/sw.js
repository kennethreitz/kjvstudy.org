// KJV Study Service Worker - Offline Bible Access
const CACHE_VERSION = 'v1';
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

// Activate event - clean up old caches
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
  );
});

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
