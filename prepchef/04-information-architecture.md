# 04 — Information Architecture

Design principle: **one center of gravity — the week's plan — with "Today" as the daily
front door.** No recipe-browser identity: recipes are reached through the plan, never
through search/browse in v1.

## 1. Sitemap

```
PrepChef (PWA)
│
├── Onboarding (first-run, linear, ≤4 min)
│   ├── 1. Account (email / Google)
│   ├── 2. Body & goal (age, height, weight, sex, goal, activity)
│   ├── 3. Targets reveal (calories + macros, plain-language, editable)
│   ├── 4. Food rules (diet preference, allergies — explicit "none" required)
│   ├── 5. Tastes (like/dislike chips, locale-aware)
│   ├── 6. Practicalities (household size, budget band, skill, time, equipment,
│   │      country → locale pack, units)
│   ├── 7. Prep style (1 or 2 sessions, which days, breakfast templates)
│   └── 8. First plan generation (streams in) → lands on Plan
│
├── Today  ····················· default route after day 1
│   ├── Today's meals (breakfast / lunch / dinner cards → Recipe)
│   ├── Macro adherence strip (planned vs target — no logging)
│   ├── Next prep session countdown → Prep Mode
│   ├── Shopping progress chip → Groceries
│   └── Feedback owed (yesterday's meals: 👍 / 👎 / Skipped — dismissible)
│
├── Plan  (week view)
│   ├── Assistant command bar ("Tell me what to change…")
│   ├── Prep session cards (Sun / Wed) → Prep Schedule detail → Prep Mode
│   ├── Day rows (Mon–Sun): meal entries with macros, cost band, lock toggle
│   │   └── Meal entry → Meal sheet (bottom sheet over the week)
│   │       ├── Recipe preview → full Recipe page
│   │       ├── Replace (3 alternatives) · Move day · Lock · Regenerate (+note)
│   │       └── Didn't happen → Repair proposal (before/after diff, Confirm)
│   ├── Day totals vs targets (per-day macro bar)
│   └── [no plan] Generate my week → prep-style setup → generation
│
├── Groceries
│   ├── Category groups (produce / protein / dairy / pantry / frozen / spices / other)
│   │   └── Item: checkbox · normalized qty · "used in 3 meals" chip · locale name
│   ├── Already have (staples + de-planned purchased items)
│   ├── + Add item · Print · Share (read-only link)
│   └── Offline badge + sync state
│
├── Recipe page (from plan/meal sheet only)
│   ├── Photo · macros/serving · times · difficulty · cost band
│   ├── Ingredients (scaled to household) ⇄ Steps
│   ├── Storage · freezer · reheating · substitutions
│   └── Cook Mode (fullscreen, wake-lock, large type)
│
├── Prep Mode (fullscreen from prep session card)
│   ├── Ordered tasks w/ time estimates & parallel hints
│   ├── Step-through, wake-lock
│   └── Done → batches marked available · Didn't finish → Repair
│
├── Recap (weekly; in-app + email deep-link)
│   ├── Meals eaten · prep completed · protein adherence
│   ├── Utilization ("everything you bought got used") · est. savings (labeled)
│   └── CTA: Plan next week
│
└── Settings
    ├── Profile & targets (body, goal, activity → recompute prompt)
    ├── Food rules (diet, allergies, dislikes)
    ├── Practicalities (budget, time, skill, equipment, locale, units)
    ├── Pantry staples (editable assumption checklist)
    ├── Breakfast rotation
    ├── Subscription (plan, Stripe portal)
    └── Account (email, export data, delete account, dark/light/auto)
```

## 2. Navigation model

- **Bottom tab bar, 4 tabs:** Today · Plan · Groceries · Settings. Recipe, Cook Mode,
  Prep Mode, and Recap are contextual full-screen surfaces, not tabs.
- **Route logic:** brand-new user → Onboarding; no active plan → Plan (generate state);
  otherwise → Today.
- **Meal sheet is a bottom sheet** over the week — you're editing the week, not browsing
  recipes.
- **All AI mutations render as diffs** (before/after week strip) with one Confirm —
  applies to assistant commands, repairs, and regenerations.
- **Assistant command bar** lives on Plan only; shows a "what I can do" chip row on focus
  (replace · exclude · time · calories · fix my week).

## 3. Object model

| Object | Primary surface | Notes |
|---|---|---|
| Plan (week) | Plan tab | One active per household |
| Prep session | Plan + Prep Mode | 1–2 per plan; owns batch tasks |
| Plan entry | Day rows | batch-portion / fresh-cook / breakfast / leftovers / eating-out / empty — all first-class |
| Recipe | Recipe page | Only reachable via plan; no global browse |
| Grocery list | Groceries tab | Always derived from active plan + manual items |
| Targets | Today strip + Settings | Computed; adherence shown, never logged intake |
| Feedback | Attached to entries | Surfaces on Today; no history UI in v1 |
| Taste profile | Invisible | Surfaced only as "because you liked X" hints |

## 4. State variants each surface must handle

- **Today:** normal · nothing planned today ("out day" copy) · feedback owed · prep day
  ("today you cook for the week") · no active plan (CTA to Plan).
- **Plan:** no plan · generating (streamed skeleton) · active · repair diff pending ·
  week complete (recap teaser).
- **Groceries:** empty · active · offline/cached · shared read-only view.
- **Prep session card:** upcoming · in progress · done · skipped (repair offered, calm).

## 5. Notifications (v1: email only; PWA push unreliable)

| Trigger | Channel | Content |
|---|---|---|
| Plan day (default: day before prep, 10am) | Email | "Ready to plan your week" deep-link |
| Prep-day morning | Email | "Prep day — ~1h 40m, list attached" |
| Weekly recap | Email + in-app | Recap |
| Skipped meals/prep | **Never emailed** | Tone rule (FR-31) |
