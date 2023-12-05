Text to Speech Converter
This Python script uses the ElevenLabs API to convert text to speech. It provides a GUI for user interaction, built using the Tkinter library.

Features
Convert text to speech and download the output as an MP3 file.
Choose from different voices and models for the speech synthesis.
Upload your own voice for the speech synthesis.
Play the synthesized speech over your microphone or speakers.
Refresh the list of available voices and models.
Dependencies
This script requires the following Python libraries:

requests
pydub
tkinter
sounddevice
numpy
pyaudio
threading
glob
re

You can install these dependencies using pip:
pip install requests pydub tkinter sounddevice numpy pyaudio

Usage
Replace your_api_key with your actual ElevenLabs API key.
Run the script in a Python environment where all the dependencies are installed.
Use the GUI to input the text you want to convert to speech, choose a voice and model, and download the MP3 file.
Optionally, you can upload your own voice, play the synthesized speech over your microphone or speakers, and refresh the list of available voices and models.
Note
This script is designed to work with the ElevenLabs API. You need to have an API key from ElevenLabs to use their service.
