---
name: optimize-linkedin
description: Generate optimized LinkedIn profile copy (headline, about, experience descriptions, skills list) from the master resume and preferences, for the user to paste into LinkedIn. Use when the user asks to optimize, improve, or rewrite their LinkedIn profile.
---

# Optimize LinkedIn

Produce ready-to-paste LinkedIn profile copy optimized for recruiter search.

**Important:** this skill primarily generates text. Scraping LinkedIn,
auto-messaging, and auto-sending connection requests violate LinkedIn's ToS —
never do those, even if asked. Profile *editing*: Umair has explicitly
accepted (2026-07-15, after being informed of the ToS risk) that in his own
logged-in, supervised browser session the agent may type prepared copy into
the profile edit fields, provided **he clicks every Save himself**, one pass
only, stopping immediately on any security challenge. Default remains
paste-it-yourself whenever he's not present and supervising.

## Steps

1. Read `career/profile/master-resume.md`, `career/profile/profile.md`, and
   `career/profile/preferences.md`. If the master resume is empty, fill it
   first (see tailor-resume skill).
2. If the user can paste their current LinkedIn profile text, ask for it —
   critiquing the real thing beats writing blind. Otherwise work from the
   master resume.
3. Research (WebSearch) what terms recruiters search for the target roles in
   preferences.md — current title conventions and skill keywords.
4. Write `career/linkedin/profile-copy.md` containing:
   - **Headline** (220 chars max): role + specialty + proof, keyword-front-
     loaded. Give 3 variants.
   - **About section** (~150–250 words): first person, hook in the first two
     lines (that's all that shows uncollapsed), achievements with numbers,
     target keywords woven in, ends with what they're looking for + contact.
   - **Experience descriptions:** for each role in the master resume, 2–4
     punchy lines (LinkedIn is skimmed, not read — shorter than the resume).
   - **Skills list:** the 15–25 skills to pin, ordered by recruiter-search
     value; mark the top 3 to feature.
   - **Settings checklist:** turn on "Open to Work" (recruiters-only mode if
     currently employed), set target titles + locations from preferences.md,
     custom URL, headline photo/banner reminders.
5. Present the copy section by section and iterate on the user's feedback.
   Save the final version back to the same file.

## Rules

- Everything must be truthful and consistent with the master resume — a
  recruiter will compare the profile to the submitted resume.
- No buzzword salad ("passionate visionary synergist"). Concrete nouns and
  numbers win recruiter searches and human skims alike.
