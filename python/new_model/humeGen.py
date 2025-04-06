import os
import base64
import aiofiles
from pathlib import Path
from dotenv import load_dotenv
from hume import AsyncHumeClient
from hume.tts import PostedUtterance

class HumeTTS:
    def __init__(self):
        # Load environment variables from a .env file.
        load_dotenv()
        api_key = os.getenv("HUME_API_KEY")
        if not api_key:
            raise EnvironmentError("HUME_API_KEY not found in environment variables")
        # Initialize the Hume client.
        self.hume = AsyncHumeClient(api_key=api_key)
        # Default output filename in the current directory.
        self.default_output = "out.wav"

    async def _write_audio_to_file(self, base64_audio: str, filename: str) -> Path:
        """
        Decodes a base64 audio string and writes it to a file.
        Returns the Path of the written file.
        """
        file_path = Path(filename)
        audio_data = base64.b64decode(base64_audio)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(audio_data)
        return file_path

    async def synthesize(self, text: str, description: str = "A refined, British aristocrat", output_filename: str = None) -> Path:
        """
        Synthesizes the provided text using Hume TTS API.
        Optionally, a description (voice style) and output filename can be provided.
        Returns the path of the saved audio file.
        """
        if output_filename is None:
            output_filename = self.default_output

        # Call Hume's TTS API with a single utterance.
        response = await self.hume.tts.synthesize_json(
            utterances=[
                PostedUtterance(
                    description=description,
                    text=text
                )
            ]
        )

        # Write the generated audio to the specified output file.
        file_path = await self._write_audio_to_file(response.generations[0].audio, output_filename)
        return file_path
    


# Example usage:
# async def main():
#     tts_client = HumeTTS()
#     result_path = await tts_client.synthesize("Hello, world! This is a test using Hume TTS.", 
#                                                 description="A refined, British aristocrat")
#     print("Audio output saved to", result_path)
#
# if __name__ == "__main__":
#     asyncio.run(main())
