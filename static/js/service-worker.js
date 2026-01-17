// Finance Tracker - Service Worker (Production v2.8)
const CACHE_NAME = 'finance-tracker-v2.8-security';
const urlsToCache = [
    '/',
    '/login',
    '/register',
    '/balance_sheet',
    '/portfolio/overview',
    '/static/css/design-system.css',
    '/static/js/offline-db.js',
    '/static/js/sync-manager.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css'
];

// Install event
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event (Network-First Strategy)
self.addEventListener('fetch', (event) => {
    // 1. Skip non-GET requests (POST, PUT, DELETE)
    // This fixes the "Add Item" and "Reset Account" crash
    if (event.request.method !== 'GET') {
        return;
    }

    // 2. Skip API calls (handled by sync-manager or bypassed)
    if (event.request.url.includes('/api/')) return;

    // 3. Navigation Requests (HTML Pages) - Network First, then Cache
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    // Cache the fresh copy
                    const responseToCache = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                    return networkResponse;
                })
                .catch(() => {
                    // Network failed (Offline)
                    // Special Case: If logging out offline, show Login page
                    if (event.request.url.includes('/logout')) {
                        return caches.match('/login');
                    }

                    // Fallback to cached page
                    return caches.match(event.request)
                        .then((cachedResponse) => {
                            if (cachedResponse) return cachedResponse;
                            // Fallback to root/home if specific page not cached
                            return caches.match('/');
                        });
                })
        );
        return;
    }

    // 4. Static Assets (CSS, JS, Images) - Cache First, then Network
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) return response; // Cache Hit

                return fetch(event.request).then(
                    (networkResponse) => {
                        // Check if valid
                        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                            return networkResponse;
                        }

                        // Cache new assets
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });

                        return networkResponse;
                    }
                );
            })
    );
});
