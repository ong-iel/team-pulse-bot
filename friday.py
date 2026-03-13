import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_channel_id():
    result = client.conversations_list()
    for channel in result["channels"]:
        if channel["name"] == "team-pulse":
            return channel["id"]
    return None

def get_monday_thread_ts(channel_id):
    # Look back 7 days to find Monday's prompt
    result = client.conversations_history(
        channel=channel_id,
        limit=200
    )
    for msg in result["messages"]:
        if "Monday Compass Check" in msg.get("text", "") and msg.get("user") is None:
            return msg["ts"]
    return None

channel_id = get_channel_id()
if channel_id:
    monday_ts = get_monday_thread_ts(channel_id)
    if monday_ts:
        replies = client.conversations_replies(
            channel=channel_id,
            ts=monday_ts
        )
        messages = replies["messages"][1:]
    for msg in messages:
            user_id = msg["user"]
            user_text = msg["text"]
            client.chat_postMessage(
                channel=channel_id,
                text=(
                    f"👋 Hey <@{user_id}> — here's what you set out to do this week:\n\n"
                    f"_{user_text}_\n\n"
                    f"How did it go? Please share:\n"
                    f"✅ What did you accomplish?\n"
                    f"🔄 What's still open?\n"
                    f"❌ What blocked you — and what's the solution?\n\n"
                    f"💬 Did anything significant come up this week that wasn't in your Monday plan? Share it here too.\n\n"
                    f"⚠️ *Please reply in thread* to this message.\n\n"
                    f"📋 *Reminder:* don't forget to fill in the meeting agenda with your areas of focus for next week before Monday! 🗓️"
                )
            )
        print("Friday reflections posted successfully")
    else:
        print("No Monday thread found")
