# Job Search Preferences

> Used by `/find-jobs` to score openings and by the `job-hunter` agent to decide
> which companies to target for reverse-recruiting outreach.

## Target roles

<!-- List titles in priority order. Be specific: "Senior Travel Operations Manager", not "manager". -->

1. TODO
2. TODO
3. TODO

## Seniority

- TODO (e.g. mid, senior, lead, head-of)

## Industries

- **Preferred:** TODO
- **Acceptable:** TODO
- **Avoid:** TODO

## Location & work style

- **Remote:** TODO (remote-only / hybrid ok / on-site ok)
- **Acceptable locations:** TODO
- **Time zones (if remote):** TODO

## Company profile

- **Size:** TODO (startup / scale-up / enterprise / any)
- **Dealbreakers:** TODO (e.g. "no gambling companies", "no 6-day work weeks")

## Scoring rubric (used by /find-jobs)

Score each opening 0–10:

| Signal | Weight |
|---|---|
| Title matches a target role | 3 |
| Location/remote policy fits | 2 |
| Salary at or above target (when listed) | 2 |
| Industry preferred | 1 |
| Seniority fits | 1 |
| No dealbreakers present | 1 (auto-0 overall if a dealbreaker is hit) |

Only openings scoring **7+** go into the tracker as `sourced`; 5–6 are listed as
"borderline — your call"; below 5 are dropped silently.

## Search sources

Prefer, in order: company careers pages, LinkedIn Jobs, Indeed, Glassdoor,
Wellfound (startups), Otta, and niche boards relevant to the target industry.
Always verify a posting is still live before adding it to the tracker.
