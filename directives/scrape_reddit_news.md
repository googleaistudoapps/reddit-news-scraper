# Directive: Scrape Reddit News

## Goal
Scrape the latest news articles from specified subreddits (e.g., r/news, r/worldnews) to keep track of current events.

## Inputs
- `SUBREDDITS`: List of subreddits to scrape (e.g., "news,worldnews")
- `LIMIT`: Number of posts to fetch per subreddit.

## Execution Tools
- `execution/scrape_reddit.py`: The Python script that performs the scraping.

## Steps
1. Determine the target subreddits and limit.
2. Run `execution/scrape_reddit.py` with the inputs as environment variables or arguments.
3. Save the results to `.tmp/reddit_news_raw.json`.

## Expected Output
- A JSON file in `.tmp/` containing the titles, URLs, and summaries of the top posts.
