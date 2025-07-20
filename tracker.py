# tracker.py

import os
import requests
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
from slack_sdk import WebClient

# Load env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

configure(api_key=GEMINI_API_KEY)
model = GenerativeModel("gemini-1.5-pro")
slack_client = WebClient(token=SLACK_BOT_TOKEN)

urls = [
    
    "https://www.oneplus.com/support/softwareupgrade",
    "https://miuirom.xiaomi.com/rom/u11.html",  # Official MIUI page
    "https://learn.microsoft.com/en-us/windows/whats-new/",
    "https://developer.apple.com/news/releases/",
    "https://source.android.com/docs/setup/start/release-notes",
    "https://www.samsung.com/global/galaxy/what-is/one-ui/",
    "https://slack.com/release-notes",
    "https://www.notion.so/changelog"
]



def fetch_page(url):
    print(f"🔍 Fetching: {url}")
    try:
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            print(f"📄 Page size: {len(res.text)} chars")
            return res.text
        else:
            print(f"❌ Failed with status {res.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None


def summarize(text):
    try:
        res = model.generate_content(
            f"Summarize the following. Highlight **NEW FEATURES** and **PRICING CHANGES**:\n\n{text}"
        )
        return res.text
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None


def send_to_slack(summary):
    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=(
                ":rocket: *Weekly Competitor Feature Tracker*\n\n"
                f"{summary}\n\n"
                ":chart_with_upwards_trend: _Stay ahead of the competition!_"
            ),
        )
        print("✅ Posted to Slack:", response)
    except Exception as e:
        print(f"❌ Slack error: {e}")


def run_tracker():
    report = []
    for url in urls:
        html = fetch_page(url)
        if html:
            summary = summarize(html)
            if summary:
                report.append(f"✅ *{url}*\n{summary}\n")

    final_summary = "\n\n".join(report)
    if final_summary:
        send_to_slack(final_summary)
        return final_summary
    else:
        return "⚠️ No summaries available!"


if __name__ == "__main__":
    result = run_tracker()
    print("\n=== Final Report ===")
    print(result)
