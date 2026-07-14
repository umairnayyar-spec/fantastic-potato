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

## Hard rules

- **Drafts only.** Never send email or LinkedIn messages yourself. The user
  reviews and sends everything.
- One message per person — never mass-blast identical text; every draft must
  contain at least one company-specific line that couldn't be pasted
  elsewhere.
- Be honest about the candidate's background; the message must survive the
  contact reading the attached resume.
- If no named contact can be found with confidence, say so and fall back to
  the best generic channel (careers@ address, application form) rather than
  guessing a person.
