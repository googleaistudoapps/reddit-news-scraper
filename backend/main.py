from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import subprocess

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLEANED_POSTS_PATH = ".tmp/cleaned_posts.json"
CONFIG_PATH = "config.json"

@app.get("/signals")
async def get_signals():
    if not os.path.exists(CLEANED_POSTS_PATH):
        return []
    with open(CLEANED_POSTS_PATH, "r") as f:
        return json.load(f)

@app.get("/config")
async def get_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {"subreddits": ["FlutterDev", "SideProject", "SaaS", "ArtificialInteligence", "OpenAI"]}

@app.post("/config")
async def update_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    return {"status": "success"}

@app.post("/run-scan")
async def run_scan():
    try:
        # Run collector
        subprocess.run(["./.venv/bin/python3", "execution/rss_collector.py"], check=True)
        # Run cleaner
        subprocess.run(["./.venv/bin/python3", "execution/data_cleaner.py"], check=True)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
