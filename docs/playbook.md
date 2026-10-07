# SEASONEXT social media playbook

How the SEASONEXT channels are run: mandate, workflow, post categories, methods, rules
and tools. Written so that anyone on the team can take over at any point.

## 1. Mandate

From the SEASONEXT proposal (WP5, Task 5.2 "Outreach, Engagement and Capacity building",
months 3 to 48):

> (a) Communication of general information to a wide audience, including social media
> platforms. Management of SEASONEXT's social media will rotate sequentially among PhD
> and Post-doc researchers every three months. This structured rotation is designed to
> enhance their communication and dissemination skills.

- Milestone M5.2: dedicated accounts on X and LinkedIn.
- Target set by the PI (October 2026): at least 2 posts per month. Our aim is about one
  meaningful post per week.
- Rotation in three-month blocks: October to December 2026 Athanasios Tsilimigkras,
  January to March 2027 Kalliopi-Mikaela Papa, then alternating.
- Every post is reviewed before publication.

## 2. Channels

| Channel | Address |
|---|---|
| LinkedIn (main) | https://www.linkedin.com/showcase/seasonext/ |
| X | https://x.com/seasonext |
| Bluesky | https://bsky.app/profile/seasonext-tuc.bsky.social |
| Website | https://www.seasonext.tuc.gr/en/home |
| Project email | seasonext.tuc@gmail.com |

All accounts belong to the project email. Passwords and two-factor backup codes are
kept outside this repository, in a place the PI can access.

**Scheduling** goes through one Buffer account (project email, free plan, three channels).
Anyone on the team can log in and post directly in Buffer, with or without the rest of
this setup.

**LinkedIn in Buffer.** A LinkedIn page has no login of its own; Buffer reaches it through
the personal profile of one of the page's Super admins, with only the SEASONEXT page
selected, so Buffer posts as the page and never as a person. LinkedIn asks for a refresh
every 60 days (also after a password change or a role change). Any Super admin then clicks
*Refresh* on the channel in Buffer; the channel and its queue stay. The page keeps at least
two Super admins for this reason.

## 3. Workflow

| Step | Where | Who |
|---|---|---|
| Steering: focus, requests, dates, idea bank | Notion, *Steering* page | anyone on the team |
| Ideas proposed | Notion, Posts database, status *Idea* | weekly scout run, or anyone |
| Idea chosen | status *Selected* | person on rotation |
| Draft written (text and figure) | Notion post page, status *In review* | person on rotation, with assistant support |
| Review and edits | directly in the Notion page, or as comments | PI and person on rotation |
| Approval | two ticks: *Approved: PI* and *Approved: rotation* | both |
| Scheduling | Buffer, all three channels, at the planned date and time | daily run after both ticks |
| Archive | `posts/<date>_<slug>/` in this repository | daily run |
| Metrics | Notion: link, impressions, reactions | about a week after posting |

Rules that make this work:

- **The Notion page is the final text.** From *In review* on, whatever is in the post page
  is what gets published: LinkedIn text, X/Bluesky text, Greek first comment, alt text,
  image. Edits are made there.
- **Both approvals are needed.** A post with one tick does not move.
- **Scheduled as soon as approved.** After both ticks, the next daily run schedules the
  post in Buffer for its planned date and time. Once in Buffer, it publishes even if
  nothing else runs. To change an approved post, untick an approval: the next run takes
  it out of Buffer and returns it to *In review*.
- **Review window of at least two working days.** A draft reaches *In review* at least two
  full working days before its planned date. The weekly rhythm: drafts on Monday, review
  on Tuesday and Wednesday, publication on Thursday. Urgent event posts may use a shorter
  window if both reviewers agree.
- **Approve by the evening before** the planned date (the daily run is at 08:00 Athens time).
  A post that is not approved by then moves to the next Tuesday or Thursday, and the
  reviewers are told.
- **Publication time.** All three channels at the same time, 10:00 Athens time, on Tuesday,
  Wednesday or Thursday (when LinkedIn engagement is highest). A planned date may set a
  different time.
- **Reviewers are notified** by a comment mentioning them when a draft reaches *In review*.
  The reviewers are the people listed at the top of the Steering page; Notion sends an
  app notification and an email (each person's Notion settings must allow email
  notifications).
- **Requests.** Anyone can ask for a post or give context by adding a row to *Requests
  and notes* on the Steering page. Urgent requests are handled the next morning, others
  on Monday; the run answers in the same row.

## 4. Post categories

