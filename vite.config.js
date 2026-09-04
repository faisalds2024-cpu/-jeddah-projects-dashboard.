import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: process.env.GITHUB_ACTIONS ? '/-jeddah-projects-dashboard./' : '/',
  plugins: [react(), tailwindcss()],
  publicDir: 'data',
  server: { host: '127.0.0.1' }
})
