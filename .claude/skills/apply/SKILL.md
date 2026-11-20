---
name: apply
description: Fill in an online job application form using Playwright and the candidate profile. Auto-submits roles scoring 8+ that pass every safety gate (see Auto-submit policy); everything else pauses for user review before submission. Use when the user asks to apply to a job or fill in an application.
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
3. Screenshot the fully-filled form and decide the path using the
   **Auto-submit policy** below:
   - **All gates pass →** click Submit without asking.
   - **Any gate fails →** show the user the screenshot and a summary of every
     answer, name the failed gate(s), and submit only after they explicitly
     confirm in this conversation.
4. After submitting, screenshot the confirmation page and save both
   screenshots under `career/applications/<company>-<role-slug>/`. If no
   confirmation page/message appears, mark the row `submit-unconfirmed` and
   tell the user — don't retry blindly.
5. Update the tracker: status → `applied`, date, "follow up in 7 days" as
   next action, and note `auto-submitted` or `user-approved`; append to the
   Activity log. Include every auto-submission in the end-of-run report.

## Auto-submit policy (set by Umair, 2026-11-20)

Standing approval to submit **without asking** only when ALL of these hold:

1. Tracker score is **8 or higher**, re-scored from the live job description
   read in this run (provisional/unverified scores don't count).
2. The posting is live and the URL is the employer's own ATS/careers page
   (not LinkedIn Easy Apply, not an aggregator).
3. A tailored resume for this exact role exists in `career/resumes/`.
4. Every required field was answered straight from `profile.md` or the
   tailored resume — nothing guessed, nothing left blank. Any new question
   (custom essay, unusual screening question, a forced salary number,
   relocation/visa wording not covered by profile.md) fails this gate.
5. No account creation, login wall, CAPTCHA, assessment/test, or video
   step is needed.
6. No dealbreaker from preferences.md and no nationality restriction.
7. Not already applied to this company in the last 30 days (check tracker).
8. Daily cap: at most **5 auto-submissions per calendar day**; beyond that,
   queue for review.

If any gate fails, fall back to user review for that application. The user
can revoke this policy at any time; if they do, delete this section.

## Hard rules

- **Never submit without explicit user confirmation in this conversation**
  unless every gate of the Auto-submit policy passes. A general "apply to
  everything" does not widen the policy.
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