| Category | Purpose | When | Data | How it is made |
|---|---|---|---|---|
| Forecast vs reality | Show every month how the seasonal forecasts did for Crete | monthly, around the 10th | C3S seasonal forecasts (10 systems), ERA5 | `scripts/forecast_vs_reality.py`, fixed figure and text template (section 5) |
| Explainer (published as "Did you know?") | One concept behind SEASONEXT in plain words | monthly | textbook knowledge, illustrative public data | topic from the backlog (section 9) |
| Event in context | Put a notable weather or water event in Crete or Greece into numbers | within a week of the event | NOA station totals and records, CLIMADAT-Grid, reservoir data | event figure against station records (section 6) |
| World day | Join international observances | fixed dates (section 7) | varies | proposed 2 to 4 weeks ahead |
| Field news | New systems, datasets and reports | when they appear | the release itself | short summary and what it means for Crete |
| Published work | Team papers, public deliverables, talks | on publication | the publication | `scripts/paper_card.py` |
| Project life | Workshops, visits, conferences | when they happen | photos | photo and a few lines |

**A typical month.** Week 1: explainer. Week 2: forecast vs reality. Weeks 3 and 4:
flexible. Priority for flexible slots: our own news (published work, project life), then a
world day in that week, then events, then field news. A major event can take any slot.

## 5. Forecast vs reality: method

Question: a month ahead, what did the seasonal forecasts say about Crete, and what happened?

1. **Forecast.** For target month M, the Copernicus C3S forecasts started on the 1st of
   month M-1 (published around the 10th of M-1), lead month 2. All systems in the C3S
   multi-system (10 as of August 2026: ECMWF, UK Met Office, Météo-France, DWD, CMCC,
   NCEP, JMA, two ECCC systems, BoM).
2. **Region and variables.** The four 1° grid cells along Crete (35-36° N, 23-27° E);
   monthly precipitation total and monthly mean 2 m temperature.
3. **Normal.** Terciles of 1993-2016, the C3S common re-forecast period. Each system is
   compared with its own re-forecasts for the same start month and lead (members and
   years pooled), which removes model bias.
4. **Probabilities.** For each system, the share of ensemble members in the lower, middle
   and upper third; the plain average across systems. With no information, each third has
   a 33 % chance.
5. **Observed.** ERA5 monthly means over the Crete land points (land-sea mask above 0.5,
   cosine-latitude weights); its third from ERA5 1993-2016 for the same calendar month.
6. **Scoring.**
   - The forecast *leans* to its most likely third only if that third has at least 40 %
     (the threshold C3S uses on its most-likely-category maps). Below that: *no signal*,
     not scored.
   - *Hit*: the observed third is the leaned third. *Miss*: any other third.
   - *On the line*: the observation is within a tenth of the middle third's width of a
     boundary next to the leaned third, so it could go either way. Reported, not scored.
   - A running scorecard (hits out of scored months) is posted every quarter. A reliable
     forecast that says 60 % should be right about 60 % of the time, so misses are
     expected and shown.
7. **Figure.** Equal-width thirds, with the 24 reference years as dots placed by rank
   (monthly rain is too skewed for a value axis); the tint of each third shows its
   forecast probability.

**Why ERA5 and not stations for the observed side.** The forecast is an area average
whose normal comes from 1993-2016, so the observation must be an area average with the
same reference period. The NOA station network starts in 2006-2009 and its station list
changes over time, the public NOA file gives monthly rainfall but only temperature
extremes, and current data need an account with download limits. ERA5 is open,
consistent, available about five days after the end of the month, and is what C3S
verifies against. Its limitation is that it is a model reanalysis. Planned: compare ERA5,
ERA5-Land and AgERA5 with the NOA Crete stations (2009-2025) and adopt the product that
agrees best, following Papa and Koutroulis (2025).

## 6. Event in context: method

- Event totals come from the NOA / meteo.gr station network. Where a source gives a
  rounded and an exact value, the lower one is used.
- Each station is compared with its own measured record (NOA monthly rainfall
  2006-2025, complete years only, `scripts/noa_stations.py`): share of an average year,
  and whether the event exceeded the wettest month on record.
- CLIMADAT-Grid (Crete subset in `reference/`) is used only as map background. Station
  positions on maps are approximate until NOA station coordinates are available.
- No attribution of a single event to climate change without an attribution study.

## 7. Calendar

- 2 February World Wetlands Day; 11 February International Day of Women and Girls in Science
- 22 March World Water Day; 23 March World Meteorological Day
- 5 June World Environment Day; 17 June Desertification and Drought Day
- 13 October International Day for Disaster Risk Reduction
- EGU General Assembly (spring): abstracts and talks by the team
- SEASONEXT stakeholder workshops (M12, M24, M36, M46)

## 8. Rules for every post

- **No unpublished project results.** Public data, published work, events and explainers
  only. Showing that something can be computed from public data is fine; showing project
  methods or results before publication is not.
