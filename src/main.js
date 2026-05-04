import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { setupAxiosInterceptors } from './utils/auth';
import PrimeVue from 'primevue/config';
import 'primeicons/primeicons.css';
import './assets/mobile.css';
import './assets/responsive.css';
import './assets/glassmorphism.css';
import './assets/toast.css';
import toast from './utils/toast';
import keyboardShortcuts from './utils/keyboardShortcuts';
import favoritesManager from './utils/favorites';
import { PerformanceMonitor } from './utils/performance';

// Performance: Start app initialization measurement
PerformanceMonitor.startMeasurement('app-initialization');

// Setup axios interceptors for auth
setupAxiosInterceptors();

const app = createApp(App);
app.use(router);
app.use(PrimeVue);

// Make utilities available globally
app.config.globalProperties.$toast = toast;
app.config.globalProperties.$shortcuts = keyboardShortcuts;
app.config.globalProperties.$favorites = favoritesManager;
app.config.globalProperties.$performance = PerformanceMonitor;

// Performance: Register service worker for caching
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('✅ Service Worker registered successfully:', registration.scope);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New version available
              toast.info('New version available! Refresh to update.', {
                duration: 10000,
                action: {
                  text: 'Refresh',
                  handler: () => window.location.reload()
                }
              });
            }
          });
        });
      })
      .catch(error => {
        console.warn('⚠️ Service Worker registration failed:', error);
      });
  });
}

// Performance: Preload critical routes
router.beforeEach((to, from, next) => {
  // Preload dashboard component if going to login (likely next destination)
  if (to.name === 'LoginPage') {
    import('./components/Dashboard.vue').catch(() => {
      // Ignore preload errors
    });
  }
  next();
});

app.mount('#app');

// Performance: End app initialization measurement
PerformanceMonitor.endMeasurement('app-initialization');
