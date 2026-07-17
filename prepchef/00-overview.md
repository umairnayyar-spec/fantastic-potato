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

## Working assumptions (important)

The kickoff prompt contained a placeholder — `[PASTE THE FULL PRODUCT VISION HERE]` — that was
never filled in, and no vision document exists in this repository. Everything below is built
from the one-paragraph summary that *was* provided:

> PrepChef is an AI-powered weekly meal planning platform that helps users eat healthier,
> save money, reduce food waste, and remove the daily stress of deciding what to eat.

Assumptions made in the absence of the full vision doc:

1. **Target user:** busy adults/households cooking dinner at home 3–6 nights a week, not
   professional chefs and not macro-tracking athletes.
2. **Business model:** consumer subscription (freemium), with grocery affiliate revenue as a
   later option.
3. **Initial market:** English-speaking, single currency/measurement locale at launch.
4. **Team:** two founders (one technical), no dedicated content or ops staff at launch.
5. **Platform:** mobile-first responsive web app first; native apps later.

If the full vision contradicts any of these — particularly target user or business model —
the MVP scope (doc 02) and roadmap (doc 08) should be revisited first; the architecture
(docs 06–07) is deliberately built to survive those pivots.
