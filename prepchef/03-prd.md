# 03 — Product Requirements Document (v1)

**Product:** PrepChef v1 (MVP)
**Status:** Draft for founder review
**Positioning:** *PrepChef decides what's for dinner — so you don't have to.*

## 1. Problem statement

Households that cook at home face a small but relentless daily burden: deciding what to
eat, checking what it requires, and shopping for it. The decision recurs ~5 times a week,
is often made under time pressure at the worst moment of the day, and failure modes are
expensive (takeout) and wasteful (unused groceries). Existing meal planners generate plans
but abandon the user the moment real life diverges from the plan, which it always does.

## 2. Target users & personas

| Persona | Description | Key need |
|---|---|---|
| **Overloaded parent** (primary) | 30–45, household of 3–5, cooks 4–6 nights/wk, kids with preferences | Plans everyone will eat; fast weeknight recipes; one shopping trip |
| **Busy professional couple** | 25–40, household of 2, cooks 3–5 nights/wk | Variety, low decision effort, less takeout guilt |
| **Solo simplifier** (secondary) | 22–35, household of 1 | Right-sized portions, leftovers handled intelligently |

## 3. Goals & success metrics

| Goal | Metric | v1 target |
|---|---|---|
| Households adopt the loop | Onboarding → first plan generated | ≥ 80% |
| Plans get used in the real world | ≥ 1 grocery item checked off, per plan | ≥ 60% of plans |
| Plans survive contact with reality | Planned meals marked *cooked* | ≥ 60% (retained households) |
| **Retention (north star)** | Households generating a plan in week 4 | **≥ 35% of onboarded cohort** |
| Learning loop works | 👍 rate on meals, week 4 vs. week 1 | +15% relative |
| Unit economics | LLM inference cost per active household per month | ≤ $0.30 |
| Willingness to pay (signal) | Free → paid conversion at day 30 | ≥ 4% |

Guardrail metrics: plan-generation p95 latency ≤ 15s; hard-constraint violations
(allergen/diet in a served plan) = **0** (this is a correctness requirement, not a metric
to optimize).

## 4. Functional requirements

Priority: **P0** = MVP-blocking · **P1** = should ship in v1, cuttable · **P2** = v1.x.

### 4.1 Accounts & household (P0)

- FR-1 Email/password + Google OAuth sign-up; email verification.
- FR-2 A user belongs to exactly one **household** in v1; household is the unit of
  planning, preferences, and billing.
- FR-3 Household setup: # adults, # kids; per-household dietary constraints
  (vegetarian, vegan, pescatarian, halal, kosher-style, gluten-free, dairy-free,
  nut-allergy, shellfish-allergy, custom-avoid list). **Constraints are hard filters** —
  a recipe violating any household constraint must never be selectable, swappable, or
  suggested, including by the AI repair path.
- FR-4 Hard dislikes (ingredient-level, e.g. "no mushrooms") — also hard filters.
- FR-5 Time budget (weeknight max: 20/30/45/60+ min) and skill level (beginner /
  comfortable / confident) — soft preferences.
- FR-6 Taste bootstrap: swipe/tap through 8 candidate recipes ("would you eat this?");
  results seed the preference profile.
- FR-7 (P1) Invite a second member into the household (shared plan & list, single set of
  household preferences in v1).

### 4.2 Plan generation (P0)

- FR-8 Generate a weekly dinner plan of N meals (user picks 3–6, default 4) assigned to
  user-chosen weeknights.
- FR-9 Generation must respect: hard filters (constraints/dislikes), time budget per
  night, taste profile, **ingredient-overlap optimization** (shared perishables across the
  week), variety (no recipe repeated within 21 days unless 👍-rated and user opts into
  favorites repetition), seasonal tag bias.
- FR-10 If a recipe yields ≥ 2 servings above household size, offer an automatic
  "Leftovers" entry the following night (user can decline).
