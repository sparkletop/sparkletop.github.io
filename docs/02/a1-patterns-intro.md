---
tags:
    - Artikler
---

??? abstract "Introduktion til kapitlet"

	Generativ komposition kan være kernen i den kreative proces, når man komponerer, hvilket ofte er tilfældet inden for computermusikken. Men i bredere forstand kan vi også bruge generative processer til at skabe samples, sekvenser, variationer mm. til brug i mere traditionel komposition og lydproduktion.

	I SuperCollider udgør de såkaldte patterns et centralt redskab til generativ komposition. Dette kapitel introducerer først til patterns på et grundlæggende niveau, med særligt fokus på hvordan det centrale redskab `Pbind` knytter generative patterns til musikalske parametre som tonehøjde og rytmik. I [næste kapitel](../03/a1-indlejring.md) går vi mere i dybden med hvordan patterns blandt andet ved hjælp af en teknik kaldet *indlejring* kan kombineres til at danne komplekse, generative systemer. 

# Introduktion til patterns

SuperCollider indeholder et yderst righoldigt bibliotek af patterns, som vi kan kombinere på utallige, kreative måder. Men hvad er patterns egentlig? Patterns er *opskrifter på strømme af værdier*. Det lyder måske abstrakt, men det er egentlig ikke så galt: `Pseq` definerer en sekvens af værdier (ligesom en sequencer), `Pwhite` definerer en strøm af tilfældigt genererede værdier, `Pseries` definerer en lineær række af værdier (fx 1, 2, 3), osv. Og ja, du har nok allerede gættet hvordan man kan spotte et pattern - navnene på SuperColliders pattern-klasser starter belejligt nok altid med `P`. Det første pattern vi skal forstå er det såkaldte `Pbind`, som udgør rammen for de øvrige patterns, vi anvender.

## Rammen for generativ komposition: Pbind

Som udgangspunkt for generativ komposition laver vi en instans af klassen `Pbind`, som vi så kan afspiller med method'en `.play` (husk at boote lydserveren med `s.boot;`, hvis du ikke har gjort det allerede):

```sc title="Den simplest mulige Pbind-komposition"
// Kør denne linje for at starte kompositionen
~eksempel = Pbind().play;

// Kør denne linje for at stoppe igen
~eksempel.stop;
```

`Pbind` har den funktion, at den "binder" musikalske parametre sammen til en strøm af begivenheder. I Pbind bruger vi på den ene side *nøgler*, angivet med `\degree`, `\dur`, `\scale` og andre betegnelser til at angive kompositionsmæssige parametre, og vi bruger *patterns* eller *faste værdier* til at styre disse parametre.

Her er et enkelt eksempel, hvor vi med nøglen `\degree` vælger at knytte den musikalske parameter *skalatrin* sammen med en fast værdi, nemlig værdien 0 (første skalatrin).

``` sc title="Pbind og "
(
~eksempel = Pbind(
	\degree, 0,
).play;
)
~eksempel.stop;
```

Men ovenstående bliver hurtigt lidt ensformigt at lytte til. I stedet for faste værdier kan vi bruge et pattern til at generere forskellige værdier. Vi starter med `Pseq`, som vi kan bruge til at generere en sekvens af værdier - stadig skalatrin, fordi vi bruger `\degree`-nøglen.

``` sc title="Enkel tonesekvens med Pseq"
(
Pbind(
	\degree, Pseq([0, 1, 3, 4, 7]),
).play;
)
```

Alternativt kan vi lade computeren vælge skalatrin for os. Vi kan fx bruge `Pwhite` til at generere 5 tilfældige skalatrin inden for en oktav (trin 0-7).

``` sc title="Tilfældighed med Pwhite"
(
Pbind(
	\degree, Pwhite(0, 7, 5),
).play;
)
```

Vi kan også kombinere en fast sekvens med tilfældigt valgte værdier ved at knytte `Pwhite` til `\degree` og dermed tonehøjde, mens vi knytter `Pseq` til `\dur` og dermed varighed/rytmik. På den måde får vi en komposition med både faste og tilfældige parametre.

