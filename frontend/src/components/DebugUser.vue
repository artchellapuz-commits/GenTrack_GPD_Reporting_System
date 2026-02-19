<template>
  <div style="padding: 20px; background: white; margin: 20px;">
    <h2>Debug User Data</h2>
    
    <div style="margin: 20px 0;">
      <h3>LocalStorage User Data:</h3>
      <pre style="background: #f5f5f5; padding: 15px; border-radius: 8px; overflow: auto;">{{ userData }}</pre>
    </div>
    
    <div style="margin: 20px 0;">
      <h3>Auth Checks:</h3>
      <ul>
        <li>isAdmin(): {{ isAdminCheck }}</li>
        <li>getUserRole(): {{ userRoleCheck }}</li>
        <li>isAuthenticated(): {{ isAuthCheck }}</li>
        <li>canManageUsers(): {{ canManageCheck }}</li>
      </ul>
    </div>
    
    <div style="margin: 20px 0;">
      <button @click="refreshData" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">
        Refresh Data
      </button>
      
      <button @click="fixAdminStatus" style="padding: 10px 20px; background: #f56565; color: white; border: none; border-radius: 8px; cursor: pointer; margin-left: 10px;">
        Force Admin Status
      </button>
    </div>
  </div>
</template>

<script>
import { isAdmin, getUserRole, isAuthenticated, canManageUsers } from '../utils/auth';

export default {
  name: 'DebugUser',
  data() {
    return {
      userData: null,
      isAdminCheck: false,
      userRoleCheck: '',
      isAuthCheck: false,
      canManageCheck: false
    };
  },
  mounted() {
    this.refreshData();
  },
  methods: {
    refreshData() {
      const userStr = localStorage.getItem('user');
      this.userData = userStr ? JSON.parse(userStr) : null;
      this.isAdminCheck = isAdmin();
      this.userRoleCheck = getUserRole();
      this.isAuthCheck = isAuthenticated();
      this.canManageCheck = canManageUsers();
    },
    fixAdminStatus() {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      user.is_staff = true;
      if (!user.profile) user.profile = {};
      user.profile.role = 'ADMIN';
      localStorage.setItem('user', JSON.stringify(user));
      alert('Admin status set! Reloading page...');
      setTimeout(() => location.reload(), 1000);
    }
  }
};
</script>
