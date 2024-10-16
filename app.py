from flask import Flask, render_template, request, jsonify
import requests
import os
import datetime
import re
import threading
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
import glob

app = Flask(__name__)

# Replace 'your_api_key' with your actual API key
your_api_key = "YOUR API KEY"

def get_user_voices(api_key):
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": api_key}
    response = requests.get(url, headers=headers)
    return response.json()["voices"]

def get_models(api_key):
    url = "https://api.elevenlabs.io/v1/models"
    headers = {"xi-api-key": api_key}
    response = requests.get(url, headers=headers)
    return response.json()

def add_voice(api_key, name, description, labels, audio_files):
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {"xi-api-key": api_key}
    data = {"name": name, "description": description, "labels": labels}
    files = [("files", (audio_file.split("/")[-1], open(audio_file, "rb"))) for audio_file in audio_files]
    response = requests.post(url, data=data, files=files, headers=headers)
    if response.status_code == 200:
        return response.json()["voice_id"]
    else:
        return None

def download_mp3(api_key, user_input_text, chosen_user_voice_id, chosen_model_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{chosen_user_voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }
    data = {
        "text": user_input_text,
        "model_id": chosen_model_id,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        timestamp = datetime.datetime.now().strftime("%m-%d-%H-%M")
        safe_user_input_text = re.sub(r'[\\/*?:"<>|]', "", user_input_text)
        safe_user_input_text = safe_user_input_text[:50]
        file_path = os.path.join(
            os.environ["USERPROFILE"] if "USERPROFILE" in os.environ else os.environ["HOME"],
            "Downloads",
            f"output_{timestamp}_{safe_user_input_text}.mp3",
        )
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        return None

def play_fixed_mp3(output_device):
    downloads_dir = os.path.join(
        os.environ["USERPROFILE"] if "USERPROFILE" in os.environ else os.environ["HOME"],
        "Downloads",
    )
    output_files = glob.glob(os.path.join(downloads_dir, "output_*.mp3"))
    latest_file = max(output_files, key=os.path.getctime)
    audio = AudioSegment.from_mp3(latest_file)
    samples = np.array(audio.get_array_of_samples())
    if output_device == "BOTH":
        sd.play(
            samples,
            samplerate=44100,
            device="CABLE Input (VB-Audio Virtual Cable),  Windows DirectSound",
            blocking=False,
        )
        sd.play(samples, samplerate=44100, device=sd.default.device, blocking=False)
    elif output_device == "CABLE":
        device = "CABLE Input (VB-Audio Virtual Cable),  Windows DirectSound"
        sd.play(samples, samplerate=44100, device=device, blocking=True)
    elif output_device == "HEADPHONES":
        device = sd.default.device
        sd.play(samples, samplerate=44100, device=device, blocking=True)
    time.sleep(len(audio) / 1000)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/voices', methods=['GET'])
def api_voices():
    voices = get_user_voices(your_api_key)
    return jsonify(voices)

@app.route('/api/models', methods=['GET'])
def api_models():
    models = get_models(your_api_key)
    return jsonify(models)

@app.route('/api/add_voice', methods=['POST'])
def api_add_voice():
    name = request.form['name']
    description = request.form['description']
    labels = request.form['labels']
    audio_files = request.files.getlist('audio_files')
    audio_file_paths = []
    for audio_file in audio_files:
        file_path = os.path.join('uploads', audio_file.filename)
        audio_file.save(file_path)
        audio_file_paths.append(file_path)
    voice_id = add_voice(your_api_key, name, description, labels, audio_file_paths)
    if voice_id:
        return jsonify({"voice_id": voice_id})
    else:
        return jsonify({"error": "Error creating voice"}), 500

@app.route('/api/convert', methods=['POST'])
def api_convert():
    user_input_text = request.form['text']
    chosen_user_voice_id = request.form['voice_id']
    chosen_model_id = request.form['model_id']
    file_path = download_mp3(your_api_key, user_input_text, chosen_user_voice_id, chosen_model_id)
    if file_path:
        return jsonify({"file_path": file_path})
    else:
        return jsonify({"error": "Error converting text to speech"}), 500

if __name__ == '__main__':
    app.run(debug=True)
