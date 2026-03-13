import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_channel_id():
    result = client.conversations_list()
    for channel in result["channels"]:
        if channel["name"] == "team-pulse":
            return channel["id"]
    return None

channel_id = get_channel_id()
if channel_id:
    client.chat_postMessage(
        channel=channel_id,
        text="☀️ Good morning! Time for your *Daily Standup*.\n\nPlease write the things you are focusing on today, using this format:\n*[Project / Milestone] — I am doing [task] so that [outcome]*\n\nWe wear many hats, so share as much as reflects your day.\n\n⚠️ *Please reply in thread* — not in the main channel.\n\nHave a great day! 💪"
    )
    print("Standup prompt posted successfully")
