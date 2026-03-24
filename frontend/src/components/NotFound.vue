<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <i class="pi pi-exclamation-triangle"></i>
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist or has been moved.</p>
      <div class="actions">
        <button class="btn-primary" @click="$router.push('/')">
          Go to Home
        </button>
        <button class="btn-secondary" @click="$router.go(-1)">
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.not-found-content i {
  font-size: 4rem;
  color: #f59e0b;
  margin-bottom: 1.5rem;
}

.not-found-content h1 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.not-found-content p {
  color: #64748b;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-secondary {
  background: #e2e8f0;
  color: #475569;
}

.btn-secondary:hover {
  background: #cbd5e1;
}

@media (max-width: 768px) {
  .actions {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
