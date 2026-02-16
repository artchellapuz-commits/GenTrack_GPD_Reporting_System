// Keyboard Shortcuts Manager

class KeyboardShortcuts {
  constructor() {
    this.shortcuts = new Map();
    this.isEnabled = true;
    this.init();
  }

  init() {
    document.addEventListener('keydown', this.handleKeyPress.bind(this));
  }

  handleKeyPress(event) {
    if (!this.isEnabled) return;
    
    // Don't trigger shortcuts when typing in inputs
    const tagName = event.target.tagName.toLowerCase();
    if (tagName === 'input' || tagName === 'textarea' || tagName === 'select') {
      // Allow Ctrl+K even in inputs
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        // Let QuickSearch handle this
        return;
      }
      return;
    }

    const key = this.getKeyCombo(event);
    const handler = this.shortcuts.get(key);
    
    if (handler) {
      event.preventDefault();
      handler(event);
    }
  }

  getKeyCombo(event) {
    const parts = [];
    
    if (event.ctrlKey || event.metaKey) parts.push('ctrl');
    if (event.altKey) parts.push('alt');
    if (event.shiftKey) parts.push('shift');
    
    parts.push(event.key.toLowerCase());
    
    return parts.join('+');
  }

  register(keyCombo, handler, description = '') {
    this.shortcuts.set(keyCombo, handler);
    
    // Store description for help menu
    if (!this.descriptions) {
      this.descriptions = new Map();
    }
    this.descriptions.set(keyCombo, description);
  }

  unregister(keyCombo) {
    this.shortcuts.delete(keyCombo);
    if (this.descriptions) {
      this.descriptions.delete(keyCombo);
    }
  }

  enable() {
    this.isEnabled = true;
  }

  disable() {
    this.isEnabled = false;
  }

  getAll() {
    const shortcuts = [];
    this.shortcuts.forEach((handler, key) => {
      shortcuts.push({
        key,
        description: this.descriptions?.get(key) || ''
      });
    });
    return shortcuts;
  }

  clear() {
    this.shortcuts.clear();
    if (this.descriptions) {
      this.descriptions.clear();
    }
  }
}

// Create singleton instance
const keyboardShortcuts = new KeyboardShortcuts();

// Register default shortcuts
keyboardShortcuts.register('ctrl+d', () => {
  window.location.href = '/#/dashboard';
}, 'Go to Dashboard');

keyboardShortcuts.register('ctrl+u', () => {
  window.location.href = '/#/upload';
}, 'Go to Upload');

keyboardShortcuts.register('ctrl+r', () => {
  window.location.href = '/#/view';
}, 'Go to View Reports');

keyboardShortcuts.register('ctrl+g', () => {
  window.location.href = '/#/generate';
}, 'Go to Generate Report');

keyboardShortcuts.register('ctrl+h', () => {
  window.location.href = '/#/';
}, 'Go to Home');

keyboardShortcuts.register('?', () => {
  // Show keyboard shortcuts help
  const shortcuts = keyboardShortcuts.getAll();
  const helpText = shortcuts.map(s => `${s.key}: ${s.description}`).join('\n');
  alert('Keyboard Shortcuts:\n\n' + helpText);
}, 'Show keyboard shortcuts help');

export default keyboardShortcuts;
