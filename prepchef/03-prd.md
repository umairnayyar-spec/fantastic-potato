# 03 — Product Requirements Document (v1)

**Product:** PrepChef v1 (MVP) · **Status:** Draft for founder review
**Positioning:** *Your week of healthy eating, planned in five minutes.*

## 1. Problem statement

People who want to eat healthier face a weekly compounding chore: set targets, find
realistic recipes, plan a coherent week, shop for it, and cook it — repeatedly, under time
pressure, with ingredients that are actually available and affordable where they live.
Existing tools fail by recommending unrealistic or locally unavailable recipes, ignoring
meal prep, generating waste, and abandoning the user the moment the plan meets reality.

## 2. Target users & personas

| Persona | Description | Key need |
|---|---|---|
| **Gym-goer / recomposition** (primary) | 20–40, trains 3–6×/wk, wants protein targets hit without chicken-and-rice monotony | Macro-fitted plans, batch prep, taste |
| **Busy professional** (primary) | 25–45, cooks to save money/health, decision-fatigued | ≤5-min planning, 1–2 prep sessions, easy repair |
| **Local-market user (PK pack)** | Any of the above in Pakistan | Recipes from ingredients at their actual market, halal default, no oven assumed |
| **Parent/household cook** (secondary) | Plans for 2–5 people | Scaled portions, budget bands, one shopping trip |

## 3. Goals & success metrics

| Goal | Metric | v1 target |
|---|---|---|
| Planning is genuinely fast | Median time: open app → plan + list ready (returning user) | **≤ 5 min** |
| Onboarding completes | Signup → first plan generated | ≥ 75% |
| Plans reach the kitchen | Plans with ≥1 prep session started or ≥3 meals marked eaten | ≥ 55% |
| **Retention (north star)** | Users generating a plan in week 4 | **≥ 35% of cohort** |
| Learning loop works | 👍 rate week 4 vs week 1 | +15% relative |
| Localization is real | PK-pack plan quality parity: swap rate ≤ 1.3× US pack | tracked |
| Unit economics | Inference cost / active user / month | ≤ $0.30 |
| Willingness to pay | Free→paid conversion, day 30 | ≥ 4% |

Guardrails: plan generation p95 ≤ 20s streamed; **zero** allergen/diet violations in
served plans (correctness requirement, deploy-blocking); macro fit within ±10% of daily
targets for ≥ 90% of generated days.

## 4. Functional requirements

Priority: **P0** = MVP-blocking · **P1** = should ship, cuttable · **P2** = v1.x.

### 4.1 Onboarding & profile (P0)

- FR-1 Email/password + Google OAuth; email verification.
- FR-2 Profile inputs: age, height, weight, sex, goal (lose/maintain/gain/health),
  activity level (5 bands), dietary preference (none/vegetarian/vegan/pescatarian/halal/
  kosher-style/gluten-free/dairy-free), allergies (structured list + custom), liked and
  disliked foods (chip-pick from top ~60 ingredients, per locale), budget band (3 levels),
  household size (adults/kids), cooking skill (3 levels), weekly cooking-time budget,
  country → locale pack, equipment booleans (oven/blender/microwave), units
  (defaulted by locale, overridable).
- FR-3 Allergies and dietary preference are **hard filters** at every surface — generate,
  swap, shuffle, assistant, repair. Enforced by deterministic code, never left to the LLM.
- FR-4 Onboarding completable in ≤ 4 minutes; every step after account creation
  skippable-with-defaults except allergies (explicit "none" required).
- FR-5 All profile fields editable later in Settings; changes affect the *next*
  generation, with an offer to regenerate the current week.

### 4.2 Nutrition targets (P0)

- FR-6 Compute BMR (Mifflin-St Jeor), TDEE (activity multiplier), calorie target
  (goal-adjusted: −15–20% cut / maintenance / +10% surplus), protein (1.6–2.2 g/kg by
  goal), fat (≥ 20% kcal), carbs (remainder). Pure functions, unit-tested, never the LLM.
