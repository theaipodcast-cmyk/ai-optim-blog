---
description: Orchestrates the full AI Optimism blog pipeline. Checks init state then runs scraper, writer, and publisher as subagents in sequence.
allowed-tools: Bash, Read, Write
---

# AI Optimism Blog — Daily Pipeline

Run each phase using the designated subagent. Do not do the work yourself.
Stop the entire pipeline and report the exact error if any agent returns a FAILED status.

## Phase 1: Init check
Read init.md.
If ANY item is marked [ ]: spawn the **initializer** subagent and wait for INIT_OK before continuing.
If ALL items are marked [x]: skip to Phase 2.

## Phase 2: Scrape
Spawn the **scraper** subagent.
Wait for SCRAPE_OK. If SCRAPE_FAILED: stop, report error, do not continue.

## Phase 3: Write
Spawn the **writer** subagent.
Wait for WRITE_OK. If WRITE_FAILED: stop, report error, do not continue.

## Phase 4: Publish
Spawn the **publisher** subagent.
Wait for PUBLISH_OK. If PUBLISH_FAILED: stop, report error, do not continue.

## Final report
Print:
- "Pipeline complete."
- The live post URL (from publisher output)
- Output of: git log --oneline -1

$ARGUMENTS