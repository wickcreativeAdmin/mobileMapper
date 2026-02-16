# Mobile Mapper

A mobile-first chart editor for Clone Hero with automatic tempo detection. Create rhythm game note charts directly from your phone or desktop browser.

![Mobile Mapper](https://img.shields.io/badge/Platform-Web-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## ✨ Features

### Core Charting
- **Auto Tempo Detection** - Analyzes audio files to detect BPM and beat positions using librosa
- **Multi-Instrument Support** - Chart for Guitar, Bass, and Drums
- **Multiple Difficulties** - Easy, Medium, Hard, and Expert per instrument
- **Visual Waveform** - See audio waveform behind the note highway for precise placement
- **Grid Snapping** - Snap to 1 beat, 1/2 beat, or 1/4 beat intervals
- **Copy/Paste** - Select, copy, paste, and nudge note sections
- **Sustain Notes** - Draw sustain tails by scrolling while in sustain mode

### Pro Mode
- **Tap Notes** - Notes that don't require strumming (rendered as outlines)
- **Forced Notes** - Override HOPO behavior (rendered as dashed outlines)
- **Open Notes** - Purple bar notes for guitar/bass (strum with no frets)

### Mobile-First Design
- Touch-friendly highway scrolling
- Large tap targets for note placement
- Swipe to scroll through the chart
- Reverse scroll option
- Works offline after initial load

### Desktop Enhancements
- **Side Panel Layout** - Full-height highway with controls in side panels
- **Keyboard Shortcuts** - Full keyboard support for fast charting:

| Key | Action |
|-----|--------|
| `1-5` or `G/R/Y/B/O` | Place notes |
| `0` or `` ` `` | Open note (guitar/bass) |
| `Shift + note` | Toggle sustain mode |
| `Space` | Play/Pause |
| `↑/↓` or `W/S` | Scroll up/down |
| `←/→` or `A/D` | Jump by beat |
| `Shift + ↑/↓` | Fast scroll (4 grid units) |
| `T` | Toggle tap mode |
| `F` | Toggle force mode |
| `Q` | Grid snap: 1 beat |
| `E` | Grid snap: 1/2 beat |
| `Ctrl+C` | Copy selection |
| `Ctrl+V` | Paste at current position |

### Export & Metadata
- **Standard .chart Export** - Compatible with Clone Hero and Moonscraper
- **Metadata Editor** - Song name, artist, album, year, genre, charter, preview times
- **Auto-generated song.ini** - Proper metadata file for Clone Hero
- **Save/Resume** - Auto-saves progress to browser, manual save to .chartmaker file

### Audio Features
- **Note Clap** - Audio feedback when crossing notes during playback
- **Variable Playback Speed** - 25%, 50%, 75%, or 100% speed
- **3-Second Silence Option** - Best practice for Clone Hero charts

## 🛠 Tech Stack

### Frontend
- **React 18** - UI components and state management
- **Tailwind CSS** - Utility-first styling
- **Babel** - JSX transformation in browser
- **Web Audio API** - Audio playback and note clap generation

### Backend
- **Python 3.11+** - Server runtime
- **Flask** - Web framework and API
- **Flask-CORS** - Cross-origin resource sharing
- **librosa** - Audio analysis and tempo detection
- **NumPy** - Numerical computations

### Deployment
- **Railway** - Cloud hosting platform
- **Gunicorn** - Production WSGI server
- **Nixpacks** - Build system with FFmpeg support

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js (optional, for development)
- FFmpeg (for audio processing)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mobile-mapper.git
   cd mobile-mapper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

### Deploy to Railway

1. Fork this repository
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Railway will auto-detect the configuration and deploy

## 📁 Project Structure

```
mobile-mapper/
├── app.py              # Flask server and API endpoints
├── static/
│   └── index.html      # React frontend (single-file app)
├── requirements.txt    # Python dependencies
├── railway.toml        # Railway configuration
├── nixpacks.toml       # Build configuration (FFmpeg)
├── Procfile           # Process definition
├── Aptfile            # System dependencies
└── README.md          # This file
```

## 🎮 Usage Guide

### Creating a New Chart

1. **Upload Audio** - Select an MP3, WAV, or OGG file
2. **Wait for Analysis** - Tempo detection takes a few seconds
3. **Navigate** - Swipe/scroll through the song
4. **Place Notes** - Tap lane buttons or use keyboard (1-5)
5. **Add Sustains** - Tap the sustain zone, scroll, tap again
6. **Export** - Download your .chart file

### Tips for Better Charts

- Use the waveform to align notes with audio peaks
- Start at a slower playback speed for complex sections
- Use the note clap feature to verify sync without watching
- Copy/paste repeated sections to save time
- Add 3 seconds of silence at the start for Clone Hero

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Keep the single-file frontend architecture (index.html contains everything)
- Test on both mobile and desktop
- Maintain backward compatibility with saved .chartmaker files
- Follow existing code style

### Feature Ideas

- [ ] Undo/Redo system
- [ ] Import existing .chart files
- [ ] Section markers and events
- [ ] Lyrics/vocals editor
- [ ] Star Power phrases
- [ ] MIDI import
- [ ] Multiple audio stems

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Clone Hero](https://clonehero.net/) - The rhythm game this tool creates charts for
- [Moonscraper](https://github.com/FireFox2000000/Moonscraper-Chart-Editor) - Inspiration for features and .chart format
- [librosa](https://librosa.org/) - Excellent audio analysis library
- [Railway](https://railway.app/) - Easy deployment platform

## 📞 Support

- **Issues** - Report bugs or request features via GitHub Issues
- **Discussions** - Join the conversation in GitHub Discussions

---

Made with ❤️ by the charting community
