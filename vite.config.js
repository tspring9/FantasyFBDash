import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// If deploying to GitHub Pages at https://<user>.github.io/<repo>/,
// base must match the repo name exactly (with leading and trailing slash).
// If deploying to a custom domain or Cloudflare Pages at the root,
// change base to '/'.
export default defineConfig({
  plugins: [react()],
  base: '/FantasyFBDash/',
})
