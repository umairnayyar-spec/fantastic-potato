---
name: tailor-resume
description: Produce a tailored 1-2 page resume for a specific job from career/profile/master-resume.md, optimized for that posting's keywords and ATS screening. Use when the user asks to tailor, customize, or update a resume/CV for a role.
---

# Tailor Resume

Create a job-specific resume from the master resume. Input: a job posting URL,
a pasted job description, or a tracker row number.

## Steps

1. Read `career/profile/master-resume.md` and `career/profile/profile.md`.
   If the master resume is still mostly `TODO`s, stop and help the user fill
   it in first (interview them section by section) — a tailored resume built
   on an empty master is worthless.
2. Get the job description: WebFetch the URL, or use the pasted text, or look
   up the link in `career/applications/tracker.md`.
3. Extract from the posting: must-have requirements, nice-to-haves, repeated
   keywords, and the exact job title.
4. Write the tailored resume to
   `career/resumes/<company>-<role-slug>.md`:
   - 1–2 pages maximum. Lead with a 2–3 sentence summary rewritten to mirror
     the posting's language.
   - Select and reorder bullets from the master resume so the most relevant
     achievements appear first. Rephrase to use the posting's terminology
     where truthful.
   - Weave in matching terms from the master resume's keywords bank —
     naturally, in bullets, never as a keyword-stuffing block.
   - Plain formatting that survives ATS parsing: standard section headings
     (Experience, Education, Skills), no tables, no images, no columns.
5. Also produce a short cover note (150–200 words) at the bottom of the same
   file under a `## Cover note` heading, ready to paste into application
   forms that ask for one.
6. Update the tracker row: status → `tailored`, log the action.
7. Show the user a diff-style summary: what was emphasized, what was cut,
   and which keywords were matched.

## Hard rules

- **Never invent.** Every line must be traceable to the master resume or
  profile. If the posting demands something the candidate doesn't have, do
  not paper over it — flag the gap to the user instead.
- Keep dates, titles, and employers exactly as in the master resume.
- If the user wants a PDF/DOCX, generate it from the markdown with a script
  (e.g. pandoc if available, else a small Python docx generator) and save it
  next to the .md file.
