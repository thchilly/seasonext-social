# Context for the assistant

This repository runs the SEASONEXT social media channels. Read `docs/playbook.md` first;
it is the source of truth for workflow, categories, methods and rules.

## Systems

- **Notion** (review and approval). Shared page "SEASONEXT social media (shared)":
  https://app.notion.com/p/3f2ddedad6d181979d18df880f9d6ece. Posts database data source:
  `collection://aa80441d-5365-4749-a38c-cf19fe4c2473`.
- **Steering page** (https://app.notion.com/p/3f2ddedad6d1810eaeecd28a29b4de29): reviewers
  to mention, this month's focus, and three tables: Requests and notes
  `collection://d306b804-0886-4232-8745-64721b3499d1`, Coming up
  `collection://6a85feb6-71b1-4013-b506-2d7a98e591bf`, Idea bank
  `collection://98a1f8c0-0cca-4291-a18c-3ada041f7eb1`. Notion is the state: read it at
  the start of every task; nothing is remembered between runs.
- **Buffer** (scheduling). Organization `6ac630a1a3d4f2aacdf0a02f`; channels: LinkedIn
  page `6ac635826a5c39ccb63f83d9`, X `6ac631026a5c39ccb63f4fc2`, Bluesky
  `6ac631586a5c39ccb63f51e1`. Timezone Europe/Athens. Free plan: 10 scheduled posts per
  channel.
- **Images for Buffer** must have a permanent public URL. Commit the image to
  `posts/<date>_<slug>/image.png`, push, then use
  `https://raw.githubusercontent.com/thchilly/seasonext-social/main/posts/<date>_<slug>/image.png`.

## What the assistant may and may not do

- May: propose ideas, write drafts, make figures, create and update Notion post pages,
  mention reviewers in comments, schedule posts in Buffer **only after both approvals**,
  archive published posts, fill metrics.
- Timing: at least two full working days between *In review* and the planned date;
  all channels at the same time, default 10:00 Athens, Tuesday to Thursday.
- Never: publish immediately (`shareNow`), schedule a post missing an approval, change
  an approved text, post unpublished project results, or present a forecast as a warning.
- The Notion page text at approval is final. Copy it verbatim to Buffer and to
  `posts/<date>_<slug>/post.md`.

## Writing

- Professional, neutral, factual. Plain words; explain acronyms. No hype, no emoji in
  post text, no em dashes.
- Every number needs a source listed with the post. Where sources differ, use the
  lower value.

## Repository conventions

- Commits are authored by the maintainer only. No co-author lines and no mention of the
  assistant in commit messages (see `.claude/settings.json`).
- `drafts/` and `cache/` are local and never committed. Only published posts go into `posts/`.
- Python: `requirements.txt`. Copernicus key from `~/.cdsapirc` or `CDSAPI_URL` / `CDSAPI_KEY`;
  never commit keys.
- Figures: `scripts/brand.py` style, 1350 × 1350 px; check every rendered image by eye.

## Scheduled run

Instructions for the daily run are in `docs/routine.md`.
