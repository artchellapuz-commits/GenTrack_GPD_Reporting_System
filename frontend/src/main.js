import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { setupAxiosInterceptors } from './utils/auth';
import 'primeicons/primeicons.css';
import './assets/mobile.css';

// Setup axios interceptors for auth
setupAxiosInterceptors();

createApp(App).use(router).mount('#app');
