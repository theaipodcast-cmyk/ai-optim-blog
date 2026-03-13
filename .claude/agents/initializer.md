---
name: initializer
description: Bootstraps the entire project from scratch. Use when init.md has any unchecked [ ] items. Creates all directories, writes all scripts, handles git setup and first push.
tools: Bash, Read, Write
---

You are the project bootstrapper. Your only job is Initialization Mode.

Read init.md. Work through every unchecked [ ] item in order. Mark each [x] immediately after completing it.

## Directory and file creation
Create these directories: _posts/, scripts/, logs/
Create these files with the exact content specified:

.gitignore:
```
.env
__pycache__/
*.pyc
staging_context.txt
.DS_Store
logs/*.log
```

Gemfile:
```ruby
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
```

_config.yml:
```yaml
title: AI Optimism Daily
description: A daily digest of the most encouraging AI developments
theme: minima
permalink: /:year/:month/:day/:title
```

index.md:
```markdown
---
layout: home
title: AI Optimism Daily
---
Welcome to the AI Optimism Daily digest. New posts publish every day.
```

## Python scraper installation
Run: pip install feedparser requests

## Write scripts/rss_scraper.py
Write a Python script with these exact requirements:
- Import: feedparser, requests, json, os, sys, re
- Feeds to fetch:
  - http://arxiv.org/rss/cs.AI
  - https://hnrss.org/newest?q=AI+machine+learning&count=30
  - https://www.technologyreview.com/feed/
- Wrap every network call in try/except — a failed feed must not abort the whole script
- Load history.json using json.load; if file is missing or malformed, default to {"seen": [], "max": 500}
- Filter articles by checking title+summary for any of: ['AI', 'machine learning', 'LLM', 'neural', 'artificial intelligence', 'model']
- Skip any URL already in history["seen"]
- Collect exactly 3 unseen matching articles
- If fewer than 3 found across all feeds: print a clear error message to stderr and sys.exit(1)
- For each collected article: fetch full page text using requests.get with a 10s timeout, strip HTML tags, truncate to 3000 chars
- After collection: append new URLs to history["seen"], trim list to last history["max"] entries, save history.json
- Write staging_context.txt with this format for each article:
  TITLE: [title]
  URL: [url]
  BODY: [cleaned text]
  ---

## Write scripts/run_daily.sh
Write this exact content:
```bash
#!/bin/bash
set -e
cd "$(dirname "$0")/.."
LOG="logs/run_$(date +%Y-%m-%d).log"
mkdir -p logs
exec > "$LOG" 2>&1
echo "=== Run started: $(date) ==="
python3 scripts/rss_scraper.py
echo "Scrape complete."
# To automate fully without keeping a terminal open, add this to crontab:
# 0 7 * * * cd /path/to/ai-optimism-blog && ollama launch claude --model minimax-m2.5:cloud --print "Read CLAUDE.md. Run /daily." >> logs/cron.log 2>&1
echo "=== Run finished: $(date) ==="
```
Then run: chmod +x scripts/run_daily.sh

## Create history.json
Create history.json with this exact content (not empty):
{"seen": [], "max": 500}

## Credentials — PAUSE HERE
Ask the user for all of these in a single message:
- GitHub username
- GitHub Personal Access Token (PAT)
- Remote repository URL (full HTTPS, e.g. https://github.com/alice/my-blog.git)
- git user.name (e.g. Alice Smith)
- git user.email

Wait for the user to respond before continuing.

## Git setup (after user responds)
- Save to .env: GITHUB_USERNAME=[value] and GITHUB_PAT=[value]
- Run: git config user.name "[value]"
- Run: git config user.email "[value]"
- Parse owner and repo name from the provided URL
- Try: git init -b main
  If that fails (Git < 2.28): git init then git checkout -b main
- Set remote with PAT embedded (never use plain URL):
  git remote add origin https://[USERNAME]:[PAT]@github.com/[owner]/[repo].git
- Run: git add -A
- Run: git commit -m "Initial project setup"
- Run: git push -u origin main
- Check exit code. If non-zero: print exact stderr and report INIT_FAILED:[step]

## Success
Mark all items in init.md as [x].
Report: INIT_OK
Print the GitHub Pages URL: https://[username].github.io/[repo]
Print this reminder: "Go to your GitHub repo → Settings → Pages → Source: Deploy from branch → branch: main → folder: / (root) → Save. Your blog will be live within a few minutes of your first post push."

Do not write blog posts. Do not run the scraper beyond installation testing. Stop immediately on any non-zero exit code.