import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

response = client.chat_postMessage(
    channel="#new-channel",
    text="✅ Hello from your Competitor Tracker Bot!"
)

print("Message sent:", response)
