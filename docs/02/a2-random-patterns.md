---
tags:
    - Artikler
---
# Patterns og tilfældighed

I SuperCollider findes der mange forskellige patterns, som genererer tilfældige værdier. Herunder sammenlignes de mest almindelige af disse, idet der også gives eksempler på hvornår de forskellige redskaber meningsfuldt kan anvendes. Dog er der ikke nogen endegyldig facitliste for hvilke patterns man skal bruge i hvilke situationer, da de kan anvendes og kombineres frit.

Man kan - meget groft - skelne mellem to kategorier:

- **Tilfældighedsgeneratorer**, som genererer tilfældige værdier ud fra 2-3 parametre såsom øvre/nedre grænser og middelværdier
- **Listebaserede generatorer**, som på forskellig vis genererer tilfældigt output baseret på lister

## Tilfældighedsgeneratorer

Hvorfor mon der er flere forskellige tilfældighedsgeneratorer at vælge imellem? Jo, det skyldes, at der er stor forskel på hvor sandsynlige, de mulige værdier er.

`Pwhite`

:   Alle tal mellem et givet minimum og maksimum er lige sandsynlige. Relateret til den måde hvorpå man genererer [hvid støj](https://en.wikipedia.org/wiki/White_noise#Statistical_properties). Anvendes typisk når man ønsker "helt" tilfældige værdier med mulighed for store og små spring. Fx ved atonal eller arytmisk komposition.
    ![10.000 værdier genereret med `Pwhite(0, 100, 10000)`](../media/figures/pwhite.png){: .w100 }

`Pbrown`

:   Genererer tilfældige værdier, men med begrænsede trin. Algoritmen kendes også som en [random walk/drunkard's walk](https://en.wikipedia.org/wiki/Random_walk). Pbrown bruges, når man ønsker en gradvis udvikling i en strøm af tilfældigt valgte værdier, dvs. hvor springene mellem de enkelte skridt er begrænsede. Det kunne fx være ved trinbevægelser i melodier eller en cutoff-frekvens, som skal bevæge sig mere organisk mellem forskellige værdier.
    ![10.000 værdier genereret med `Pbrown(0, 100, 2, 10000)`](../media/figures/pbrown.png)

`Pgauss`

:   Tal tæt på en middelværdi er mere sandsynlige end tal, der ligger længere væk. Baseret på [normalfordelingen/Gaussfordelingen](https://da.wikipedia.org/wiki/Normalfordeling). Anvendes fx hvis man ønsker, at de fleste værdier skal ligge i omegnen af et centrum, fx midt i stereobilledet eller en skala, men hvor der kan være nogle fåvildskud.
    ![10.000 værdier genereret med `Pgauss(50, 17, 10000)`](../media/figures/pgauss.png)

`Pexprand`

:   Tal tættest på minimumværdien er mest sandsynlige. Baseret på [eksponentialfordeling](https://en.wikipedia.org/wiki/Exponential_distribution). Anvendes typisk hvor man ønsker en Pwhite-lignende fordeling inden for fx frekvens eller lydstyrke (teknisk set fordi menneskelig perception på disse parametre bedst kan beskrives med eksponentiel/logaritmisk funktion).
    ![10.000 værdier genereret med `Pexprand(0.01, 100, 10000)`](../media/figures/pexprand.png)

`Phprand`

:   Tal tættest på en øvre grænse er mest sandsynlige.
    ![10.000 værdier genereret med `Phprand(0, 100, 10000)`](../media/figures/phprand.png)

`Plprand`

:   Tal tættest på en nedre grænse er mest sandsynlige. Anvendes, hvor man kun ønsker få værdier tæt på en øvre grænse.
    ![10.000 værdier genereret med `Plprand(0, 100, 10000)`](../media/figures/plprand.png)

## Listebaserede generatorer

Disse patterns anvender vi, hvis vi gerne vil definere en række mulige udfald, men vil lade algoritmen bestemme hvordan der vælges mellem valgmulighederne eller hvilken rækkefølge en foruddefineret sekvens afspilles i.

Der findes tre patterns, som minder meget om hinanden og alle tre vælger tilfældige elementer fra en liste, som vi angiver:

`Prand`

:   Vælger tilfældige tal fra en given liste. Anvendes, når man blot ønsker, at algoritmen vælger blandt et andet givne valgmuligheder.

`Pxrand`

:   Fungerer præcis ligesom `Prand`, bortset fra, at samme element ikke vælges to gange i træk. Anvendes, hvis vi fx ikke ønsker tone- eller rytmegentagelser.

`Pwrand`

:   Vælger også tilfældige tal fra en given liste, men med forskellige sansyndligheder for valg af de enkelte elementer. Anvendes, hvis nogle valgmuligheder skal forekomme oftere end andre. Det kunne fx være rytmiske variationer, som er mindre hyppige end mere almindelige grooves.

`Pshuf`

:   Fungerer ligesom den almindelige `Pseq`, bortset fra, at den givne liste afspilles i en tilfældig rækkefølge. Kan være nyttigt, hvor man ønsker at gentage en sekvens, selvom selve sekvensen er sat i tilfældig rækkefølge - det kan give en fornemmelse af regelmæssighed, selvom rækkefølgen er ny.