- FR-7 Targets shown on one simple screen (number + one-line meaning each); editable
  within clinically safe bounds (floors: 1,200/1,500 kcal; warnings outside evidence-based
  ranges). Not medical advice — disclaimer required.
- FR-8 No food logging. The dashboard shows **planned** intake vs. target ("adherence
  view"), never a "remaining calories" meter.

### 4.3 Weekly plan generation (P0)

- FR-9 User selects: prep model (1 or 2 sessions/week + which days), days to cover
  (default Mon–Sun), lunches/dinners needed (accounting for known eating-out days).
- FR-10 Generator selects batch recipes from the curated corpus satisfying, in priority
  order: (1) hard filters; (2) locale availability ≥ threshold; (3) daily macro fit ±10%
  when portioned; (4) time budget & skill & equipment; (5) budget band; (6) ingredient
  overlap (shared perishables across batches); (7) taste profile; (8) variety vs. last 3
  weeks; (9) seasonal bias.
- FR-11 Breakfasts: rotation of 2–3 user-picked templates (macro-counted). Snack
  suggestions computed to fill residual macros. Both count toward daily totals.
- FR-12 Each meal displays: kcal, protein, carbs, fat, prep time, cook time, difficulty,
  cost band. Each day displays totals vs. targets.
- FR-13 Plan entries support types: batch-portion, fresh-cook, breakfast-template,
  leftovers, eating-out, empty. Eating-out days reduce coverage, never generate guilt copy.
- FR-14 p95 ≤ 20s with streaming skeleton; persisted with full generation context
  (model, prompt version, candidate set, scores) for reproducibility and evals.

### 4.4 Plan flexibility (P0)

- FR-15 Replace meal (3 filtered alternatives) · swap meals between days (drag or menu) ·
  lock meals (survive shuffle/regenerate) · shuffle unlocked · regenerate single meal with
  optional one-line instruction. All obey FR-3 and update macros/list live.
- FR-16 Whole-week regenerate: ≤ 1×/week free tier, ≤ 3× paid (cost control).
- FR-17 Swap/regenerate p95 ≤ 4s.

### 4.5 AI assistant — constrained command layer (P0)

- FR-18 A command bar on the plan accepts free text; intents parse to structured
  operations: replace / exclude-ingredient / time-constrain / macro-constrain / repair /
  prep-shift. Vision examples are the acceptance tests ("I only have eggs", "Replace
  Thursday dinner", "I don't want chicken this week", "I only have 20 minutes", "meals
  under 500 calories").
- FR-19 Every assistant result is a **proposed diff** (before/after) requiring
  confirmation. Unparseable requests get an honest "here's what I can do" menu, never a
  hallucinated action. Out-of-scope requests (nutrition advice, arbitrary chat) are
  declined with the menu.
- FR-20 Rate-limited per tier; p95 ≤ 6s.

### 4.6 Grocery list (P0)

- FR-21 Consolidated from the active plan: canonical-ingredient aggregation, unit
  normalization, household scaling, pantry-staples subtraction (editable static staples
  list — no inventory).
- FR-22 Grouped: produce / protein / dairy / pantry / frozen / spices / other. Locale
  ingredient names. Check-off persists offline (PWA cache + sync).
- FR-23 Manual items; print stylesheet (P1); tokenized read-only share link (P1).
- FR-24 Plan edits update the list coherently; checked (purchased) items never silently
  vanish — they move to "already bought" if de-planned.

### 4.7 Prep schedule (P0)

- FR-25 Per prep session, derive an ordered task plan across its recipes (proteins →
  grains/staples → sauces → chop → portion → store), with per-task and total estimated
  time, parallelization hints ("while rice cooks…"), and storage instructions
  (container, fridge/freezer, keeps-until).
- FR-26 Prep mode: step-through UI, wake-lock, large type. "Session done" marks batches
  available; "didn't prep" triggers repair (FR-29).

### 4.8 Recipe pages (P0)

- FR-27 Ingredients (scaled), instructions, nutrition/serving, times, difficulty, storage
  + freezer suitability + reheating notes, curated substitutions, cost band. Rights-clean
  content and imagery only (see FR-34).

### 4.9 Feedback & learning (P0)

- FR-28 Per-meal: **Ate it 👍 / Ate it 👎 / Skipped** (optional one-line note on 👎).
  Signals update the preference profile (recipe, ingredient, cuisine levels) and
  measurably shift the next generation.

### 4.10 Plan repair (P0 — hero feature)

- FR-29 One-tap "didn't happen" on a meal or an entire prep session → reflow the
  remaining week prioritizing already-purchased ingredients; at most one meal rolls
  forward; list updates per FR-24. p95 ≤ 6s.
- FR-30 Free-text repair via the assistant ("prep ran out Thursday", "I only have eggs")
  → proposed diff under hard filters.
- FR-31 Tone: judgment-free. No streaks broken, no red states, no "you missed" copy.

### 4.11 Dashboard — "Today" (P0)

- FR-32 Today's meals (tap → recipe), planned-vs-target macro adherence for today,
  shopping progress, next prep session countdown. No weight tracking (P2: optional weekly
  weigh-in re-tuning TDEE).

### 4.12 Weekly recap (P1)

- FR-33 Meals eaten, prep sessions completed, protein adherence, ingredient utilization,
  estimated eating-out savings (labeled estimate; locale-benchmark methodology agreed
  before ship). In-app + email; guilt-free framing.

### 4.13 Content & localization (P0 — content workstream)

- FR-34 ~350 rights-clean recipes, batch-friendly bias; every ingredient row references a
  canonical ingredient (qty, unit, prep note); nutrition computed per serving from
  ingredient data and spot-verified; tags: cuisine, meal role, diet flags
  (human-verified), times, difficulty, equipment, season, freezer-safe.
- FR-35 Locale packs (PK, US): per-ingredient availability + local name + cost band;
  per-recipe availability score; pack defaults (halal filter on for PK, units, staples
  list, eating-out cost benchmark). A recipe is servable in a locale only above the
  availability threshold.
- FR-36 Diet/allergen flags are human-verified before a recipe becomes servable
  (backstops FR-3's zero-violation rule).

### 4.14 Billing (P1)

- FR-37 Free: full loop, 3 swaps + 1 regenerate/week. Paid via Stripe (~$8/mo US; PPP
  pricing for PK decided in M5): unlimited flexibility, recap history, favorites. 14-day
  full trial, no card. Repair and feedback never paywalled.

## 5. Non-functional requirements

- **NFR-1 Correctness:** zero hard-filter violations; golden-household eval suite gates
  every prompt/model/corpus change in CI.
- **NFR-2 Nutrition integrity:** all nutrition math deterministic and unit-tested; LLM
  output never contains numbers shown to users (it selects; code computes).
- **NFR-3 Cost:** ≤ $0.30 inference/active user/month; server-side per-user daily budget.
- **NFR-4 Performance:** generate ≤ 20s p95 streamed; swap ≤ 4s; repair/assistant ≤ 6s;
  other interactions ≤ 300ms server.
- **NFR-5 Offline:** grocery list and today's recipes readable/checkable offline (store
  aisles and kitchens have bad reception).
- **NFR-6 Privacy:** health-adjacent data (weight, goals, allergies) encrypted at rest,
  never used across households, never sold; export + delete self-serve from day one;
  Supabase RLS on every table.
- **NFR-7 Auditability:** every generation logged (inputs, prompt version, output,
  tokens, latency).
- **NFR-8 Accessibility & design:** WCAG 2.1 AA; light + dark mode; i18n-ready strings
  (English-only at launch).
- **NFR-9 Availability:** 99.5%; degraded mode = read-only plan + list if generation is
  down.

## 6. Open questions (founder decisions; none block M0–M1)

1. PK pricing: PPP-adjusted subscription vs. free-longer strategy for the PK pack.
2. Recipe corpus sourcing: commission vs. license structured data — budget call in M1.
3. Which locale leads the beta (founder distribution advantage likely PK — confirm).
4. Recap savings methodology per locale (delivery benchmark source).
5. Working title "PrepChef" — trademark screen before spend on brand assets.
