import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// In Docker dev mode the backend is a separate service, so the API proxy
// target is configurable (defaults to localhost for bare-metal dev).
const apiTarget = process.env.VITE_API_PROXY || 'http://localhost:8000'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    host: true, // listen on 0.0.0.0 so the dev server is reachable from outside the container
    proxy: {
      '/api': apiTarget,
    },
  },
})
