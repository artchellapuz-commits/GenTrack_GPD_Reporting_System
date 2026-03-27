// Toast Notification System
class ToastManager {
  constructor() {
    this.toasts = [];
    this.container = null;
    this.init();
  }

  init() {
    // Create toast container if it doesn't exist
    if (!document.getElementById('toast-container')) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById('toast-container');
    }
  }

  show(message, type = 'info', duration = 3000) {
    const toast = {
      id: Date.now() + Math.random(),
      message,
      type,
      duration
    };

    this.toasts.push(toast);
    this.render(toast);

    // Auto remove after duration
    if (duration > 0) {
      setTimeout(() => {
        this.remove(toast.id);
      }, duration);
    }

    return toast.id;
  }

  success(message, duration = 3000) {
    return this.show(message, 'success', duration);
  }

  error(message, duration = 4000) {
    return this.show(message, 'error', duration);
  }

  warning(message, duration = 3500) {
    return this.show(message, 'warning', duration);
  }

  info(message, duration = 3000) {
    return this.show(message, 'info', duration);
  }

  render(toast) {
    const toastEl = document.createElement('div');
    toastEl.className = `toast toast-${toast.type} toast-enter`;
    toastEl.id = `toast-${toast.id}`;
    
    const icon = this.getIcon(toast.type);
    
    toastEl.innerHTML = `
      <div class="toast-icon">
        <i class="pi ${icon}"></i>
      </div>
      <div class="toast-content">
        <p class="toast-message">${toast.message}</p>
      </div>
      <button class="toast-close" onclick="window.toast.remove(${toast.id})">
        <i class="pi pi-times"></i>
      </button>
    `;

    this.container.appendChild(toastEl);

    // Trigger animation
    setTimeout(() => {
      toastEl.classList.remove('toast-enter');
    }, 10);
  }

  remove(id) {
    const toastEl = document.getElementById(`toast-${id}`);
    if (toastEl) {
      toastEl.classList.add('toast-exit');
      setTimeout(() => {
        toastEl.remove();
        this.toasts = this.toasts.filter(t => t.id !== id);
      }, 300);
    }
  }

  getIcon(type) {
    const icons = {
      success: 'pi-check-circle',
      error: 'pi-times-circle',
      warning: 'pi-exclamation-triangle',
      info: 'pi-info-circle'
    };
    return icons[type] || icons.info;
  }

  clear() {
    this.toasts.forEach(toast => this.remove(toast.id));
  }
}

// Create global instance
const toast = new ToastManager();

// Make it available globally
if (typeof window !== 'undefined') {
  window.toast = toast;
}

export default toast;
