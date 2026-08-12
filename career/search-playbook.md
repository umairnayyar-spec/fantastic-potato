# Search Playbook — what works, refined each round

> `/find-jobs` reads this before searching and appends a "Round log" entry
> after. The goal: every round is sharper than the last. Newest learnings on top.

## Winning techniques (use these first)

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
2. **WebFetch is blocked in the cloud sourcing session** → can't open a
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

- Add `jobs.workable.com` + SmartRecruiters scoping — likely surfaces more
  GCC scale-ups.
- For Pakistan-local: try `rozee.pk` and `mustakbil.com` domain-scoped (the
  main PK ATS/boards) — WebSearch under-indexes these.
- For Sweden: scope to `careers.<company>.com` for the named targets
  (Microsoft, GlobalConnect, Dustin) rather than generic Sweden queries.
- Try scoping to `linkedin.com/jobs/view` for individual LinkedIn postings.

## Round log

- **Round 5 — 2026-07-17 (test run of token-optimized skill, 2 searches, GCC +
  Sweden).** Confirms Round 4's yield problem from a different angle: Sweden
  generic query ("Sweden OR Stockholm") returned 0 genuinely Sweden-based
  roles — WebSearch keyword-matches the country name but surfaces
  Europe-broad/Barcelona/US postings that mention international scope. Do
  not run generic Sweden queries again; go straight to the "to try" hypothesis
  of scoping `careers.<company>.com` for named targets. GCC query mostly
  returned roles already in tracker or mislocated (surfaced on a Dubai query
  but actually Barcelona/unconfirmed). The two new-looking hits (Trendyol
  HRBP Dubai, Trendyol HRBP Gulf/Riyadh) were NOT queued — caveat 3 already
  flags Trendyol Gulf roles as nationality-restricted from Round 3; not worth
  re-discovering the same dealbreaker. **0 rows added this round — correct
  behavior, not a failed run:** the alternative was padding the tracker with
  roles that would die on contact. 2-search budget was enough to reach this
  conclusion; did not need the 3rd call.
- **Round 4 — 2026-07-17.** Reality-check on Round 3's 8 ATS-scoped links:
  actually opened all 8 at apply time. Result: Teramind (dead/404), UpGuard
  (dead/404), Flow (Saudi-citizenship-only, auto-0), Netomi (US/Canada
  sponsorship required, auto-0 for Umair), Clifford Chance (dead/404). Only
  Celonis, Cohere, Lumos, Remote.com, Manychat survived to "worth attempting."
  **~50% of ATS-scoped links were dead or hit a hidden dealbreaker within a
  day.** Lesson banked: "direct ATS link" is necessary but not sufficient —
  always treat cloud-sourced rows as unverified until someone opens them with
  a real browser; don't celebrate a sourcing round on link-count alone. Also
  ran broader searches (LinkedIn jobs, named tech companies, Pakistan/UAE
  boards) — most Pakistan/UAE results were aggregator category pages with no
  nameable posting; LinkedIn direct-view links skewed US/UK on-site roles
  needing relocation. Added Epoch AI (9, applied same day) and RemotePass (7,
  later found dead) from that batch — real yield was 1 applied role from
  ~20 links surfaced across the day. Token cost was high for the yield:
  4-market full sweeps with one query per title-cluster burned a lot of
  budget on searches that returned duplicate/aggregator noise. Going forward:
  cap 3 WebSearch calls/run, rotate 2 markets per round instead of sweeping
  all 4, and auto-queue survivors straight into APPLY-CHECKLIST.md so a
  sourcing round produces something immediately actionable, not just tracker
  rows that need a second pass to become applications.
- **Round 3 — 2026-07-16.** Switched to ATS-domain-scoped search. Huge
  quality jump: ~15 direct-link roles vs prior rounds' board pages. Added
  best 8 to tracker (rows 8–15). Lesson banked: ATS scoping is now the
  default first move.
- **Round 2 — 2026-07-16.** Pakistan-weighted broad search. Named leads:
  Director of People & Culture (Islamabad), Reckitt HRBP. Sweden = target
  companies only. Board-page noise high — motivated the Round 3 change.
- **Round 1 — 2026-07-16.** Broad market search, no domain scoping. Mostly
  aggregator pages; 4 fuzzy leads. Established the problem.
