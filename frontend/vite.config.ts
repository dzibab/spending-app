import { defineConfig, normalizePath } from 'vite'
import react from '@vitejs/plugin-react'
import basicSsl from '@vitejs/plugin-basic-ssl'
import viteTsconfigPaths from 'vite-tsconfig-paths'
// import svgr from 'vite-plugin-svgr'

// @ts-ignore
import path from 'path'

// https://vite.dev/config/
// @ts-ignore
export default defineConfig({
  plugins: [react(),
    viteTsconfigPaths(),
    basicSsl()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  },
  resolve: {
    // @ts-ignore
    alias: {
      '@': () => normalizePath(path.resolve(__dirname, 'src'))    }
  },
})
