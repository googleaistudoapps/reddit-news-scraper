import json
import os
import dateutil.parser
from datetime import datetime, timedelta, timezone

def clean_data(min_comments=30):
    input_path = ".tmp/raw_rss_feeds.json"
    if not os.path.exists(input_path):
        print("Error: raw_rss_feeds.json not found.")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    seen_links = set()
    cleaned = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=72)

    for entry in data:
        link = entry.get("link")
        if not link or link in seen_links:
            continue
        
        # 1. Popularity Filter (Default: 30+ comments)
        if entry.get("num_comments", 0) < min_comments:
            continue
            
        # 2. Age Filter (72 hours)
        try:
            updated_str = entry.get("updated")
            updated_dt = dateutil.parser.parse(updated_str)
            if updated_dt < cutoff:
                continue
        except Exception:
            pass

        seen_links.add(link)
        cleaned.append({
            "title": entry.get("title"),
            "link": entry.get("link"),
            "timestamp": entry.get("updated"),
            "subreddit": entry.get("subreddit"),
            "author": entry.get("author"),
            "content": entry.get("summary"),
            "num_comments": entry.get("num_comments"),
            "ups": entry.get("ups")
        })

    with open(".tmp/cleaned_posts.json", "w") as f:
        json.dump(cleaned, f, indent=4)
    print(f"Cleaned {len(cleaned)} posts with {min_comments}+ comments. Saved to .tmp/cleaned_posts.json")

if __name__ == "__main__":
    clean_data()
