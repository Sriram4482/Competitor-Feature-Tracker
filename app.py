# app.py

import streamlit as st
from tracker import run_tracker

st.set_page_config(page_title="Competitor Feature Tracker", page_icon="🚀")
st.title("🚀 Competitor Feature Tracker")
st.write(
    "Click below to fetch competitor updates. It will scrape → summarize → send to Slack → and show here!"
)

if st.button("🔍 Run Tracker Now"):
    result = run_tracker()
    st.subheader("📄 Summary")
    st.markdown(result)
else:
    st.info("👆 Click the button above to run the tracker.")
