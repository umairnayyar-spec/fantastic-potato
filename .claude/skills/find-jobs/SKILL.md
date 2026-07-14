---
name: find-jobs
description: Search the web for job openings matching career/profile/preferences.md, score them against the rubric, and add qualifying roles to the application tracker. Use when the user asks to find jobs, source roles, or look for openings.
---

# Find Jobs

Source new job openings that match the candidate's preferences.

## Steps

1. Read `career/profile/preferences.md` and `career/profile/profile.md`. If
   either still contains unfilled `TODO`s that block searching (no target
   roles, no location), stop and ask the user to fill them in first.
2. Read `career/applications/tracker.md` so you never re-add a company/role
   pair that's already tracked.
3. Use WebSearch (and WebFetch to open promising results) to find live
   openings. Search each target role title combined with the location/remote
   preference across the sources listed in preferences.md. Run multiple
   searches — one per target role at minimum.
4. For each opening found, verify it is still live by fetching the posting,
   then score it 0–10 using the rubric in preferences.md. Note the actual
   evidence for the score (salary listed? remote policy stated?).
5. Update `career/applications/tracker.md`:
   - Add each opening scoring 7+ as a new row with status `sourced`,
     today's date in "Last action", and "tailor resume + apply" as next action.
   - Append a dated line to the Activity log summarizing the run.
6. Report back: a short table of what was added (company, role, score, why),
   the borderline 5–6 scorers for the user to judge, and nothing else.

## Rules

- Never add duplicate rows. Match on company + role title.
- Only include postings you actually verified are live — no stale aggregator
  links.
- If the user gives extra context in the command (e.g. `/find-jobs fintech
  only`), apply it on top of preferences.md for this run.
