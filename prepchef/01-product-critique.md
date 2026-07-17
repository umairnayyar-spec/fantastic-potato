# 01 — Product Critique

You asked me to challenge assumptions, so I will. The honest starting point: **meal planning
is a graveyard category.** Mealime, PlateJoy, eMeals, Eat This Much, Paprika, Whisk (now
Samsung Food), and dozens of dead startups have all built "personalized weekly meal plans
with a grocery list." The concept demos beautifully and retains terribly. Users churn in
2–6 weeks. If we build "the same thing but with an LLM," we inherit the same churn curve
with higher COGS. The critique below is organized around why those products die and what
PrepChef must do differently.

## 1. Core critique

### 1.1 Four value props is zero value props

"Eat healthier, save money, reduce waste, remove stress" are four different products with
four different buyers:

- **Eat healthier** → competes with MyFitnessPal/Noom; buyer wants tracking and accountability.
- **Save money** → competes with Flipp/store loyalty apps; buyer wants price comparison.
- **Reduce waste** → an outcome, not a motivation; nobody downloads an app to reduce waste,
  they feel good when it happens as a side effect.
- **Remove daily stress** → the actual felt pain ("what's for dinner?" at 4pm) and the only
  one of the four that is *daily* and *emotional*.

**Position on stress-removal as the wedge.** "We decide what's for dinner so you don't have
to." Money saved and waste reduced become *measurable proof* the product surfaces
("you saved ~$34 and used everything you bought this week"), and "healthier" becomes a
default bias of the plans, not a tracking feature. This matters for every downstream
decision: onboarding questions, home screen, metrics, marketing.

### 1.2 The retention killer is the plan-vs-reality gap

Every competitor fails the same way: Monday's plan meets Wednesday's reality. The user got
home late, ate out, has leftovers, is exhausted. A rigid weekly plan now induces *guilt* —
the product that promised to remove stress is generating it. The user quietly stops opening
the app.

