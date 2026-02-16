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

// Setup axios interceptors for auth
setupAxiosInterceptors();

const app = createApp(App);
app.use(router);
app.use(PrimeVue);

// Make utilities available globally
app.config.globalProperties.$toast = toast;
app.config.globalProperties.$shortcuts = keyboardShortcuts;
app.config.globalProperties.$favorites = favoritesManager;

app.mount('#app');
