import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { setupAxiosInterceptors } from './utils/auth';
import PrimeVue from 'primevue/config';
import 'primeicons/primeicons.css';
import './assets/mobile.css';

// Setup axios interceptors for auth
setupAxiosInterceptors();

const app = createApp(App);
app.use(router);
app.use(PrimeVue);
app.mount('#app');