The differentiating insight: **the product is not a plan generator, it is a plan *repair*
system.** "I didn't cook Tuesday" must be a one-tap, judgment-free action that reflows the
rest of the week (tonight's meal uses the perishables first, one meal rolls forward, the
grocery list doesn't break). Competitors treat deviation as an edge case; PrepChef should
treat it as the main case. This is genuinely where an LLM adds value over the rule engines
competitors use — replanning under messy, natural-language constraints ("we have half a
roast chicken left and I have 20 minutes") is exactly what LLMs are good at and rule
engines are terrible at.

### 1.3 "AI-powered" is not a moat

Any competitor can call the same APIs we can. The defensible assets are:

1. **The household preference graph** — what this specific household actually cooked,
   skipped, swapped, and rated, accumulated over months. Week 12's plan should be
   dramatically better than week 1's, and that data doesn't port to a competitor.
2. **A curated, tested recipe corpus** with structured, normalized ingredients (which is
   what makes grocery-list consolidation and plan repair actually work).

The LLM is the interface and the constraint-solver, not the moat. Plan accordingly.

### 1.4 The two hardest promises are "save money" and "reduce waste"

- **Save money** literally requires grocery price data. There is no good general API for
  store-level prices; partnerships (Instacart/Kroger APIs) are slow, region-limited, and
  wrong for an MVP. Do not promise dollar-exact savings in v1.
- **Reduce waste** literally requires knowing what's in the pantry. Manual pantry inventory
  is the single most-abandoned feature in this category — users will not scan or type their
  fridge contents twice. In v1, waste reduction must come *structurally*: plans that share
  perishable ingredients across meals (buy cilantro once, use it three times), correct
  purchase quantities, and leftover-aware scheduling. That delivers most of the benefit
  with zero user labor.

### 1.5 Recipe content is a legal and trust minefield

- **Scraping** recipes from the web is legally grey and produces garbage-quality structured
  data.
- **Pure LLM-generated recipes are untested recipes.** One "that was inedible" experience
  destroys trust in the entire product. LLMs also hallucinate quantities and steps.
- The right model: a **curated seed library (~300–500 recipes)** — public-domain,
  commissioned, or licensed — with rigorously structured ingredient data. The AI *selects,
  sequences, scales, and adapts* from this corpus; it does not invent recipes in v1.
  (Recipe *instructions* as such are not copyrightable in the US, but creative descriptions
  and photos are — so we rewrite instructions and use our own or stock imagery.)

### 1.6 Households, not users

Dinner is a household decision. One picky kid vetoes a plan for four people. If the model
is single-user, the product fails for exactly the segment (busy families) that needs it
most and pays best. The data model must be household-centric from day one — this is cheap
to do at the schema level now and brutally expensive to retrofit.

### 1.7 Unit economics of "AI-powered"

If every plan generation, swap, and repair is a large-context LLM call, COGS scales with
engagement — the inverse of a healthy subscription. The architecture must make the common
path cheap: retrieval + a small structured LLM call for selection, caching, and batch
generation. Target well under $0.30/user/month in inference at MVP usage patterns
(detailed in doc 07).

## 2. Weaknesses (summary)

1. Undifferentiated positioning in a high-churn category; four diluted value props.
2. Two of the four promises (price savings, waste tracking) are not deliverable in v1.
3. No stated retention mechanism; weekly planning is a chore users abandon.
4. "AI-powered" as identity rather than as means; no data moat articulated.
5. Recipe content sourcing unaddressed (legal risk + quality risk).
6. Household complexity unaddressed (multi-member preferences, conflicts, kids).
7. No monetization stated; category has strong subscription fatigue.
8. Inference cost model unexamined.
9. No plan for the cold-start problem (week-1 plan quality before any feedback exists).

## 3. Suggested improvements

1. **Reposition:** "PrepChef decides what's for dinner." Stress removal is the promise;
   savings and waste are surfaced as weekly proof metrics.
2. **Make plan repair the hero feature.** One-tap "didn't cook it," natural-language
   mid-week adjustments, guilt-free tone throughout.
3. **Effort-minimal onboarding:** 6–8 taps (household size, dietary constraints, hard
   dislikes, time budget, skill level, cuisines) — not a 40-question quiz. Learn the rest
   from behavior.
4. **Close the feedback loop cheaply:** after each planned meal, a single prompt —
   Cooked it 👍 / Cooked it 👎 / Skipped. Three buttons, no forms. This feeds the
   preference graph (the moat).
5. **Structural waste reduction** instead of pantry inventory: ingredient-overlap
   optimization in plan generation, plus a static "pantry staples" checklist (things we
   assume you have: oil, salt, flour…) that users can edit once.
6. **Dinner-only in v1.** Dinner is the stressful decision. Breakfast/lunch dilute effort.
7. **Weekly proof-of-value moment:** a Sunday recap — meals cooked, estimated money saved
   vs. takeout, ingredients fully used. This is the retention and word-of-mouth engine.
8. **Cold start:** seed week-1 quality with a short "pick 8 meals you'd happily eat" swipe
   during onboarding — doubles as taste-profile bootstrapping and a delightful first-run.

## 4. Missing features (not in the stated vision, needed eventually)

| Feature | Why it matters | When |
|---|---|---|
| Plan repair / mid-week reflow | The retention mechanism (see 1.2) | **MVP** |
| Cooked/skipped feedback loop | Builds the preference moat | **MVP** |
| Consolidated grocery list w/ unit normalization | The plan is useless without it | **MVP** |
| Pantry-staples assumption list | Cheap waste/cost win, no inventory burden | **MVP** |
| Household member profiles & conflict handling | Families are the paying segment | **MVP (lightweight)** |
| Leftovers as first-class plan entries | Reality of home cooking | MVP-lite (auto "leftovers night" slot) |
| Batch-prep / cook-once-eat-twice mode | Popular behavior, differentiator | v1.x |
| Grocery delivery integration (Instacart etc.) | Convenience + affiliate revenue | v2 |
| Real price data / store selection | Makes "save money" literal | v2 |
| Nutrition targets (macro-level) | "Healthier" as feature, not vibe | v2 |
| Receipt/pantry photo capture (ambient inventory) | Waste reduction v2 without manual entry | v2+ |
| Native mobile apps + push notifications | Engagement channel | v2 |
| Shared household accounts (partner sees list) | Real-world shopping is delegated | v1.x |

## 5. Bottom line

The vision is pointed at a real, daily, emotional pain — that part is right. The risks are
(a) positioning blur, (b) building a plan *generator* when the market has proven you need a
plan *companion*, and (c) promising outcomes (exact savings, waste tracking) that require
data we won't have in v1. Doc 02 scopes an MVP that tests the one hypothesis that matters:
**will a household let PrepChef decide dinner for them for four consecutive weeks?**
Everything else is downstream of that answer.

---

## Addendum — critique of the full (expanded) vision

The full vision doc arrived after the critique above was written. It resolves several of my
original complaints — it names the meal-prep cooking model explicitly, makes ingredient
reuse a stated principle, and (unusually and correctly) treats localization as a first-class
strength rather than an afterthought. The Pakistan example is the sharpest product insight
in the doc: nobody serves that user well today, and "locally realistic recipes" is a real
moat because it requires curated data, not a bigger model. Keep that.

Now the pushback:

### A1. Breakfast + lunch + dinner + snack × 7 days is 28+ generated meals/week

That's 4–7× the content surface, plan complexity, and inference cost of the core problem,
and it drags plan quality down (28 good slot-fills is much harder than 10). The vision's own
cooking model — "cook once or twice for the week" — points at the fix: **generate the week
as 2 batch-cook sessions that yield the week's lunches and dinners**, treat breakfast as a
user-picked rotation of 3–4 simple templates (macro-counted, near-zero variety demand in
real behavior — people eat the same breakfast), and offer snacks as a static suggestion
list that fills remaining macros. Full daily totals still work; generation stays tractable.

### A2. The tracker trap

Macro targets, "remaining calories," and weight tracking pull the product toward
MyFitnessPal — a *tracking* product with brutal engagement demands (log every bite or the
numbers lie). PrepChef's promise is the opposite: *follow the plan and the numbers take
care of themselves*. So: compute targets, show per-meal and per-day macros on the plan,
show adherence ("you followed the plan ≈ you hit your protein") — but **no food logging,
no calorie-remaining meter, and weight tracking deferred** to v1.x as an optional weekly
weigh-in. If users must log off-plan eating for the dashboard to be honest, we've built
the wrong product.

### A3. "Localization" must mean locale packs, not a country dropdown

Real localization = per-locale ingredient availability, naming (coriander/cilantro/دھنیا),
cost bands, units, and religiously appropriate defaults. That is curated data work per
locale. Promising it for every country in a dropdown guarantees it's fake (the LLM will
happily generate "Pakistani" recipes with ingredients unavailable in Lahore). v1 ships
**two curated locale packs — Pakistan and US** — done properly: every recipe in the corpus
scored for availability per locale, halal-by-default in the PK pack, metric/imperial
handled. This is also the honest test of whether localization is the moat the vision
claims.

### A4. Estimated costs: bands, not numbers

"Estimated cost" per meal and "average grocery prices" imply price data we won't have.
Locale-relative **cost bands** (₹/₹₹/₹₹₹, $/$$/$$$) per recipe and a budget-band preference
are deliverable and useful; dollar-precise estimates are fabrications wearing a UI. Real
prices are a v2 partnership problem.

### A5. The AI assistant needs walls

"Ask anything" chat is an unbounded surface: unbounded inference cost, unbounded failure
modes, and it competes with ChatGPT, which we will lose. Every example in the vision
("replace Thursday dinner", "no chicken this week", "only 20 minutes", "under 500
calories", "I only have eggs") is a **plan operation with parameters**. Build it as intent
parsing → structured operations (swap/filter/regenerate/repair) → the same validated
pipeline, with a visible menu of what it can do. Cheaper, testable, and it can't promise
what it can't deliver.

### A6. Kitchen equipment: three booleans, not an inventory

Equipment lists are another abandonment-prone inventory. Ask what changes recipe
eligibility — oven? blender? microwave? — and stop. (In the PK locale pack, oven-free
matters a lot; that's a locale-pack default, not a 20-item checklist.)

### A7. What the expanded vision still misses (carried forward from the original critique)

Plan **repair** and the **cooked/skipped feedback loop** appear nowhere in the vision, and
they remain the retention mechanism this category always lacks. "Easily swap or regenerate"
is pre-week flexibility; *mid-week reality* (prep session skipped, batch ran out, ate out
twice) is where users churn. Both stay in the MVP as previously argued.
