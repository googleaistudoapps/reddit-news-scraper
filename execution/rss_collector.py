import requests
import json
import os
import time
from datetime import datetime, timezone

def collect_reddit_json():
    # Load subreddits from config.json or use defaults
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            subreddits = config.get("subreddits", ["FlutterDev", "SideProject", "SaaS", "ArtificialInteligence", "OpenAI"])
    else:
        # Fallback to env or defaults
        subreddits = os.getenv("SUBREDDITS", "FlutterDev,SideProject,SaaS,ArtificialInteligence,OpenAI").split(",")

    all_posts = []
    headers = {'User-Agent': 'Mozilla/5.0 (ReditnewsScraper/1.1)'}

    for sub in subreddits:
        sub = sub.strip()
        if not sub: continue
        
        # Using .json endpoint for richer data (includes comment counts)
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=50"
        print(f"Fetching JSON for r/{sub}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                for post in posts:
                    item = post.get("data", {})
                    all_posts.append({
                        "title": item.get("title"),
                        "link": f"https://www.reddit.com{item.get('permalink')}",
                        "updated": datetime.fromtimestamp(item.get("created_utc"), tz=timezone.utc).isoformat(),
                        "summary": item.get("selftext") or item.get("title"),
                        "subreddit": sub,
                        "author": item.get("author", "unknown"),
                        "num_comments": item.get("num_comments", 0),
                        "ups": item.get("ups", 0)
                    })
            else:
                print(f"Failed to fetch r/{sub}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error fetching r/{sub}: {e}")
        
        # Rate limiting courtesy
        time.sleep(1)

    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/raw_rss_feeds.json", "w") as f:
        json.dump(all_posts, f, indent=4)
    print(f"Collected {len(all_posts)} posts to .tmp/raw_rss_feeds.json")

if __name__ == "__main__":
    collect_reddit_json()
