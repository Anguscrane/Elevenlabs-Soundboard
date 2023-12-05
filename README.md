GitHub Copilot: # Text to Speech Converter

This Python application utilizes the ElevenLabs API to convert text into speech. It provides a user-friendly GUI for interaction, where users can input text, select a voice, and choose a model for the conversion. The output is an MP3 file that can be played over the speakers or a virtual audio cable.

## Features

- Text to speech conversion using the ElevenLabs API
- GUI for user interaction
- Option to play the output over speakers or a virtual audio cable
- Option to upload an audio file to create a new voice
- Progress bar to indicate the status of the conversion

## Dependencies

This application requires the following Python libraries:

- requests
- pydub
- tkinter
- sounddevice
- numpy
- pyaudio
- threading
- glob
- re

You can install these dependencies using pip:

```bash
pip install requests pydub tkinter sounddevice numpy pyaudio
```

## Usage

1. Replace 'your_api_key' with your actual ElevenLabs API key.
2. Run the script. A GUI will appear.
3. Enter the text you want to convert to speech.
4. Choose a voice and a model for the conversion.
5. Click the "Download MP3" button to start the conversion. The output will be saved as an MP3 file in your Downloads folder.
6. You can also upload a voice by clicking the "Upload Voice" button and selecting the audio files.

## Note

This application is designed to work with the ElevenLabs API. You need to have an API key from ElevenLabs to use this application.
