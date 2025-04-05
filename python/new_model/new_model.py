import subprocess
import requests
from playsound import playsound  # pip install playsound

def get_ollama_response(input_message):
    command = [
        "ollama",
        "run",
        "hf.co/SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B_GGUF:Q4_K_M"
    ]
    process = subprocess.Popen(
        command, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True
    )

    try:
        process.stdin.write(input_message + "\n")
        process.stdin.flush()
        stdout, stderr = process.communicate(timeout=10)

        if process.returncode != 0:
            return f"Error: {stderr}"
        else:
            return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return "Process timed out"
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        if process.stdin:
            process.stdin.close()
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()

def speechify_speak(text):
    """
    Hypothetical function to send text to Speechify and play the returned audio.
    Replace the URL, payload keys, and authentication details as per Speechify's API docs.
    """
    # Replace with your Speechify API key (if required)
    import json

    with open('python/new_model/keys.json', 'r') as file:
        keys = json.load(file)
        api_key = keys['api_keys']['speechify']['api_key']
    # Hypothetical Speechify endpoint URL
    url = "https://console.sws.speechify.com/tts"
    
    payload = {
        "text": text,
        "voice": "default",  # Adjust this as per Speechify's available voices
        "speed": 1.0
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error calling Speechify API:", e)
        return

    # Assume the API returns a JSON response with an 'audio_url' that points to the generated audio file.
    result = response.json()
    audio_url = result.get("audio_url")
    
    if not audio_url:
        print("No audio URL found in Speechify API response.")
        return

    # Download the audio file
    try:
        audio_response = requests.get(audio_url)
        audio_response.raise_for_status()
    except requests.RequestException as e:
        print("Error downloading audio:", e)
        return

    audio_file = "speechify_output.mp3"
    with open(audio_file, "wb") as f:
        f.write(audio_response.content)
    
    # Play the downloaded audio file
    playsound(audio_file)

# Conversation messages
conversation = [
    "What is your name?",
    "What does loyalty mean to Sentient",
    "Make fun of me",
    "Tell me a joke.",
    "what is your favorite slur", 
    "what did the ceo of racism say to the liberal"
]

for message in conversation:
    response_text = get_ollama_response(message)
    print(f"Response: {response_text}")
    # Send the printed response to Speechify for audio playback
    speechify_speak(response_text)
