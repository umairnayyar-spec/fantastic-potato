# 02 — MVP Scope & v1 Exclusions (reconciled with full vision)

## The hypothesis the MVP must test

> A user will let PrepChef plan their week — targets, meals, groceries, and prep schedule —
> actually execute the prep session and shop from the list, and come back for a new plan
> **four weeks in a row**.

Success bar: **week-4 planning retention ≥ 35%** of onboarded users, **≥ 60% of plans with
a completed prep session or ≥ 60% of planned meals marked eaten**, and 👍 rate improving
week-over-week. The vision's own success criterion — *under five minutes from opening the
app to a complete week* — is a hard product requirement, measured in analytics.

## MVP: the core loop

```
Onboard (≤ 4 min)
   → Targets computed (calories + macros, shown simply)
   → Weekly plan generated (2 batch-cook sessions → week of lunches + dinners;
     breakfast rotation; snack suggestions; per-meal macros; locale-aware)
   → Review & adjust (swap / lock / shuffle / regenerate one meal / assistant commands)
   → Grocery list (consolidated, categorized, check-off, print, share)
   → Prep day: guided prep schedule (task sequence + est. time)
   → Through the week: today's meals surface; one-tap ate-it / skipped
   → Mid-week repair ("prep ran out", "ate out twice") reflows the week
   → Weekly recap → next week's plan is measurably better
```

### In scope (v1)

1. **Onboarding** (the vision's list, trimmed to what changes output): age, height,
   weight, sex, goal, activity level → targets; dietary preference + allergies (hard
   filters); liked/disliked foods (quick-pick chips, not free-form essays); budget band;
   household size; cooking skill; weekly cook-time budget; **country → locale pack**;
   equipment as three booleans (oven / blender / microwave). Google OAuth + email.
2. **Nutrition targets** — Mifflin-St Jeor BMR → TDEE → calorie + protein/carb/fat
   targets, deterministic code (never the LLM). Simple explanation screen; targets
   editable within safe bounds. **No food logging anywhere.**
3. **Plan generation** — meal-prep-first: user picks 1 or 2 prep sessions (e.g., Sunday +
   Wednesday); PrepChef selects batch recipes from the curated corpus that (a) pass hard
   filters, (b) hit daily macro targets within ±10% when portioned across the week,
   (c) maximize ingredient overlap, (d) respect budget band, locale availability,
   equipment, skill, and time budget, (e) vary against recent weeks. Breakfasts: user
   picks 2–3 from a macro-fitted template rotation. Snacks: suggested list to fill macro
   gaps. Each meal shows calories/protein/carbs/fat, prep + cook time, difficulty, and
   locale cost band.
4. **Plan flexibility** — per the vision, all five verbs: replace a meal (3 alternatives),
   swap between days, lock favorites, shuffle unlocked meals, regenerate a single meal.
   Whole-week regenerate limited (cost control).
5. **AI assistant (constrained)** — a command bar over structured operations. The vision's
   examples all map: "replace Thursday dinner" → swap op; "no chicken this week" →
   exclusion + regenerate; "only 20 minutes" → time-filtered swap; "under 500 calories" →
   macro-filtered swap; "I only have eggs" → repair op. Every result is a proposed diff
   the user confirms. No open-ended chat.
6. **Grocery list** — consolidated across the plan, unit-normalized, scaled, minus pantry
   staples; grouped by category (produce/protein/dairy/pantry/frozen/spices); check-off
   (offline-capable PWA); manual items; print stylesheet; shareable read-only link.
   (Export-to-CSV deferred — print + share covers the real use.)
7. **Prep schedule** — generated task plan per prep session (proteins → grains → sauces →
   chop → portion → store), interleaved across the session's recipes, with estimated total
   time and storage instructions per batch. This is a *derived view* of the plan, not a
   separately generated artifact — keeps it consistent under swaps/repairs.
8. **Recipe pages** — ingredients (scaled), instructions, nutrition, times, difficulty,
   storage/freezer/reheat notes, substitutions (from curated substitution data), cost
   band. Reached from the plan only; no browsing/search surface in v1.
9. **Feedback loop** — per-meal: Ate it 👍 / Ate it 👎 / Skipped. Feeds the preference
   profile used in next generation.
10. **Plan repair** — one-tap "didn't happen" on a prep session or meal; free-text repair
    via the assistant. Reflow prioritizes already-bought ingredients; grocery list updates
    coherently; guilt-free tone mandated.
11. **Dashboard = "Today"** — today's meals, plan-adherence view of macros (planned vs.
    target — *not* logged), shopping progress, next prep session reminder. No weight
    tracking in v1 (v1.x: optional weekly weigh-in that re-tunes TDEE).
12. **Weekly recap** — meals eaten, prep sessions done, protein adherence, ingredient
    utilization, estimated savings vs. eating out (labeled estimate). Email + in-app.
13. **Localization** — two curated locale packs at launch: **Pakistan** (halal default,
    metric, local ingredient names, oven-optional bias, ₨ cost bands) and **United
    States** (imperial default, $ cost bands). Corpus: ~350 recipes total, every recipe
    availability-scored per locale (~250 servable per locale, overlapping).
14. **Design system** — Next.js + Tailwind + shadcn/ui, mobile-first, light + dark mode,
    Apple/Linear/Notion-calm aesthetic. (Cheap to do from day one with this stack;
    expensive to retrofit.)
15. **Billing** — freemium + Stripe (~$8/mo or PPP-adjusted regional pricing given the PK
    locale; decide in M5). Free tier completes the full loop with limited swaps. 14-day
    full trial. Repair and feedback are never paywalled.

### Explicitly OUT of v1

| Excluded | Why |
|---|---|
| Food logging / calorie-remaining meter | Tracker trap (critique A2). Adherence view instead |
| Weight tracking & progress charts | v1.x optional weigh-in; charts imply a tracking product |
| Full breakfast/snack generation | Rotation templates + suggestions cover it at 1/5 the complexity (A1) |
| Real grocery prices, store integration, delivery | No data source; cost bands in v1; partnerships are v2 |
| Pantry/fridge inventory | Highest-abandonment feature in category; overlap optimization instead |
| "Any country" localization | Fake without curated data (A3); two real locale packs instead |
| Open-ended AI chat | Unbounded cost/failure surface (A5); command layer instead |
| AI-generated novel recipes | Untested recipes destroy trust; AI selects/adapts from tested corpus |
| Kitchen equipment inventory beyond 3 booleans | A6 |
| Per-household-member profiles | Household-level prefs in v1; member profiles v1.x |
| Native apps / push notifications | PWA + email until the loop retains |
| Social/community features, recipe import, meal photos | No contribution to the hypothesis |
| CSV/third-party grocery export | Print + share link covers actual behavior |
| Urdu (or any) translation | English UI across both locale packs at launch; i18n-ready strings from day one |

### Cut-line discipline

If forced to cut within the MVP, cut in order: recap → billing → share link → print
stylesheet → second locale pack (keep PK if the founder's distribution advantage is there,
else US). **Never cut:** prep schedule, repair, feedback buttons, grocery consolidation,
macro-fitted generation — that set *is* the product.
