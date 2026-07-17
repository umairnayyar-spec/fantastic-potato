# PrepChef — Product Strategy & Architecture

This document set is the pre-code deliverable for PrepChef: product critique, MVP definition,
PRD, information architecture, user flows, database design, technical architecture, and
implementation roadmap.

## Documents

| Doc | Contents |
|---|---|
| [01-product-critique.md](01-product-critique.md) | Critique, weaknesses, improvements, missing features |
| [02-mvp-scope.md](02-mvp-scope.md) | Recommended MVP and explicit v1 exclusions |
| [03-prd.md](03-prd.md) | Product Requirements Document for v1 |
| [04-information-architecture.md](04-information-architecture.md) | Screens, navigation, content hierarchy |
| [05-user-flows.md](05-user-flows.md) | Core user flows (onboarding, planning, shopping, feedback) |
| [06-database-design.md](06-database-design.md) | Postgres schema, entity relationships, key queries |
| [07-technical-architecture.md](07-technical-architecture.md) | System design, AI pipeline, infra, cost controls |
| [08-roadmap.md](08-roadmap.md) | Milestone-based implementation roadmap |

## Vision basis

Docs 01–04 were first drafted against a one-paragraph vision; the founder subsequently
provided the **full product vision** (health/macro targets, all meals, meal prep as the
cooking model, localization as a headline strength, AI assistant, Next.js + Supabase
stack). The document set has been reconciled with that fuller vision:

- **01-product-critique.md** keeps the original critique and adds an addendum critiquing
  the expanded vision specifically.
- **02–08** are written against the *reconciled* scope: the founder's vision, minus the
  pieces argued out in the critique, plus the retention mechanics (plan repair, feedback
  loop) the original critique established.

Key reconciled positions (details and reasoning in docs 01–02):

1. **Cooking model:** meal-prep-first — 1–2 batch cook sessions covering the week's
   lunches + dinners — per the founder's vision. This replaces the earlier dinner-only
   recommendation.
2. **Nutrition:** BMR/TDEE/macro *targets* and per-meal macros are in (deterministic math,
   core to the gym-goer/health segment). Food *logging/tracking* stays out — PrepChef is a
   decider, not a tracker.
3. **Localization:** in as a v1 differentiator, but as curated **locale packs** (launch:
   Pakistan + United States), not as an "any country" promise.
4. **Breakfast:** simple rotation templates, not full generation. Snacks: suggested list
   only.
5. **AI assistant:** in, but as a constrained command layer over structured plan
   operations — not open-ended chat.
6. **Business model (unchanged assumption):** freemium subscription; single language
   (English) at launch across both locale packs.
