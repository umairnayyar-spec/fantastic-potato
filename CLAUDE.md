## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Prompt optimisation

Before responding, classify the request:

- **Simple** (factual question, quick calculation, short rewrite, yes/no, definition, follow-up in an ongoing task): just answer. Don't mention this rule.
- **Complex** (output will be reused or published, such as a CV, post, email, proposal, code, strategy or research; multi-step; depends on missing context; or ambiguous enough that a wrong guess wastes effort):
  1. Restate the request as an optimised prompt in 3-5 lines: goal, audience, context, constraints, output format, quality bar.
  2. If something critical is missing, ask at most 2 questions. Otherwise state assumptions and proceed.
  3. Answer using the optimised prompt.

When unsure, treat it as simple. Overrides: a message starting with `!p` is always optimised; `!q` never is.
