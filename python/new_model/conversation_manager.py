from datetime import datetime, timedelta

class ConversationManager:
    def __init__(self, topic):
        self.last_message_time = None
        self.response_delay_threshold = timedelta(minutes=5)  # Example threshold
        self.default_response = "continue speaking"
        self.topic = topic

    def receive_message(self, message: str) -> str:
        current_time = datetime.now()
        response = self.default_response

        if self.last_message_time:
            time_since_last_message = current_time - self.last_message_time
            if time_since_last_message > self.response_delay_threshold:
                response = self.generate_delayed_response(message)
            else:
                response = self.generate_standard_response(message)
        else:
            response = self.generate_standard_response(message)

        self.last_message_time = current_time
        return response

    def generate_opening(self) -> str:
        return f"you are a twitch streamer named Rot-Bot known for {self.topic}. Introduce yourself to start the stream"
    
    def generate_closing(self) -> str:
        return f"you are a twitch streamer named Rot-Bot known for {self.topic}. End the stream and say goodbye"

    def generate_next(self) -> str:
        # Check if there are comments queued

        # If queued, respond
            # decide randomly to address commenter
            # decide to thank commenter
            # put together name, comment, donation to ask to respond to commenter
        # otherwise, randomly
            # generate a story topic and introduce a story if there is none currently or keep talking on the last comment
            # continue a story if there is one currently
        
        return f"Introduce a story about some wild experiences youve had"
