
import requests
from pydub import AudioSegment
import io
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import datetime
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import numpy as np
import pyaudio
import time
import threading
import glob
import re

# Replace 'your_api_key' with your actual API key
your_api_key = "Your api key"

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

    data = {
        "name": name,
        "description": description,
        "labels": labels
    }

    files = [("files", (audio_file.split("/")[-1], open(audio_file, "rb"))) for audio_file in audio_files]

    response = requests.post(url, data=data, files=files, headers=headers)

    if response.status_code == 200:
        return response.json()["voice_id"]
    else:
        return None


def download_mp3(api_key, user_input_text, chosen_user_voice_id, chosen_model_id, result_label):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{chosen_user_voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": user_input_text,
        "model_id": chosen_model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    # Make the progress bar visible and start it
    progress.pack()
    progress.start()

    def request():
        response = requests.post(url, json=data, headers=headers)

        # Stop the progress bar and hide it
        progress.stop()
        progress.pack_forget()

        if response.status_code == 200:
                # Generate a unique filename using a timestamp and the user's input text
                timestamp = datetime.datetime.now().strftime("%m-%d-%H-%M")
                # Remove any characters that are not allowed in filenames
                safe_user_input_text = re.sub(r'[\\/*?:"<>|]', "", user_input_text)
                # Limit the length of the user's input text to avoid excessively long filenames
                safe_user_input_text = safe_user_input_text[:50]
                file_path = os.path.join(os.environ['USERPROFILE'] if 'USERPROFILE' in os.environ else os.environ['HOME'], "Downloads", f"output_{timestamp}_{safe_user_input_text}.mp3")
                with open(file_path, 'wb') as f:
                    f.write(response.content)


                result_label.config(text="MP3 file downloaded successfully.")

        # Check what to play over
        if play_over_microphone.get() & play_over_speakers.get():
            play_fixed_mp3("BOTH")
        elif play_over_microphone.get():
            play_fixed_mp3("CABLE")
        # Else, check the value of play_over_speakers
        elif play_over_speakers.get():
            play_fixed_mp3("HEADPHONES")
        # Else, do nothing (or show an error message)

    # Run the request in a separate thread
    threading.Thread(target=request).start()
def on_submit():
    # Get the user input text
    user_input_text = text_entry.get('1.0', 'end').strip()
    chosen_user_voice_id = your_voices[voices_combobox.current()]['voice_id']
    chosen_model_id = available_models[models_combobox.current()]["model_id"]
    download_mp3(your_api_key, user_input_text, chosen_user_voice_id, chosen_model_id, result_label)

def on_upload():
    file_paths = filedialog.askopenfilenames(
        title="Select audio files", filetypes=[("Audio files", "*.wav;*.mp3")]
    )
    if file_paths:
        # Create a new window for user input
        input_window = tk.Toplevel(window)
        input_window.title("Enter Voice Name")

        # Label and Entry for the user to input the name
        tk.Label(input_window, text="Enter a name for the voice:").pack(pady=5)
        name_entry = tk.Entry(input_window, width=30)
        name_entry.pack(pady=5)

        # Function to handle the OK button click
        def on_ok():
            name = name_entry.get() or file_paths[0].split("/")[-1]
            description = "Voice created from uploaded file"
            labels = ""
            voice_id = add_voice(your_api_key, name, description, labels, file_paths)
            if voice_id:
                your_voices.append({"name": name, "voice_id": voice_id})
                voices_combobox["values"] = [voice["name"] for voice in your_voices]
                voices_combobox.current(len(your_voices) - 1)
                result_label.config(text=f"Voice '{name}' created successfully.")
            else:
                result_label.config(text="Error creating voice.")

            input_window.destroy()  # Close the input window after processing

        # OK button to confirm the name
        ok_button = tk.Button(input_window, text="OK", command=on_ok)
        ok_button.pack(pady=5)

def play_fixed_mp3(output_device):
    # Get the list of all output files
    downloads_dir = os.path.join(os.environ['USERPROFILE'] if 'USERPROFILE' in os.environ else os.environ['HOME'], "Downloads")
    output_files = glob.glob(os.path.join(downloads_dir, "output_*.mp3"))

    # Find the most recently created file
    latest_file = max(output_files, key=os.path.getctime)

    print(latest_file)
    # Load the MP3 file
    audio = AudioSegment.from_mp3(latest_file)

    # Convert to numpy array
    samples = np.array(audio.get_array_of_samples())

    # Set the device based on the output_device parameter
    if output_device == "BOTH":
        # Play the audio over both the CABLE input and the default speakers
        sd.play(samples, samplerate=44100, device="CABLE Input (VB-Audio Virtual Cable),  Windows DirectSound", blocking=False)
        sd.play(samples, samplerate=44100, device=sd.default.device, blocking=False)
    elif output_device == "CABLE":
        device = "CABLE Input (VB-Audio Virtual Cable),  Windows DirectSound"
        sd.play(samples, samplerate=44100, device=device, blocking=True)
    elif output_device == "HEADPHONES":
        device = sd.default.device  # Set to default speakers
        sd.play(samples, samplerate=44100, device=device, blocking=True)

    # Wait for the playback to finish (adjust the sleep duration as needed)
    time.sleep(len(audio) / 1000)

# Function to refresh the voices and models
def refresh():
    global your_voices, voice_options, available_models, model_options
    your_voices = get_user_voices(your_api_key)
    voice_options = [voice['name'] for voice in your_voices]
    voices_combobox['values'] = voice_options
    voices_combobox.current(0)

    available_models = get_models(your_api_key)
    model_options = [f"{model['name']} - {model['description']}" for model in available_models]
    models_combobox['values'] = model_options
    models_combobox.current(0)

# Get voices associated with your account
your_voices = get_user_voices(your_api_key)
voice_options = [voice['name'] for voice in your_voices]

# Get available models
available_models = get_models(your_api_key)
model_options = [f"{model['name']} - {model['description']}" for model in available_models]

# Create the main window
window = tk.Tk()
window.title("Text to Speech Converter")

# Create and place widgets
tk.Label(window, text="Enter the text you want to convert:").pack(pady=5)
text_entry = tk.Text(window, width=50, height=10)
text_entry.pack(pady=5, expand=True, fill=tk.BOTH)

tk.Label(window, text="Choose a voice:").pack(pady=5)
max_voice_option_length = max(len(option) for option in voice_options)
voices_combobox = ttk.Combobox(window, values=voice_options, state="readonly", width=max_voice_option_length)
voices_combobox.pack(pady=5)
voices_combobox.current(0)

tk.Label(window, text="Choose a model:").pack(pady=5)
max_model_option_length = max(len(option) for option in model_options)
models_combobox = ttk.Combobox(window, values=model_options, state="readonly", width=max_model_option_length)
models_combobox.pack(pady=5)
models_combobox.current(0)

# Add a Checkbutton for custom save path
play_over_microphone = tk.BooleanVar()
custom_path_checkbox = tk.Checkbutton(window, text="Play over microphone", variable=play_over_microphone)
custom_path_checkbox.pack(pady=5)

play_over_speakers = tk.BooleanVar()
speakers_checkbox = tk.Checkbutton(window, text="Play over speakers", variable=play_over_speakers)
speakers_checkbox.pack(pady=5)

submit_button = tk.Button(window, text="Download MP3", command=on_submit)
submit_button.pack(pady=5)

upload_button = tk.Button(window, text="Upload Voice", command=on_upload)
upload_button.pack(pady=5)

result_label = tk.Label(window, text="")
result_label.pack(pady=5)

# Add a Refresh button
refresh_button = tk.Button(window, text="Refresh", command=refresh)
refresh_button.pack(pady=5)

# Add a Progress bar
progress = ttk.Progressbar(window, length=200, mode='indeterminate')
progress.pack(pady=5)

# Hide the progress bar initially
progress.pack_forget()

# Make the window resizable
window.resizable(True, True)

# Configure the grid to expand with the window
for i in range(10):  # Adjust as needed
    window.grid_columnconfigure(i, weight=1)
    window.grid_rowconfigure(i, weight=1)

# Start the Tkinter event loop
window.mainloop()
