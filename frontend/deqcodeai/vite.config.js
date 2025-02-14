import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from "path";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Backend server URL
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            console.log(`Proxying request to: ${proxyReq.path}`);
          });
          proxy.on('proxyRes', (proxyRes) => {
            console.log(`Received response with status: ${proxyRes.statusCode}`);
          });
          proxy.on('error', (err, req) => {
            console.error('Proxy error occurred:', err.message);
          });
        },
      },
    },
  },
  resolve:{
    alias:{
      "@": path.resolve(__dirname,"./src")
    },
  }
});
