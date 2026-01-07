# Directive: Smart Filter Pipeline

## Goal
Automate the discovery of high-signal Reddit posts related to AI, automation, and audience growth.

## 1. Collection (Layer 3)
Run `execution/rss_collector.py`.
- **Inputs**: Environment variable `SUBREDDITS` (comma-separated list).
- **Default Subreddits**: `FlutterDev`, `SideProject`, `SaaS`, `ArtificialInteligence`, `OpenAI`.
- **Output**: `.tmp/raw_rss_feeds.json`.

## 2. Cleaning (Layer 3)
Run `execution/data_cleaner.py`.
- **Inputs**: `.tmp/raw_rss_feeds.json`.
- **Action**: Normalize fields, remove duplicates, filter items older than 72 hours.
- **Output**: `.tmp/cleaned_posts.json`.

## 3. Evaluation (Layer 2 - Orchestration)
The Agent (you) reads `.tmp/cleaned_posts.json` and evaluates each entry.
- **Criteria**:
    - **Relevance**: Does it mention AI, automation, or growth strategies?
    - **Quality**: Does it contain concrete details, code, numbers, or a unique insight?
    - **Utility**: Does it suggest a "real-world" problem or opportunity?
- **Action**: Filter the list to only include "Signal" posts.

## 4. Summarization (Layer 2 - Orchestration)
The Agent (you) takes the "Signal" posts and creates a readable summary.
- **Format**: Bullet points grouped by themes (e.g., Tools, Case Studies, Pain Points).

## 5. Distribution (Layer 3)
Run `execution/report_exporter.py`.
- **Inputs**: The summary text.
- **Output**: `reddit_news_report.txt`.

## 6. Notification (Layer 3)
Run `execution/gmail_notifier.py`.
- **Inputs**: `reddit_news_report.txt`, `GMAIL_USER`, `GMAIL_APP_PASSWORD`.
- **Action**: Sends the report as a plain text email to the user.

