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
      // Remove console logs in production
      config.optimization.minimizer[0].options.terserOptions.compress.drop_console = true
    }
  }
})