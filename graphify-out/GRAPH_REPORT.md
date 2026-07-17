# Graph Report - .  (2026-07-17)

## Corpus Check
- Corpus is ~33,096 words - fits in a single context window. You may not need a graph.

## Summary
- 124 nodes · 169 edges · 11 communities (9 shown, 2 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.89)
- Token cost: 150,850 input · 12,500 output

## Community Hubs (Navigation)
- Graphify Skill & References
- Job-Search Agent & Skills
- PrepChef Retention & Repair Loop
- PrepChef Product Strategy Docs
- PrepChef Planning & Prep Features
- Career Data & Handoff Files
- Travel Site Frontend Code
- Umrah Landing Page Content
- PrepChef Data Model & RLS
- Weekly Recap
- Repo README

## God Nodes (most connected - your core abstractions)
1. `Graphify Skill Pipeline` - 16 edges
2. `Product Requirements Document (v1)` - 12 edges
3. `Job-Hunter Agent (Reverse Recruiter)` - 11 edges
4. `PrepChef Overview` - 8 edges
5. `Outreach Skill (Reverse Recruiting)` - 7 edges
6. `Application Pipeline Tracker` - 7 edges
7. `Implementation Roadmap` - 7 edges
8. `Application Tracker (Single Source of Truth)` - 6 edges
9. `Apply Skill (Form Filling with Review Pause)` - 6 edges
10. `Session Handoff Protocol` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Human-Approval Guardrails` --semantically_similar_to--> `Diff Confirmation Pattern`  [INFERRED] [semantically similar]
  career/README.md → prepchef/04-information-architecture.md
- `Master Resume (Source of Truth)` --semantically_similar_to--> `Curated Recipe Corpus`  [INFERRED] [semantically similar]
  career/profile/master-resume.md → prepchef/01-product-critique.md
- `Job Scoring Rubric` --semantically_similar_to--> `AI Planning Pipeline`  [INFERRED] [semantically similar]
  career/profile/preferences.md → prepchef/07-technical-architecture.md
- `Search Playbook` --semantically_similar_to--> `Household Preference Graph`  [INFERRED] [semantically similar]
  career/search-playbook.md → prepchef/01-product-critique.md
- `Travel Wide Umrah Landing Page` --conceptually_related_to--> `Candidate Profile (career/profile/profile.md)`  [INFERRED]
  index.html → .claude/agents/job-hunter.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Reverse-Recruiting Workflow (Source-Tailor-Apply-Outreach-Track)** — claude_agents_job_hunter_job_hunter, claude_skills_find_jobs_skill_find_jobs, claude_skills_tailor_resume_skill_tailor_resume, claude_skills_apply_skill_apply, claude_skills_outreach_skill_outreach, claude_skills_pipeline_skill_pipeline [EXTRACTED 1.00]
- **Human-in-the-Loop Approval Gates** — claude_agents_job_hunter_human_approval_gate, claude_skills_apply_skill_submit_review_checkpoint, claude_skills_outreach_skill_approval_required_sending_policy, claude_skills_optimize_linkedin_skill_supervised_editing_consent [INFERRED 0.85]
- **Graphify Pipeline and Its Reference Documents** — claude_skills_graphify_skill_graphify, claude_skills_graphify_references_add_watch_add_and_watch, claude_skills_graphify_references_exports_export_targets, claude_skills_graphify_references_extraction_spec_subagent_prompt, claude_skills_graphify_references_github_and_merge_clone_and_merge, claude_skills_graphify_references_hooks_hooks_reference, claude_skills_graphify_references_query_query_flows, claude_skills_graphify_references_transcribe_whisper_transcription, claude_skills_graphify_references_update_incremental_update [EXTRACTED 1.00]
- **PrepChef Retention Mechanism** — prepchef_01_product_critique_plan_repair, prepchef_01_product_critique_feedback_loop, prepchef_01_product_critique_household_preference_graph, prepchef_03_prd_weekly_recap [EXTRACTED 1.00]
- **Career Profile Source of Truth** — career_profile_profile, career_profile_preferences, career_profile_master_resume [EXTRACTED 1.00]
- **Zero-Violation Correctness System** — prepchef_03_prd_hard_filters, prepchef_07_technical_architecture_eval_harness, prepchef_07_technical_architecture_greedy_fallback, prepchef_06_database_design_generation_logs [EXTRACTED 1.00]

## Communities (11 total, 2 thin omitted)

### Community 0 - "Graphify Skill & References"
Cohesion: 0.09
Nodes (29): Graphify Slash Command Registration, Project Graphify Rules (Root CLAUDE.md), Add-URL & Watch Reference, Export Targets Reference (Wiki/Neo4j/FalkorDB/SVG/GraphML), Graphify MCP Server (graphify.serve), Discrete Confidence Rubric (Anti-Bimodal-Collapse), Deterministic Node-ID Format (Full-Path Stem), Extraction Subagent Prompt Spec (+21 more)

### Community 1 - "Job-Search Agent & Skills"
Cohesion: 0.15
Nodes (23): Application Tracker (Single Source of Truth), Master Resume (master-resume.md), Job Preferences & Scoring Rubric (preferences.md), Candidate Profile (career/profile/profile.md), Job-Search Playbook (Accumulated Round Learnings), Human Approval Gate (Submit/Send Reserved for Candidate), Job-Hunter Agent (Reverse Recruiter), Reverse-Recruiting Loop (6 Stages) (+15 more)

### Community 2 - "PrepChef Retention & Repair Loop"
Cohesion: 0.13
Nodes (16): Search Playbook, Curated Recipe Corpus, Cooked/Skipped Feedback Loop, Household Preference Graph, Locale Packs, Plan Repair System, Stress-Removal Wedge, MVP Core Loop (+8 more)

### Community 3 - "PrepChef Product Strategy Docs"
Cohesion: 0.26
Nodes (15): PrepChef Overview, Product Critique, Cost Bands, Tracker Trap, MVP Scope & v1 Exclusions, Cut-Line Discipline, Product Requirements Document (v1), Nutrition Targets Engine (Mifflin-St Jeor) (+7 more)

### Community 4 - "PrepChef Planning & Prep Features"
Cohesion: 0.15
Nodes (14): Job Scoring Rubric, Constrained AI Assistant, Meal-Prep-First Cooking Model, AI Assistant Command Layer, Consolidated Grocery List, Hard Filters (Diet & Allergen), Weekly Plan Generation, Prep Schedule (+6 more)

### Community 5 - "Career Data & Handoff Files"
Cohesion: 0.38
Nodes (10): Application Pipeline Tracker, Session Handoff Protocol, LinkedIn Profile Copy, Motive Outreach Draft, Master Resume (Source of Truth), Job Search Preferences, Candidate Profile, Human-Approval Guardrails (+2 more)

### Community 6 - "Travel Site Frontend Code"
Cohesion: 0.25
Nodes (7): form, hamburger, navbar, navLinks, observer, revealItems, success

### Community 7 - "Umrah Landing Page Content"
Cohesion: 0.50
Nodes (4): Booking Enquiry Contact Form, Detailed Hotel Pricing Table (15/21 Days, ISB-JED), Travel Wide Umrah Landing Page, Umrah Package Tiers (Economy / Economy Plus / Premium)

### Community 8 - "PrepChef Data Model & RLS"
Cohesion: 0.67
Nodes (3): Household-Centric Data Model, households (tenant table), Row-Level Security Model

## Knowledge Gaps
- **31 isolated node(s):** `navbar`, `hamburger`, `navLinks`, `form`, `success` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Work Memory (save-result Feedback Loop & LESSONS.md)` connect `Graphify Skill & References` to `Job-Search Agent & Skills`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Product Requirements Document (v1)` (e.g. with `Cost Bands` and `Cooked/Skipped Feedback Loop`) actually correct?**
  _`Product Requirements Document (v1)` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `navbar`, `hamburger`, `navLinks` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Graphify Skill & References` be split into smaller, more focused modules?**
  _Cohesion score 0.08620689655172414 - nodes in this community are weakly interconnected._
- **Should `Job-Search Agent & Skills` be split into smaller, more focused modules?**
  _Cohesion score 0.14624505928853754 - nodes in this community are weakly interconnected._
- **Should `PrepChef Retention & Repair Loop` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._