// PWA utility functions for offline support and installation

export const pwaUtils = {
  // Check if app is running as PWA
  isPWA() {
    return window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone === true;
  },

  // Check if device is mobile
  isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  },

  // Check if online
  isOnline() {
    return navigator.onLine;
  },

  // Install PWA prompt
  async promptInstall(deferredPrompt) {
    if (!deferredPrompt) return false;
    
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    return outcome === 'accepted';
  },

  // Request notification permission
  async requestNotificationPermission() {
    if (!('Notification' in window)) {
      return false;
    }

    if (Notification.permission === 'granted') {
      return true;
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }

    return false;
  },

  // Show notification
  showNotification(title, options = {}) {
    if (Notification.permission === 'granted') {
      return new Notification(title, {
        icon: '/icons/icon-192x192.png',
        badge: '/icons/icon-72x72.png',
        ...options
      });
    }
  },

  // Cache data for offline use
  async cacheData(key, data) {
    try {
      localStorage.setItem(`offline_${key}`, JSON.stringify({
        data,
        timestamp: Date.now()
      }));
      return true;
    } catch (error) {
      console.error('Cache error:', error);
      return false;
    }
  },

  // Get cached data
  getCachedData(key, maxAge = 3600000) { // 1 hour default
    try {
      const cached = localStorage.getItem(`offline_${key}`);
      if (!cached) return null;

      const { data, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp > maxAge) {
        localStorage.removeItem(`offline_${key}`);
        return null;
      }

      return data;
    } catch (error) {
      console.error('Cache retrieval error:', error);
      return null;
    }
  },

  // Queue action for when online
  queueOfflineAction(action) {
    try {
      const queue = JSON.parse(localStorage.getItem('offline_queue') || '[]');
      queue.push({
        action,
        timestamp: Date.now()
      });
      localStorage.setItem('offline_queue', JSON.stringify(queue));
      return true;
    } catch (error) {
      console.error('Queue error:', error);
      return false;
    }
  },

  // Process offline queue
  async processOfflineQueue(callback) {
    try {
      const queue = JSON.parse(localStorage.getItem('offline_queue') || '[]');
      const results = [];

      for (const item of queue) {
        try {
          const result = await callback(item.action);
          results.push({ success: true, action: item.action, result });
        } catch (error) {
          results.push({ success: false, action: item.action, error });
        }
      }

      localStorage.removeItem('offline_queue');
      return results;
    } catch (error) {
      console.error('Queue processing error:', error);
      return [];
    }
  },

  // Get device info for analytics
  getDeviceInfo() {
    return {
      isPWA: this.isPWA(),
      isMobile: this.isMobile(),
      isOnline: this.isOnline(),
      platform: navigator.platform,
      userAgent: navigator.userAgent,
      screenSize: `${window.screen.width}x${window.screen.height}`,
      viewport: `${window.innerWidth}x${window.innerHeight}`
    };
  }
};

export default pwaUtils;
