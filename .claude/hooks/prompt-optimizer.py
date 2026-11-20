#!/usr/bin/env python3
"""UserPromptSubmit hook: nudge Claude to optimise complex prompts only.

Reads the hook JSON on stdin. If the prompt looks complex (or starts with !p),
prints a reminder that Claude Code adds to the context. Simple prompts and
prompts starting with !q pass through untouched.
"""
import json
import re
import sys

KEYWORDS = re.compile(
    r"\b(write|draft|build|create|design|plan|strategy|proposal|implement|"
    r"refactor|research|analy[sz]e|compare|outline|script|campaign|cv|resume|"
    r"cover letter|post|email|report|spec)\b",
    re.IGNORECASE,
)
MIN_WORDS = 15

REMINDER = (
    "Prompt optimisation: this request looks complex. Before answering, restate it "
    "in 3-5 lines as an optimised prompt (goal, audience, context, constraints, "
    "output format, quality bar). Ask at most 2 questions only if something critical "
    "is missing; otherwise state assumptions and proceed."
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    prompt = (data.get("prompt") or "").strip()
    if not prompt or prompt.startswith("/"):
        return
    if prompt.lower().startswith("!q"):
        return
    forced = prompt.lower().startswith("!p")
    complex_ = len(prompt.split()) >= MIN_WORDS or KEYWORDS.search(prompt)
    if forced or complex_:
        print(REMINDER)


if __name__ == "__main__":
    main()
