/**
 * Service Worker for NPC Reporting System
 * Provides offline caching and performance optimization
 */

const CACHE_NAME = 'npc-reporting-v1.0.0';
const STATIC_CACHE = 'npc-static-v1.0.0';
const API_CACHE = 'npc-api-v1.0.0';

// Files to cache immediately
const STATIC_ASSETS = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/favicon.ico',
  '/manifest.json'
];

// API endpoints to cache
const CACHEABLE_APIS = [
  '/api/plants/',
  '/api/units/',
  '/api/dashboard-summary/',
  '/api/generation-reports/summary/'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('🔧 Service Worker: Installing...');
  
  event.waitUntil(
    Promise.all([
      // Cache static assets
      caches.open(STATIC_CACHE).then(cache => {
        console.log('📦 Service Worker: Caching static assets');
        return cache.addAll(STATIC_ASSETS.filter(url => url !== '/'));
      }),
      
      // Cache API responses
      caches.open(API_CACHE).then(cache => {
        console.log('🌐 Service Worker: Preparing API cache');
        return Promise.resolve();
      })
    ]).then(() => {
      console.log('✅ Service Worker: Installation complete');
      self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('🚀 Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== STATIC_CACHE && cacheName !== API_CACHE) {
            console.log('🗑️ Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Service Worker: Activation complete');
      return self.clients.claim();
    })
  );
});

// Fetch event - handle requests with caching strategy
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }
  
  // Handle static assets
  if (isStaticAsset(url.pathname)) {
    event.respondWith(handleStaticRequest(request));
    return;
  }
  
  // Handle navigation requests (SPA routing)
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }
  
  // Default: network first
  event.respondWith(fetch(request));
});

// Handle API requests with cache-first strategy for cacheable endpoints
async function handleApiRequest(request) {
  const url = new URL(request.url);
  const isCacheable = CACHEABLE_APIS.some(api => url.pathname.includes(api));
  
  if (isCacheable) {
    try {
      // Try cache first
      const cache = await caches.open(API_CACHE);
      const cachedResponse = await cache.match(request);
      
      if (cachedResponse) {
        console.log('📋 Service Worker: Serving API from cache:', url.pathname);
        
        // Update cache in background
        fetch(request).then(response => {
          if (response.ok) {
            cache.put(request, response.clone());
          }
        }).catch(() => {
          // Ignore background update errors
        });
        
        return cachedResponse;
      }
      
      // Fetch from network and cache
      const response = await fetch(request);
      if (response.ok) {
        cache.put(request, response.clone());
        console.log('🌐 Service Worker: Cached API response:', url.pathname);
      }
      return response;
      
    } catch (error) {
      console.error('❌ Service Worker: API request failed:', error);
      return new Response(
        JSON.stringify({ error: 'Network error, please try again' }),
        { 
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  }
  
  // Non-cacheable API requests - network only
  return fetch(request);
}

// Handle static assets with cache-first strategy
async function handleStaticRequest(request) {
  try {
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      console.log('📦 Service Worker: Serving static from cache:', request.url);
      return cachedResponse;
    }
    
    // Fetch from network and cache
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
    
  } catch (error) {
    console.error('❌ Service Worker: Static request failed:', error);
    return fetch(request);
  }
}

// Handle navigation requests (SPA routing)
async function handleNavigationRequest(request) {
  try {
    // Try network first for navigation
    const response = await fetch(request);
    return response;
  } catch (error) {
    // Fallback to cached index.html for offline SPA routing
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match('/');
    
    if (cachedResponse) {
      console.log('📱 Service Worker: Serving offline SPA fallback');
      return cachedResponse;
    }
    
    return new Response(
      '<h1>Offline</h1><p>Please check your internet connection.</p>',
      { 
        headers: { 'Content-Type': 'text/html' }
      }
    );
  }
}

// Helper function to identify static assets
function isStaticAsset(pathname) {
  return (
    pathname.startsWith('/static/') ||
    pathname.startsWith('/assets/') ||
    pathname.includes('.css') ||
    pathname.includes('.js') ||
    pathname.includes('.png') ||
    pathname.includes('.jpg') ||
    pathname.includes('.svg') ||
    pathname.includes('.ico') ||
    pathname.includes('.woff') ||
    pathname.includes('.ttf')
  );
}

// Background sync for offline actions (future enhancement)
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    console.log('🔄 Service Worker: Background sync triggered');
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  // Implement background sync logic here
  // For example, sync offline form submissions
  console.log('🔄 Service Worker: Performing background sync...');
}

// Push notifications (future enhancement)
self.addEventListener('push', event => {
  if (event.data) {
    const data = event.data.json();
    console.log('📬 Service Worker: Push notification received:', data);
    
    event.waitUntil(
      self.registration.showNotification(data.title, {
        body: data.body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        tag: 'npc-notification'
      })
    );
  }
});

// Notification click handler
self.addEventListener('notificationclick', event => {
  console.log('🔔 Service Worker: Notification clicked');
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('/')
  );
});

// Message handler for communication with main thread
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('⏭️ Service Worker: Skip waiting requested');
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_STATS') {
    getCacheStats().then(stats => {
      event.ports[0].postMessage(stats);
    });
  }
});

// Get cache statistics
async function getCacheStats() {
  const cacheNames = await caches.keys();
  const stats = {};
  
  for (const cacheName of cacheNames) {
    const cache = await caches.open(cacheName);
    const keys = await cache.keys();
    stats[cacheName] = keys.length;
  }
  
  return stats;
}

console.log('🎯 Service Worker: Loaded and ready');