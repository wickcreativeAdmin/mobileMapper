# ChartMaker

Mobile-friendly Clone Hero chart creation tool with automatic tempo detection.

## Features

- **Auto tempo detection** - Upload an MP3 and get automatic BPM mapping
- **Three tempo map granularities** - Beat-level, measure-level, or section-level
- **Mobile-optimized UI** - Swipe to scroll, tap to place notes
- **Variable playback speed** - 25%, 50%, 75%, 100%
- **Export .chart files** - Ready for Moonscraper or Clone Hero

## Architecture

- **Backend**: Python/Flask with librosa for audio analysis
- **Frontend**: Single HTML file with React (no build step needed)

## Deployment

### Backend (Railway)

1. Create a new project on Railway
2. Connect your GitHub repo or use Railway CLI
3. Point to the `/backend` directory
4. Railway will auto-detect Python and deploy

The backend will be available at `https://your-project.railway.app`

### Frontend

1. Update `API_URL` in `frontend/index.html` to point to your Railway backend
2. Host the `index.html` anywhere:
   - GitHub Pages
   - Netlify (just drag the file)
   - Vercel
   - Any static hosting

### Quick Local Testing

```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend  
cd frontend
python -m http.server 8080
# Open http://localhost:8080
```

## Usage

1. Open the app on your phone
2. Tap "Select MP3" and choose an audio file
3. Wait for tempo analysis (10-30 seconds)
4. Use the charting interface:
   - Swipe up/down on the highway to scroll
   - Tap G/R/Y/B/O buttons to place notes at current position
   - Use -1/+1 buttons for precise beat navigation
   - Adjust playback speed as needed
5. Tap "Export" to download your .chart file

## Tempo Map Types

- **Section**: Fewest changes, only updates when tempo shifts significantly (>2 BPM)
- **Measure**: Updates every 4 beats, good balance
- **Beat**: Maximum precision, updates every beat

## Notes

- The exported .chart includes the auto-detected BPM map and offset
- Only ExpertSingle difficulty is created - add other difficulties in Moonscraper
- Sustain notes, star power, etc. should be added in Moonscraper after
