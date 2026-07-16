---
name: outreach
description: Reverse recruiting - research a target company, identify the hiring manager or recruiter, and draft a personalized outreach message (Gmail draft and/or LinkedIn message text). Use when the user asks to reach out, network, contact a recruiter, or do reverse recruiting.
---

# Outreach (Reverse Recruiting)

Instead of waiting for applications to be read, proactively contact the people
who can hire. Input: a company name, a tracker row, or "top N in my pipeline".

## Steps

1. Read `career/profile/profile.md`, `career/profile/master-resume.md`, and
   the relevant tracker rows.
2. Research the company with WebSearch/WebFetch:
   - What they do, recent news (funding, launches, expansion) — hooks for a
     personalized opener.
   - Who to contact, in priority order: the likely hiring manager for the
     role → an internal recruiter/talent partner → a team member in a
     similar role. Find names via the company site, LinkedIn public pages,
     and news. Record the evidence for why this person is the right contact.
3. Find a contact channel: a published email address, a contact form, or
   LinkedIn. **Never guess email addresses** by pattern (jane.doe@...) —
   only use addresses actually published somewhere.
4. Draft the message and save it to
   `career/outreach/<company>-<contact-slug>.md`:
   - **Subject:** specific, not "Opportunity" (e.g. "Head of Ops opening —
     8 yrs running travel operations").
   - **Body:** 100–150 words. One line of genuine, specific interest in the
     company (from step 2), two lines of the candidate's most relevant
     proof (numbers from the master resume), one clear ask (15-min chat or
     "happy to apply formally if there's a fit"). No flattery padding.
   - A 300-character LinkedIn connection-note variant underneath.
5. If a real email address was found and the Gmail tools are available,
   create a **Gmail draft** (never send) addressed to the contact, and tell
   the user it's sitting in their drafts folder for review.
6. Update the tracker: status → `outreach-sent` only after the user actually
   sends; until then note "outreach drafted". Log the action.

## Sending policy — APPROVAL REQUIRED (Umair, 2026-07-15)

Outreach emails are prepared fully automatically — research, contact
identification, personalized writing, Gmail draft creation — but **every
send requires Umair's explicit approval first**. Batch approval is fine:
present all pending messages together ("here are 4 outreach emails ready —
approve all, or pick") and send the approved ones. Never send anything he
hasn't seen in this or the current session.

Rails — all mandatory, no exceptions:

- **Email only.** Never auto-send LinkedIn messages or connection requests —
  LinkedIn automation violates their ToS and risks account restriction.
  LinkedIn copy is always handed to Umair to paste.
- **Published addresses only.** Never send to a guessed/pattern-derived
  address.
- **One message per person, ever** (plus at most one follow-up after 7+ days
  of silence). Never re-send, never blast.
- **Genuinely personalized.** Every message must contain at least one
  company-specific line that couldn't be pasted elsewhere; if the research
  didn't produce one, don't send — flag instead.
- **Max 10 outreach sends per day.**
- **Log every send** in the tracker Activity log (date, recipient, company).
- **Only about roles in the tracker.** No speculative cold outreach to
  companies Umair hasn't sourced or approved targeting.

## Hard rules
- Be honest about the candidate's background; the message must survive the
  contact reading the attached resume.
- If no named contact can be found with confidence, say so and fall back to
  the best generic channel (careers@ address, application form) rather than
  guessing a person.