``` sc title="Kombination af Pwhite og Pseq"
(
Pbind(
	\degree, Pwhite(0, 7),
	\dur, Pseq([0.25, 0.5, 0.25], 4),
).play;
)
```

## Pseq - en fleksibel sequencer

I `Pseq` noterer vi først en liste med de elementer, som skal indgå i vores sekvens. Det gør vi med kantede parenteser, adskilt af kommaer, fx sådan her: `[a, b, c]`

``` sc title="En sekvens med Pseq"
(
Pbind(
	\degree, Pseq([0, 1, 2, 7]),
).play;
)
```

Vi kan som det næste argument (det, som står inde i Pbind-parenteserne) angive hvor mange gange sekvensen skal afspilles

``` sc title="Repetition med Pseq"
(
Pbind(
	\degree, Pseq([0, 1, 2, 7], 2),
).play;
)
```

I stedet for et bestemt antal gentagelser kan vi gentage uendeligt med nøgleordet `inf`:

``` sc title="Uendelig gentagelse med Pseq"
(
~eksempel = Pbind(
	\degree, Pseq([0, 1, 2, 7], inf),
).play;
)
~eksempel.stop;
```

Vi kan vælge at bruge `Pseq` til at styre flere forskellige parametre. Selvom den nederste `Pseq` herunder gentager sekvensen i det uendelige, slutter vores samlede sekvens af begivenheder, så snart den første Pseq i Pbind'en er fædig.

``` sc title="Flere Pseqs på én gang"
(
Pbind(
	\degree, Pseq([0, 1, 2, 7, 4, 3, 1, 2]),
	\dur, Pseq([0.25, 0.5, 0.25, 1], inf),
).play;
)
```

Det kan nogle gange være en god idé at bruge variabler til at fordele vores kode over flere linjer. Eksemplet herunder giver samme resultat som ovenfor:

``` sc title="Organisér koden med variabler"
(
~skalatrin = [0, 1, 2, 7, 4, 3, 1, 2];
~varigheder = [0.25, 0.5, 0.25, 1];
Pbind(
	\degree, Pseq(~skalatrin),
	\dur, Pseq(~varigheder, inf),
).play;
)
```

`Pseq` er i øvrigt beslægtet med andre listebaserede patterns, fx `Pshuf`, som sætter elementerne i tilfældig rækkefølge, eller `Prand`, som vælger tilfældige elementer fra listen.

``` sc title="Pseq's uforudsigelige søskende: Pshuf og Prand"
Pbind(\degree, Pshuf([0, 2, 4, 7], 2)).play; // samme tilfældige sekvens, afspillet to gange
Pbind(\degree, Prand([0, 2, 4, 7], 8)).play; // tilfældigt valgte elementer for hver tone
```

Elementerne i vores `Pseq`-sekvens kan være andre patterns, fx `Pwhite`, som vi så ovenfor. På den måde kan man blande variation og dynamik ind i sin komposition, men samtidig repetere og fastholde delelementer, så dele af sekvensen er genkendelig.

``` sc title="Indlejring af Pwhite i Pseq"
(
Pbind(
	\degree, Pseq([
		-7, 7,             // først et par faste toner
		Pwhite(-3, -1, 3), // derefter tre tilfældige, lidt dybe toner
		Pwhite(2, 4, 3),   // derefter tre tilfældige, lidt højere toner
	], 2).trace,         // afspil hele sekvensen to gange (og vis outputtet med .trace)
	\dur, 0.5,
).play;
)
```

Vi ser nærmere på forskellige teknikker til indlejring af patterns [i næste kapitel](../03/a1-indlejring.md).

## Introduktion til Pwhite, en tilfældighedsgenerator

`Pwhite` genererer tilfældige tal inden for et minimum og et maksimum.

```sc title="Elementær brug af Pwhite"
(
~eksempel = Pbind(
	\degree, Pwhite(0, 4),
).play;
)
~eksempel.stop;
```

Modsat `Pseq` kører `Pwhite` som udgangspunkt uendeligt, men vi kan begrænse *antallet* af tilfældige tal med et yderligere argument:

``` sc title="Pwhite med begrænset antal"
(
Pbind(
	\degree, Pwhite(0, 4, 3),
).play;
)
```

