import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../components/LandingPage.vue';
import Dashboard from '../components/Dashboard.vue';
import UploadExcel from '../components/UploadExcel.vue';
import ViewReports from '../components/ViewReports.vue';
import GenerateReport from '../components/GenerateReport.vue';
import WaterNomination from '../components/WaterNomination.vue';
import LoginPage from '../components/Login.vue';
import RegisterPage from '../components/Register.vue';
import { isAuthenticated } from '../utils/auth';

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/upload',
    name: 'Upload',
    component: UploadExcel,
    meta: { requiresAuth: true }
  },
  {
    path: '/view',
    name: 'View',
    component: ViewReports,
    meta: { requiresAuth: true }
  },
  {
    path: '/generate',
    name: 'Generate',
    component: GenerateReport,
    meta: { requiresAuth: true }
  },
  {
    path: '/water-nomination',
    name: 'WaterNomination',
    component: WaterNomination,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Navigation guards
router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated();
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  }
  // Check if route requires guest (login/register)
  else if (to.matched.some(record => record.meta.requiresGuest)) {
    if (authenticated) {
      // If already logged in, redirect to dashboard
      next('/dashboard');
    } else {
      next();
    }
  }
  else {
    next();
  }
});

export default router;
