# Daily run

Instructions for the scheduled run that supports the SEASONEXT social media workflow.
It runs once a day at 08:00 Athens time as a scheduled cloud agent (Claude Code routine)
with access to this repository and to the Notion and Buffer connectors. To recreate it
under another account: create a daily routine on this repository, attach the Notion and
Buffer connectors, set `CDSAPI_URL` and `CDSAPI_KEY` in its environment, and use the
text below as its instructions.

Rules from `CLAUDE.md` and `docs/playbook.md` apply throughout. The run never publishes
immediately and never schedules a post without both approvals.

## Principle: Notion is the state

Every decision is read from Notion at the start of each run; nothing is remembered
between runs. Buffer only executes schedules, and this repository only hosts published
images and the archive.

| Notion | What the run reads | What the run writes |
|---|---|---|
| Steering page | reviewers to notify, this month's focus | a short report, only when something happened |
| Requests and notes | open requests, urgent flags, standing notes | Response, Status |
| Coming up | dates in the next six weeks | nothing |
| Idea bank | topics and priorities | Used date |
| Posts | status, approvals, planned date, page text | new ideas and drafts, Scheduled/Posted, Buffer IDs, metrics |

## Every day

1. **Read the state** from the tables above.
2. **Schedule approved posts.** Posts with both *Approved: PI* and *Approved: rotation*
   ticked and status *In review*:
   - copy the image and the final texts from the Notion page into
     `posts/<date>_<slug>/` (`image.png`, `post.md`, and the figure script if any),
     commit and push;
   - create one Buffer post per channel at the planned date and time (10:00 Athens if
     no time is set, the same time on all three channels): LinkedIn text with the Greek version as first comment when present;
     the short text on X and Bluesky; image from its raw GitHub URL, with alt text;
   - set the status to *Scheduled* and record the Buffer post IDs.
3. **Move late posts.** If a post in *In review* has its planned date today and is not
   approved by both, move the planned date to the next Tuesday or Thursday and mention
   the reviewers in a comment.
4. **Withdraw unapproved posts.** If a *Scheduled* post has lost an approval, delete its
   Buffer posts and set the status back to *In review*.
5. **Close published posts.** For *Scheduled* posts whose time has passed, check Buffer;
   if sent, set *Posted*, the posted date and the LinkedIn link. About a week later, fill
   impressions and reactions.
6. **Handle urgent requests** (Requests and notes, *Urgent* ticked, status *Open*): act
   as for Monday step 10, set *Picked up*, and write what was done in *Response*.
7. **Quick news check** (two or three searches): major weather or water events in Crete
   and Greece, and major releases on the watchlist (for example a new C3S seasonal
   system). If something is clearly worth a post, add it as an *Idea* and mention the
   reviewers in a comment on it.
8. **Keep the record complete.** Posts sent from Buffer that have no Notion page
   (written directly in Buffer) get a page with status *Posted*.

## Mondays

9. **Check the plan** for the next two weeks against the typical month (playbook
   section 4), the Steering page and *Coming up*.
10. **Propose ideas** for each open slot: up to three per slot, status *Idea*, each with a
   one-line pitch, category, sources, suggested figure and a check against the rules.
   Use, in this order: open requests, the *Coming up* dates, the Idea bank (*Next* first)
   for explainers and data stories, and the full watchlist search below. Skip anything
   already in the Posts database.
11. **Draft selected ideas.** For ideas set to *Selected*: write the full draft (all text
    versions, alt text, sources, figure) in the post page, set *In review*, and add a
    comment mentioning the reviewers listed on the Steering page, with the planned date.
    The planned date leaves at least two full working days for review: drafts made on
    Monday go out on Thursday at 10:00.
    If nothing is selected for a slot due in the week after next, draft the top idea by
    the priority rule. Mark Idea bank topics as used.

## On the 7th of each month

12. **Forecast vs reality** for the previous month: run
    `python scripts/fetch_forecast_vs_reality.py YYYY-MM` and `python scripts/forecast_vs_reality.py YYYY-MM`,
    write the text from the template of the previous post in the series, create the draft
    (status *In review*, planned for the first Tuesday to Thursday at least two working
    days later) and notify the reviewers.

## Watchlist (Mondays in full, daily in brief)

- Forecast providers: ECMWF and C3S news (new systems, monthly seasonal release),
  Copernicus monthly climate bulletins, WMO and NOAA ENSO updates, European Drought
  Observatory.
- Greece and Crete: meteo.gr (NOA) articles, Hellenic National Meteorological Service,
  civil protection, Cretan press on rain, drought and reservoirs, water authorities.
- Science: new papers on seasonal forecasting, Mediterranean hydroclimate, HYPE and bias
  adjustment; publications by the SEASONEXT team; EGU and ISIMIP news.

## Limits and reporting

- At most four new Notion pages per run.
- Report on the Steering page (one short comment) only when the run did something or
  needs a person. Quiet days leave no trace, so nobody gets daily notifications.
