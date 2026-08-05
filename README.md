# League Stat Sheet

A fantasy football BI dashboard for The Liquorball Syndicate, built from ESPN
Fantasy Football exports (2018-2025).

## Files
- `streamlit_app.py` — the app
- `data/dashboard_data.json` — pre-aggregated league data (standings, matchups,
  draft results, and weekly player points/projections have already been
  crunched into this one file, so the app has no dependency on the raw CSVs)
- `requirements.txt` — Python dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repo (keep `streamlit_app.py` and the `data/`
   folder in the same relative location — the app loads the JSON via a path
   relative to the script, so folder structure matters).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and click "New app."
3. Point it at your repo, branch, and `streamlit_app.py` as the main file.
4. Deploy. No secrets or environment variables needed — everything the app
   needs ships in `data/dashboard_data.json`.

## Notes
- Draft "Best & Busts" analysis only covers seasons with weekly projection
  data: 2019, 2020, 2022–2025 (2018 and 2021 are missing from the source
  export).
- Manager identity is "First Name + Last Initial," derived from ESPN owner
  records, so it stays stable across team-name changes year to year.
