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
        text="🧭 Good morning, team! Time for your *Monday Compass Check*.\n\nPlease copy paste your focus for this week directly from our meeting agenda into this thread. This is your moment to land in the work week — take a breath and be intentional about where you're putting your energy.\n\nWhen sharing your tasks, please use this format:\n*[Project / Milestone] — Task*\n\n⚠️ *Please reply in thread* — click 'Reply in thread' below, not in the main channel.\n\nHave a fruitful week! 🌱"
    )
    print("Monday prompt posted successfully")
