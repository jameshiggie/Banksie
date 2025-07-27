const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Determine the target based on environment
  const target = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  
  console.log(`🔗 Setting up proxy to: ${target}`);
  
  app.use(
    '/api',
    createProxyMiddleware({
      target: target,
      changeOrigin: true,
      ws: true, // Enable WebSocket proxying
      logLevel: 'debug',
      onError: (err, req, res) => {
        console.error('Proxy error:', err.message);
      },
      onProxyReq: (proxyReq, req, res) => {
        console.log(`🔄 Proxying ${req.method} ${req.url} to ${target}${req.url}`);
      }
    })
  );
}; 