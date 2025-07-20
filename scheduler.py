# scheduler.py

import schedule
import time
from tracker import run_tracker

def job():
    print("⏰ Running scheduled tracker...")
    result = run_tracker()
    print(result)

schedule.every().friday.at("10:00").do(job)

print("✅ Scheduler started. Waiting for Friday 10 AM...")

while True:
    schedule.run_pending()
    time.sleep(60)
