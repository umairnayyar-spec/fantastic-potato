# 07 — Technical Architecture

Stack per the vision (Next.js + TypeScript + Tailwind + shadcn/ui + Supabase/Postgres) —
endorsed: it's the right call for a 1–2 person team shipping a polished PWA fast. The
interesting architecture is not the stack; it's the **AI planning pipeline** and the
discipline around what the LLM is and is not allowed to do.

## 1. System overview

```
┌────────────────────────────── Vercel ──────────────────────────────┐
│  Next.js (App Router, TS, Tailwind, shadcn/ui, PWA)                │
│  ├─ RSC pages: Today / Plan / Groceries / Recipe / Settings        │
│  ├─ Route handlers (API): plan ops, assistant, share, stripe hooks │
│  └─ Vercel Cron: weekly plan emails, recap builder                 │
└────────────┬───────────────────────────────┬───────────────────────┘
             │                               │
   ┌─────────▼──────────┐          ┌─────────▼─────────┐
   │ Supabase           │          │ Planning service   │
   │  Postgres + RLS    │◄────────►│ (TS module, runs   │
   │  Auth (email/OAuth)│          │  in route handlers)│
   │  Storage (images)  │          │  filter→score→LLM→ │
   │  Edge fn: share    │          │  validate→persist  │
   └────────────────────┘          └─────────┬─────────┘
                                             │
                                   ┌─────────▼─────────┐
                                   │ Anthropic API      │
                                   │  Sonnet: generate  │
                                   │  Haiku: intents/   │
                                   │         swaps      │
                                   └───────────────────┘
   Stripe (billing) · Resend (email) · PostHog (product analytics) · Sentry
```

One deployable (the Next.js app) + Supabase. **No microservices, no queues, no Redis in
v1.** Plan generation completes in ~10–20s — within serverless limits (use streaming +
`maxDuration` on Vercel; if limits pinch, move generation to a Supabase Edge Function or a
single Fly.io worker later — the planning service is a pure TS module either way, so the
host is swappable).

## 2. The AI planning pipeline (the core IP)

**Doctrine: the LLM chooses; code computes and enforces.**

```
1. FILTER (SQL)      hard constraints: diet, allergens, locale servability, equipment,
                     skill, time, batch-friendliness  → 60–150 candidates
2. SCORE (TS)        deterministic: macro-fit per portioning options, ingredient-overlap
                     matrix, cost band, taste-profile score, variety penalty, season
                     → top ~40, each as one compact row (id, title, macros, time,
                     cost, key ingredients, tags)
3. SELECT (LLM)      Sonnet, structured output (tool call): pick batch recipes + assign
                     portions to day/slots + prep session assignment + human-readable
                     "why this week works" note. Input is the scored table + targets +
                     constraints digest — NOT raw recipes. ~2–4k input tokens.
4. VALIDATE (TS)     re-check every hard filter, macro ±10%/day, servings arithmetic,
                     prep-session capacity. Violation → auto-repair via one retry with
                     violations listed → still bad → fall back to pure-code greedy
                     assembly (always available, slightly less clever, never wrong).
5. DERIVE (TS)       prep schedule (task graph from recipes' components), grocery list
                     (consolidation), day totals. Pure functions of the selected plan.
6. PERSIST + LOG     plan rows + generation_logs (prompt version, inputs, output, tokens).
```

Swaps/shuffle/replace: steps 1–2 only + Haiku for ranked alternatives (or pure code —
A/B it). Assistant: Haiku parses text → typed op (`replace | exclude | time_constrain |
macro_constrain | repair | prep_shift`) → the op runs through the same pipeline → diff
returned; unparseable → capability menu, no free generation.

**Why this shape matters:**
- *Correctness:* allergen safety never depends on model behavior (NFR-1/2).
- *Cost:* small structured calls, prompt-cached preamble; the corpus is never stuffed
  into context.
- *Evolvability:* the LLM can be swapped/upgraded per step; the fallback assembler means
  the product works even during an API outage (degraded, not down).

## 3. Cost model (NFR-3 ≤ $0.30/user/mo)

Typical active week: 1 generate (Sonnet ~4k in/1k out ≈ $0.027) + ~4 Haiku ops (~$0.004)
+ 1–2 repairs (Sonnet small ≈ $0.02) ≈ **$0.05–0.08/week ⇒ $0.20–0.32/mo** before prompt
caching; caching the static preamble (system + schema + locale digest) cuts input cost
roughly in half. Enforcement: per-household daily op budget in code (429 with friendly
copy), whole-week regenerates capped by tier.

## 4. Eval & safety harness (built in M2, gates every release)

- **Golden households:** ~30 synthetic profiles crossing locales × diets × allergies ×
  budgets × equipment. CI runs generation for all; asserts zero hard-filter violations,
  macro fit, overlap score floor, no recipe repetition, latency budget.
- **Assistant suite:** the vision's five utterances + ~40 variants → expected typed ops.
- Prompt/model/corpus changes are PRs that must pass the harness; `generation_logs`
  feeds new regression cases from production misses.
- Nutrition disclaimers surfaced at targets screen; hard floors on calorie targets in
  code (FR-7).

## 5. Frontend architecture

- **App Router + RSC:** read surfaces (Today, Plan, Recipe) are server components;
  mutations via server actions returning typed diffs; optimistic UI for lock/check/swap.
- **PWA:** installable; service worker caches app shell + active plan + grocery list +
  today's recipes. Grocery check-off writes to IndexedDB outbox → syncs (per-item
  last-write-wins on `updated_at` — granular enough that conflicts are trivial).
- **Design system:** shadcn/ui + Tailwind tokens; light/dark via CSS variables from day
  one; spacious Apple/Linear-calm defaults; Framer Motion for the few meaningful
  transitions (plan reveal, diff confirm) only.
- **i18n-ready:** all strings through a message layer (English-only at launch); units and
  ingredient names localized via data, not translation files.
- **State:** server is source of truth; TanStack Query for client cache; no global state
  library.

## 6. Cross-cutting

- **Auth:** Supabase Auth (email + Google). Session in HTTP-only cookies via
  `@supabase/ssr`.
- **RLS everywhere** (schema in doc 06); service-role key only in server-side content
  pipeline and Stripe webhooks.
- **Payments:** Stripe Checkout + customer portal; webhook → `subscriptions` table;
  PPP pricing = separate Stripe prices per locale pack.
- **Email:** Resend + React Email templates (plan-ready, prep-day, recap).
- **Analytics:** PostHog (funnel: onboard steps, generate, prep-started, feedback,
  week-4 return; the ≤5-min planning metric is a PostHog insight). Sentry for errors.
- **Privacy:** health-adjacent fields encrypted at rest (Supabase default) and excluded
  from analytics events; delete-account = cascade delete + Stripe cancel; export = JSON
  dump edge function (NFR-6).
- **Environments:** local (Supabase CLI) → preview (Vercel PR + branch DB) → prod.
  Migrations via Supabase CLI in CI. Secrets in Vercel/Supabase env, never in repo.

## 7. Deliberate non-choices (revisit triggers)

| Choice avoided | Revisit when |
|---|---|
| Microservices / queues / Redis | Generation moves off-request or >30s |
| pgvector embeddings | Free-text taste matching underperforms chips+signals |
| CMS/admin UI for content | Corpus > ~600 recipes or a non-technical editor joins |
| Native apps | Week-4 retention proven and push notifications become the bottleneck |
| Fine-tuning | Prompt+eval harness plateaus on selection quality |
| Multi-region infra | PK latency to us-east measurably hurts (CDN covers reads; writes are rare) |
