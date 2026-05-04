import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  
  // Performance optimizations
  build: {
    // Optimize bundle splitting
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor libraries
          vendor: ['vue', 'vue-router'],
          
          // Chart libraries
          charts: ['chart.js', 'vue-chartjs'],
          
          // UI libraries
          ui: ['primevue'],
          
          // Utilities
          utils: ['axios', 'lodash']
        }
      }
    },
    
    // Chunk size warning limit (1MB)
    chunkSizeWarningLimit: 1000,
    
    // Minification options
    minify: 'terser',
    terserOptions: {
      compress: {
        // Remove console logs in production
        drop_console: true,
        drop_debugger: true,
        // Remove unused code
        dead_code: true,
        // Optimize conditionals
        conditionals: true,
        // Optimize comparisons
        comparisons: true,
        // Optimize sequences
        sequences: true,
        // Optimize properties
        properties: true
      },
      mangle: {
        // Mangle variable names for smaller size
        toplevel: true
      }
    },
    
    // Source maps for debugging (disable in production for smaller size)
    sourcemap: process.env.NODE_ENV === 'development',
    
    // Target modern browsers for better optimization
    target: 'es2015',
    
    // CSS code splitting
    cssCodeSplit: true,
    
    // Optimize CSS
    cssMinify: true
  },
  
  // Development server optimization
  server: {
    port: 3000,
    strictPort: true, // Don't try other ports if 3000 is in use
    host: true,
    
    // Proxy API requests to backend
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    },
    
    // Enable HTTP/2 for better performance
    https: false,
    
    // Optimize HMR
    hmr: {
      overlay: true
    }
  },
  
  // Resolve aliases for cleaner imports
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@services': resolve(__dirname, 'src/services'),
      '@assets': resolve(__dirname, 'src/assets')
    }
  },
  
  // Optimize dependencies
  optimizeDeps: {
    // Pre-bundle these dependencies
    include: [
      'vue',
      'vue-router',
      'axios',
      'primevue/config',
      'chart.js',
      'vue-chartjs'
    ],
    
    // Exclude these from pre-bundling
    exclude: []
  },
  
  // CSS preprocessing
  css: {
    // PostCSS configuration
    postcss: {
      plugins: []
    }
  },
  
  // Define global constants
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    
    // Performance flags
    'process.env.ENABLE_PERFORMANCE_MONITORING': JSON.stringify(
      process.env.NODE_ENV === 'development'
    )
  },
  
  // Experimental features
  experimental: {
    // Enable render function optimization
    renderBuiltUrl: (filename, { hostType }) => {
      if (hostType === 'js') {
        return { js: `/${filename}` }
      } else {
        return { css: `/${filename}` }
      }
    }
  },
  
  // Preview server configuration (for production builds)
  preview: {
    port: 4173,
    host: true,
    
    // Proxy for preview mode
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})