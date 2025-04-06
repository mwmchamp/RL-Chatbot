import os
import json
from datetime import datetime
from pathlib import Path
import openai

class LogUpdater:
    def __init__(self, logs_dir="logs", personality_file="personality.txt"):
        self.logs_dir = Path(logs_dir)
        self.personality_file = Path(personality_file)
        self.logs_dir.mkdir(exist_ok=True)
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise EnvironmentError("OPENAI_API_KEY not found in environment variables")
        openai.api_key = self.openai_api_key

    def new_episode(self, comments, dialogue, audio, timestamp):
        # Create a new folder with the timestamp
        episode_dir = self.logs_dir / timestamp
        episode_dir.mkdir(exist_ok=True)

        # Save comments and dialogue as JSON
        episode_data = {
            "comments": comments,
            "dialogue": dialogue
        }
        with open(episode_dir / "episode_data.json", "w") as f:
            json.dump(episode_data, f, indent=4)

        # Generate a summary using ChatGPT
        summary = self._generate_summary(comments, dialogue)
        with open(episode_dir / "summary.txt", "w") as f:
            f.write(summary)

        # Save the audio file
        audio_path = episode_dir / "audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio)

    def update_understanding(self):
        # Collect summaries from the last 5 episodes
        summaries = self._collect_recent_summaries(5)
        if not summaries:
            return

        # Generate an updated understanding using ChatGPT
        updated_understanding = self._generate_updated_understanding(summaries)

        # Update the personality file if there's a significant difference
        if self._is_significant_difference(updated_understanding):
            with open(self.personality_file, "w") as f:
                f.write(updated_understanding)

    def _generate_summary(self, comments, dialogue):
        prompt = f"Summarize the following conversation and comments:\n\nComments: {comments}\n\nDialogue: {dialogue}\n\nInclude the overall vibe."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def _collect_recent_summaries(self, count):
        summaries = []
        episodes = sorted(self.logs_dir.iterdir(), key=os.path.getmtime, reverse=True)
        for episode in episodes[:count]:
            summary_file = episode / "summary.txt"
            if summary_file.exists():
                with open(summary_file, "r") as f:
                    summaries.append(f.read())
        return summaries

    def _generate_updated_understanding(self, summaries):
        prompt = f"Based on the following summaries, update the understanding of the personality:\n\n{summaries}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()

    def _is_significant_difference(self, updated_understanding):
        if not self.personality_file.exists():
            return True
        with open(self.personality_file, "r") as f:
            current_understanding = f.read()
        return current_understanding != updated_understanding
