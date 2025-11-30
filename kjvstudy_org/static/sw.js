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

// All pages to pre-cache in background (388 pages)
const PAGES_TO_CACHE = [
  "/anthropology",
  "/armor-of-god",
  "/beatitudes",
  "/biblical-angels",
  "/biblical-covenants",
  "/biblical-festivals",
  "/biblical-maps",
  "/biblical-prophets",
  "/biblical-timeline",
  "/bibliology",
  "/blood-in-scripture",
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
  "/book/Solomon's Song",
  "/book/Titus",
  "/book/Zechariah",
  "/book/Zephaniah",
  "/christology",
  "/ecclesiology",
  "/eschatology",
  "/family-tree",
  "/fruits-of-the-spirit",
  "/grace",
  "/hamartiology",
  "/i-am-statements",
  "/interlinear",
  "/justification",
  "/kingdom-of-god",
  "/law-and-gospel",
  "/messianic-prophecies",
  "/miracles-of-jesus",
  "/names-of-christ",
  "/names-of-god",
  "/parables",
  "/parables/the-good-samaritan",
  "/parables/the-importunate-widow",
  "/parables/the-mustard-seed",
  "/parables/the-pearl-of-great-price",
  "/parables/the-pharisee-and-publican",
  "/parables/the-prodigal-son",
  "/parables/the-sower",
  "/parables/the-talents",
  "/parables/the-unjust-steward",
  "/parables/the-unmerciful-servant",
  "/parables/the-wheat-and-tares",
  "/personifications",
  "/pneumatology",
  "/prayers-of-the-bible",
  "/providence",
  "/reading-plans",
  "/reading-plans/chronological",
  "/reading-plans/gospels-acts",
  "/reading-plans/new-testament",
  "/reading-plans/one-year",
  "/reading-plans/paul-epistles",
  "/reading-plans/pentateuch",
  "/reading-plans/prophets",
  "/reading-plans/psalms-proverbs",
  "/resources",
  "/sanctification",
  "/search",
  "/soteriology",
  "/spirits-and-demons",
  "/stories",
  "/stories/abraham-and-lot-separate",
  "/stories/abraham-offers-isaac",
  "/stories/adam-and-eve-in-the-garden",
  "/stories/angel-visits-mary",
  "/stories/baby-moses-in-the-basket",
  "/stories/beast-and-mark",
  "/stories/boaz-redeems-ruth",
  "/stories/cain-and-abel",
  "/stories/calms-the-storm",
  "/stories/centurions-servant",
  "/stories/conversion-of-saul",
  "/stories/crossing-the-red-sea",
  "/stories/daniel-in-lions-den",
  "/stories/daniel-in-the-lions-den",
  "/stories/daniel-refuses-kings-food",
  "/stories/daniels-visions",
  "/stories/david-and-goliath",
  "/stories/david-and-jonathan",
  "/stories/day-of-pentecost",
  "/stories/elihu-speaks-words-of-wisdom",
  "/stories/elijah-and-the-prophets-of-baal",
  "/stories/elijah-and-the-ravens",
  "/stories/elijah-and-the-still-small-voice",
  "/stories/elijah-and-the-widows-oil",
  "/stories/elijah-taken-to-heaven",
  "/stories/elisha-and-the-widows-oil",
  "/stories/escape-to-egypt",
  "/stories/esther-becomes-queen",
  "/stories/esther-saves-her-people",
  "/stories/esthers-brave-plan",
  "/stories/ezekiel-valley-of-dry-bones",
  "/stories/ezra-reads-the-law",
  "/stories/fall-of-babylon",
  "/stories/feeds-five-thousand",
  "/stories/fiery-furnace",
  "/stories/fire-from-heaven",
  "/stories/first-missionary-journey",
  "/stories/for-such-a-time-as-this",
  "/stories/forgives-sinful-woman",
  "/stories/from-persecutor-to-preacher",
  "/stories/garden-of-gethsemane",
  "/stories/gideon-and-the-fleece",
  "/stories/gideons-three-hundred",
  "/stories/god-calls-samuel",
  "/stories/god-creates-the-world",
  "/stories/god-speaks-from-the-whirlwind",
  "/stories/great-commission",
  "/stories/hamans-plot",
  "/stories/hannahs-prayer",
  "/stories/hannahs-prayer-for-a-son",
  "/stories/heals-blind-man",
  "/stories/heals-jairus-daughter",
  "/stories/heals-on-sabbath",
  "/stories/heals-paralyzed-man",
  "/stories/heals-ten-lepers",
  "/stories/hidden-treasure-and-pearl",
  "/stories/isaiahs-vision",
  "/stories/israel-demands-a-king",
  "/stories/jacob-and-esau",
  "/stories/jacob-wrestles-with-god",
  "/stories/jacobs-ladder",
  "/stories/jesus-and-children",
  "/stories/jesus-and-zacchaeus",
  "/stories/jesus-appears-to-thomas",
  "/stories/jesus-baptized",
  "/stories/jesus-calms-the-storm",
  "/stories/jesus-feeds-five-thousand",
  "/stories/jesus-heals-ten-lepers",
  "/stories/jesus-heals-the-blind-man",
  "/stories/jesus-heals-the-paralyzed-man",
  "/stories/jesus-raises-lazarus",
  "/stories/jesus-restores-peter",
  "/stories/jesus-tempted",
  "/stories/jesus-walks-on-water",
  "/stories/job-cries-out-and-friends-accuse",
  "/stories/jobs-faith-through-suffering",
  "/stories/jobs-physical-affliction",
  "/stories/jobs-restoration-and-blessing",
  "/stories/jobs-righteousness-and-prosperity",
  "/stories/johns-vision-of-christ",
  "/stories/jonah-and-nineveh",
  "/stories/jonah-and-the-great-fish",
  "/stories/jonah-prays-from-the-fish",
  "/stories/jonah-runs-from-god",
  "/stories/jonahs-anger-and-gods-compassion",
  "/stories/joseph-reveals-himself",
  "/stories/joseph-sold-into-slavery",
  "/stories/josephs-coat-and-dreams",
  "/stories/justice-and-generosity",
  "/stories/kids",
  "/stories/letters-to-seven-churches",
  "/stories/man-with-many-spirits",
  "/stories/mary-and-martha",
  "/stories/naaman-is-healed",
  "/stories/naomis-loss-and-return",
  "/stories/nebuchadnezzars-dream",
  "/stories/nehemiahs-burden",
  "/stories/new-heaven-new-earth",
  "/stories/nineveh-repents",
  "/stories/no-room-at-the-inn",
  "/stories/noah-and-the-ark",
  "/stories/paul-silas-in-prison",
  "/stories/pauls-shipwreck",
  "/stories/permission-to-rebuild",
  "/stories/peter-denies-jesus",
  "/stories/peter-john-heal-lame-man",
  "/stories/peters-vision",
  "/stories/prison-songs-at-midnight",
  "/stories/rahab-and-the-spies",
  "/stories/raises-lazarus",
  "/stories/raises-widows-son",
  "/stories/rebuilding-despite-opposition",
  "/stories/renewal-and-covenant",
  "/stories/return-of-christ",
  "/stories/rich-man-and-lazarus",
  "/stories/road-to-emmaus",
  "/stories/ruth-and-boaz",
  "/stories/ruth-and-naomi",
  "/stories/ruth-at-the-threshing-floor",
  "/stories/ruth-meets-boaz",
  "/stories/ruths-loyalty-and-love",
  "/stories/samson-and-delilah",
  "/stories/samson-the-strong-man",
  "/stories/samsons-birth-announced",
  "/stories/samsons-exploits",
  "/stories/samsons-final-victory",
  "/stories/samsons-riddle-and-wedding",
  "/stories/samuel-anoints-david",
  "/stories/samuel-anoints-saul",
  "/stories/samuels-death",
  "/stories/satans-challenge-and-jobs-first-test",
  "/stories/sauls-disobedience",
  "/stories/seven-seals",
  "/stories/shadrach-meshach-and-abednego",
  "/stories/shepherds-and-angels",
  "/stories/shipwreck-and-malta",
  "/stories/solomons-wisdom",
  "/stories/teaching-in-athens",
  "/stories/the-ark-is-captured",
  "/stories/the-ascension",
  "/stories/the-birth-of-isaac",
  "/stories/the-boy-samuel-hears-god",
  "/stories/the-burning-bush",
  "/stories/the-call-of-abraham",
  "/stories/the-crucifixion",
  "/stories/the-fall-of-man",
  "/stories/the-fiery-furnace",
  "/stories/the-golden-calf",
  "/stories/the-good-samaritan",
  "/stories/the-great-banquet",
  "/stories/the-jews-are-delivered",
  "/stories/the-last-supper",
  "/stories/the-lost-coin",
  "/stories/the-lost-sheep",
  "/stories/the-mustard-seed",
  "/stories/the-passover",
  "/stories/the-persistent-widow",
  "/stories/the-pharisee-and-tax-collector",
  "/stories/the-prodigal-son",
  "/stories/the-resurrection",
  "/stories/the-rich-fool",
  "/stories/the-sheep-and-goats",
  "/stories/the-sower",
  "/stories/the-talents",
  "/stories/the-ten-commandments",
  "/stories/the-ten-plagues",
  "/stories/the-ten-virgins",
  "/stories/the-tower-of-babel",
  "/stories/the-unmerciful-servant",
  "/stories/the-walls-of-jericho",
  "/stories/the-wheat-and-weeds",
  "/stories/the-wise-men",
  "/stories/throne-room-of-heaven",
  "/stories/transfiguration",
  "/stories/triumphal-entry",
  "/stories/two-witnesses",
  "/stories/walks-on-water",
  "/stories/wall-completed",
  "/stories/water-into-wine",
  "/stories/wise-and-foolish-builders",
  "/stories/woman-and-dragon",
  "/stories/woman-at-the-well",
  "/stories/woman-touched-his-cloak",
  "/stories/workers-in-the-vineyard",
  "/stories/writing-on-the-wall",
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
  "/ten-commandments",
  "/tetragrammaton",
  "/the-twelve-apostles",
  "/theology-proper",
  "/topics",
  "/topics/Anxiety",
  "/topics/Baptism",
  "/topics/Communion",
  "/topics/Contentment",
  "/topics/Faith",
  "/topics/Fasting",
  "/topics/Forgiveness",
  "/topics/Generosity",
  "/topics/Grace",
  "/topics/Heaven",
  "/topics/Holiness",
  "/topics/Holy Spirit",
  "/topics/Hope",
  "/topics/Humility",
  "/topics/Joy",
  "/topics/Judgment",
  "/topics/Love",
  "/topics/Marriage",
  "/topics/Mental Health",
  "/topics/Obedience",
  "/topics/Parenting",
  "/topics/Patience",
  "/topics/Peace",
  "/topics/Prayer",
  "/topics/Repentance",
  "/topics/Rest",
  "/topics/Salvation",
  "/topics/Service",
  "/topics/Spiritual Warfare",
  "/topics/Stewardship",
  "/topics/Suffering",
  "/topics/Temptation",
  "/topics/The Church",
  "/topics/Wisdom",
  "/topics/Work",
  "/topics/Worship",
  "/trinity",
  "/types-and-shadows",
  "/verse-of-the-day",
  "/women-of-the-bible",
  "/worship"
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
