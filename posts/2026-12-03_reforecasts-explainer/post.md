# Did you know? Every forecast system has its own normal

- Category: Explainer
- Planned: Thu 2026-12-03, 10:00 Athens time, on LinkedIn, X and Bluesky
- Language: EN; LinkedIn also in Greek; the lab's LinkedIn page is tagged
- Image: image.png (made by figure.py)
- Approved by: PI and researcher on rotation

## LinkedIn

Our monthly Forecast vs reality posts compare each forecast with its own re-forecasts. What is a re-forecast, and why does every forecast need one?

A seasonal forecast system is a computer model of the atmosphere, ocean and land. Like any model, it has its habits: in some places it rains a little too much or too little, or it runs slightly warm or cool. To learn these habits, forecast centres run the same system again for past years, starting from the observed conditions of each year, as if the forecast had been made at the time. These runs are called re-forecasts, or hindcasts. For the Copernicus (C3S) seasonal forecasts, they cover 1993-2016.

The figure shows why they matter. It takes October rainfall over the Crete area in forecasts started on 1 September. In its re-forecasts, each of the 10 C3S systems has its own "near normal" middle third: from about 12 to 24 mm in one system to about 19 to 46 mm in another. A forecast of 37 mm would be wetter than normal for five systems and near normal for the other five.

So a forecast value means little on its own. Each system is compared with its own re-forecasts for the same start month, which removes its typical bias, and only then are the systems averaged. That is how the chances in our monthly checks are made. Re-forecasts also show how often a system was right in the past, which is how forecast skill is measured.

Data: C3S seasonal forecasts. Contains modified Copernicus Climate Change Service information 2026.

SEASONEXT is led by Hydromech, the Hydrology and Hydraulic Engineering Laboratory, TUC.

Κάθε σύστημα εποχικής πρόγνωσης έχει το δικό του «κανονικό». Για να το μάθουν, τα κέντρα πρόγνωσης τρέχουν το ίδιο σύστημα για παλαιότερα έτη, σαν να είχε γίνει η πρόγνωση τότε: αυτές είναι οι αναδρομικές προγνώσεις (re-forecasts ή hindcasts), για τα συστήματα της Copernicus (C3S) την περίοδο 1993-2016. Για τη βροχή του Οκτωβρίου στην περιοχή της Κρήτης, το κανονικό μεσαίο τρίτο κυμαίνεται από 12-24 mm περίπου σε ένα σύστημα έως 19-46 mm περίπου σε άλλο. Μια πρόγνωση 37 mm θα ήταν πιο υγρή από το κανονικό για πέντε συστήματα και κανονική για τα άλλα πέντε. Γι' αυτό κάθε σύστημα συγκρίνεται πρώτα με τις δικές του αναδρομικές προγνώσεις και μόνο μετά υπολογίζεται ο μέσος όρος όλων.

#SeasonalForecasting #Copernicus #Crete #ClimateServices

## X and Bluesky

Did you know? Every seasonal forecast system has its own "normal". For October rain over Crete, the near-normal range in the re-forecasts of 10 C3S systems runs from 12-24 mm in one to 19-46 mm in another. So each forecast is compared with its own past runs first.

## Alt text

Graphic in the "Did you know?" series, titled "Every forecast system has its own normal". For October rainfall over the Crete area, ten horizontal bars show the near-normal middle third of each Copernicus seasonal forecast system in its re-forecasts for 1993-2016: CMCC 12 to 24 mm, JMA 9 to 27, ECCC system 5 12 to 31, BoM 13 to 32, ECCC system 4 18 to 35, DWD 18 to 40, NCEP 18 to 40, ECMWF 18 to 42, UK Met Office 18 to 42, Météo-France 19 to 46. A dashed line marks a forecast of 37 mm: it lies above the bar, wetter than normal, for the first five systems, and inside the bar, near normal, for the other five. A note below reads: the same 37 mm is wetter than normal for 5 systems and near normal for 5, so each forecast is judged against its own re-forecasts.

## Sources and checks

- Middle thirds per system (mm, October, forecasts started 1 September, re-forecasts 1993-2016, members and years pooled, mean of the four 1° grid cells 35-36° N, 23-27° E): CMCC 11.6-24.2; JMA 9.1-27.5; ECCC system 5 12.4-30.6; BoM 13.0-32.3; ECCC system 4 18.1-34.8; DWD 17.7-39.7; NCEP 17.9-39.9; ECMWF 17.5-41.5; UK Met Office 17.6-41.6; Météo-France 18.8-45.7. Computed from the public C3S dataset "seasonal-monthly-single-levels" (CDS, CC BY 4.0) with the same code as the monthly checks (`scripts/forecast_vs_reality.py`), via `scripts/fetch_forecast_vs_reality.py 2026-10`.
- "About 12 to 24 mm" (CMCC) and "about 19 to 46 mm" (Météo-France): rounded from the values above.
- 37 mm: an illustrative value, not a forecast. Above the upper edge of 5 systems (by at least 2.2 mm) and inside the middle third of the other 5 (by at least 2.7 mm), so the split does not depend on rounding.
- 1993-2016 as the C3S common re-forecast period: C3S seasonal forecast documentation (Copernicus Knowledge Base).
- Not stated in the post: the systems' middle thirds are not compared with ERA5. Over Crete's land points, ERA5 gives higher October rainfall (1993-2016 mean 49 mm) than over the full 1° box including sea (41 mm), so a direct model-vs-ERA5 gap would mix model bias with the area difference. The post only compares the systems with each other.
- No new forecast, no project results; public C3S data processed with the published method of the monthly checks.
- Figure: brand style, 1350 x 1350 px, checked by eye.
