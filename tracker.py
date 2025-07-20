import os
import requests
import streamlit as st
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
from slack_sdk import WebClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load .env locally
load_dotenv()

# Load secrets (Streamlit Cloud or fallback to local)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
SLACK_BOT_TOKEN = st.secrets.get("SLACK_BOT_TOKEN", os.getenv("SLACK_BOT_TOKEN"))
SLACK_CHANNEL = st.secrets.get("SLACK_CHANNEL", os.getenv("SLACK_CHANNEL"))

SENDGRID_API_KEY = st.secrets.get("SENDGRID_API_KEY", os.getenv("SENDGRID_API_KEY"))
EMAIL_USER = st.secrets.get("EMAIL_USER", os.getenv("EMAIL_USER"))
EMAIL_TO = st.secrets.get("EMAIL_TO", os.getenv("EMAIL_TO"))

# Configure Gemini & Slack
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel("gemini-1.5-pro")
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# URLs to track
urls = [
    "https://www.oneplus.com/support/softwareupgrade",
    "https://miuirom.xiaomi.com/rom/u11.html",
    "https://learn.microsoft.com/en-us/windows/whats-new/",
    "https://developer.apple.com/news/releases/",
    "https://source.android.com/docs/setup/start/release-notes",
    "https://www.samsung.com/global/galaxy/what-is/one-ui/",
    "https://slack.com/release-notes",
    "https://www.notion.so/changelog"
]

# Fetch page
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

# Summarize with Gemini
def summarize(text):
    try:
        res = model.generate_content(
            f"Summarize the following. Highlight **NEW FEATURES** and **PRICING CHANGES**:\n\n{text}"
        )
        return res.text
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None

# Send to Slack
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

# Send email via SendGrid
def send_email_report(subject, body):
    message = Mail(
        from_email=EMAIL_USER,
        to_emails=EMAIL_TO,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent! Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ SendGrid error: {e}")

# Run tracker
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
        send_email_report("🚀 Competitor Tracker Report", final_summary)
        return final_summary + "\n\n📧 Email sent!"
    else:
        return "⚠️ No summaries available!"

# Run directly
if __name__ == "__main__":
    result = run_tracker()
    print("\n=== Final Report ===")
    print(result)
