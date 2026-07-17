# Handoff — instructions for the next working session

> Written by the cloud session; consumed by Cowork (or any session Umair
> opens). Protocol: git pull, do everything listed under "Do now", update
> this file (move completed items to "Done"), commit and push. Umair only has
> to say: "pull the repo and do what career/HANDOFF.md says."

## Do now (updated 2026-07-17 by cloud session)

### CRITICAL: Pull latest and check tracker rows 8–15

**Before applying to anything:**
1. `git fetch origin main && git pull origin main`
2. Open `career/applications/tracker.md`
3. You're now seeing rows 8–15 (Flow, Celonis, Cohere, Teramind, UpGuard,
   Lumos, Netomi, Manychat) — these are the HIGH-QUALITY direct-URL roles
   from ATS-scoped search (Round 3, 2026-07-16).
4. The old rows 2–7 (Clifford Chance, STIXOR, undisclosed fintech, undisclosed
   Islamabad, Reckitt) are still unverified and should only be attempted if
   you can get a live posting link.

### Apply to rows 8–15 with the PDF resume

**PDF is ready:** `career/resumes/resume-remotecom.pdf` (2 pages, A4 format).

For each of rows 8–15:
1. Open the direct ATS link (Greenhouse/Lever/Ashby URL).
2. Read the full JD.
3. **For remote US startups (Cohere, Teramind, UpGuard, Lumos, Netomi, Manychat):
   CHECK the JD or recruiter email for Pakistan eligibility.** Many say "remote"
   but mean US-work-auth-only. Do NOT apply unless you confirm they hire from
   Pakistan via EOR/contractor.
4. Apply with the PDF resume.
5. Update the tracker: mark status → `applied`, note date, any blockers.
6. If the form asks for info not in `career/profile/profile.md`, add it there
   under "Standard application answers" so future apps reuse it.

**Rows 2–7 (Clifford Chance, STIXOR, undisclosed, Reckitt):** Only apply if you
can verify live + get a real apply link. WebFetch is blocked in cloud, so these
were sourced but not opened. Skip if they're dead or still unverified.

### After applying: Outreach + LinkedIn + Commit

5. **Motive outreach — finalize and send (pending Umair approval).** Open
   `career/outreach/motive-draft.md`. Message is written; fill two blanks:
   - Motive recruiter/hiring manager contact (LinkedIn or published email only).
   - [ROLE] placeholder = actual job title from application form.
   Create Gmail draft. Show Umair, send only on his explicit approval.

6. **LinkedIn — fill fields, Umair clicks Save.** In Umair's logged-in session,
   open https://www.linkedin.com/in/umairkhan99/ and FILL (you type, he saves):
   - Headline (pick one of 3 variants from `career/linkedin/profile-copy.md`; A recommended).
   - About section.
   - Each Experience blurb.
   - Skills (pin top 3).
   - Languages.
   - Open to Work (5 target titles + locations from the file, recruiters-only).
   **Rules:**
   - Ask Umair to pick headline first, then do sections one at a time.
   - Wait for his Save after each section.
   - If LinkedIn shows security challenge/captcha/warning → STOP, go fully manual.
   - Record live edits back into profile-copy.md.

7. **Commit and push** all updates to `claude/job-search-agent-dz7jbc`:
   - Tracker updates (application statuses, blockers, notes).
   - HANDOFF.md (move completed items to Done, add notes).
   - Any profile.md additions from forms.
   - LinkedIn profile-copy.md if edited live.

## Done (updated 2026-07-17 by cloud session)

- 2026-07-15 — Motive application submitted via Cowork (job 8620742002).
- 2026-07-16 — Three /find-jobs rounds completed; 14 new sourced roles added
  (rows 2–15 in tracker). Round 3 switched to ATS-domain-scoped search (direct
  URLs). Playbook updated with learnings.
- 2026-07-17 — PDF resume generated (headless Chrome) and ready in
  `career/resumes/resume-remotecom.pdf`.

## Standing conventions

- The tracker (`career/applications/tracker.md`) is the single source of truth.
  Log every action (apply, outreach, screening, offer, etc.) with date + next action.
- Outreach sends and application submits always need Umair's explicit approval
  before hitting send/submit.
- After each session: update HANDOFF.md, commit, push — the other session
  picks it up.
- Remote "work from anywhere" roles still need Pakistan eligibility check — many
  US startups are US-work-auth-only despite global branding.
