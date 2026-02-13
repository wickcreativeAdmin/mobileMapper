# ChartMaker

Mobile Clone Hero chart creation with auto tempo detection.

## Deploy to Railway

1. Push this repo to GitHub
2. Connect to Railway
3. Deploy — that's it!

The app will be available at your Railway URL.

## Files

```
app.py           - Flask backend + serves frontend
static/
  index.html     - React frontend
requirements.txt - Python dependencies
Procfile         - Gunicorn config
railway.toml     - Railway config
nixpacks.toml    - System dependencies (ffmpeg)
```

## Local Development

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```
