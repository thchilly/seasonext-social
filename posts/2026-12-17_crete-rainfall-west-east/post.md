# Did you know? Crete's rainfall from west to east

- Category: Explainer
- Planned: Thu 2026-12-17, 10:00 Athens time, on LinkedIn, X and Bluesky
- Language: EN; LinkedIn also in Greek; the lab's LinkedIn page is tagged
- Image: image.png (made by figure.py)
- Approved by: PI and researcher on rotation

## LinkedIn

Did you know? Crete is not one climate when it comes to rain. Measured at stations, an average year brings more than four times as much rain to the mountains of the west as to the southeast coast.

The map shows average yearly rainfall across the island on a 1 km grid (CLIMADAT-Grid, 1981-2019). The labels are the yearly averages measured at eight stations of the National Observatory of Athens (2006-2025).

Two patterns stand out. First, the west is wetter than the east: on the grid, Crete west of Rethymno gets about 1,050 mm a year on average, and the area east of the Lasithi Plateau about 690 mm. Second, the mountains are much wetter than the coasts. At Xyloskalo, at the top of the Samaria Gorge, the station measures about 1,540 mm in an average year; in Chania, about 25 km away on the coast, about 580 mm. Anogeia on Psiloritis (about 990 mm) and Tzermiado on the Lasithi Plateau (about 1,020 mm) get about twice as much as Heraklion (about 460 mm). Ierapetra, on the southeast coast, gets about 360 mm.

The grid and the stations cover different years, and a grid smooths between points, so their numbers differ. Both show the same pattern.

This is why the same storm, or the same seasonal forecast, means different things in Chania and in Sitia, and for each reservoir and aquifer. A forecast on a grid of about 100 km sees Crete as a few large squares and averages these differences away, which is why SEASONEXT works at fine resolution.

Data: CLIMADAT-Grid (Varotsos et al. 2025, CC BY 4.0); National Observatory of Athens / meteo.gr station records.

SEASONEXT is led by Hydromech, the Hydrology and Hydraulic Engineering Laboratory, TUC.

Η βροχή στην Κρήτη διαφέρει πολύ από τόπο σε τόπο. Ο χάρτης δείχνει τη μέση ετήσια βροχόπτωση σε πλέγμα 1 km (CLIMADAT-Grid, 1981-2019) και τις μέσες ετήσιες τιμές οκτώ σταθμών του Εθνικού Αστεροσκοπείου Αθηνών (2006-2025). Η δυτική Κρήτη είναι πιο βροχερή από την ανατολική: περίπου 1.050 mm τον χρόνο δυτικά του Ρεθύμνου και περίπου 690 mm ανατολικά του οροπεδίου Λασιθίου. Τα βουνά δέχονται πολύ περισσότερη βροχή από τις ακτές: στο Ξυλόσκαλο, στην αρχή του φαραγγιού της Σαμαριάς, περίπου 1.540 mm τον χρόνο, στα Χανιά περίπου 580 mm και στην Ιεράπετρα περίπου 360 mm. Γι' αυτό η ίδια καταιγίδα ή η ίδια εποχική πρόγνωση σημαίνει άλλο πράγμα για τα Χανιά και άλλο για τη Σητεία.

#Crete #Rainfall #Hydrology #WaterManagement

## X and Bluesky

Did you know? Rain in Crete varies more than fourfold. Measured yearly averages: about 1,540 mm at Xyloskalo (Samaria Gorge), 580 mm in Chania, 460 mm in Heraklion, 360 mm in Ierapetra. The west and the mountains get the most.

## Alt text

Graphic in the "Did you know?" series, titled "Crete gets far more rain in the west and on its mountains". A map of Crete shaded by average yearly rainfall on a 1 km grid for 1981-2019, from about 530 mm on the coasts to over 1,700 mm in the White Mountains, with darker areas also on Psiloritis and the Lasithi mountains. Eight stations are labelled with their measured yearly averages for 2006-2025: Chania 580 mm, Samaria (Xyloskalo) 1,540 mm, Rethymno 520 mm, Anogeia 990 mm, Heraklion 460 mm, Tzermiado 1,020 mm, Ierapetra 360 mm, Sitia 500 mm. Below, bars show the island average in bands from west to east, falling from about 1,010 to 1,130 mm in the west to about 640 to 770 mm in the east: about 1,050 mm a year west of Rethymno and about 690 mm east of the Lasithi Plateau.

## Sources and checks

- Station averages (NOA / meteo.gr monthly records 2006-2025, complete years only, `scripts/noa_stations.py`; mm per year, first year, complete years): Samaria/Xyloskalo 1,544.7 (2008, 17); Chania 576.2 (2006, 19); Rethymno 516.9 (2007, 18); Anogeia 989.2 (2008, 16); Heraklion 462.2 (2006, 19); Tzermiado 1,023.9 (2006, 19); Ierapetra 356.4 (2008, 17); Sitia 504.6 (2010, 15). Rounded to 10 mm in the text and figure. NOA "Samaria" is taken as the Xyloskalo station, as in the 8 October floods post.
- "More than four times": 1,544.7 / 356.4 = 4.3. "About twice": Anogeia 989.2 and Tzermiado 1,023.9 against Heraklion 462.2 (2.1 and 2.2).
- Grid (CLIMADAT-Grid v1, mean annual precipitation 1981-2019, land cells, `reference/`): west of 24.5° E (Rethymno) 1,054 mm; east of 25.5° E (Lasithi Plateau) 693 mm; whole island 866 mm; range 530 to 1,755 mm. Varotsos et al. (2025), Earth System Science Data 17, 4455-4477, doi:10.5194/essd-17-4455-2025; CC BY 4.0.
- Grid values are higher than station values at the same place (e.g. 862 mm at Chania on the grid against 576 mm measured): different periods (1981-2019 vs 2006-2025) and smoothing; stated in the post.
- Xyloskalo to Chania: about 24 km in a straight line ("about 25 km").
- "A grid of about 100 km": the C3S seasonal forecasts are on a 1° grid (about 90 by 110 km at Crete's latitude).
- The 2 November rain in the southwest is not used (no NOA totals checked). No project results; public, published datasets only.
- Figure: brand style, 1350 x 1350 px, checked by eye. Station positions approximate.
