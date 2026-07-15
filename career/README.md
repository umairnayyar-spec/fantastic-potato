# Job-Search Agent

A Claude Code-native job-hunting system: a reverse-recruiting agent plus six
slash-command skills that source roles, tailor your resume, fill in
applications, draft outreach to hiring managers, and keep your LinkedIn and
pipeline in shape. Everything runs inside Claude Code — no API keys, no
servers.

## One-time setup (15 minutes)

Fill in the three profile files — they are the single source of truth every
skill reads from:

1. `career/profile/profile.md` — contact details, work authorization, salary,
   standard application answers.
2. `career/profile/preferences.md` — target roles, locations, dealbreakers.
3. `career/profile/master-resume.md` — your FULL work history with numbers.

Fastest way: open Claude Code in this repo and say
*"interview me to fill in my career profile files"*.

## Daily use

| Command | What it does |
|---|---|
| `/find-jobs` | Searches the web for matching openings, scores them, adds 7+/10 to the tracker |
| `/tailor-resume <job url or tracker #>` | Builds an ATS-friendly 1–2 page resume + cover note for that job |
| `/apply <job url or tracker #>` | Fills the application form in a browser, shows you everything, submits **only after you confirm** |
| `/outreach <company or tracker #>` | Reverse recruiting: finds the hiring manager/recruiter, drafts a personalized message (Gmail draft — you send) |
| `/optimize-linkedin` | Generates paste-ready LinkedIn headline, About, experience copy, and skills list |
| `/pipeline` | Pipeline status, overdue follow-ups, and tracker updates |

Or run the whole loop at once — ask for the **job-hunter** agent:

> "Use the job-hunter agent to do a full pass on my job search."

It sources → tailors → prepares applications → drafts outreach → reports, and
hands you a batch of submit/send decisions at the end.

## Guardrails (built into every skill)

- **You always click Submit on applications.** The agent prepares; you fire.
- **Outreach emails auto-send** (authorized 2026-07-14) under strict rails:
  published addresses only, personalized, one per person, ≤10/day, every
  send logged and reported. LinkedIn messages are never auto-sent.
- **Nothing is ever fabricated** — resumes and messages only contain what's in
  your master resume.
- **No LinkedIn automation** (it violates LinkedIn's ToS) — LinkedIn output is
  always copy you paste in yourself.
- **No guessed email addresses** — outreach only uses published contacts.

## Where things land

```
career/
  profile/            your data (fill these in)
  resumes/            tailored resumes, one per job
  outreach/           drafted messages, one per contact
  linkedin/           profile-copy.md to paste into LinkedIn
  applications/
    tracker.md        the pipeline — single source of truth
    <company-role>/   screenshots of filled + submitted forms
```
