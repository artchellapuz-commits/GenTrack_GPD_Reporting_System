const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, // Disable ESLint during development
  devServer: {
    historyApiFallback: {
      // Handle all routes that don't match static files
      rewrites: [
        { from: /^\/api\/.*$/, to: function(context) {
          return context.parsedUrl.pathname;
        }},
        { from: /./, to: '/index.html' }
      ]
    },
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
  configureWebpack: config => {
    if (process.env.NODE_ENV === 'production') {
      // Performance optimizations for production
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendors',
              chunks: 'all',
            },
            common: {
              name: 'common',
              minChunks: 2,
              chunks: 'all',
              enforce: true
            }
          }
        }
      }
      
      // Only configure terser if it exists
      if (config.optimization.minimizer && config.optimization.minimizer[0]) {
        const terserPlugin = config.optimization.minimizer[0];
        if (terserPlugin.options && terserPlugin.options.terserOptions) {
          terserPlugin.options.terserOptions.compress = {
            ...terserPlugin.options.terserOptions.compress,
            drop_console: true,
            drop_debugger: true
          }
        }
      }
    }
  }
})