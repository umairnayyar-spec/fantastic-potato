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
2. **Read `career/search-playbook.md`** — it holds the accumulated learnings
   about which search techniques work. Use its "Winning techniques" as your
   default approach and try its "To try next round" hypotheses.
3. Read `career/applications/tracker.md` so you never re-add a company/role
   pair that's already tracked.
4. Search — **ATS-domain-scoped queries first** (the playbook's #1 lever):
   pass `allowed_domains` of ATS hosts (greenhouse/lever/ashby/workable/etc.)
   so results are direct applyable postings, not aggregator pages. Run one
   query per (title-cluster × market). Fall back to broad + local-board
   queries only for GCC/Pakistan-local roles that ATS scoping misses.
5. For each opening: if WebFetch is available, open it to confirm live and
   read the JD; if WebFetch is blocked (cloud sourcing session), treat a
   direct ATS link as high-confidence and mark the row "verify on apply."
   Score 0–10 using the rubric in preferences.md, noting the evidence. For
   remote roles, flag whether Pakistan-based candidates are eligible (many US
   "remote" roles are US-only — see playbook caveat 1).
6. Update `career/applications/tracker.md`:
   - Add each opening scoring 7+ as a new row with status `sourced`,
     today's date, and the direct posting URL when available.
   - Append a dated line to the Activity log.
7. **Update `career/search-playbook.md`**: append a "Round log" entry (what
   you tried, what worked, what didn't) and promote any new winning technique
   to the top section. This is what makes each round better than the last.
8. Report back: a short table of what was added, the borderline scorers, and
   one line on what you improved this round.

## Rules

- Never add duplicate rows. Match on company + role title.
- Only include postings you actually verified are live — no stale aggregator
  links.
- If the user gives extra context in the command (e.g. `/find-jobs fintech
  only`), apply it on top of preferences.md for this run.
