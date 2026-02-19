const CACHE_NAME = 'npc-reporting-v1';

// Install event - just skip waiting, don't cache anything yet
self.addEventListener('install', event => {
  console.log('Service Worker installing...');
  event.waitUntil(self.skipWaiting());
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - network first, then cache
self.addEventListener('fetch', event => {
  // Skip caching for API requests and external resources
  if (event.request.url.includes('/api/') || 
      !event.request.url.startsWith(self.location.origin)) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Network first strategy
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Check if valid response
        if (response && response.status === 200) {
          // Clone and cache the response
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache).catch(err => {
                // Silently fail cache writes
                console.log('Cache write failed:', err.message);
              });
            })
            .catch(err => {
              console.log('Cache open failed:', err.message);
            });
        }
        
        return response;
      })
      .catch(err => {
        // Network failed, try cache
        console.log('Network failed, trying cache:', err.message);
        return caches.match(event.request)
          .then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            
            // Return offline page
            return new Response('Offline - content not available', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
      })
  );
});

// Background sync for offline data submission
self.addEventListener('sync', event => {
  console.log('Background sync:', event.tag);
  if (event.tag === 'sync-reports') {
    event.waitUntil(syncReports());
  }
});

async function syncReports() {
  try {
    const cache = await caches.open('pending-reports');
    const requests = await cache.keys();
    
    const results = await Promise.allSettled(
      requests.map(async request => {
        try {
          const response = await fetch(request);
          if (response.ok) {
            await cache.delete(request);
          }
          return response;
        } catch (error) {
          console.error('Sync failed for request:', error);
          return null;
        }
      })
    );
    
    console.log('Sync completed:', results.length, 'requests processed');
  } catch (error) {
    console.error('Sync reports failed:', error);
  }
}

// Push notifications
self.addEventListener('push', event => {
  console.log('Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New update available',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  };

  event.waitUntil(
    self.registration.showNotification('NPC Reporting System', options)
      .catch(err => {
        console.log('Notification failed:', err.message);
      })
  );
});

// Notification click
self.addEventListener('notificationclick', event => {
  console.log('Notification clicked');
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/').catch(err => {
      console.log('Failed to open window:', err.message);
    })
  );
});

console.log('Service Worker loaded');
