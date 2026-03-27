<template>
  <div id="app">
    <!-- Main Content -->
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import './assets/styles.css';
@import './assets/sakai-theme.css';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Main Content */
.app-main {
  flex: 1;
  background: #f8fafc;
}
</style>
