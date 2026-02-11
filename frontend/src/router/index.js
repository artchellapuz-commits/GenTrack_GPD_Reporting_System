import { createRouter, createWebHistory } from 'vue-router';
import UploadExcel from '../components/UploadExcel.vue';
import ViewReports from '../components/ViewReports.vue';
import GenerateReport from '../components/GenerateReport.vue';

const routes = [
  {
    path: '/',
    redirect: '/upload',
  },
  {
    path: '/upload',
    name: 'Upload',
    component: UploadExcel,
  },
  {
    path: '/reports',
    name: 'Reports',
    component: ViewReports,
  },
  {
    path: '/generate',
    name: 'Generate',
    component: GenerateReport,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
