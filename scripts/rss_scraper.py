#!/usr/bin/env python3
import feedparser
import requests
import json
import os
import sys
import re

# Feeds to fetch
FEEDS = [
    "http://arxiv.org/rss/cs.AI",
    "https://hnrss.org/newest?q=AI+machine+learning&count=30",
    "https://www.technologyreview.com/feed/"
]

# Keywords to filter by
KEYWORDS = ['AI', 'machine learning', 'LLM', 'neural', 'artificial intelligence', 'model']

HISTORY_FILE = "history.json"
STAGING_FILE = "staging_context.txt"

def load_history():
    """Load history from JSON file, return default if missing or malformed."""
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            return {"seen": data.get("seen", []), "max": data.get("max", 500)}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"seen": [], "max": 500}

def save_history(history):
    """Save history to JSON file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def filter_article(title, summary):
    """Check if article contains any keyword."""
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in KEYWORDS)

def clean_html(text):
    """Strip HTML tags from text."""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    # Remove extra whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def fetch_full_text(url):
    """Fetch full page text, strip HTML, truncate to 3000 chars."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        text = clean_html(response.text)
        return text[:3000]
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""

def main():
    history = load_history()
    seen = set(history["seen"])
    collected = []

    # Fetch and filter from each feed
    for feed_url in FEEDS:
        try:
            print(f"Fetching: {feed_url}")
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")

                # Check if already seen
                if link in seen:
                    continue

                # Check if it matches our keywords
                if filter_article(title, summary):
                    # Fetch full text
                    full_text = fetch_full_text(link)
                    collected.append({
                        "title": title,
                        "url": link,
                        "body": full_text
                    })
                    seen.add(link)
                    print(f"Collected: {title}")

                    if len(collected) >= 3:
                        break
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}", file=sys.stderr)
            # Continue with other feeds

        if len(collected) >= 3:
            break

    # Check if we have enough articles
    if len(collected) < 3:
        print(f"Error: Only found {len(collected)} articles, need 3", file=sys.stderr)
        sys.exit(1)

    # Write staging context
    with open(STAGING_FILE, 'w') as f:
        for article in collected:
            f.write(f"TITLE: {article['title']}\n")
            f.write(f"URL: {article['url']}\n")
            f.write(f"BODY: {article['body']}\n")
            f.write("---\n")

    # Update and save history
    history["seen"] = list(seen)
    # Trim to max entries
    if len(history["seen"]) > history["max"]:
        history["seen"] = history["seen"][-history["max"]:]
    save_history(history)

    print(f"Successfully collected {len(collected)} articles")

if __name__ == "__main__":
    main()