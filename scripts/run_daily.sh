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