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

def download_mp3(api_key, user_input_text, chosen_user_voice_id, chosen_model_id, result_label, use_custom_path):
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

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        if use_custom_path:
            save_path = "C:/Users/s_den/OneDrive/Desktop/Soundboard/output.mp3"
        else:
            save_path = os.path.join(os.path.expanduser("~"), "Downloads",
                                     "output at " + datetime.datetime.now().strftime("%H") + "-" +
                                     datetime.datetime.now().strftime("%M") + "-" +
                                     datetime.datetime.now().strftime("%S") + ".mp3")

        with open(save_path, 'wb') as f:
            f.write(response.content)

        result_label.config(text="MP3 file downloaded successfully.")
    else:
        result_label.config(text=f"Error: {response.status_code}, {response.text}")
def on_submit():
    user_input_text = text_entry.get()
    chosen_user_voice_id = your_voices[voices_combobox.current()]['voice_id']
    chosen_model_id = available_models[models_combobox.current()]["model_id"]
    download_mp3(your_api_key, user_input_text, chosen_user_voice_id, chosen_model_id, result_label, use_custom_path.get())

    if use_custom_path.get():
        # Move play_fixed_mp3() inside the if block to play the audio only when using custom path
        play_fixed_mp3()

# Remove the following line, as it plays the audio outside the button click event
# play_fixed_mp3()

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

def play_fixed_mp3():
    # Set the file path
    file_path = r"C:\Users\s_den\OneDrive\Desktop\Soundboard\output.mp3"

    # Load the MP3 file
    audio = AudioSegment.from_mp3(file_path)

    # Convert to numpy array
    samples = np.array(audio.get_array_of_samples())

    # Play the audio using sounddevice to VB-Cable virtual device
    sd.play(samples, samplerate=44100, device="CABLE Input (VB-Audio Virtual Cable),  Windows DirectSound", blocking=True,)

    # Wait for the playback to finish (adjust the sleep duration as needed)
    time.sleep(len(audio) / 1000)

# Replace 'your_api_key' with your actual API key
your_api_key = "your_api_key"

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
text_entry = tk.Entry(window, width=50)
text_entry.pack(pady=5)

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
use_custom_path = tk.BooleanVar()
custom_path_checkbox = tk.Checkbutton(window, text="Play on soundboard", variable=use_custom_path)
custom_path_checkbox.pack(pady=5)

submit_button = tk.Button(window, text="Download MP3", command=on_submit)
submit_button.pack(pady=5)

upload_button = tk.Button(window, text="Upload Voice", command=on_upload)
upload_button.pack(pady=5)

result_label = tk.Label(window, text="")
result_label.pack(pady=5)

# Start the Tkinter event loop
window.mainloop()