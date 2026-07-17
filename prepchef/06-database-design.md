# 06 — Database Design (Postgres / Supabase)

Principles: **household is the tenant** (RLS boundary) even while v1 UX is single-user —
retrofitting multi-tenancy is brutal, doing it now is ~free. **Recipes/ingredients are
content** (admin-written, world-readable when published); **plans/feedback are tenant
data**. All nutrition numbers live in content tables and are computed by code — the LLM
never writes numbers. Enums as Postgres enums; `timestamptz` everywhere; soft business
data (generation logs) partitioned later if needed.

## 1. Entity overview

```
auth.users ─ profiles ─┐
                       ├─ households ─┬─ meal_plans ─┬─ plan_entries ─ meal_feedback
                       │              │              ├─ prep_sessions ─ prep_tasks
                       │              │              └─ grocery_lists ─ grocery_items
                       │              ├─ preference_signals
                       │              ├─ nutrition_targets
                       │              └─ subscriptions
CONTENT: ingredients ─ ingredient_locales
         recipes ─ recipe_ingredients ─→ ingredients
                └ recipe_locales, recipe_tags
         locales, breakfast_templates
OPS:     generation_logs, eval_cases
```

## 2. Schema (DDL sketch)

```sql
-- ===== Tenancy & profile =====
create table households (
  id uuid primary key default gen_random_uuid(),
  locale_code text not null references locales(code),
  adults smallint not null default 1 check (adults between 1 and 12),
  kids smallint not null default 0 check (kids between 0 and 12),
  budget_band smallint not null default 2 check (budget_band between 1 and 3),
  staples_removed text[] not null default '{}',   -- deviations from locale default staples
  staples_added   text[] not null default '{}',
  created_at timestamptz not null default now()
);

create table profiles (                -- 1:1 with auth.users
  user_id uuid primary key references auth.users(id) on delete cascade,
  household_id uuid not null references households(id),
  display_name text,
  sex text not null check (sex in ('male','female')),         -- for BMR only
  birth_year smallint not null,
  height_cm numeric(5,1) not null,
  weight_kg numeric(5,1) not null,
  goal text not null check (goal in ('lose','maintain','gain','health')),
  activity_level smallint not null check (activity_level between 1 and 5),
  diet_preference text not null default 'none',   -- none|vegetarian|vegan|pescatarian|halal|kosher_style|gluten_free|dairy_free
  allergies text[] not null default '{}',          -- canonical allergen keys; '{}' means explicitly none
  cooking_skill smallint not null default 2 check (cooking_skill between 1 and 3),
  time_budget_min_per_week smallint not null default 240,
  has_oven boolean not null default true,
  has_blender boolean not null default true,
  has_microwave boolean not null default true,
  units text not null default 'metric' check (units in ('metric','imperial')),
  onboarded_at timestamptz,
  created_at timestamptz not null default now()
);

create table nutrition_targets (       -- append-only snapshots; latest = active
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references profiles(user_id) on delete cascade,
  bmr_kcal int not null, tdee_kcal int not null,
  kcal int not null, protein_g int not null, carbs_g int not null, fat_g int not null,
  method text not null default 'mifflin_v1',
  inputs jsonb not null,               -- snapshot of weight/goal/etc used
  created_at timestamptz not null default now()
);

-- ===== Content: locales & ingredients =====
create table locales (
  code text primary key,               -- 'pk', 'us'
  name text not null,
  default_units text not null,
  currency text not null,
  halal_default boolean not null default false,
  default_staples text[] not null,     -- canonical ingredient keys
  eating_out_benchmark numeric(8,2),   -- per-meal cost benchmark for recap estimates
  active boolean not null default false
);

create table ingredients (
  id uuid primary key default gen_random_uuid(),
  key text unique not null,            -- 'chicken_breast'
  name text not null,
  category text not null check (category in
    ('produce','protein','dairy','pantry','frozen','spices','other')),
  default_unit text not null,          -- 'g','ml','unit'
  unit_conversions jsonb not null default '{}',  -- {'cup': 240, 'tbsp': 15, ...} → default_unit
  kcal_per_100 numeric(7,2), protein_per_100 numeric(6,2),
  carbs_per_100 numeric(6,2), fat_per_100 numeric(6,2),
  allergen_keys text[] not null default '{}',
  diet_flags text[] not null default '{}',       -- 'vegetarian','vegan','halal_ok',...
  perishability smallint not null default 2 check (perishability between 1 and 3)
);

create table ingredient_locales (
  ingredient_id uuid references ingredients(id),
  locale_code text references locales(code),
  local_name text,                     -- 'coriander' vs 'cilantro' vs 'dhania'
  availability smallint not null check (availability between 0 and 3), -- 0 none…3 everywhere
  cost_band smallint check (cost_band between 1 and 3),
  seasonal_months smallint[],
  primary key (ingredient_id, locale_code)
);

-- ===== Content: recipes =====
create table recipes (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  status text not null default 'draft' check (status in ('draft','review','published','retired')),
  meal_roles text[] not null,          -- {'lunch','dinner'} ; breakfast templates separate
  cuisine text not null,
  instructions jsonb not null,         -- ordered steps, our own prose
  prep_min smallint not null, cook_min smallint not null,
  difficulty smallint not null check (difficulty between 1 and 3),
  base_servings smallint not null,
  batch_friendly boolean not null default false,
  batch_max_servings smallint,         -- how far it scales sensibly
  requires_oven boolean not null default false,
  requires_blender boolean not null default false,
  freezer_safe boolean not null default false,
  storage_notes text, reheat_notes text,
  image_path text,
  -- computed by content pipeline from recipe_ingredients (per base serving):
  kcal int, protein_g numeric(6,1), carbs_g numeric(6,1), fat_g numeric(6,1),
  diet_flags text[] not null default '{}',       -- computed ∩ human-verified
  allergen_keys text[] not null default '{}',
  flags_verified_by uuid, flags_verified_at timestamptz,  -- FR-36 human gate
  created_at timestamptz not null default now()
);

create table recipe_ingredients (
  recipe_id uuid references recipes(id) on delete cascade,
  ingredient_id uuid references ingredients(id),
  qty numeric(8,2) not null, unit text not null,
  prep_note text, optional boolean not null default false,
  substitution_ids uuid[] not null default '{}', -- curated swaps
  primary key (recipe_id, ingredient_id)
);

create table recipe_locales (          -- materialized by content pipeline
  recipe_id uuid references recipes(id) on delete cascade,
  locale_code text references locales(code),
  availability_score numeric(3,2) not null,      -- min/weighted ingredient availability
  cost_band smallint not null,
  servable boolean not null,                     -- score ≥ threshold
  primary key (recipe_id, locale_code)
);

create table breakfast_templates (
  id uuid primary key default gen_random_uuid(),
  title text not null, locale_codes text[] not null,
  kcal int not null, protein_g int not null, carbs_g int not null, fat_g int not null,
  instructions jsonb not null, diet_flags text[] not null default '{}',
  allergen_keys text[] not null default '{}'
);

-- ===== Planning =====
create table meal_plans (
  id uuid primary key default gen_random_uuid(),
  household_id uuid not null references households(id),
  week_start date not null,
  status text not null default 'active' check (status in ('draft','active','completed','abandoned')),
  breakfast_template_ids uuid[] not null default '{}',
  generation_id uuid,                  -- latest generation_logs row
  created_at timestamptz not null default now(),
  unique (household_id, week_start)
);

create table prep_sessions (
  id uuid primary key default gen_random_uuid(),
  plan_id uuid not null references meal_plans(id) on delete cascade,
  scheduled_date date not null,
  status text not null default 'upcoming' check (status in ('upcoming','in_progress','done','skipped')),
  est_total_min smallint
);

create table prep_tasks (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references prep_sessions(id) on delete cascade,
  position smallint not null,
  description text not null,
  recipe_ids uuid[] not null default '{}',
  est_min smallint not null,
  parallel_hint text,                  -- "while rice cooks"
  done boolean not null default false
);

create table plan_entries (
  id uuid primary key default gen_random_uuid(),
  plan_id uuid not null references meal_plans(id) on delete cascade,
  entry_date date not null,
  slot text not null check (slot in ('breakfast','lunch','dinner','snack')),
  entry_type text not null check (entry_type in
    ('batch_portion','fresh_cook','breakfast_template','leftovers','eating_out','empty')),
  recipe_id uuid references recipes(id),
  breakfast_template_id uuid references breakfast_templates(id),
  prep_session_id uuid references prep_sessions(id),   -- for batch portions
  servings numeric(4,1) not null default 1,
  locked boolean not null default false,
  position smallint not null default 0,
  unique (plan_id, entry_date, slot, position)
);

create table meal_feedback (
  entry_id uuid primary key references plan_entries(id) on delete cascade,
  user_id uuid not null references profiles(user_id),
  verdict text not null check (verdict in ('ate_up','ate_down','skipped')),
  note text,
  created_at timestamptz not null default now()
);

create table preference_signals (      -- the moat; append-only
  id uuid primary key default gen_random_uuid(),
  household_id uuid not null references households(id),
  subject_type text not null check (subject_type in ('recipe','ingredient','cuisine')),
  subject_key text not null,           -- recipe id / ingredient key / cuisine name
  signal text not null check (signal in
    ('onboard_like','onboard_dislike','ate_up','ate_down','skipped','swapped_out','swapped_in','excluded')),
  weight numeric(4,2) not null,
  created_at timestamptz not null default now()
);
create index on preference_signals (household_id, subject_type, subject_key);

-- ===== Grocery =====
create table grocery_lists (
  id uuid primary key default gen_random_uuid(),
  plan_id uuid unique not null references meal_plans(id) on delete cascade,
  share_token text unique             -- nullable until shared
);

create table grocery_items (
  id uuid primary key default gen_random_uuid(),
  list_id uuid not null references grocery_lists(id) on delete cascade,
  ingredient_id uuid references ingredients(id),   -- null for manual items
  display_name text not null,
  qty numeric(8,2), unit text,
  category text not null,
  source text not null default 'plan' check (source in ('plan','manual')),
  state text not null default 'needed' check (state in ('needed','checked','already_have')),
  checked_at timestamptz,
  updated_at timestamptz not null default now()    -- offline sync: last-write-wins per item
);

-- ===== Ops / AI =====
create table generation_logs (
  id uuid primary key default gen_random_uuid(),
  household_id uuid not null,
  plan_id uuid,
  kind text not null check (kind in ('generate','swap','shuffle','repair','assistant')),
  prompt_version text not null,
  model text not null,
  input_snapshot jsonb not null,       -- profile, targets, candidate ids, constraints
  output jsonb not null,               -- chosen recipe ids / ops diff
  input_tokens int, output_tokens int, latency_ms int,
  violation_check jsonb not null,      -- validator result (must be clean to serve)
  created_at timestamptz not null default now()
);

create table subscriptions (
  household_id uuid primary key references households(id),
  stripe_customer_id text, stripe_subscription_id text,
  tier text not null default 'free' check (tier in ('free','plus')),
  status text, trial_ends_at timestamptz, current_period_end timestamptz
);
```

