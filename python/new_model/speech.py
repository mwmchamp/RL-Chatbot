from speechify import Speechify
import requests

# Initialize the Speechify client with your token.
client = Speechify(token="gSgF8uGClYEwpc4XgPQdASKJEmUbkDXwSwFlXDAUst8=")

# Request text-to-speech conversion.
response = client.tts.audio.speech(
    input="hi norah",
    voice_id="default"
)

# Assume the response is a dictionary that includes an 'audio_url' key.
audio_url = response.get("audio_url")

if not audio_url:
    print("Audio URL not found in the response. Response received:")
    print(response)
else:
    # Download the audio file from the URL.
    audio_response = requests.get(audio_url)
    audio_response.raise_for_status()  # Raise an error for bad responses.

    # Save the audio content to a local file.
    output_filename = "output.mp3"
    with open(output_filename, "wb") as f:
        f.write(audio_response.content)

    print(f"Audio has been downloaded and saved as {output_filename}")
