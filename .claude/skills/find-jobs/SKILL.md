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
4. **Token budget: max 3 WebSearch calls per run.** Search —
   **ATS-domain-scoped queries first** (the playbook's #1 lever): pass
   `allowed_domains` of ATS hosts (greenhouse/lever/ashby/workable/etc.) so
   results are direct applyable postings, not aggregator pages.
   - **Rotate markets instead of covering all four every run.** Check the
     playbook's Round log for which markets the last 1–2 rounds covered and
     pick the 2 markets covered longest ago (or never) for this run. Do NOT
     run one query per every title-cluster × market combination — that's how
     token budget disappears. One well-OR'd query per market slot, 2 slots max.
   - When parsing results, extract only company / role / URL / one-line
     evidence per hit. Do not restate WebSearch's own prose summary or copy
     its "Sources" boilerplate into your reasoning — go straight to the table.
5. Treat a direct ATS/LinkedIn posting URL as sourced-but-unverified — mark
   it "sourced (verify on apply)". WebFetch is blocked in the cloud sourcing
   session, so live/dead status and geo-eligibility can only be confirmed at
   apply time (Cowork or the user's own browser). **Known failure rate: in
   practice roughly 40–50% of ATS-scoped links go dead or carry a hidden
   dealbreaker (nationality restriction, sponsorship-only) within days of
   being surfaced** — see playbook Round 4 note. Don't over-promise quality
   in the report; flag this plainly.
   Score 0–10 using the rubric in preferences.md, noting the evidence. For
   remote roles, flag whether Pakistan-based candidates are eligible (many US
   "remote" roles are US-only — see playbook caveat 1).
6. Update `career/applications/tracker.md`:
   - Add each opening scoring 7+ as a new row with status `sourced`,
     today's date, and the direct posting URL when available.
   - Append a dated line to the Activity log.
7. **Queue the same 7+ rows into `career/applications/APPLY-CHECKLIST.md`**
   in its existing format (one `## Application N: Company (Role) — SCORE X`
   block per role, URL + the standard field table from `profile.md`, resume
   path from `career/resumes/`). This is what lets Cowork/the user go
   straight to filling forms next session without a separate handoff step.
   If the file doesn't exist, create it with the header block first.
8. **Update `career/search-playbook.md`**: append a "Round log" entry (which
   2 markets you covered, what worked, what didn't — including dead-link/
   dealbreaker rate if known) and promote any new winning technique to the
   top section. This is what makes each round better than the last.
9. Report back — keep it to a table, nothing else: what was added (company,
   role, score), the borderline scorers, and one line on what you improved
   or learned this round.

## Rules

- Never add duplicate rows. Match on company + role title.
- Only include postings you actually verified are live — no stale aggregator
  links.
- If the user gives extra context in the command (e.g. `/find-jobs fintech
  only`), apply it on top of preferences.md for this run.
