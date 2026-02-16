import os
import tempfile
import traceback
import urllib.request
import urllib.parse
import json
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

RESOLUTION = 192
TIME_SIG = 4

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/lyrics/search', methods=['GET'])
def search_lyrics():
    """
    Search for lyrics using lyrics.ovh API
    """
    artist = request.args.get('artist', '')
    title = request.args.get('title', '')
    
    if not artist or not title:
        return jsonify({'success': False, 'error': 'Artist and title required'}), 400
    
    print(f"Searching lyrics for: {artist} - {title}")
    
    try:
        # Use lyrics.ovh API (free, no key needed)
        # Clean up the search terms
        clean_artist = artist.strip()
        clean_title = title.strip()
        # Remove common prefixes like track numbers
        import re
        clean_title = re.sub(r'^\d+[\s\-\.]+', '', clean_title)
        
        url = f"https://api.lyrics.ovh/v1/{urllib.parse.quote(clean_artist)}/{urllib.parse.quote(clean_title)}"
        print(f"Lyrics API URL: {url}")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'MobileMapper/1.0'})
        with urllib.request.urlopen(req, timeout=20) as response:  # Increased timeout
            data = json.loads(response.read().decode())
            
            if 'lyrics' in data:
                # Clean up lyrics
                lyrics = data['lyrics'].strip()
                # Split into lines, removing empty ones
                lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
                
                print(f"Found {len(lines)} lines of lyrics")
                
                return jsonify({
                    'success': True,
                    'lyrics': lyrics,
                    'lines': lines,
                    'artist': clean_artist,
                    'title': clean_title
                })
            else:
                return jsonify({'success': False, 'error': f'No lyrics found for "{clean_artist} - {clean_title}"'}), 404
                
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        if e.code == 404:
            return jsonify({'success': False, 'error': f'No lyrics found for "{artist} - {title}"'}), 404
        return jsonify({'success': False, 'error': f'API error: {e.code}'}), 500
    except urllib.error.URLError as e:
        print(f"URL Error: {e}")
        return jsonify({'success': False, 'error': 'Connection failed. The lyrics service may be unavailable.'}), 500
    except Exception as e:
        print(f"Lyrics search error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/lyrics/parse', methods=['POST'])
def parse_lrc():
    """
    Parse LRC format lyrics (timestamped)
    """
    data = request.get_json()
    lrc_content = data.get('lrc', '')
    
    if not lrc_content:
        return jsonify({'success': False, 'error': 'No LRC content provided'}), 400
    
    try:
        lines = []
        # LRC format: [mm:ss.xx]text or [mm:ss]text
        pattern = r'\[(\d{1,2}):(\d{2})(?:\.(\d{2}))?\](.+)'
        
        for line in lrc_content.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                centiseconds = int(match.group(3)) if match.group(3) else 0
                text = match.group(4).strip()
                
                time_seconds = minutes * 60 + seconds + centiseconds / 100
                
                if text:  # Skip empty lines
                    lines.append({
                        'time': time_seconds,
                        'text': text
                    })
        
        return jsonify({
            'success': True,
            'lines': lines
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """
    Accepts an MP3 file, runs beat detection, returns tempo map.
    """
    print("=== /analyze endpoint hit ===")
    
    if 'file' not in request.files:
        print("Error: No file in request")
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        print("Error: Empty filename")
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    print(f"Received file: {file.filename}")
    
    # Save to temp file for librosa to read
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        print(f"Saved to temp file: {tmp_path}")
        print("Importing librosa...")
        
        import librosa
        import numpy as np
        
        print("Loading audio file...")
        y, sr = librosa.load(tmp_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        print(f"Audio loaded: {duration:.1f}s, sr={sr}")
        
        # Beat tracking
        print("Running beat detection...")
        tempo_est, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Handle numpy scalar
        tempo_est = float(tempo_est) if hasattr(tempo_est, 'item') else float(tempo_est)
        print(f"Detected tempo: {tempo_est:.1f} BPM, {len(beat_times)} beats")
        
        if len(beat_times) < 2:
            return jsonify({
                'success': False, 
                'error': 'Could not detect enough beats in audio'
            }), 400
        
        intervals = np.diff(beat_times)
        first_beat = float(beat_times[0])
        
        # Generate tempo maps
        print("Generating tempo maps...")
        
        # Beat-level
        map_beat = []
        for i in range(len(beat_times) - 1):
            bpm = int(round(60.0 / intervals[i]))
            tick = i * RESOLUTION
            if not map_beat or map_beat[-1]['bpm'] != bpm:
                map_beat.append({'tick': tick, 'bpm': bpm})
        
        # Measure-level
        measure_data = []
        for i in range(0, len(beat_times) - TIME_SIG, TIME_SIG):
            dur = beat_times[i + TIME_SIG] - beat_times[i]
            bpm = int(round((TIME_SIG * 60.0) / dur))
            measure_data.append({'beat_idx': i, 'bpm': bpm})
        
        map_measure = []
        for i, m in enumerate(measure_data):
            tick = i * TIME_SIG * RESOLUTION
            if not map_measure or map_measure[-1]['bpm'] != m['bpm']:
                map_measure.append({'tick': tick, 'bpm': m['bpm']})
        
        # Section-level
        map_section = []
        section_bpms = []
        section_start = 0
        
        for i, m in enumerate(measure_data):
            section_bpms.append(m['bpm'])
            is_last = (i == len(measure_data) - 1)
            next_diff = False
            
            if not is_last:
                avg = np.mean(section_bpms)
                if abs(measure_data[i + 1]['bpm'] - avg) > 2.0:
                    next_diff = True
            
            if next_diff or is_last:
                avg_bpm = int(round(np.mean(section_bpms)))
                tick = section_start * TIME_SIG * RESOLUTION
                if not map_section or map_section[-1]['bpm'] != avg_bpm:
                    map_section.append({'tick': tick, 'bpm': avg_bpm})
                section_start = i + 1
                section_bpms = []
        
        beat_times_list = [float(t) for t in beat_times]
        
        print("Analysis complete, returning results")
        
        return jsonify({
            'success': True,
            'duration': float(duration),
            'globalTempo': tempo_est,
            'firstBeat': first_beat,
            'beatCount': len(beat_times),
            'beatTimes': beat_times_list,
            'tempoMaps': {
                'beat': map_beat,
                'measure': map_measure,
                'section': map_section
            }
        })
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        # Clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
            print("Cleaned up temp file")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
