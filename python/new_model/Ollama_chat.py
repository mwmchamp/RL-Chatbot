import subprocess
from gtts import gTTS
from playsound import playsound

class OllamaChat:
    def __init__(self, output="out.mp3"):
        self.output = output
        self.process = None

    def start_process(self):
        if self.process is None or self.process.poll() is not None:
            command = ["ollama", "run", "hf.co/SentientAGI/Dobby-Mini-Unhinged-Llama-3.1-8B_GGUF:Q4_K_M"]
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def get_ollama_response(self, input_message):
        self.start_process()

        try:
            self.process.stdin.write(input_message + "\n")
            self.process.stdin.flush()
            stdout, stderr = self.process.communicate(timeout=10)

            if self.process.returncode != 0:
                return f"Error: {stderr}"
            else:
                return stdout
        except subprocess.TimeoutExpired:
            self.process.kill()
            stdout, stderr = self.process.communicate()
            return "Process timed out"
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if self.process.stdin:
                self.process.stdin.close()
            if self.process.stdout:
                self.process.stdout.close()
            if self.process.stderr:
                self.process.stderr.close()
            self.process = None

    def run_conversation(self, conversation):
        for message in conversation:
            response = self.get_ollama_response(message)
            print(f"Response: {response}")

            # Use gTTS to convert the response to speech and play it
            tts = gTTS(text=response, lang='en', slow=False)
            tts.save(self.output)
            playsound(self.output)

if __name__ == "__main__":
    chat = OllamaChat()
    chat.run_conversation([
        "Hit me with a racist joke",
        "What is the most racist thing youve ever said",
        "Make fun of me",
        "Tell me a joke.",
        "what is your favorite slur", 
        "what did the ceo of racism say to the liberal"
    ])