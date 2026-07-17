# 05 — User Flows

Conventions: `→` screen transition · `[ ]` decision · `( )` system action · **bold** =
moment that must feel great. Error/edge handling is listed per flow.

## Flow 1 — Onboarding → first plan (target ≤ 4 min + generation)

```
Landing → Sign up [Google | email]
  → Body & goal (age, height, weight, sex, goal, activity)
  → (compute BMR/TDEE/macros)
  → **Targets reveal** — "To lose ~0.5 kg/week: 1,850 kcal, 140g protein" [Adjust | Looks good]
  → Food rules: diet preference · allergies (must pick "None" explicitly)
  → Tastes: like/dislike chips (locale-ordered, skippable)
  → Practicalities: household · budget band · skill · time/wk · equipment (3 toggles)
      · country → (locale pack + units set)
  → Prep style: [1 session | 2 sessions] + day picker · breakfast templates (pick 2–3)
  → (generate plan — streamed: prep sessions appear, then days fill in)
  → **First plan revealed** → coach-marks: swap, lock, assistant bar → Plan
```
Edges: OAuth fail → email path; generation timeout → retry with cached candidate set;
allergy step cannot be skipped; every other step has sane defaults.

## Flow 2 — Weekly planning (returning user; target ≤ 5 min total)

```
Email "ready to plan" → Plan (new-week state, last week's structure prefilled)
  → [keep prep days? tweak?] → Generate (streamed)
  → Review: [happy] → done
     [not happy with a meal] → Meal sheet → Replace (3 alts) | Regenerate + note
     [wrong shape] → assistant: "make Wednesday lighter" → diff → Confirm
     [rare] → Regenerate week (1×)
  → Groceries auto-updates → done
```

## Flow 3 — Plan flexibility (vision's five verbs)

```
Replace:   Meal sheet → Replace → (3 filtered alternatives w/ macros & cost) → pick → (macros+list update)
Move:      Meal sheet → Move day → day picker → (day totals recompute)
Lock:      Meal card lock toggle → (survives shuffle/regenerate)
Shuffle:   Plan overflow menu → Shuffle unlocked → (re-sequence, no new recipes)
Regen one: Meal sheet → Regenerate [+ optional note "spicier"] → new meal → [Undo]
```
Edge: an alternative violating time/budget prefs never appears; hard filters absolute.

## Flow 4 — Grocery shopping

```
Groceries → (list = plan − staples, consolidated & scaled)
  → [share to partner?] → read-only link (no login)
  → in store: check off items (offline-safe; syncs later)
  → [item unavailable] → Meal sheet from item's "used in" chip → Replace meal
       → (list updates; checked items preserved under "already bought")
  → [+ Add item] manual rows
Print: Groceries → Print → print stylesheet (grouped, checkboxes)
```

## Flow 5 — Prep day (hero flow #1)

```
Email "prep day" → Today ("Today you cook for the week" state) → Start prep
  → Prep Mode: ordered tasks with time estimates
     ("1. Rice on — 25 min ▸ 2. While rice cooks: sear chicken ▸ …")
  → step-through, check off tasks → **Session done — "You just cooked 8 meals"**
  → (batches marked available; storage instructions per batch)
Edges: [ran out of time mid-session] → "Save progress" → remaining tasks proposed for
tonight or next session (repair engine); [missing ingredient] → substitution suggestion
from curated data or meal replacement.
```

## Flow 6 — Daily follow + feedback (the retention habit)

```
Open app (or recap email link) → Today
  → meals of the day → [tap] → Recipe → [Cook Mode if fresh-cook | reheat notes if batch]
  → evening / next open: **one-tap feedback** Ate it 👍 / Ate it 👎 / Skipped
     → [👎] optional one-line why → (preference profile updates)
Feedback owed accumulates quietly (max 1 prompt/day, dismissible; never emailed).
```

## Flow 7 — Mid-week repair (hero flow #2)

```
A. One-tap:  Meal or prep card → "Didn't happen"
   → (reflow: prioritize bought perishables; ≤1 meal rolls forward; list coherent)
   → **before/after diff** → Confirm | Undo
B. Free-text: Plan → assistant bar → "we ate out twice, prep ran out" | "I only have eggs"
   → (intent parse → repair op → candidate reflow under hard filters)
   → diff → Confirm
C. Unparseable/out-of-scope → "Here's what I can do" menu (replace · exclude · time ·
   calories · fix my week) — never a fake action.
Tone: zero guilt copy anywhere in this flow (FR-31).
```

## Flow 8 — Assistant command examples (acceptance tests)

| Input | Parsed op | Result surface |
|---|---|---|
| "Replace Thursday dinner" | replace(entry=Thu dinner) | 3 alternatives |
| "I don't want chicken this week" | exclude(chicken, week) + regen affected | diff |
| "I only have 20 minutes" (on a day) | time_constrain(day, 20) | swap proposal |
| "meals under 500 calories" | macro_constrain(≤500 kcal) | filtered swaps |
| "I only have eggs" | repair(available=[eggs]) | tonight fix + week reflow diff |

## Flow 9 — Weekly recap → next week

```
Sunday evening: recap email → Recap
  → meals eaten · prep done · protein adherence · utilization · est. savings (labeled)
  → **"Plan next week"** → Flow 2 (with taste profile improved)
```

## Flow 10 — Upgrade

```
Free user hits 4th swap → gentle sheet: "You've used this week's included swaps.
PrepChef Plus: unlimited changes." → [Start 14-day trial] → Stripe checkout → unlocked
Never gated: repair, feedback, grocery list, prep mode.
```

## Flow 11 — Settings changes that affect the plan

```
Settings → change (e.g. vegetarian on, budget down, weight update)
  → (targets recompute where relevant — shown as a diff: "protein 140g → 132g")
  → [active plan conflicts? e.g. now-vegetarian week] →
     "Your current week has 4 meals that no longer fit — regenerate them?" [Yes | keep this week]
```
