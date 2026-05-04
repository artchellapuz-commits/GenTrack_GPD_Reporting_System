<template>
  <div v-if="showPrompt" class="pwa-install-prompt">
    <div class="prompt-content">
      <i class="pi pi-mobile" style="font-size: 2rem; color: #3b82f6;"></i>
      <div class="prompt-text">
        <h3>Install NPC Reports</h3>
        <p>Install our app for quick access and offline support</p>
      </div>
      <div class="prompt-actions">
        <button @click="install" class="btn-install">Install</button>
        <button @click="dismiss" class="btn-dismiss">Not Now</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import pwaUtils from '../utils/pwaUtils';

export default {
  name: 'PWAInstallPrompt',
  setup() {
    const showPrompt = ref(false);
    let deferredPrompt = null;

    onMounted(() => {
      // Listen for beforeinstallprompt event
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        // Show prompt if not already installed and user hasn't dismissed
        if (!pwaUtils.isPWA() && !localStorage.getItem('pwa_prompt_dismissed')) {
          showPrompt.value = true;
        }
      });

      // Check if already installed
      window.addEventListener('appinstalled', () => {
        showPrompt.value = false;
        deferredPrompt = null;
      });
    });

    const install = async () => {
      if (deferredPrompt) {
        const accepted = await pwaUtils.promptInstall(deferredPrompt);
        if (accepted) {
          showPrompt.value = false;
          deferredPrompt = null;
        }
      }
    };

    const dismiss = () => {
      showPrompt.value = false;
      localStorage.setItem('pwa_prompt_dismissed', 'true');
    };

    return {
      showPrompt,
      install,
      dismiss
    };
  }
};
</script>

<style scoped>
.pwa-install-prompt {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  animation: slideUp 0.3s ease-out;
}

.prompt-content {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 15px;
  max-width: 500px;
}

.prompt-text h3 {
  margin: 0 0 5px 0;
  font-size: 1.1rem;
  color: #1e293b;
}

.prompt-text p {
  margin: 0;
  font-size: 0.9rem;
  color: #64748b;
}

.prompt-actions {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.btn-install, .btn-dismiss {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-install {
  background: #3b82f6;
  color: white;
}

.btn-install:hover {
  background: #2563eb;
}

.btn-dismiss {
  background: #f1f5f9;
  color: #64748b;
}

.btn-dismiss:hover {
  background: #e2e8f0;
}

@keyframes slideUp {
  from {
    transform: translateX(-50%) translateY(100px);
    opacity: 0;
  }
  to {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .pwa-install-prompt {
    left: 10px;
    right: 10px;
    transform: none;
  }
  
  .prompt-content {
    flex-direction: column;
    text-align: center;
  }
  
  .prompt-actions {
    margin-left: 0;
    width: 100%;
  }
  
  .btn-install, .btn-dismiss {
    flex: 1;
  }
}
</style>
