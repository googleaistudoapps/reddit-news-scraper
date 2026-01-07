import schedule
import time
import subprocess
import os
import json
from datetime import datetime

def job():
    print(f"[{datetime.now()}] Starting scheduled Popular Reddit Signal Scan...")
    try:
        # Load subreddits to log what we're scanning
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                subreddits = config.get("subreddits", [])
                print(f"Monitoring: {', '.join(subreddits)}")

        # 1. Collect (Now uses JSON API and config.json)
        subprocess.run(["./.venv/bin/python3", "execution/rss_collector.py"], check=True)
        
        # 2. Clean (Now enforces 30+ comments)
        subprocess.run(["./.venv/bin/python3", "execution/data_cleaner.py"], check=True)
        
        # 3. Generate Report (Synthesize signals into TXT)
        CLEANED_PATH = ".tmp/cleaned_posts.json"
        if os.path.exists(CLEANED_PATH):
            with open(CLEANED_PATH, "r") as f:
                posts = json.load(f)
            
            if posts:
                report_content = "# Daily Popular Reddit Signals (30+ Comments)\n\n"
                for p in posts:
                    report_content += f"## {p['title']}\n"
                    report_content += f"- Subreddit: r/{p['subreddit']}\n"
                    report_content += f"- Comments: {p['num_comments']}\n"
                    report_content += f"- Link: {p['link']}\n\n"
                
                with open("reddit_news_report.txt", "w") as f:
                    f.write(report_content)
                
                # 4. Notify via Gmail
                subprocess.run(["./.venv/bin/python3", "execution/gmail_notifier.py"], check=True)
                print("Scheduled digest sent successfully.")
            else:
                print("No popular posts (30+ comments) found today. No email sent.")
        
    except Exception as e:
        print(f"Error during scheduled job: {e}")

# Schedule for 08:00 AM
schedule.every().day.at("08:00").do(job)

# For testing purposes, you can uncomment this to run the job immediately
# job()

print("SignalAgent Scheduler (Popular Only) started. Waiting for 08:00 AM...")
while True:
    schedule.run_pending()
    time.sleep(60)
