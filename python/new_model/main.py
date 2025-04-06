import humeGen
import asyncio
from playsound import playsound
from pathlib import Path
from Ollama_chat import OllamaChat
from conversation_manager import ConversationManager
import sys
import time

# compile audio into a file as we go


OUTPUT = str(Path.cwd() / "out.wav")

async def main():
    topic = "playing minecraft while roasting people in the chat and encouraging banter"
    manager = ConversationManager(topic)
    chat = OllamaChat()
    tts_client = humeGen.HumeTTS()

    message = manager.generate_opening()
    response = chat.get_ollama_response(message)
    await tts_client.synthesize(response, description="A sassy British gamer girl who talks quickly")
    await asyncio.to_thread(playsound, OUTPUT)
    print("response", response, file=sys.stderr)

    stop_time = time.time() + 60 * 1  # Stop after 1 min
    while time.time() < stop_time:
        next_message = manager.generate_next()
        response = chat.get_ollama_response(next_message)
        await tts_client.synthesize(response, description="A sassy British gamer girl who talks quickly")
        await asyncio.to_thread(playsound, OUTPUT)
        print("response", response, file=sys.stderr)

    end_message = manager.generate_closing()
    response = chat.get_ollama_response(end_message)
    await tts_client.synthesize(response, description="A sassy British gamer girl who talks quickly")
    await asyncio.to_thread(playsound, OUTPUT)
    print("response", response, file=sys.stderr)

    # summarize what went on in the chat, and save a log with description at top and all interactions below. Archive

    # Update the overall vibe summary with anything new from the last 5 episodes


asyncio.run(main())