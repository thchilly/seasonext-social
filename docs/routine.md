# Daily run

Instructions for the scheduled run that supports the SEASONEXT social media workflow.
It runs once a day at 08:00 Athens time as a scheduled cloud agent (Claude Code routine)
with access to this repository and to the Notion and Buffer connectors. To recreate it
under another account: create a daily routine on this repository, attach the Notion and
Buffer connectors, set `CDSAPI_URL` and `CDSAPI_KEY` in its environment, and use the
text below as its instructions.

Rules from `CLAUDE.md` and `docs/playbook.md` apply throughout. The run never publishes
immediately and never schedules a post without both approvals.

Run scripts with `python3`: in the cloud environment, `python` is a different interpreter
without the project packages.

## Principle: Notion is the state

Every decision is read from Notion at the start of each run; nothing is remembered
between runs. Buffer only executes schedules, and this repository only hosts published
images and the archive. Ticking the two approvals is the only thing people have to do;
the run keeps status, dates, Buffer IDs and the archive up to date.

| Notion | What the run reads | What the run writes |
|---|---|---|
| Steering page | reviewers to notify, this month's focus | a short report, only when something happened |
| Requests and notes | open requests, urgent flags, standing notes | Response, Status |
| Coming up | dates in the next six weeks | nothing |
| Idea bank | topics and priorities | Used date |
| Posts | status, approvals, planned date, page text | new ideas and drafts, typo fixes, Scheduled/Posted, Buffer IDs, metrics |

## Every day

1. **Read the state** from the tables above.
2. **Proofread.** For every post in *In review* or *Scheduled* whose text changed since
   it was last checked (no comment from the run after the last edit), check the English
   and the Greek: spelling, grammar, accents, terms; numbers that agree across the
   LinkedIn text, the X/Bluesky text, the alt text and the sources; length limits
   (playbook section 8); the LinkedIn layout and the lab line.
   - **Obvious typos** (a misspelt word, a missing or wrong Greek accent, a doubled
     word, a double space, punctuation): fix them directly in the Notion page and leave
     one comment listing each fix as "old → new". No new approval is needed.
   - **Anything that changes meaning** (a number, a name, a date, a claim, a rewritten
     sentence): do not change it. Leave one comment with the suggested fix, mentioning
     the reviewers. A post with such an issue is not scheduled until a reviewer has fixed
     it or replied that it is fine.
   - Style preferences are not errors and are not raised.
3. **Schedule approved posts.** Posts with both *Approved: PI* and *Approved: rotation*
   ticked, status *In review*, and no open issue from step 2:
   - check Buffer for posts already created for it (IDs in *Buffer IDs*, or posts on the
     same channel at the same time) and create only what is missing;
   - copy the image and the final texts from the Notion page into
     `posts/<date>_<slug>/` (`image.png`, `post.md`, and the figure script if any),
     commit and push;
   - create one Buffer post per channel at the planned date and time (10:00 Athens if
     no time is set, the same time on all three channels):
     - LinkedIn: the LinkedIn section of the page exactly as it stands (English, the lab
       line, the Greek, the hashtags), with the lab's page tagged on its name (IDs in
       `CLAUDE.md`);
     - X and Bluesky: the short English text;
     - all three: the image from its raw GitHub URL, with the alt text;
   - set the status to *Scheduled* and record the Buffer post IDs.
4. **Bring Buffer in line with edits.** For *Scheduled* posts whose Notion text or image
   differs from `posts/<date>_<slug>/`, after step 2: edit the Buffer posts to match,
   update the archive, commit and push, and leave a comment saying what changed. A
   change made on the publication day after 08:00 is only picked up by a manual
   *Run now* of this routine, or by editing the post in Buffer directly.
5. **Move late posts.** If a post in *In review* has its planned date today and is not
   approved by both (or has an open issue), move the planned date to the next Tuesday or
   Thursday and mention the reviewers in a comment.
6. **Withdraw unapproved posts.** If a *Scheduled* post has lost an approval, delete its
   Buffer posts and set the status back to *In review*.
7. **Close published posts.** For *Scheduled* posts whose time has passed, check Buffer;
   if sent, set *Posted*, the posted date and the LinkedIn link. About a week later, fill
   impressions and reactions.
8. **Handle urgent requests** (Requests and notes, *Urgent* ticked, status *Open*): act
   as for Monday step 12, set *Picked up*, and write what was done in *Response*.
9. **Quick news check** (two or three searches): major weather or water events in Crete
   and Greece, and major releases on the watchlist (for example a new C3S seasonal
   system). If something is clearly worth a post, add it as an *Idea* and mention the
   reviewers in a comment on it.
10. **Keep the record complete.** Posts sent from Buffer that have no Notion page
    (written directly in Buffer) get a page with status *Posted*.

## Mondays

11. **Check the plan** for the next two weeks against the typical month (playbook
    section 4), the Steering page and *Coming up*.
12. **Propose ideas** for each open slot: up to three per slot, status *Idea*, each with a
    one-line pitch, category, sources, suggested figure and a check against the rules.
    Use, in this order: open requests, the *Coming up* dates, the Idea bank (*Next* first)
    for explainers and data stories, and the full watchlist search below. Skip anything
    already in the Posts database.
13. **Draft selected ideas.** For ideas set to *Selected*: write the full draft in the
    post page (LinkedIn text in the layout of playbook section 8 with English, lab line
    and Greek; X/Bluesky text; alt text; sources; figure), proofread it, set *In review*,
    and add a comment mentioning the reviewers listed on the Steering page, with the
    planned date. The planned date leaves at least two full working days for review:
    drafts made on Monday go out on Thursday at 10:00.
    If nothing is selected for a slot due in the week after next, draft the top idea by
    the priority rule. Mark Idea bank topics as used.

## On the 7th of each month

14. **Forecast vs reality** for the previous month: run
    `python3 scripts/fetch_forecast_vs_reality.py YYYY-MM` and `python3 scripts/forecast_vs_reality.py YYYY-MM`,
    write the text (English and Greek) from the template of the previous post in the
    series, create the draft (status *In review*, planned for the first Tuesday to
    Thursday at least two working days later) and notify the reviewers.

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
