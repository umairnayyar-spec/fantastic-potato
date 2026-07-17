# 02 — MVP Scope & v1 Exclusions

## The hypothesis the MVP must test

> A household will let PrepChef decide dinner for them, follow the plan well enough to shop
> from its grocery list, and come back for a new plan **four weeks in a row**.

Success metric: **week-4 planning retention ≥ 35%** of households that completed onboarding
(cohort basis), and ≥ 60% of planned meals marked "cooked" among retained households.
If we can't hit that, no amount of price data, nutrition tracking, or native apps will save
the product — and if we can, all of those become worth building.

## MVP: the core loop

One loop, executed end-to-end, nothing else:

```
Onboard (≤3 min)
   → Generate weekly dinner plan (3–6 meals, household-aware)
   → Review & adjust (swap / remove / "make it faster")
   → Consolidated grocery list (check-off while shopping)
   → Cook nights: today's recipe front and center
   → One-tap feedback: Cooked 👍 / Cooked 👎 / Skipped
   → Mid-week repair: "didn't cook it" reflows the week
   → Weekly recap (proof of value) → next week's plan is measurably better
```

### In scope (v1)

1. **Onboarding** — household size (adults/kids), dietary constraints (vegetarian, halal,
   allergies, etc.), hard dislikes, weeknight time budget, cooking skill, cuisine
   preferences via an 8-recipe "would you eat this?" swipe. Email/password + Google OAuth.
2. **Plan generation** — AI selects and sequences 3–6 dinners from the curated recipe
   corpus, optimizing for: household constraints (hard filters), taste profile (learned),
   time budget per night, **ingredient overlap across the week** (structural waste/cost
   reduction), and variety vs. recent weeks. One auto "leftovers night" slot when a recipe
   yields extra servings.
3. **Plan adjustment** — per-meal: swap (3 alternatives offered), remove, regenerate with a
   one-line instruction ("something lighter"). Whole-plan regenerate once per week.
4. **Grocery list** — auto-consolidated across the week's recipes: unit-normalized,
   aggregated by ingredient, grouped by store aisle/category, minus pantry staples;
   check-off UI that works one-handed in a store; add manual items; shareable read-only
   link (so a partner can shop).
5. **Pantry staples list** — a default assumed-staples checklist, editable once in
   settings. No inventory tracking.
6. **Cook mode** — today's recipe: ingredients, scaled quantities, steps, servings. Plain,
   readable, screen-stays-awake.
7. **Feedback loop** — three-button per-meal feedback; drives the household preference
   profile used in generation.
8. **Plan repair** — "didn't cook it" one-tap reflow; free-text repair ("we're eating out
   Thursday") handled by the AI; grocery list updates coherently.
9. **Weekly recap** — meals cooked, streak, rough savings vs. delivery/takeout benchmark
   (clearly labeled as an estimate), ingredients fully used.
10. **Recipe corpus** — 300–500 curated, tested, rights-clean recipes with fully
    structured ingredients (canonical ingredient IDs, quantities, units, prep notes),
    tagged (cuisine, diet flags, time, difficulty, kid-friendliness).
11. **Platform** — mobile-first responsive web app (PWA: installable, grocery list cached
    offline). No native apps.
12. **Billing** — freemium: free = 1 active plan/week with limited swaps; paid (~$8/mo)
    = unlimited swaps/repairs + recap history. Stripe. (Charging from early on is itself a
    validation signal, but the free tier must let a household complete the full loop.)

### Explicitly OUT of v1 (and why)

| Excluded | Why |
|---|---|
| Pantry/fridge inventory tracking | Highest-abandonment feature in the category; structural overlap optimization captures most of the value with zero user labor |
| Real grocery price data / store APIs | No viable general API; partnerships are a v2 job. v1 shows *estimated* savings only |
| Grocery delivery integration | Depends on partnerships; adds checkout complexity; not needed to test the hypothesis |
| Breakfast, lunch, snacks, desserts | Dinner is the stress point; other meals triple content needs and dilute plan quality |
| Nutrition/macro tracking & goals | Different product muscle (tracking vs. deciding); "healthier by default" tagging suffices in v1 |
| AI-generated novel recipes | Untested recipes are a trust grenade; AI selects/adapts from the tested corpus only |
| Social features (sharing plans, community, comments) | Zero contribution to the core hypothesis |
| Native iOS/Android apps | 2–3× build cost pre-validation; PWA covers the loop. Cost: no reliable push — mitigate with email + calendar-file nudges, accept the gap |
| Meal-kit style portioned delivery | Entirely different (logistics) business |
| Multiple simultaneous plans / meal-prep-only mode | Variants of the loop; add after the loop retains |
| Wearable/health-platform integrations | v3 territory |
| Localization / multi-currency / metric-imperial switching | Single locale at launch |
| In-app chat with a general cooking assistant | Scope trap: unbounded surface, unbounded inference cost. The AI appears only inside structured actions (generate, swap, repair) |

### MVP cut-line discipline

If timeline pressure forces cuts *within* the MVP, cut in this order (last = most
protected): weekly recap → billing → shareable list link → swipe onboarding (replace with
checkboxes) → leftovers slot. **Never cut:** plan repair, feedback buttons, grocery-list
consolidation. Those three are the product.
