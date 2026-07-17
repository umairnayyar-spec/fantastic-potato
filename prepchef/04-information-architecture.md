# 04 — Information Architecture

Design principle: **the app has one center of gravity — "this week" — and everything else
is subordinate to it.** Meal planners die when they become recipe browsers with a planner
bolted on; PrepChef inverts that: there is no browse-first experience.

## 1. Sitemap

```
PrepChef (PWA)
│
├── Onboarding (first-run only, linear)
│   ├── 1. Account (email / Google)
│   ├── 2. Household size (adults / kids)
│   ├── 3. Dietary constraints & allergies
│   ├── 4. Hard dislikes
│   ├── 5. Time budget & skill
│   ├── 6. Taste swipe (8 recipes)
│   └── 7. First plan generation (streams in) → lands on This Week
│
├── This Week  ················· home / default route
│   ├── Tonight card (primary object: today's meal → Cook Mode)
│   ├── Week strip (Mon–Sun entries: meal | leftovers | "out" | empty)
│   │   └── Meal entry → Meal Detail sheet
│   │       ├── Swap (3 alternatives)
│   │       ├── Adjust (free text)
│   │       ├── Remove
│   │       └── Didn't cook it  → Repair proposal (diff view)
│   ├── Repair bar ("Something change? Tell me") → free-text repair
│   └── [pre-plan state] Generate my week → plan setup (nights, # meals)
│
├── Grocery List
│   ├── Category groups (produce / meat & fish / dairy / pantry / frozen / other)
│   │   └── Item row: checkbox · qty (normalized) · "used in 3 meals" chip
│   ├── Already have (staples + de-planned purchased items)
│   ├── + Add item
│   └── Share (read-only link)
│
├── Cook Mode (fullscreen, from Tonight card)
│   ├── Ingredients (scaled) ⇄ Steps (tabbed)
│   ├── Wake-lock on · large-type toggle
│   └── Done → feedback prompt (👍 / 👎 / Skipped)
│
├── Recap (weekly, also via email deep-link)
│   ├── Meals cooked · estimated savings · utilization
│   └── CTA: Plan next week
│
└── Settings
    ├── Household (size, constraints, dislikes, time, skill)
    ├── Pantry staples (editable assumption checklist)
    ├── Members (P1: invite partner)
    ├── Subscription (plan, billing portal)
    └── Account (email, export data, delete account)
```

## 2. Navigation model

- **Bottom tab bar (3 tabs):** This Week · Grocery List · Settings. Recap and Cook Mode
  are contextual full-screen surfaces, not tabs. Three tabs is deliberate: every added tab
  competes with the core loop.
- **Tonight card** is the largest element on This Week from 2pm onward (time-aware
  emphasis); before 2pm the week strip leads.
- Meal Detail opens as a **bottom sheet**, not a page — keeps the week visible behind it,
  reinforcing "you're editing the week, not browsing recipes."
- Repair proposals render as a **before/after diff of the week strip** with a single
  Confirm — the user always approves AI changes (matches FR-23).

## 3. Content hierarchy & object model

| Object | Where it lives | Notes |
|---|---|---|
| **Plan (week)** | This Week | The root object; one active per household |
| **Plan entry** | Week strip | Meal, Leftovers, Eating-out, or Empty — all first-class states |
| **Recipe** | Only inside Meal Detail / Cook Mode | No global recipe browser in v1 (anti-goal) |
| **Grocery list** | Grocery tab | Always derived from the active plan + manual items |
| **Feedback** | Attached to plan entries | Never a separate "history" surface in v1 |
| **Taste profile** | Invisible | Surfaced only as "because you liked X" one-liners on suggestions |

## 4. State variants each surface must handle

- **This Week:** no plan yet (first run / new week) · plan active · week complete (recap
  teaser) · repair pending (diff view) · generation in progress (streamed skeleton).
- **Grocery List:** empty (no plan) · active · offline (cached, sync-pending badge) ·
  shared-view (read-only, no auth).
- **Tonight card:** meal night · leftovers night · eating-out night · nothing planned
  ("Want a quick suggestion?") · feedback owed for yesterday (gentle, dismissible).

## 5. Notification & email touchpoints (v1: email only, PWA has no reliable push)

| Trigger | Channel | Content |
|---|---|---|
| Plan day (user-chosen, default Sun 10am) | Email | "Your week is ready to plan" → deep-link |
| Weekly recap | Email + in-app | Recap summary |
| Feedback nudge | In-app only | Never email someone about a skipped meal (tone rule FR-24) |
