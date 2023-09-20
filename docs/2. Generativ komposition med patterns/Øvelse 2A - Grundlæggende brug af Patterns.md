# Øvelse 2A: Grundlæggende brug af Patterns

Med denne øvelse får du grundlæggende erfaring med brug af patterns. Opgaverne er simple i forhold til potentialet i patterns, men en god forståelse af de grundlæggende forhold er afgørende for at man kan arbejde med de mere komplicerede teknikker senere hen.

## Opgave 1: Find fire fejl

1. Find og ret fejlene i de fire eksempler herunder.
1. Læs fejlmeddelelsen, før du retter fejlen.
1. Forklar i en kommentar for hvert eksempel hvad du har rettet og hvad problemet bestod i.
1. Ryd SuperColliders post window (Ctrl+Shift+p) inden du starter med et nyt eksempel.

```sc title="Opgave 1: Find fire fejl"
(
Pbind(
	Pwhite(0, 7), \degree,
).play;
)

(
Pbind(
	\degree, Pseq(3, 7),
).play;
)

(
Pbind(
	\degree, Pwhite(0, 7);
	\dur, 0.5;
).play;
)

(
Pbind(
	\dur, 0.25,
	\octave, Pseq([3. 4. 5]),
).play;
)
```

## Skabelon til opgave 2-6

I opgave 2-6 skal du skrive dine egne Pbind-kompositioner. Du kan blot kopiere nedenstående skabelon for at gå i gang:

```sc title="Skabelon"
(
Pbind(

).play;
)
```

## Opgave 2: Tonehøjde i `Pbind`

Denne opgave fokuserer på brug af nøgler til angivelse af tonehøjde i Pbind. Der skal ikke anvendes patterns (ud over Pbind).

Spil følgende toner i uendelig gentagelse:

1. Tonen c (brug `\degree`).
1. Tonen d (brug `\degree` eller `\root`).
1. Tonen d ved oktav 3 (brug `\degree og \octave`).
1. Tredje trin på en c-mol skala (brug `\scale` og `\degree`).
1. En A-dur-akkord (brug `\root` og `\degree`).
1. En f-mol-akkord (vælg selv passende nøgler).

## Opgave 3: Rytmik i `Pbind`

Denne opgave fokuserer på brug af nøgler til angivelse af rytmik og frasering i Pbind samt tempoangivelse med `TempoClock`. Der skal ikke anvendes patterns (ud over Pbind).

Spil tonen c i uendelig gentagelse med følgende rytmik og frasering:

1. Fjerdedele (én tone pr. taktslag).
1. Ottendedele (to toner pr. taktslag).
1. Sekstendedele (4 toner pr. taktslag).
1. Ottendedele med legato-frasering.
1. Ottendedele med staccato-frasering.
1. Fjerdedele ved 40 BPM.
1. Ottendedele ved 150 BPM.

## Opgave 4: Sekvenser med `Pseq`

Denne opgave fokuserer på brug af `Pseq` til at angive sekvenser.

Spil følgende ved hjælp af `Pseq`:

1. Første frase i melodien til 'Mester Jakob' (brug nøglen `\degree`).
1. Første frase i melodien til 'Mester Jakob' i D#-dur (brug `\root` til at angive grundtonen).
1. Første frase i melodien til 'Mester Jakob', spillet i en frygisk skala i stedet for en dur-skala (brug `\scale`).
1. Et c, der veksler mellem oktav 3 og 4.
1. En akkordbrydning (Dm7).
1. En selvkomponeret rytme, som indeholder ottendele, fjerdedele og halvnoder (brug `\dur`).
1. En sekvens, hvor alle toner spilles legato pånær hver 4. tone i sekvensen, som spilles staccato (brug nøglen `\legato`).

## Opgave 5: Tilfældighed med `Pwhite`

Afspil følgende ved hjælp af `Pwhite`:

1. 10 toner, valgt tilfældigt inden for en C-dur-skala.
1. Tilfældige frekvenser mellem 500 og 1000 hz (brug nøglen `\freq`).
1. Spil en uendelig række af akkordbrydninger med uregelmæssig rytmik og frasering.
1. Spil tilfældige skalatrin inden for en F-mol-skala, hvor alle toner gentages én gang (brug `.stutter`).

## Opgave 6: Tilfældighed med lister

1. Afspil med `Prand` 10 tilfældigt valgte elementer fra arrayet `~skalatrin`.
1. Afspil med `Pshuf` arrayet `~skalatrin` 2 gange i en tilfældig rækkefølge.
1. Afspil arrayet `~skalatrin` i en tilfældig rækkefølge 4 gange, gentag herefter dette med en ny tilfældig rækkefølge (dette kan gøres ved at kombinere `Pshuf` og `.repeat`).   

```sc
~skalatrin = [-2, 0, 1, 3, 4, 6];
```
