# Project Initialization State
`[ ]` = must be created. Mark `[x]` immediately upon completion.

## 1. Directory Structure
- [ ] Create _posts/ directory
- [ ] Create scripts/ directory
- [ ] Create logs/ directory
- [ ] Create .gitignore
- [ ] Create Gemfile
- [ ] Create _config.yml
- [ ] Create index.md

## 2. Core Scripts
- [ ] Run pip install feedparser requests
- [ ] Write scripts/rss_scraper.py
- [ ] Write scripts/run_daily.sh and chmod +x it
- [ ] Create history.json as {"seen": [], "max": 500}

## 3. Credentials & Git Setup
- [ ] Prompt user for GitHub username, PAT, repo URL, git user.name, git user.email
- [ ] Save credentials to .env
- [ ] Configure git user.name and user.email
- [ ] Run git init (with -b main flag or fallback)
- [ ] Set remote with PAT embedded in URL
- [ ] Make initial commit and push to main
- [ ] Notify user to enable GitHub Pages in repo settings