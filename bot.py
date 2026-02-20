import os
import logging
from datetime import datetime
from slack_bolt import App
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

CHANNEL_NAME = "team-pulse"
monday_thread_ts = None

def get_channel_id():
    result = app.client.conversations_list()
    for channel in result["channels"]:
        if channel["name"] == CHANNEL_NAME:
            return channel["id"]
    return None

def post_monday_prompt():
    global monday_thread_ts
    channel_id = get_channel_id()
    if channel_id:
        result = app.client.chat_postMessage(
            channel=channel_id,
            text="🧭 *Monday Compass Check* — Copy paste your focus for this week in this thread 👇"
        )
        monday_thread_ts = result["ts"]
        logging.info(f"Monday prompt posted, ts: {monday_thread_ts}")

def post_daily_standup():
    channel_id = get_channel_id()
    if channel_id:
        app.client.chat_postMessage(
            channel=channel_id,
            text="☀️ *Daily Standup* — Write your focus for today in this thread 👇"
        )

def post_friday_reflection():
    global monday_thread_ts
    channel_id = get_channel_id()
    if not channel_id or not monday_thread_ts:
        logging.warning("Missing channel or monday thread ts")
        return

    replies = app.client.conversations_replies(
        channel=channel_id,
        ts=monday_thread_ts
    )

    messages = replies["messages"][1:]  # skip the bot's own prompt

    for msg in messages:
        user_id = msg["user"]
        user_text = msg["text"]
        app.client.chat_postMessage(
            channel=channel_id,
            text=(
                f"👋 <@{user_id}> — here's what you set out to do this week:\n\n"
                f"_{user_text}_\n\n"
                f"How did it go? Please share:\n"
                f"✅ What did you accomplish?\n"
                f"🔄 What's still open?\n"
                f"❌ What blocked you — and what's the solution?"
            )
        )

scheduler = BackgroundScheduler()

# Monday 9am
scheduler.add_job(post_monday_prompt, 'cron', day_of_week='mon', hour=9, minute=0)

# Tuesday to Friday 9am
scheduler.add_job(post_daily_standup, 'cron', day_of_week='tue,wed,thu,fri', hour=9, minute=0)

# Friday 3pm
scheduler.add_job(post_friday_reflection, 'cron', day_of_week='fri', hour=15, minute=0)

scheduler.start()

if __name__ == "__main__":
    logging.info("Bot is running...")
    app.start(port=int(os.environ.get("PORT", 3000)))

