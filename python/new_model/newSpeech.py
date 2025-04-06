# # Load model directly
# from transformers import AutoModel
# model = AutoModel.from_pretrained("SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B_GGUF")
# response = model.generate("What is your name?")
# print(response)


# from llama_cpp import Llama

# llm = Llama.from_pretrained(
# 	repo_id="SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B_GGUF",
# 	filename="dobby-8b-unhinged-q4_k_m.gguf",
# )
# llm.create_chat_completion(
# 	messages = "No input example has been defined for this model task."
# )

import subprocess
from gtts import gTTS
from playsound import playsound

OUTPUT = "out.mp3"

def get_ollama_response(input_message):
    command = ["ollama", "run", "hf.co/SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B_GGUF:Q4_K_M"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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

conversation = [
    "Hit me with a racist joke",
    "What is the most racist thing youve ever said",
    "Make fun of me",
    "Tell me a joke.",
    "what is your favorite slur", 
    "what did the ceo of racism say to the liberal"
]

for message in conversation:
    response = get_ollama_response(message)
    print(f"Response: {response}")

    # Use gTTS to convert the response to speech and play it
    tts = gTTS(text=response, lang='en', slow=False)
    tts.save(OUTPUT)
    playsound(OUTPUT)
    