import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../components/LandingPage.vue';
import Dashboard from '../components/Dashboard.vue';
import UploadExcel from '../components/UploadExcel.vue';
import ViewReports from '../components/ViewReports.vue';
import GenerateReport from '../components/GenerateReport.vue';
import WaterNomination from '../components/WaterNomination.vue';
import ApprovalQueue from '../components/ApprovalQueue.vue';
import AuditLogs from '../components/AuditLogs.vue';
import UserManagement from '../components/UserManagement.vue';
import PasswordResetRequests from '../components/PasswordResetRequests.vue';
import DebugUser from '../components/DebugUser.vue';
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
    path: '/about',
    name: 'AboutGPD',
    component: () => import('../components/AboutGPD.vue')
  },
  {
    path: '/features',
    name: 'Features',
    component: () => import('../components/Features.vue')
  },
  {
    path: '/documentation',
    name: 'Documentation',
    component: () => import('../components/Documentation.vue')
  },
  {
    path: '/support',
    name: 'Support',
    component: () => import('../components/Support.vue')
  },
  {
    path: '/contact',
    name: 'ContactUs',
    component: () => import('../components/ContactUs.vue')
  },
  {
    path: '/careers',
    name: 'Careers',
    component: () => import('../components/Careers.vue')
  },
  {
    path: '/privacy',
    name: 'PrivacyPolicy',
    component: () => import('../components/PrivacyPolicy.vue')
  },
  {
    path: '/terms',
    name: 'TermsOfService',
    component: () => import('../components/TermsOfService.vue')
  },
  {
    path: '/security',
    name: 'Security',
    component: () => import('../components/Security.vue')
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
    path: '/archive',
    name: 'Archive',
    component: () => import('../components/ArchivePage.vue'),
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
  {
    path: '/approval-queue',
    name: 'ApprovalQueue',
    component: ApprovalQueue,
    meta: { requiresAuth: true }
  },
  {
    path: '/audit-logs',
    name: 'AuditLogs',
    component: AuditLogs,
    meta: { requiresAuth: true }
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/password-reset-requests',
    name: 'PasswordResetRequests',
    component: PasswordResetRequests,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/debug-user',
    name: 'DebugUser',
    component: DebugUser,
    meta: { requiresAuth: true }
  },
  {
    path: '/signatory-authorization',
    name: 'SignatoryAuthorization',
    component: () => import('../components/SignatoryAuthorizationRequest.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/scheduled-reports',
    name: 'ScheduledReports',
    component: () => import('../components/ScheduledReports.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analytics',
    name: 'AdvancedAnalytics',
    component: () => import('../components/AdvancedAnalytics.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sign/:token',
    name: 'SigningPage',
    component: () => import('../components/SigningPage.vue'),
    props: true
  },
  {
    path: '/signature-setup/:token',
    name: 'SignatureSetup',
    component: () => import('../components/SignatureSetup.vue'),
    props: true
  },
  {
    path: '/report-storage',
    name: 'ReportStorage',
    component: () => import('../components/ReportStorage.vue'),
    meta: { requiresAuth: true }
  },
  // Catch-all route for 404s - must be last
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../components/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Always scroll to top when navigating to a new page
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  }
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
      // Check if route requires admin
      if (to.matched.some(record => record.meta.requiresAdmin)) {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const isAdmin = user.is_staff || (user.profile && user.profile.role === 'ADMIN');
        
        if (!isAdmin) {
          // Not admin, redirect to dashboard
          next('/dashboard');
        } else {
          next();
        }
      } else {
        next();
      }
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