- **Never present a forecast as a warning or as official.** Warnings belong to civil
  protection and the Hellenic National Meteorological Service.
- **Every number is sourced**, and sources are listed with the post.
- **Credits on every figure.** Copernicus data: "Contains modified Copernicus Climate
  Change Service information [year]". Other data: source and licence.
- **Respectful tone** around casualties and damage.
- **Language.** English first; Crete-specific posts also get a short Greek version (first
  comment on LinkedIn, and on the website).
- **Accessibility.** Every image has alt text.
- **Writing.** Professional and neutral. Plain words; acronyms explained. No em dashes.
  LinkedIn about 1,200 to 1,600 characters; X and Bluesky under 280.

## 9. Idea bank

Evergreen topics for explainers, data stories, series and team posts are kept in the
*Idea bank* table on the Steering page (for example: probabilities and terciles, why
seasonal forecasts work, re-forecasts, forecast skill, weather regimes as a textbook
concept, stations versus reanalysis versus satellites, why 1 km matters, drought indices,
Crete's rainfall gradient, Crete's reservoirs, a quarterly forecast scorecard, meet the
team). Anyone can add; *Priority: Next* moves a topic up. Topics close to ongoing
SEASONEXT research (such as weather regimes) stay at textbook level until the project's
results are published.

## 10. Figure style

- 1350 × 1350 px square on warm off-white paper, built on `scripts/brand.py`, laid out
  like a journal page: a masthead (navy rule, series name, logo), a serif title that says
  what the figure shows (shrunk automatically if it would overflow), a short subtitle, the
  content, and a footer with the data credits in at most two lines across the full width.
- Typefaces: Source Serif 4 for titles, headings and headline numbers; Barlow (DIN-style,
  like the logo lettering) for labels, data and credits.
- Colours: navy `#151d2c` and blue `#4d71b1` from the logo; terracotta `#c0703f` as the
  opposite pole (dry or warm).
- One message per figure. Highlight one thing and keep the rest grey. Thin marks, no
  gridlines unless needed. Numbers are written as labels; colour never carries meaning alone.
- Every rendered image is checked by eye before review (overlaps, clipping, overflow).

## 11. Automation

One scheduled run per day at 08:00 Athens time, in the cloud (instructions in
`docs/routine.md`):

- **Every day:** read the state from Notion; schedule posts that have both approvals and
  archive them in `posts/`; withdraw posts that lost an approval; handle urgent requests;
  a brief check for major events and releases.
- **Mondays:** full watchlist search, ideas for the open slots (from requests, upcoming
  dates and the idea bank), drafts for the selected ones, reviewers notified.
- **On the 7th:** prepare the forecast vs reality post and create its draft.

The run belongs to the account of the person maintaining it. If that person leaves, any
team member can recreate it from `docs/routine.md`. Nothing else depends on it: the
accounts, Notion, Buffer and this repository are shared, and posts can always be written
and scheduled by hand.

## 12. Decision log

- **2026-10-07 Platforms.** LinkedIn is the main channel; X and Bluesky carry the same
  posts; the website keeps a news archive. Instagram, TikTok and YouTube are not used
  (video effort, different audience). Facebook may follow for Greek local stakeholders.
- **2026-10-07 Notion for review, Buffer for publishing.** Notion is where the team
  reviews and approves; Buffer (free plan) schedules to all three channels. Direct
  platform APIs were rejected: X posting is pay-per-use since February 2026 and
  LinkedIn's page API requires an app review aimed at commercial use.
- **2026-10-07 Forecast vs reality method** as in section 5. It follows how C3S presents tercile
  forecasts, is simple to explain, and runs unchanged every month.
- **2026-10-07 Event figures use station records**, not gridded climatology at
  approximate coordinates: measured values, no coordinates needed, and record-breaking
  can be shown.
- **2026-10-07 Conservative numbers.** Where a source gives two values, the lower is used.
- **2026-10-07 Public repository.** Buffer takes images only from a permanent public
  address, so published images are stored here. The repository also documents the whole
  setup for the team. Drafts are never pushed; only published posts are archived.
- **2026-10-08 Figure style.** Serif titles and numbers, off-white paper, logo in the
  masthead and a two-line footer, 1350 px, to move away from a generic look. Explainers
  carry the label "Did you know?" (lighter than "Explainer"); "Event in context" stays
  neutral because these posts are often about disasters. The monthly series is
  called "Forecast vs reality", and its title asks whether the forecasts got the month right.
- **2026-10-07 Notion text is final, two approvals.** What is in the Notion page at
  approval is published; both the PI and the person on rotation approve every post.
