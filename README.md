# League Stat Sheet (React / Vite)

The original chat-artifact dashboard, packaged as a real static site: same
recharts visuals, same scoreboard theme, same scrolling champions marquee.
No Streamlit — this is the actual React component running in a real
single-page app.

## Files
- `src/App.jsx` — the dashboard component (all data is baked in as a JS
  constant near the top of the file — no separate data file, no API calls)
- `src/main.jsx` — Vite/React entry point
- `index.html` — HTML shell
- `vite.config.js` — build config; **`base` must match your repo name**
- `.github/workflows/deploy.yml` — auto-builds and deploys to GitHub Pages
  on every push to `main`

## Run locally
```bash
npm install
npm run dev
```
Opens at `http://localhost:5173`.

## Deploy to GitHub Pages (recommended — free, matches the workflow already in this repo)

1. **Push this folder to your GitHub repo** (e.g. `tspring9/FantasyFBDash`).
2. **Check `vite.config.js`** — `base` is currently set to `/FantasyFBDash/`.
   If your repo has a different name, change it to match:
   ```js
   base: '/your-repo-name/',
   ```
3. In the repo, go to **Settings → Pages** and under "Build and deployment,"
   set **Source** to **"GitHub Actions"** (not "Deploy from a branch").
4. Push to `main`. The included workflow
   (`.github/workflows/deploy.yml`) will automatically install
   dependencies, build, and publish to GitHub Pages — no manual
   `npm run build` needed. Check the **Actions** tab to watch it run.
5. Your site will be live at `https://tspring9.github.io/FantasyFBDash/`
   (or whatever your GitHub username/repo combination is).

## Deploy to Cloudflare Pages instead

If you'd rather use Cloudflare Pages:
1. Change `base: '/FantasyFBDash/'` to `base: '/'` in `vite.config.js`
   (Cloudflare Pages serves from the domain root, not a repo subpath).
2. Connect your GitHub repo in the Cloudflare Pages dashboard.
3. Build command: `npm run build`. Build output directory: `dist`.
4. Cloudflare handles the rest automatically on every push.

## Updating the data later

The data lives in one place: the `const DATA = {...}` block near the top
of `src/App.jsx`. If you get new season exports, re-run the aggregation
pipeline, regenerate that JSON, and paste it back into that constant —
everything else in the component reads from it automatically.
