import os
import requests
from dotenv import load_dotenv

load_dotenv()


class PushNotification:
    sound = "pianobar"
    url = "https://api.pushover.net/1/messages.json"

    def __init__(self) -> None:
        self.token = os.getenv("NOTIFICATION_TOKEN")
        self.user = os.getenv("NOTIFICATION_USER_KEY")

    def send(self, title, message):
        requests.post(
            self.url,
            data={
                "token": self.token,
                "user": self.user,
                "title": title,
                "message": message,
                "sound": self.sound,
            },
        )