- FR-11 Per-meal actions on the draft plan: **Swap** (show 3 alternatives), **Remove**,
  **Adjust** via one-line free text ("something lighter", "use the salmon idea but
  faster"). Whole-plan regenerate ≤ 1×/week (free tier) to bound cost.
- FR-12 Plan generation p95 ≤ 15s with a streaming/skeleton UI; swaps p95 ≤ 4s.
- FR-13 Every generated plan is reproducible: persist recipe IDs, scaling factors, and the
  generation context (model, prompt version, candidate set) for debugging and evals.

### 4.3 Grocery list (P0)

- FR-14 Auto-build one consolidated list from the active plan: aggregate identical
  canonical ingredients across recipes, normalize units (2 tbsp + ¼ cup → single line),
  scale to household size, subtract pantry staples.
- FR-15 Group by store category (produce, meat/fish, dairy, pantry, frozen, other);
  check-off persists instantly and works offline (PWA cache + sync).
- FR-16 Manual items (free text) can be added; they persist week to week ("running low"
  behavior is out of scope).
- FR-17 Editing the plan (swap/remove/repair) updates the list **coherently**: purchased
  (checked) items are never silently removed — they move to a "you already have"
  section if no longer needed.
- FR-18 (P1) Read-only shareable list link (tokenized URL, no login required to view/check).

### 4.4 Cook mode & feedback (P0)

- FR-19 "Tonight" surface: today's planned meal one tap from home; ingredients (scaled),
  steps, estimated time. Screen wake-lock during cook mode.
- FR-20 Post-meal feedback: exactly three options — **Cooked 👍 / Cooked 👎 / Skipped** —
  available from tonight's view and from the week view for past nights. Optional one-line
  note on 👎 (fed to the taste profile).
- FR-21 Feedback mutates the household taste profile (recipe-, ingredient-, and
  cuisine-level signals) and is reflected in the next generation.

### 4.5 Plan repair (P0) — *hero feature*

- FR-22 One-tap **"Didn't cook it"** on any current-week meal → PrepChef reflows the
  remaining week: prioritizes already-purchased perishables, rolls at most one meal
  forward, updates the list per FR-17. Completes ≤ 6s p95.
- FR-23 Free-text repair on the week ("we're out Thursday", "have half a roast chicken
  left") → AI restructures remaining nights under the same hard filters. The response is a
  *proposed diff* (before/after week view) the user confirms — never silent mutation.
- FR-24 Tone requirement: repair flows are guilt-free by design. No streak-breaking
  language, no red warnings for skipping. (This is a product requirement, not a style nit.)

### 4.6 Weekly recap (P1)

- FR-25 End-of-week summary: meals cooked, estimated savings vs. a delivery-cost benchmark
  (labeled "estimate"), ingredient utilization ("everything you bought got used" when
  overlap optimization achieved it), next week CTA. Delivered in-app + email.

### 4.7 Recipe corpus (P0 — content workstream, not code)

- FR-26 300–500 rights-clean recipes; every ingredient row references a **canonical
  ingredient** with quantity, unit, and optional prep note; recipes tagged: cuisine, diet
  flags (computed from ingredients *and* human-verified), active/total time, difficulty,
  kid-friendly, season; original or rewritten instructions; owned/stock imagery.
- FR-27 Diet-flag verification is a human gate: no recipe enters the servable corpus
  until its allergen/diet flags are reviewed. (Backstops FR-3's zero-violation rule.)

### 4.8 Billing (P1)

- FR-28 Free tier: 1 plan/week, 3 swaps/week, repair included (repair is the habit-former;
  never paywall it). Paid ($8/mo, Stripe): unlimited swaps/adjustments, recap history,
  favorites. 14-day full-featured trial, no card required.

## 5. Non-functional requirements

- **NFR-1 Correctness:** zero hard-constraint violations in served plans (automated eval
  suite gates every prompt/model/corpus change; violations block deploy).
- **NFR-2 Cost:** inference ≤ $0.30 per active household/month at v1 usage; per-household
  daily LLM budget enforced server-side.
- **NFR-3 Performance:** plan p95 ≤ 15s (streamed), swap ≤ 4s, repair ≤ 6s, all other
  interactions ≤ 300ms server time.
- **NFR-4 Availability:** 99.5% for the app; grocery list check-off must degrade to
  offline (local cache + background sync) — a store aisle has bad reception.
- **NFR-5 Privacy/security:** dietary and health-adjacent data is sensitive — encrypted at
  rest, never sold, never used in prompts for *other* households; GDPR-style
  export/delete from day one (cheap now, painful later).
- **NFR-6 Auditability:** every AI generation persisted with prompt version + inputs +
  outputs (see FR-13) for eval regression and support.
- **NFR-7 Accessibility:** WCAG 2.1 AA on the core loop; cook mode readable at arm's
  length (large type mode).

## 6. Open questions (need founder decision, don't block build start)

1. Price point $6 vs $8 vs $10/mo — test at launch, build nothing price-specific.
2. Kids' preferences: v1 models household-level dislikes only; per-member profiles are
   v1.x — confirm acceptable for launch marketing.
3. Recipe corpus sourcing: commission (est. $30–60/recipe) vs. license a structured
   dataset — needs a budget call within Milestone 1 (see doc 08).
4. Brand voice: recap "savings estimate" methodology must be defensible — agree the
   benchmark (e.g., regional average delivery cost per meal) before recap ships.
