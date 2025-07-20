# app.py

import streamlit as st
from tracker import run_tracker

st.set_page_config(page_title="Competitor Feature Tracker", page_icon="🚀")
st.title("🚀 Competitor Feature Tracker")
st.write("Click to scrape, summarize, store, Slack & email!")

if st.button("🔍 Run Tracker Now"):
    result = run_tracker()
    st.subheader("📄 Result")
    st.markdown(result)
else:
    st.info("👆 Click the button above to run manually.")
