import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import librosa
import numpy as np

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

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """
    Accepts an MP3 file, runs beat detection, returns tempo map.
    """
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Save to temp file for librosa to read
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Load and analyze audio
        y, sr = librosa.load(tmp_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Beat tracking
        tempo_est, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Handle numpy scalar
        tempo_est = float(tempo_est) if hasattr(tempo_est, 'item') else float(tempo_est)
        
        if len(beat_times) < 2:
            return jsonify({
                'success': False, 
                'error': 'Could not detect enough beats in audio'
            }), 400
        
        intervals = np.diff(beat_times)
        beat_bpms = 60.0 / intervals
        
        first_beat = float(beat_times[0])
        
        # Generate tempo maps at different granularities
        
        # 1. Beat-level (most precise)
        map_beat = []
        for i in range(len(beat_times) - 1):
            bpm = int(round(60.0 / intervals[i]))
            tick = i * RESOLUTION
            if not map_beat or map_beat[-1]['bpm'] != bpm:
                map_beat.append({'tick': tick, 'bpm': bpm})
        
        # 2. Measure-level (every 4 beats)
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
        
        # 3. Section-level (only change when tempo shifts by >2 BPM)
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
        
        # Also return beat times for potential visualization
        beat_times_list = [float(t) for t in beat_times]
        
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
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
