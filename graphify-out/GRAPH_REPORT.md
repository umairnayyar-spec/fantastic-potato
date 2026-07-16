# Graph Report - fantastic-potato  (2026-07-16)

## Corpus Check
- 29 files · ~21,038 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 167 nodes · 139 edges · 29 communities (21 shown, 8 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59e717aa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Experience
- What You Must Do When Invoked
- Job Search Preferences
- /graphify
- LinkedIn Profile Copy — paste-ready
- Candidate Profile — Single Source of Truth
- graphify reference: extra exports and benchmark
- app.js
- Outreach draft — Motive (gomotive)
- Job-Search Agent
- graphify reference: query, path, explain
- Handoff — instructions for the next working session
- Outreach (Reverse Recruiting)
- Pipeline
- Apply to a Job
- Find Jobs
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Optimize LinkedIn
- Tailor Resume
- Application Pipeline Tracker
- job-hunter.md
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- CLAUDE.md
- CLAUDE.md
- extraction-spec.md
- README.md

## God Nodes (most connected - your core abstractions)
1. `What You Must Do When Invoked` - 12 edges
2. `/graphify` - 10 edges
3. `Job Search Preferences` - 9 edges
4. `graphify reference: extra exports and benchmark` - 8 edges
5. `LinkedIn Profile Copy — paste-ready` - 8 edges
6. `Master Resume — Source of Truth` - 8 edges
7. `Experience` - 8 edges
8. `Candidate Profile — Single Source of Truth` - 8 edges
9. `graphify reference: query, path, explain` - 5 edges
10. `Job-Search Agent` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (29 total, 8 thin omitted)

### Community 0 - "Experience"
Cohesion: 0.12
Nodes (15): Certifications, Education, Experience, HR Business Partner (Commercial Division) — Mobilink (VimpelCom Group), Independent HR Consultant — Contract Projects, Keywords bank, Learning, Development & OD Executive — Ufone (Etisalat), Manager, Human Resources (HR Lead / Head of HR – Pakistan) — Quixel (Epic Games) (+7 more)

### Community 1 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 2 - "Job Search Preferences"
Cohesion: 0.20
Nodes (9): Company profile, Compensation, Industries, Job Search Preferences, Location & work style, Scoring rubric (used by /find-jobs), Search sources, Seniority (+1 more)

### Community 3 - "/graphify"
Cohesion: 0.20
Nodes (9): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Usage (+1 more)

### Community 4 - "LinkedIn Profile Copy — paste-ready"
Cohesion: 0.22
Nodes (8): About (~200 words), Education & certifications sections, Experience section blurbs (2–4 lines each — LinkedIn is skimmed), Headline (pick one, max 220 chars), Languages section, LinkedIn Profile Copy — paste-ready, Settings checklist (5 minutes, do once), Skills (pin the top 3 ⭐)

### Community 5 - "Candidate Profile — Single Source of Truth"
Cohesion: 0.22
Nodes (8): Candidate Profile — Single Source of Truth, Compensation, Current situation, Identity, Never do, References, Standard application answers, Work authorization

### Community 6 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 7 - "app.js"
Cohesion: 0.25
Nodes (7): form, hamburger, navbar, navLinks, observer, revealItems, success

### Community 8 - "Outreach draft — Motive (gomotive)"
Cohesion: 0.33
Nodes (5): Email draft (100–150 words), LinkedIn connection note (≤300 chars), Outreach draft — Motive (gomotive), Research hooks (verified via web search), Status

### Community 9 - "Job-Search Agent"
Cohesion: 0.33
Nodes (5): Daily use, Guardrails (built into every skill), Job-Search Agent, One-time setup (15 minutes), Where things land

### Community 10 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 11 - "Handoff — instructions for the next working session"
Cohesion: 0.40
Nodes (4): Do now (updated 2026-07-15 by cloud session), Done, Handoff — instructions for the next working session, Standing conventions

### Community 12 - "Outreach (Reverse Recruiting)"
Cohesion: 0.40
Nodes (4): Hard rules, Outreach (Reverse Recruiting), Sending policy — APPROVAL REQUIRED (Umair, 2026-07-15), Steps

### Community 13 - "Pipeline"
Cohesion: 0.40
Nodes (4): On `/pipeline` (no arguments), On `/pipeline <update>` (e.g. "/pipeline Acme moved to interviewing, call Tuesday"), Pipeline, Rules

### Community 14 - "Apply to a Job"
Cohesion: 0.50
Nodes (3): Apply to a Job, Hard rules, Steps

### Community 15 - "Find Jobs"
Cohesion: 0.50
Nodes (3): Find Jobs, Rules, Steps

### Community 16 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 17 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 18 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 19 - "Optimize LinkedIn"
Cohesion: 0.50
Nodes (3): Optimize LinkedIn, Rules, Steps

### Community 20 - "Tailor Resume"
Cohesion: 0.50
Nodes (3): Hard rules, Steps, Tailor Resume

## Knowledge Gaps
- **114 isolated node(s):** `navbar`, `hamburger`, `navLinks`, `form`, `success` (+109 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `What You Must Do When Invoked` connect `What You Must Do When Invoked` to `/graphify`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `/graphify` connect `/graphify` to `What You Must Do When Invoked`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `navbar`, `hamburger`, `navLinks` to the rest of the system?**
  _114 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Experience` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._