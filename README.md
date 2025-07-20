# 🚀 Competitor Feature Tracker

This project tracks competitor changelogs & release notes, summarizes them using Gemini AI, and posts updates to Slack.  
It also provides a Streamlit dashboard for on-demand fetching and summaries.

---

## 📂 Project Structure

competitor-feature-tracker/
├── app.py          # Streamlit dashboard
├── tracker.py      # Automated fetch & Slack post
├── .env            # API keys & Slack token (DO NOT COMMIT)
├── requirements.txt
├── README.md
└── venv/           # Python virtual environment

---

## ✅ Features

- Scrapes competitor websites for release notes.
- Uses Google Gemini Pro to summarize updates.
- Posts summaries to a Slack channel automatically.
- Offers an interactive Streamlit dashboard.

---

## ⚙️ How to Run

### 1️⃣ Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

 Run the tracker: python tracker.py
Run the Streamlit dashboard : streamlit run app.py
