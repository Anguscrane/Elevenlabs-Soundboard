GitHub Copilot: # Text to Speech Converter

This Python script uses the ElevenLabs API to convert text to speech. It provides a GUI for user interaction, where the user can input text, select a voice, and choose a model for the conversion. The output is an MP3 file that can be played over the speakers or a virtual audio cable.
Features

    Text to speech conversion using the ElevenLabs API
    GUI for user interaction
    Option to play the output over speakers or a virtual audio cable
    Option to upload an audio file to create a voice
    Progress bar to indicate the status of the conversion

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

    Replace 'your_api_key' with your actual ElevenLabs API key.
    Run the script. A GUI will appear.
    Enter the text you want to convert to speech.
    Choose a voice and a model for the conversion.
    Click the "Download MP3" button to start the conversion. The output will be saved as an MP3 file in your Downloads folder.
    You can also upload a voice by clicking the "Upload Voice" button and selecting the audio files.

Note

This script is designed to work with the ElevenLabs API. You need to have an API key from ElevenLabs to use this script.
