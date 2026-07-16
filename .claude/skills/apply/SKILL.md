---
name: apply
description: Fill in an online job application form using Playwright and the candidate profile, pausing for user review before final submission. Use when the user asks to apply to a job or fill in an application.
---

# Apply to a Job

Fill an online application form on the user's behalf. Input: a job posting /
application URL, or a tracker row number.

## Steps

1. Read `career/profile/profile.md` and find the tailored resume for this
   role in `career/resumes/` (if none exists, run the tailor-resume flow
   first — don't apply with an untailored resume).
2. Write a Playwright script (Chromium is pre-installed at
   `/opt/pw-browsers/chromium`; set `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`)
   that:
   - Opens the application URL.
   - Takes a screenshot of the initial form and inventories every field.
   - Fills each field from `profile.md` / the tailored resume. Map common
     ATS field names (Greenhouse, Lever, Workday, Ashby, SmartRecruiters):
     name, email, phone, location, LinkedIn, resume upload, work
     authorization, salary expectation, EEO questions (answer per the
     "Standard application answers" section).
   - Uploads the resume file if the form takes one (generate PDF from the
     tailored markdown first if needed).
   - **STOPS before clicking Submit.**
3. Screenshot the fully-filled form and show it to the user with a summary of
   every answer given, flagging any field you were unsure about or left blank.
4. **Only after the user explicitly confirms**, click Submit, screenshot the
   confirmation page, and save both screenshots under
   `career/applications/<company>-<role-slug>/`.
5. Update the tracker: status → `applied`, date, "follow up in 7 days" as
   next action; append to the Activity log.

## Hard rules

- **Never submit without explicit user confirmation in this conversation.**
  No exceptions, even if the user previously said "apply to everything".
- Never guess answers to questions not covered by profile.md — ask the user
  and record their answer back into profile.md's "Standard application
  answers" so it's known next time.
- Never fabricate: no invented references, no inflated experience, no
  fake portfolio links.
- If the form requires creating an account or a CAPTCHA/login wall appears,
  stop and hand over to the user with a screenshot and a list of the values
  to paste.
- Answer honestly on work-authorization and background-check questions
  exactly as profile.md states.
