# Prace Fritsa Veermana związane z metastabilnością i opóźnioną destabilizacją

Data przeglądu: 13 sierpnia 2026 r.

Źródło wyjściowe: [profil Google Scholar Fritsa Veermana](https://scholar.google.com/citations?user=o2HjrOoAAAAJ&hl=it), 33 rekordy widoczne w profilu. Wśród rekordów są preprinty i późniejsze wersje tej samej pracy, corrigendum oraz materiały warsztatowe.

## Kryterium

Za ścisłą metastabilność przyjęto sytuację, w której dla niezmiennych parametrów rozwiązanie pozostaje przez długi czas blisko stanu wyglądającego na stabilny, ale następnie od niego odchodzi wskutek słabej niestabilności, przejścia między skalami czasowymi albo rzadkiego zdarzenia.

Przy tak ścisłym kryterium nie znalazłem na profilu pracy, która wprost używa pojęcia „metastability” dla własnego głównego wyniku i analizuje czas ucieczki z długowiecznego stanu quasi-stabilnego. Poniższe trzy prace są jednak bardzo bliskie pytaniu: badają utratę stabilności pozornie stacjonarnych struktur, bifurkacje Hopfa i późniejszą dynamikę. W pobliżu progu Hopfa dodatnia część rzeczywista wartości własnej może być bardzo mała, więc odejście od impulsu może być wolne; to jest wniosek z analizy spektralnej, a nie terminologia użyta przez autorów.

## Najtrafniejsze prace

### 1. F. Veerman, A. Doelman, *Pulses in a Gierer–Meinhardt Equation with a Slow Nonlinearity* (2013)

- Publikacja: SIAM Journal on Applied Dynamical Systems 12(1), 28–60.
- DOI: [10.1137/120878574](https://doi.org/10.1137/120878574).
- Dlaczego pasuje: autorzy znajdują kilka mechanizmów stabilizacji i destabilizacji impulsu. W symulacji po destabilizującej bifurkacji Hopfa początkowy wzrost zaburzenia przechodzi dla dłuższych czasów w ograniczony, oscylujący („breathing”) impuls. Praca pokazuje również złożone zachowanie blisko progu stabilności.
- Ograniczenie: jest to utrata stabilności przy przekroczeniu progu parametru, a nie osobna teoria czasu życia stanu metastabilnego.
- PDF: `2013_Veerman_Doelman_Pulses_slow_nonlinearity.pdf`.

### 2. F. Veerman, *Breathing Pulses in Singularly Perturbed Reaction-Diffusion Systems* (2015)

- Publikacja: Nonlinearity 28(7), 2211–2246.
- DOI: [10.1088/0951-7715/28/7/2211](https://doi.org/10.1088/0951-7715/28/7/2211).
- Dlaczego pasuje: praca rozwija nieliniową analizę słabo niestabilnego impulsu w pobliżu bifurkacji Hopfa. Stacjonarny impuls traci stabilność, a dla superkrytycznej bifurkacji pojawia się stabilny impuls okresowo oscylujący. Wynik jest potwierdzony bezpośrednią symulacją PDE.
- Ograniczenie: opisuje bifurkację i stan po destabilizacji; nie wyznacza czasu oczekiwania na ucieczkę z quasi-stabilnego stanu.
- Ważna poprawka: równanie (5.35) poprawiono w [corrigendum z 2017 r., DOI 10.1088/1361-6544/aa5259](https://doi.org/10.1088/1361-6544/aa5259).
- PDF: `2015_Veerman_Breathing_pulses.pdf`.
- Corrigendum: `2017_Veerman_Corrigendum_Breathing_pulses.pdf`.

### 3. A. Doelman, J. D. M. Rademacher, B. de Rijk, F. Veerman, *Destabilization Mechanisms of Periodic Pulse Patterns Near a Homoclinic Limit* (2018)

- Publikacja: SIAM Journal on Applied Dynamical Systems 17(2), 1833–1890.
- DOI: [10.1137/17M1122840](https://doi.org/10.1137/17M1122840).
- Dlaczego pasuje: jest to najbardziej bezpośrednia praca o destabilizacji. Pokazuje, jak długofalowe periodyczne wzorce impulsowe tracą stabilność przez dwa naprzemienne mechanizmy Hopfa, gdy zbliżają się do granicy homoklinicznej. Wzorzec może więc znajdować się bardzo blisko granicy stabilności i odejść po wzroście słabego modu niestabilnego.
- Ograniczenie: analiza jest liniowa i spektralna. Autorzy wprost zaznaczają, że pełna długoterminowa dynamika po destabilizacji wymaga analizy nieliniowej i pozostaje otwartym problemem.
- PDF: `2018_Doelman_Rademacher_deRijk_Veerman_Destabilization.pdf`.

## Prace uzupełniające / graniczne

### 4. F. Veerman, I. Schneider, *Controlling Pulse Stability in Singularly Perturbed Reaction-Diffusion Systems* (2023)

- Publikacja: Chaos 33, 083135.
- DOI: [10.1063/5.0152695](https://doi.org/10.1063/5.0152695); [preprint arXiv](https://arxiv.org/abs/2304.03342).
- Związek: pokazuje, że impuls, który bez sterowania jest niestabilny, można ustabilizować nieinwazyjnym sprzężeniem zwrotnym typu Pyragasa. Dobrze rozdziela „wygląd rozwiązania” od jego rzeczywistej stabilności spektralnej.
- Dlaczego nie jest ścisłym trafieniem: celem jest kontrola z góry znanej niestabilności, nie spontaniczna późna destabilizacja.
- PDF: `2023_Veerman_Schneider_Controlling_pulse_stability.pdf`.

### 5. A. Iuorio i in., *Modelling How Negative Plant–Soil Feedbacks Across Life Stages Affect the Spatial Patterning of Trees* (2023)

- Publikacja: Scientific Reports 13, 19128.
- DOI: [10.1038/s41598-023-44867-0](https://doi.org/10.1038/s41598-023-44867-0).
- Związek: rozróżnia przejściową i stabilną organizację przestrzenną oraz porównuje różne zachowania długoterminowe. Jest istotna, jeśli przez „metastabilność” rozumie się szeroko długotrwały wzorzec przejściowy.
- Dlaczego nie jest ścisłym trafieniem: nie wykazuje, że obserwowany wzorzec jest słabo niestabilnym stanem metastabilnym ani nie analizuje czasu ucieczki.
- PDF nie został zapisany: strona udostępnia tekst otwarty, lecz bezpośrednie pobranie pliku było blokowane w tej sesji.

## Praca podstawowa, ale poza kryterium czasowym

A. Doelman, F. Veerman, *An Explicit Theory for Pulses in Two Component, Singularly Perturbed, Reaction–Diffusion Equations* (2015), [DOI 10.1007/s10884-013-9325-2](https://doi.org/10.1007/s10884-013-9325-2), tworzy ogólną teorię istnienia, stabilności i bifurkacji impulsów. Jest ważnym tłem dla trzech prac powyżej, ale nie bada długiego stanu quasi-stabilnego zakończonego późną destabilizacją. Nie znaleziono legalnego otwartego PDF-u.

## Kontrola wszystkich 33 rekordów profilu

| # | Rekord z profilu | Ocena względem kryterium |
|---:|---|---|
| 1 | An Explicit Theory for Pulses in Two Component… | tło: stabilność i bifurkacje, brak dynamiki metastabilnej |
| 2 | Pulses in a Gierer–Meinhardt Equation with a Slow Nonlinearity | **najtrafniejsza** |
| 3 | Beyond Turing: Far-from-Equilibrium Patterns and Mechano-Chemical Feedback (bioRxiv) | nie: powstawanie wzorców daleko od równowagi |
| 4 | Breathing Pulses in Singularly Perturbed Reaction-Diffusion Systems | **najtrafniejsza** |
| 5 | Quasiperiodic Phenomena in the Van der Pol–Mathieu Equation | nie: stabilne/niestabilne rozwiązania okresowe i quasi-okresowe zależne od parametrów |
| 6 | A Predator–2 Prey Fast–Slow Dynamical System for Rapid Predator Evolution | nie: szybkie przełączenia i orbity okresowe, bez metastabilnej ucieczki |
| 7 | The Influence of Autotoxicity on the Dynamics of Vegetation Spots | graniczna, ale brak wykazanej późnej utraty stabilności |
| 8 | Modeling and Optimization of Algae Growth | nie |
| 9 | Time-Dependent Propagators for Stochastic Models of Gene Expression | nie: metoda propagatorów, bez analizy metastabilnych przejść |
| 10 | Travelling Pulses on Three Spatial Scales… | nie: istnienie impulsów wędrujących |
| 11 | Far-from-Equilibrium Traveling Pulses… | nie: istnienie impulsów wędrujących |
| 12 | Destabilization Mechanisms of Periodic Pulse Patterns Near a Homoclinic Limit | **najtrafniejsza** |
| 13 | Modelling How Negative Plant–Soil Feedbacks… | **graniczna: wzorce przejściowe i zachowania długoterminowe** |
| 14 | Analysis of a Model for Ship Maneuvering | nie |
| 15 | Parameter Inference with Analytical Propagators… | nie |
| 16 | Robust Stability of Multicomponent Membranes… | nie: odporna stabilność, nie późna destabilizacja |
| 17 | Travelling Waves Due to Negative Plant–Soil Feedbacks… | nie: fale wędrujące |
| 18 | Curvature Induced Patterns… | graniczna: stabilność badana numerycznie, brak wyniku o metastabilnej ucieczce |
| 19 | Two Interconnected Patterning Loops… in Hydra | nie |
| 20 | Controlling Pulse Stability… | **uzupełniająca: kontrola niestabilnego impulsu** |
| 21 | Travelling Front Solutions in a Spatially Heterogeneous Reaction-Diffusion System | nie: dwa stabilne tła i poruszający się front |
| 22 | Up and Beyond—Building a Mountain in the Netherlands | nie |
| 23 | Constructing Far-from-Equilibrium Patterns… | nie: konstrukcja wzorców stacjonarnych |
| 24 | Guerrilla Clonal Growth Strategy Leads to Amorphous Pattern Formation… | nie znaleziono wyniku o metastabilnej ucieczce |
| 25 | How Inertia Affects Autotoxicity-Mediated Vegetation Dynamics… | nie znaleziono wyniku o metastabilnej ucieczce |
| 26 | Beyond Turing (wersja czasopismowa) | duplikat/wersja rekordu #3; nie |
| 27 | Modelling the Impact of Soil-Borne Pathogens… (warsztat) | materiał warsztatowy związany z #13 |
| 28 | Short Amphiphilic Molecules… | nie |
| 29 | Corrigendum: Breathing Pulses… | poprawka do rekordu #4, nie osobna analiza |
| 30 | Up and Beyond… (wersja 2013) | wersja rekordu #22; nie |
| 31 | CASA-Report 10-59 October 2010 | wersja raportowa związana z rekordem #8; nie |
| 32 | Two Separate but Interconnected Pattern Formation Systems… in Hydra | wcześniejsza wersja rekordu #19; nie |
| 33 | Mathema | zbiorczy materiał SWI, nie osobna praca o metastabilności |

## Najkrótszy wniosek

Jeśli szukane są prace, w których rozwiązanie stacjonarne traci stabilność i dopiero później widoczna jest inna dynamika, należy zacząć od pozycji 1–3. Jeśli wymagana jest ścisła teoria metastabilności z oszacowaniem czasu życia quasi-stabilnego stanu przy stałych parametrach, na sprawdzonym profilu nie ma takiej pracy.
