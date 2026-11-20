# Search Playbook — what works, refined each round

> `/find-jobs` reads this before searching and appends a "Round log" entry
> after. The goal: every round is sharper than the last. Newest learnings on top.

## Winning techniques (use these first)

0. **List job boards directly instead of searching (Round 4, 2026-11-20).**
   Web-search snippets go stale: 5 of 8 ATS links from search were 404 or
   replaced. Firecrawl's Alexandria providers read an employer's ATS board
   live: `ashbyhq-com jobs/jobs` (board slug + `keyword` title filter — works
   well), `lever-co jobs/postings`, `greenhouse-io jobs/search` (its keyword
   matches full text, so results are noisy — filter titles yourself),
   `smartrecruiters-com jobs/search_jobs` (cross-company; quote the title).
   Every row it returns is live today. Use search only to discover WHICH
   companies to list, then list their boards. Verify one posting with
   `firecrawl_scrape` + a `query` prompt for location/eligibility.

1. **Target ATS platforms directly — this is the #1 lever.** Constrain the
   search to the systems companies actually post through, using
   `allowed_domains`. This returns direct, applyable posting URLs instead of
   aggregator landing pages (Bayt/Indeed/Glassdoor category pages, which are
   near-useless — they can't be applied to and can't be verified).
   Primary ATS domains:
   `boards.greenhouse.io`, `job-boards.greenhouse.io`, `jobs.lever.co`,
   `jobs.ashbyhq.com`, `jobs.workable.com`, `apply.workable.com`,
   `<company>.bamboohr.com`, `jobs.smartrecruiters.com`.
   Proven in Round 3 (2026-07-16): a single ATS-scoped query surfaced Flow,
   Celonis, Cohere, UpGuard, Netomi, Lumos, Teramind — all with direct apply
   links. The same titles without domain scoping returned only board pages.

2. **Keep queries short + OR the titles.** `"Head of People" OR "HR Director"
   Dubai 2026` beats long keyword stacks. WebSearch is US-indexed, so global
   remote/tech roles surface well; GCC/Pakistan-local roles need the local
   boards or company career pages (see caveat 2).

3. **One query per (title-cluster × market).** Title clusters that work for
   Umair: `"Head of People" OR "Head of HR" OR "HR Director"`;
   `"Senior HR Business Partner" OR "People Partner" OR "People Business
   Partner"`; `"Head of People Operations" OR "HR Operations"`;
   `"Head of Organizational Development" OR "OD"`.

## Caveats / failure modes learned

1. **"Remote" ≠ open to Pakistan.** Most US startup "remote" roles mean
   US-work-authorization-only. For every remote role, the verify step must
   check: does it accept candidates working from Pakistan (via EOR/contract),
   or is it geo-restricted? Flag remote rows `remote — check geo eligibility`.
2. **If WebFetch is blocked** (it was in the cloud sourcing sessions) → can't open a
   posting to confirm live or read full JD. ATS URLs from search are high-
   confidence (they're live listings), but final live-check + JD read happens
   in the apply session (Cowork / unrestricted). Mark cloud-sourced rows
   `sourced (ATS link, verify on apply)`.
3. **Exclusion filters matter.** Some GCC roles are "Saudi/Emirati Nationals
   Only" (e.g. Trendyol Gulf mobility role) — an automatic 0 for Umair. Read
   the snippet for nationality restrictions before scoring.
4. **Aggregator category pages = do not log.** Bayt/Indeed/Glassdoor "N jobs
   in X" links are not postings. Only log a row when there's a nameable
   company + role.

## To try next round (hypotheses)

- AI focus: frontier labs (OpenAI, Anthropic, Scale, xAI, Glean) hire HR
  US-on-site; Mistral/Photoroom need French law. Better AI targets for Umair:
  remote-first AI/tech firms ("hire anywhere"), GCC AI groups (G42 family:
  Inception42, Core42, Presight, Space42, M42; HUMAIN; MBZUAI) — these use
  their own career sites/Workday, so try `myworkdayjobs-com search_jobs`
  with their career-site URL, and Pakistan AI-native firms (10Pearls,
  Arbisoft, CureMD, Tkxel) via their own career pages.

- For Pakistan-local: try `rozee.pk` and `mustakbil.com` domain-scoped (the
  main PK ATS/boards) — WebSearch under-indexes these.
- For Sweden: scope to `careers.<company>.com` for the named targets
  (Microsoft, GlobalConnect, Dustin) rather than generic Sweden queries.
- Try scoping to `linkedin.com/jobs/view` for individual LinkedIn postings.

## Round log

- **Round 4 — 2026-11-20 (AI companies).** Search snippets mostly dead
  (Epoch AI, Legora, Deepgram, Zapier all 404). Switched to listing ~21 AI
  employers' ATS boards via Firecrawl — fast, all-live data. But HR roles at
  AI labs are US/Paris-bound. Added 1 (VRChat Head of People, remote
  anywhere). Borderline: Mistral Head of HRBP, Sonar Sr HRBP. Lesson: for a
  Pakistan base, filter on location eligibility BEFORE industry.

- **Round 3 — 2026-07-16.** Switched to ATS-domain-scoped search. Huge
  quality jump: ~15 direct-link roles vs prior rounds' board pages. Added
  best 8 to tracker (rows 8–15). Lesson banked: ATS scoping is now the
  default first move.
- **Round 2 — 2026-07-16.** Pakistan-weighted broad search. Named leads:
  Director of People & Culture (Islamabad), Reckitt HRBP. Sweden = target
  companies only. Board-page noise high — motivated the Round 3 change.
- **Round 1 — 2026-07-16.** Broad market search, no domain scoping. Mostly
  aggregator pages; 4 fuzzy leads. Established the problem.
