/**
 * Performance optimization utilities for NPC Reporting System
 */

// Performance monitoring
export class PerformanceMonitor {
  static measurements = new Map();
  
  static startMeasurement(name) {
    this.measurements.set(name, performance.now());
  }
  
  static endMeasurement(name) {
    const start = this.measurements.get(name);
    if (start) {
      const duration = performance.now() - start;
      console.log(`⚡ Performance: ${name} took ${duration.toFixed(2)}ms`);
      this.measurements.delete(name);
      return duration;
    }
    return 0;
  }
  
  static measureAsync(name, asyncFn) {
    return async (...args) => {
      this.startMeasurement(name);
      try {
        const result = await asyncFn(...args);
        this.endMeasurement(name);
        return result;
      } catch (error) {
        this.endMeasurement(name);
        throw error;
      }
    };
  }
}

// Debounce utility for search and input optimization
export function debounce(func, wait, immediate = false) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      timeout = null;
      if (!immediate) func(...args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func(...args);
  };
}

// Throttle utility for scroll and resize events
export function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Image lazy loading utility
export class LazyImageLoader {
  static observer = null;
  
  static init() {
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            this.observer.unobserve(img);
          }
        });
      });
    }
  }
  
  static observe(img) {
    if (this.observer) {
      this.observer.observe(img);
    } else {
      // Fallback for browsers without IntersectionObserver
      img.src = img.dataset.src;
    }
  }
}

// Virtual scrolling helper for large lists
export class VirtualScrollHelper {
  constructor(itemHeight, containerHeight, buffer = 5) {
    this.itemHeight = itemHeight;
    this.containerHeight = containerHeight;
    this.buffer = buffer;
  }
  
  getVisibleRange(scrollTop, totalItems) {
    const visibleCount = Math.ceil(this.containerHeight / this.itemHeight);
    const startIndex = Math.max(0, Math.floor(scrollTop / this.itemHeight) - this.buffer);
    const endIndex = Math.min(totalItems - 1, startIndex + visibleCount + this.buffer * 2);
    
    return { startIndex, endIndex, visibleCount };
  }
  
  getTransformOffset(startIndex) {
    return startIndex * this.itemHeight;
  }
}

// Memory management utilities
export class MemoryManager {
  static cleanup() {
    // Clear any global caches
    if (window.apiCache) {
      window.apiCache.clear();
    }
    
    // Force garbage collection if available (dev tools)
    if (window.gc) {
      window.gc();
    }
  }
  
  static getMemoryUsage() {
    if (performance.memory) {
      return {
        used: Math.round(performance.memory.usedJSHeapSize / 1048576),
        total: Math.round(performance.memory.totalJSHeapSize / 1048576),
        limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
      };
    }
    return null;
  }
}

// Bundle size analyzer (development only)
export class BundleAnalyzer {
  static logBundleInfo() {
    if (process.env.NODE_ENV === 'development') {
      console.group('📦 Bundle Information');
      console.log('Vue version:', '3.x');
      console.log('Router mode:', 'History');
      console.log('Build mode:', process.env.NODE_ENV);
      console.groupEnd();
    }
  }
}

// Performance metrics collection
export class MetricsCollector {
  static collectPageLoadMetrics() {
    if ('performance' in window) {
      const navigation = performance.getEntriesByType('navigation')[0];
      if (navigation) {
        const metrics = {
          dns: navigation.domainLookupEnd - navigation.domainLookupStart,
          tcp: navigation.connectEnd - navigation.connectStart,
          request: navigation.responseStart - navigation.requestStart,
          response: navigation.responseEnd - navigation.responseStart,
          dom: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
          load: navigation.loadEventEnd - navigation.loadEventStart,
          total: navigation.loadEventEnd - navigation.navigationStart
        };
        
        console.group('📊 Page Load Metrics');
        Object.entries(metrics).forEach(([key, value]) => {
          console.log(`${key}: ${Math.round(value)}ms`);
        });
        console.groupEnd();
        
        return metrics;
      }
    }
    return null;
  }
  
  static collectResourceMetrics() {
    if ('performance' in window) {
      const resources = performance.getEntriesByType('resource');
      const resourceTypes = {};
      
      resources.forEach(resource => {
        const type = this.getResourceType(resource.name);
        if (!resourceTypes[type]) {
          resourceTypes[type] = { count: 0, totalSize: 0, totalTime: 0 };
        }
        
        resourceTypes[type].count++;
        resourceTypes[type].totalSize += resource.transferSize || 0;
        resourceTypes[type].totalTime += resource.duration || 0;
      });
      
      console.group('📈 Resource Metrics');
      Object.entries(resourceTypes).forEach(([type, stats]) => {
        console.log(`${type}: ${stats.count} files, ${Math.round(stats.totalSize / 1024)}KB, ${Math.round(stats.totalTime)}ms`);
      });
      console.groupEnd();
      
      return resourceTypes;
    }
    return null;
  }
  
  static getResourceType(url) {
    if (url.includes('.js')) return 'JavaScript';
    if (url.includes('.css')) return 'CSS';
    if (url.includes('.png') || url.includes('.jpg') || url.includes('.svg')) return 'Images';
    if (url.includes('.woff') || url.includes('.ttf')) return 'Fonts';
    if (url.includes('/api/')) return 'API';
    return 'Other';
  }
}

// Initialize performance monitoring
if (typeof window !== 'undefined') {
  // Initialize lazy image loader
  LazyImageLoader.init();
  
  // Collect metrics on page load
  window.addEventListener('load', () => {
    setTimeout(() => {
      MetricsCollector.collectPageLoadMetrics();
      MetricsCollector.collectResourceMetrics();
    }, 1000);
  });
  
  // Log bundle info in development (only when explicitly called)
  // BundleAnalyzer.logBundleInfo(); // Removed automatic call
}

export default {
  PerformanceMonitor,
  debounce,
  throttle,
  LazyImageLoader,
  VirtualScrollHelper,
  MemoryManager,
  BundleAnalyzer,
  MetricsCollector
};