Angiver vi decimaltal i stedet for heltal som øvre og/eller nedre grænse for `Pwhite`s output, får vi også decimaltal som resultat:

```sc title="Pwhite - decimaltal vs. heltal"
Pbind(\degree, Pwhite(0, 7, 4).trace).play;
Pbind(\degree, Pwhite(0.0, 7.0, 4).trace).play;
```

Ligesom med `Pseq` kan vi bruge `Pwhite` til at styre en række forskellige andre parametre:

```sc title="Pwhite over det hele"
(
Pbind(
	// En fast sekvens af tonehøjder
	\degree, Pseq([0, 2, 4, 5], inf),
	
	// \db angiver Lydstyrke, målt i decibel
	\db, Pwhite(-30, -20),
	
	// \dur angiver tonevarigheder, målt i antal taktslag
	\dur, Pwhite(0.1, 0.2),

	// \pan angiver panorering, hvor -1 er venstre og 1 er højre
	\pan, Pwhite(-1.0, 1.0),
).play;
)
```

Med `Pwhite` er alle tal mellem minimum og maksimum lige sandsynlige. Dette er dog ikke altid den mest interessante statistiske fordeling - fx kan det være mere oplagt, at værdierne tættere på en bestemt grænse er mest sandsynlige, eller at udfaldene fordeler sig omkring en middelværdi efter en normalfordeling. Det kan vi gøre med `Pexprand` og `Pgauss`:

```sc title="Alternativ sandsynlighedsfordeling med Pexprand og Pgauss"
Pbind(\legato, Pexprand(0.01, 1, 8).trace).play; // værdier tættere på minimum (0.01) er mest hyppige
Pbind(\legato, Pgauss(1, 0.1, 8).trace).play; // værdier tættest på middelværdi (1) er mest hyppige
```

Det kan også være relevant at bevæge sig gradvist op eller ned med tilfældige spring, hvilket kan gøres med `Pbrown`:

```sc title="Trinvis tilfældighed med Pbrown"
Pbind(\degree, Pbrown(-7, 7, 1, 8).trace).play; // små spring
Pbind(\degree, Pbrown(-7, 7, 5, 8).trace).play; // større spring
```

Vi kigger nærmere på disse forskellige tilfældighedsgenerator i [næste afsnit](a2-random-patterns.md) samt i [cheat sheetet vedr. patterns](c2-patterns.md).

## Nyttige teknikker til at arbjede med patterns

Når vi arbejder med patterns som kompositionsredskaber, er det typisk relevante at justere eller transformere output fra patterns. Det kan fx gøres med almindelige matematiske operationer:

```sc title="Matematiske operationer med outputtet fra patterns"
Pbind(\degree, Pseq([0, 1, 2])).play;
// -> 0, 1, 2

Pbind(\degree, Pseq([0, 1, 2]) + 1).play;
// -> 1, 2, 3

Pbind(\degree, Pseq([0, 1, 2]) * 2).play;
// -> 0, 2, 4

Pbind(\degree, Pseq([0, 1, 2]) * Pseq([1, 3], inf)).play;
// -> 0, 3, 2
```

Afrunding er også muligt - fx kan vi afrunde tilfældigt genererede tal mellem -12 og +12 til nærmeste tal i 3-tabellen og derved få en skala, der er bygget op af små tertser:

```sc title="Afrunding med .round"
(
Pbind(
    \scale, Scale.chromatic,
    \degree, Pwhite(-12, 12).round(3),
).play;
)
```

Vi kan også bruge nogle specifikke pattern-methods til at gentage outputtet fra patterns på forskellig vis. Kør nedenstående kode og gæt selv hvad `.repeat`, `.stutter` og `.clump` gør:

```sc title="Pattern-methods: .repeat, .stutter og .clump"
Pbind(\degree, Pseq([0, 1, 2]).repeat(3)).play;
// -> 0, 1, 2, 0, 1, 2, 0, 1, 2

Pbind(\degree, Pseq([0, 1, 2]).stutter(3)).play;
// -> 0, 0, 0, 1, 1, 1, 2, 2, 2

Pbind(\degree, Pseq([0, 1, 2]).clump(3)).play;
// [0, 1, 2], [0, 1, 2], [0, 1, 2]
```
