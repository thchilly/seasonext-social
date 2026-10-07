# Daily run

Instructions for the scheduled run that supports the SEASONEXT social media workflow.
It runs once a day at 08:00 Athens time as a scheduled cloud agent (Claude Code routine)
with access to this repository and to the Notion and Buffer connectors. To recreate it
under another account: create a daily routine on this repository, attach the Notion and
Buffer connectors, set `CDSAPI_URL` and `CDSAPI_KEY` in its environment, and use the
text below as its instructions.

Rules from `CLAUDE.md` and `docs/playbook.md` apply throughout. The run never publishes
immediately and never schedules a post without both approvals.

## Every day

1. **Schedule approved posts.** In the Posts database, find pages with both
   *Approved: PI* and *Approved: rotation* ticked and status *In review* or *Approved*.
   For each:
   - copy the image and the final texts from the Notion page into
     `posts/<date>_<slug>/` (`image.png`, `post.md`, plus the figure script if there is one),
     commit and push;
   - create one Buffer post per channel at the planned date and time (LinkedIn text
     with the Greek version as first comment when present; the short text on X and
     Bluesky), with the image from its raw GitHub URL and the alt text;
   - set the status to *Scheduled* and record the Buffer post IDs.
2. **Withdraw unapproved posts.** If a *Scheduled* post has lost an approval, delete its
   Buffer posts and set the status back to *In review*.
3. **Close published posts.** For *Scheduled* posts whose time has passed, check Buffer;
   if sent, set *Posted*, the posted date and the LinkedIn link. About a week later, fill
   impressions and reactions.
4. **Keep the record complete.** Posts sent from Buffer that have no Notion page (written
   directly in Buffer) get a page with status *Posted*.

## Mondays

5. **Read the Steering page**: this month's focus, upcoming events, notes.
6. **Check the plan for the next two weeks** against the typical month (playbook section 4).
7. **Propose ideas** for each open slot: up to three per slot, status *Idea*, each with a
   one-line pitch, category, sources, suggested figure and a check against the rules.
   Search the watchlist below; skip anything already in the database.
8. **Draft selected ideas.** For ideas set to *Selected*, write the full draft (all text
   versions, alt text, sources, figure), set *In review*, and mention both reviewers in a
   comment with the planned date. If nothing is selected for a slot due in the week after
   next, draft the top idea by the priority rule.

## On the 7th of each month

9. **Monthly forecast check** for the previous month: run
   `python scripts/fetch_monthly_check.py YYYY-MM` and `python scripts/monthly_check.py YYYY-MM`,
   write the text from the template of the previous check, create the draft (status
   *In review*, planned for the second week) and notify reviewers.

## Watchlist

- Forecast providers: ECMWF and C3S news (new systems, monthly seasonal release),
  Copernicus monthly climate bulletins, WMO and NOAA ENSO updates, European Drought
  Observatory.
- Greece and Crete: meteo.gr (NOA) articles, Hellenic National Meteorological Service,
  civil protection, Cretan press on rain, drought and reservoirs, water authorities.
- Science: new papers on seasonal forecasting, Mediterranean hydroclimate, HYPE and bias
  adjustment; publications by the SEASONEXT team; EGU and ISIMIP news.
- The calendar in the playbook (section 7) and the Steering page.

## Limits

- At most four new Notion pages per run.
- Report what was done in a short comment on the Steering page (date, actions, anything
  that needs a person).
