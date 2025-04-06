# import torch
# from TTS.api import TTS
# import json
# import platform

# # Check if the platform is macOS
# is_mac = platform.system() == "Darwin"

# with open('python/new_model/keys.json', 'r') as file:
#     keys = json.load(file)
#     api_key = keys['api_keys']['speechify']['api_key']
#     # Hypothetical Speechify endpoint URL

# # Get device
# # On macOS, it's common to use CPU as CUDA is not typically supported
# device = "cpu" if is_mac else ("cuda" if torch.cuda.is_available() else "cpu")

# # List available 🐸TTS models
# print(TTS().list_models())

# # Init TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# # Run TTS
# # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# # Text to speech list of amplitude values as output
# wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
# # Text to speech to a file
# tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")

import requests
import base64
import json

# Replace with your actual Speechify API key
with open('python/new_model/keys.json', 'r') as file:
    keys = json.load(file)
    API_KEY = keys['api_keys']['speechify']['api_key']

# The API base URL for TTS requests (adjust if needed per your docs)
BASE_URL = "https://api.sws.speechify.com/v1/audio/speech"

# Prepare HTTP headers with authentication and content type
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Payload: you can use plain text or SSML (see docs)
payload = {
    "input": "Hello, this is Speechify converting text to speech!",
    "voice_id": "default"  # Replace with a valid voice ID if necessary
}

# Make the POST request to the Speechify API
response = requests.post(BASE_URL, headers=headers, json=payload)

if response.status_code == 200:
    try:
        # First, try to interpret the response as JSON.
        data = response.json()
        # If the API returns the audio as a base64-encoded string under the key "audio"
        audio_base64 = data.get("audio")
        if audio_base64:
            audio_bytes = base64.b64decode(audio_base64)
            with open("output.mp3", "wb") as f:
                f.write(audio_bytes)
            print("Audio saved as output.mp3")
        else:
            print("No 'audio' field found in JSON response; please check the API docs.")
    except json.JSONDecodeError:
        # If response isn't JSON, assume it is the binary audio data
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("Audio saved as output.mp3")
else:
    print(f"Error {response.status_code}: {response.text}")
