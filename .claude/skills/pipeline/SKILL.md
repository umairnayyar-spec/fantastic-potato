---
name: pipeline
description: Show the current job application pipeline status, flag overdue follow-ups, and update tracker rows (status changes, notes, interview dates). Use when the user asks about pipeline status, follow-ups, or wants to update an application's state.
---

# Pipeline

Manage `career/applications/tracker.md`.

## On `/pipeline` (no arguments)

1. Read the tracker.
2. Report:
   - A compact status summary (counts per status).
   - **Overdue follow-ups**: rows whose "Next action" date has passed —
     these come first, with a suggested action each (e.g. "applied 9 days
     ago, no response → draft a follow-up with /outreach").
   - Anything in `interviewing` or `offer` — the hot items.
   - Stale `sourced` rows older than 14 days — suggest applying or dropping.
3. If Gmail tools are available, offer to scan the inbox for replies from
   tracked companies (search by company domain) and update statuses from
   what's found — with the user's go-ahead.

## On `/pipeline <update>` (e.g. "/pipeline Acme moved to interviewing, call Tuesday")

1. Find the matching row, update status/next action/notes, append to the
   Activity log with today's date.
2. If a status moves to `offer`: congratulate, then offer to research
   comparable salary data for negotiation.
3. If `closed-lost`: record the reason if known — patterns across losses are
   fed back into preferences and resume tailoring.

## Rules

- The tracker is the single source of truth — never keep pipeline state
  anywhere else.
- Never email anyone from this skill; hand off to /outreach for any message
  drafting.