## 3. Row-level security (Supabase)

- `profiles`: user reads/writes own row.
- Household-scoped tables (`households, meal_plans, plan_entries, prep_*, grocery_*,
  meal_feedback, preference_signals, nutrition_targets, subscriptions`): access iff
  `household_id in (select household_id from profiles where user_id = auth.uid())` —
  one shared `is_household_member(hid)` security-definer function.
- Content tables (`recipes, ingredients, *_locales, breakfast_templates, locales`):
  `select` for all authenticated users **where `status='published'`/`servable`**; writes
  via service role (content pipeline) only.
- `grocery_lists` share: an edge function resolves `share_token` → read-only item view
  (+ check-off) without auth; token is revocable (null it).
- `generation_logs`: service role only.

## 4. Key access patterns (sanity-checking the schema)

1. **Candidate set for generation** (one query, no LLM): published recipes joined to
   `recipe_locales` (servable, locale), filtered by diet_flags ⊇ prefs, allergens ∩
   allergies = ∅, equipment booleans, difficulty ≤ skill, batch_friendly, time fits →
   typically 60–150 rows with macros, cost band, ingredient ids — small enough to score
   in code and hand the top ~40 to the LLM as a compact table.
2. **Grocery consolidation** (pure SQL + code): `plan_entries → recipe_ingredients`,
   scale by servings, convert units via `unit_conversions`, group by ingredient, subtract
   `locales.default_staples ± household deltas`, group by category.
3. **Taste profile at generation time**: aggregate `preference_signals` by subject with
   time-decayed weights → per-recipe/ingredient/cuisine scores; computed in code, cached
   on the household between feedback events.
4. **Repair**: current week's entries + `grocery_items.state='checked'` (what's bought) →
   reflow candidates constrained to purchased perishables first.
5. **Adherence view (Today)**: sum planned entries' macros for today vs latest
   `nutrition_targets` — no logging table needed, by design.

## 5. Migrations & seed strategy

- Supabase CLI migrations in-repo from day one; every schema change is a migration file.
- Seed pipeline (M1): CSV/JSON recipe + ingredient sources → validation script (units
  resolve, macros compute, allergens present) → `recipe_locales` materialization →
  human verification flags → publish. The pipeline is code in this repo, not a manual
  admin UI (v1 has no CMS; a CMS is v1.x if content velocity demands it).
- `pgvector` deliberately **not** in v1: candidate filtering is fully relational; add
  embeddings in v1.x if free-text taste matching needs it.
