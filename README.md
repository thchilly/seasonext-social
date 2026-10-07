# SEASONEXT social media

Workflow, figure scripts and archive of the social media posts of **SEASONEXT**
(Impact-based SEASonal hydrological Outlooks: a fit-for-purpose framework for adaptatioN
to water EXTremes), a research project led by the Technical University of Crete with
Justus Liebig University Giessen and the Swedish Meteorological and Hydrological
Institute, funded by the Hellenic Foundation for Research and Innovation (H.F.R.I.).
SEASONEXT develops seasonal forecasts of rainfall, river flow and drought, one to seven
months ahead, for water managers in Crete.

Channels: [LinkedIn](https://www.linkedin.com/showcase/seasonext/) ·
[X](https://x.com/seasonext) · Bluesky (seasonext-tuc) ·
[website](https://www.seasonext.tuc.gr/en/home)

## Contents

| Folder | What it holds |
|---|---|
| `docs/playbook.md` | How the channels are run: workflow, post categories, methods, rules |
| `docs/routine.md` | The scheduled daily run that prepares and schedules posts |
| `posts/` | Every published post: final text, image, sources, and the script that made the image |
| `scripts/` | Figure style and reusable figure templates (forecast vs reality, paper card, station records) |
| `brand/` | SEASONEXT logo, emblem and font |
| `profile/` | Profile images for the accounts |
| `reference/` | Small reference datasets used by the figures |

## How a post is made

1. Ideas and drafts are prepared from public data and published work, with the help of
   an AI assistant (Claude Code), and collected in the project's Notion workspace.
2. Every draft is reviewed and edited by the team, and approved by two people: the PI
   and the researcher on rotation.
3. Approved posts are scheduled to all channels through Buffer and archived in `posts/`.

No unpublished project results are posted. Forecasts are discussed as information, never
as warnings.

## Reproducing the figures

```bash
pip install -r requirements.txt
python scripts/forecast_vs_reality.py 2026-09   # after scripts/fetch_forecast_vs_reality.py 2026-09
python posts/<post>/figure.py               # event figures
```

Downloading Copernicus data needs a free [CDS](https://cds.climate.copernicus.eu) account,
with the key in `~/.cdsapirc` or in the `CDSAPI_URL` and `CDSAPI_KEY` environment variables.

## Data credits

- Seasonal forecasts and ERA5: Copernicus Climate Change Service (C3S). Contains modified
  Copernicus Climate Change Service information.
- CLIMADAT-Grid: Varotsos et al. (2025), Earth System Science Data, CC BY 4.0.
- Station observations: National Observatory of Athens, meteo.gr network.

## Licence

- **Code** (`scripts/`, figure scripts in `posts/`): MIT licence, see `LICENSE`.
- **Posts, texts and figures** (`posts/`, `profile/`, `docs/`): Creative Commons
  Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
  You may share and adapt them, including commercially, if you credit
  "SEASONEXT project, Technical University of Crete" and indicate changes.
- **Not covered:** the SEASONEXT logo and emblem (`brand/logo/`), which may only be used
  to refer to the project; the Barlow font (`brand/fonts/`, SIL Open Font License); and
  third-party data, which keep their own terms (see Data credits).

## Contact

seasonext.tuc@gmail.com · Hydrology and Hydraulic Engineering Laboratory, Technical
University of Crete
