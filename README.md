# ElevenLabs Soundboard

This web application utilizes the ElevenLabs API to convert text into speech. It provides a user-friendly web interface for interaction, where users can input text, select a voice, and choose a model for the conversion. The output is an MP3 file that can be downloaded.

## Features

- Text to speech conversion using the ElevenLabs API
- Web-based interface for user interaction
- Option to upload an audio file to create a new voice
- Progress bar to indicate the status of the conversion
- Modernized web interface
- New feature to insert breaks with specified duration in the text

## Dependencies

This application requires the following Python libraries:

- Flask
- requests
- pydub
- sounddevice
- numpy

You can install these dependencies using pip:

```bash
pip install Flask requests pydub sounddevice numpy
```

## Usage

1. Replace 'your_api_key' with your actual ElevenLabs API key in `app.py`.
2. Run the Flask application:

```bash
python app.py
```

3. Open your web browser and go to `http://127.0.0.1:5000/`.
4. Enter the text you want to convert to speech.
5. Choose a voice and a model for the conversion.
6. Click the "Convert to Speech" button to start the conversion. The output will be available for download as an MP3 file.
7. You can also upload a voice by clicking the "Upload Voice" button and selecting the audio files.
8. Use the "Insert Break" button to add breaks with specified duration in the text.

## Note

This application is designed to work with the ElevenLabs API. You need to have an API key from ElevenLabs to use this application.

## Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)

### Insert Break
![Insert Break](screenshots/insert_break.png)

### Upload Voice
![Upload Voice](screenshots/upload_voice.png)
