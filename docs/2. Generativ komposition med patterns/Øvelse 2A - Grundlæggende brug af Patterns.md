# Øvelse 2A: Grundlæggende brug af Patterns

I øvelse 2A.1-2A.4 skal du skrive dine egne Pbind-kompositioner. Du kan blot kopiere nedenstående skabelon for at gå i gang:

```sc title="Skabelon"
(
Pbind(

).play;
)
```

## 2A.1: Tonehøjde-nøgler i Pbind - spil følgende toner i uendelig gentagelse
- Tonen c (brug `\degree`).
- Tonen d (brug `\degree` eller `\root`).
- Tonen d ved oktav 3 (brug `\degree og \octave`).
- Tredje trin på en c-mol skala (brug `\scale` og `\degree`).
- En f-mol-akkord (vælg selv passende nøgler).

## 2A.2: Rytmik i Pbind - spil følgende i uendelig gentagelse

- Tonen c en gang pr. taktslag.
- Tonen c to gange pr. taktslag.
- Tonen c 4 gange pr. taktslag.
- Tonen c 2 gange pr. taktslag med legato-frasering.
- Tonen c 5 gange pr. taktslag med staccato-frasering.
- Tonen c 1 gang pr. taktslag ved 40 BPM.
- Tonen c fire gange pr. taktslag ved 150 BPM.

## 2A.3: Afspil følgende sekvenser i uendelig gentagelse ved hjælp af Pseq

- Første frase i melodien til 'Mester Jakob' (brug `Pseq` sammen med `\degree` og `\dur`).
- Første frase i melodien til 'Mester Jakob' i D#-dur (brug `\root` til at angive grundtonen).
- Første frase i melodien til 'Mester Jakob', spillet i en frygisk skala i stedet for en dur-skala (brug `\scale`).
- Et c, der veksler mellem oktav 3 og 4.
- En akkordbrydning (Dm7).
- En selvkomponeret rytme, som indeholder ottendele, fjerdedele og halvnoder (brug `\dur`).
- En sekvens, hvor alle toner spilles legato pånær hver 4. tone i sekvensen, som spilles staccato (brug nøglen `\legato`).

## 2A.4: Afspil følgende ved hjælp af Pwhite

- 10 toner, valgt tilfældigt inden for en C-dur-skala.
- Tilfældige frekvenser mellem 500 og 1000 hz (brug nøglen `\freq`).
- Spil en uendelig række af akkordbrydninger med uregelmæssig rytmik og frasering.
- Spil tilfældige skalatrin inden for en F-mol-skala, hvor alle toner gentages én gang (brug `.stutter`).

## 2A.5: Tilfældighed med lister 

- Afspil med `Prand` 10 tilfældigt valgte elementer fra arrayet `~skalatrin`.
- Afspil med `Pshuf` arrayet `~skalatrin` 2 gange i en tilfældig rækkefølge.
- Afspil arrayet ~skalatrin i en tilfældig rækkefølge 4 gange, gentag herefter dette med en ny tilfældig rækkefølge (dette kan gøres ved at kombinere `Pshuf` og `.repeat`).   

```sc
~skalatrin = [-2, 0, 1, 3, 4, 6];
```

## 2A.6: Find fire fejl

- Find og ret fejlene i de fire eksempler herunder.
- Vigtigt: Læs altid fejlmeddelelsen, før du retter fejlen!
- Forklar i en kommentar for hvert eksempel hvad du har rettet og hvad problemet bestod i.
- Ryd SuperColliders post window (Ctrl+Shift+p) inden du starter med et nyt eksempel.

```sc title="Find fire fejl"
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
