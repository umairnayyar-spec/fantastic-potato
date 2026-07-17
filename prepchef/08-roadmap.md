# 08 — Implementation Roadmap

Six milestones. Each ends with something runnable and a kill/keep decision. Sequencing
logic: **content pipeline and eval harness come early** (they gate everything and have the
longest lead time), the daily-loop features (feedback, repair, recap) come *before* polish
because they're the retention hypothesis, and billing comes last.

Pacing note for a Pro-plan token budget: each milestone below is sized to roughly **one
week of agentic build sessions** — start M0 after the weekly reset, one milestone per
week, architecture/review in a single session up front, boilerplate delegated to cheaper
models where possible. Timeline assumes ~1 technical founder + AI pair; calendar estimates
are working-time, not elapsed-time guarantees.

---

## M0 — Foundations (≈ 1 week)

Repo scaffold: Next.js + TS + Tailwind + shadcn/ui + PWA baseline; Supabase project,
Auth (email + Google), full schema migration from doc 06 with RLS + `is_household_member`;
CI (typecheck, lint, unit tests, migration check); Sentry + PostHog wiring; design tokens
+ light/dark; deployed preview + prod pipeline.

**Exit:** sign up → empty authenticated app shell in prod. Schema deployed. CI green.

## M1 — Onboarding, targets & content pipeline (≈ 1–1.5 weeks)

- Onboarding flow (doc 05 Flow 1) through prep-style step; targets engine (Mifflin/TDEE/
  macros) as pure unit-tested functions; targets reveal + edit with safety bounds.
- **Content pipeline** (the long pole): ingredient dictionary (~250 canonical items,
  PK + US locale rows), validation/ingest scripts, nutrition computation,
  `recipe_locales` materialization, verification flags. Seed **50 recipes** end-to-end to
  prove the pipeline; corpus build to ~350 continues as a parallel content workstream
  through M4. *Founder decision due here: commission vs. license recipe content.*
- Breakfast templates (~10 per locale).

**Exit:** a new user onboards and sees real targets; 50 validated recipes queryable with
correct macros, locale scores, and allergen flags.

## M2 — Plan generation + eval harness (≈ 1.5 weeks) — riskiest milestone

- Planning pipeline v1 (doc 07 §2): SQL filter → TS scorer (macro fit, overlap, variety)
  → Sonnet structured selection → validator → greedy fallback → persist + logs.
- Plan UI: generation streaming, week view, day totals vs targets, prep session cards,
  meal sheet, recipe pages.
- **Eval harness in CI**: golden households, zero-violation gate, macro-fit gate.
- Plan flexibility: replace (3 alts), move day, lock, shuffle, regenerate-one.

**Exit (go/no-go):** founders + 5 friendly testers generate real weeks in both locales and
would genuinely cook them; eval suite green; p95 latency in budget. If plans aren't
credible here, stop and fix the corpus/scorer — nothing downstream matters.

## M3 — Groceries + prep schedule (≈ 1 week)

Grocery consolidation (units, scaling, staples subtraction, categories, locale names);
check-off with offline outbox + sync; manual items; print stylesheet; share link (edge
function); prep schedule derivation (task graph, time estimates, parallel hints) + Prep
Mode UI (step-through, wake-lock); storage/reheat surfaces on batches.

**Exit:** the paper test — shop a real week from the list without editing it, then cook a
real prep session from Prep Mode. Founders must actually do this in both locales' spirit
(one PK-style, one US-style week).

## M4 — The daily loop: Today, feedback, repair, assistant (≈ 1.5 weeks)

Today dashboard (meals, adherence strip, prep countdown, shopping chip); feedback buttons
+ `preference_signals` + generation actually consuming the profile; one-tap repair with
diff/confirm/undo; assistant command bar (Haiku intent → typed ops → diff) passing the
five acceptance utterances + variants; weekly recap (in-app + Resend email) + plan-day and
prep-day emails; tone pass (FR-31 guilt-free copy audit).

**Exit:** the full loop closes: a skipped prep session on Wednesday produces a sane,
confirmed reflow in ≤ 3 taps; week-2 plan visibly reflects week-1 feedback.

## M5 — Polish, billing, private beta (≈ 1 week)

Design polish pass (animation, empty/edge states, a11y AA audit); performance pass
(p95 budgets, PWA install prompts); Stripe (free tier limits, trial, portal, PK PPP price
decision); data export/delete; legal (privacy policy, nutrition disclaimer, ToS);
onboarding funnel instrumentation review; corpus at ~350 recipes verified.

**Exit:** **private beta — 30–50 households** (recruit ~half PK, half US to test the
localization thesis), 4-week cohort measurement against the doc 03 metrics.

## M6 — Beta learning loop (4 weeks elapsed, low build volume)

Weekly cohort readout (retention, prep completion, swap rates by locale, 👍 trend,
inference cost); fix the top friction each week; kill/keep decisions on shaky features
(recap engagement, assistant usage); pricing test. **Decision gate at week 4:** ≥ ~35%
week-4 planning retention → public launch prep; materially below → diagnose (corpus
quality vs. loop friction vs. wrong wedge) before building anything new.

---

## Post-v1 backlog (ordered, from docs 01–02 exclusions)

1. Optional weekly weigh-in → TDEE auto-tuning (v1.x)
2. Per-member household profiles (v1.x)
3. Favorites & "repeat last week, but…" (v1.x)
4. CMS for the content team; corpus → 600+ (v1.x)
5. Native apps + push (post-retention proof)
6. Real price data / delivery partnerships (v2)
7. Additional locale packs — choose by beta demand signals (v2)
8. Pantry photo/receipt capture (v2+)

## Standing risks

| Risk | Mitigation |
|---|---|
| Corpus quality/lead time (biggest) | Pipeline in M1, content parallel workstream, 50-recipe proof early |
| Plans not credible (M2 gate fails) | Greedy fallback proves the scorer alone; fix data before prompts |
| PK locale underserved by founder distance from market | Recruit PK beta testers in M2, not M5 |
| Inference cost drift | Budget caps in code + cost column in generation_logs dashboards |
| Scope creep re-entering (tracking, chat, more meals) | Doc 02 cut-lines are the contract; changes require editing that doc first |
