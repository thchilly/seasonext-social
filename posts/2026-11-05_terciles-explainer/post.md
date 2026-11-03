# Did you know? What a 49% chance of a wet month means

- Category: Explainer
- Planned: Thu 2026-11-05, 10:00 Athens time, on LinkedIn, X and Bluesky
- Language: EN; LinkedIn also in Greek; the lab's LinkedIn page is tagged
- Image: image.png (made by figure.py)
- Approved by: PI and researcher on rotation

## LinkedIn

Our monthly Forecast vs reality posts talk about thirds and chances. What do they mean?

A seasonal forecast does not say how much it will rain. It compares the coming month with the past. Take every September from 1993 to 2016 in Crete, 24 in all, and rank them from driest to wettest. The driest 8 form the lower third, the middle 8 are "near normal", and the wettest 8 form the upper third. In ERA5, a September with less than about 9 mm of rain over Crete falls in the dry third, and one with more than about 22 mm in the wet third.

With no information at all, each third has the same chance: 33%. That is the starting point, not a forecast.

A forecast shifts these odds. Each forecast system runs many slightly different versions of the coming months, and the chance of each third is the share of those runs that fall in it. In early August, the average of 10 Copernicus (C3S) systems gave 19% for a drier, 32% for a near normal and 49% for a wetter than normal September.

So 49% is a clear lean towards wet, but not a promise. It still leaves 51% for near normal or dry. One month alone cannot show whether a forecast is good: if the forecasts are reliable, a 49% chance should come true about half the time. That is why our monthly checks keep score, hits and misses alike, month after month.

Data: C3S seasonal forecasts and ERA5. Contains modified Copernicus Climate Change Service information 2026.

SEASONEXT is led by Hydromech, the Hydrology and Hydraulic Engineering Laboratory, TUC.

Τι σημαίνει πιθανότητα 49% για έναν υγρό μήνα; Τα εποχικά προγνωστικά δεν λένε πόση βροχή θα πέσει· συγκρίνουν τον επόμενο μήνα με το παρελθόν. Οι 24 Σεπτέμβριοι της περιόδου 1993-2016 στην Κρήτη, ταξινομημένοι από τον πιο ξηρό στον πιο υγρό, χωρίζονται σε τρία ίσα τρίτα: ξηρό, κανονικό και υγρό. Χωρίς καμία πληροφορία, κάθε τρίτο έχει πιθανότητα 33%. Στις αρχές Αυγούστου, τα προγνωστικά έδιναν 19% πιθανότητα για Σεπτέμβριο πιο ξηρό από το κανονικό, 32% για κανονικό και 49% για πιο υγρό. Το 49% δείχνει σαφή κλίση προς τα υγρά, όχι βεβαιότητα: αφήνει 51% για κάτι άλλο. Γι' αυτό μετράμε επιτυχίες και αστοχίες, μήνα με τον μήνα.

#SeasonalForecasting #Copernicus #Crete #ClimateServices

## X and Bluesky

What does a 49% chance of a wet month mean? Forecasts split past Septembers in Crete into three equal thirds: dry, normal and wet. With no information, each has 33%. In early August, the forecasts gave 49% for a wet September: a clear lean, not a promise.

## Alt text

Graphic in the "Did you know?" series, titled "What a 49% chance of a wet month means". Two bands of three equal thirds, drier, near and wetter than normal, each holding 8 grey dots for the Septembers of 1993-2016 in Crete, ranked by rainfall; the thirds are separated at 9 mm and 22 mm. Top band, with no information: 33%, 33%, 33%. Bottom band, the forecast for September 2026 made in early August: 19% drier, 32% near normal, 49% wetter, with the wet third shaded more strongly. A note below reads: a 49% chance of wet still leaves 51% for near normal or dry; only a score kept over many months shows whether such odds can be trusted.

## Sources and checks

- 19%, 32% and 49% for September 2026 (mean of 10 C3S systems started 1 August 2026, lead month 2): from the published Forecast vs reality, September 2026 post (13 Oct, https://www.linkedin.com/feed/update/urn:li:share:7515668008347033600), archived in `posts/2026-10-13_forecast-vs-reality-sep/`. Systems: ECMWF, UKMO, Meteo-France, DWD, CMCC, NCEP, JMA, two ECCC systems, BoM.
- Tercile edges of about 9 mm and 22 mm: ERA5, Crete land points, Septembers 1993-2016, as shown in the same published figure.
- 1993-2016 as the reference period: the C3S common re-forecast period (C3S seasonal forecast documentation).
- Simplification: in the method, each system's thirds come from its own re-forecasts for the same start month (this removes model bias), while the observed thirds come from ERA5. The post says only "the share of those runs that fall in it"; no number depends on this.
- "A 49% chance should come true about half the time": the definition of a reliable probability forecast; stated as a condition ("if the forecasts are reliable"), not a claim about these systems.
- No new forecast, no project results. Only numbers already published on 13 Oct.
- Figure: schematic, dots placed by rank (8 per third); brand style, 1350 x 1350 px, checked by eye.
