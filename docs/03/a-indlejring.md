---
tags:
    - Artikler
---

??? abstract "Introduktion til kapitlet"

    Dette kapitel introducerer til nogle mere avancerede teknikker inden for pattern-baseret komposition. Dernæst ser vi på, hvordan man indlejrer patterns som input til andre patterns, altså en form for "pattern-inception". Vi kigger også på, hvordan man kan sammensætte patterns og skabe variationer over de mønstre, vi definerer med `Pbind`. Derefter introduceres brugen af SuperColliders patterns til komposition via MIDI-output, således at vi i stedet for SuperColliders lydserver bruger en ekstern synthesizer eller sampler som lydgenerator til at skabe mere interessant klingende kompositioner. Med disse mere avancerede anvendelser af patterns kan vi skabe komplekse og varierede kompositionsmønstre. Til sidst ser vi i en øvelse på, hvordan man i sammenhæng kan bruge de introducerede teknikker til at arbejde med minimalistisk inspireret komposition.

# Indlejrede patterns

Det er relativt let at lave en simpel, algoritmisk komposition ved hjælp af patterns. Men det kan være mere vanskeligt at bevæge sig videre fra det meget simple eller meget tilfældighedsprægede udtryk. Her kan såkaldt indlejring af patterns være med til at give et mere nuanceret og subtilt udtryk.

Generativ eller algoritmisk komposition indebærer, at man i et vist omfang overlader dele af det kompositoriske arbejde til et system eller en algoritme. Her spiller [tilfældighedsgeneratorer](../02/a-random-patterns.md) ofte en betydelig rolle. Total tilfældighed er imidlertid sjældent specielt interessant. Derfor kan man med fordel indlejre tilfældighed som et begrænset element i en ellers fastlagt struktur, eller filtrere/afgrænse/gentage tilfældigt genererede data, så der skabes orden ud af en ellers kaotisk strøm af output.

## Sekvenser af patterns

Vi har tidligere set, [hvordan vi kan generere sekvenser af værdier](../02/a-patterns-intro.md#pseq-en-fleksibel-sequencer). Men `Pseq` er fleksibel og kan lige så vel bruges til sekvenser bestående af patterns. Det betyder, at vi som elementer i vores sekvens kan angive patterns i stedet for værdier. Når `Pseq` når til et pattern, gennemløber den nemlig alle de værdier, som det pågældende pattern genererer, før den går videre. Her er eksempelvis en sekvens med en blanding af faste og tilfældigt genererede skalatrin:

```sc title="Patterns som undersekvenser"
Pbind(
    \degree, Pseq([
        // først en fast starttone, c
        0,
        // derefter to tilfældige toner
        Pwhite(0, 7, 2),
        // derefter g og h i tilfældig rækkefølge
        Pshuf([-1, -3]),
        // og til sidst et dybt g
        -3
    // sekvensen forløber tre gange
    ], 3),
).play;
```

![type:audio](../media/audio/03-pattern-sekvens.ogg)

For overskuelighedens skyld kan vi opnå præcis det samme som ovenfor med variabler til de enkelte underpatterns. Nedenstående er umiddelbart lettere at læse:

```sc title="Omskrivning med variabler"
// To Tilfældige toner
~fritValg = Pwhite(0, 7, 2);
// g og h i tilfældig rækkefølge
~dybBlanding = Pshuf([-1, -3]);

Pbind(
    \degree, Pseq([0, ~fritValg, ~dybBlanding, -3], 3),
).play;
```

## Sammenflettede sekvenser og patterns

`Place` er et særligt pattern, som er velegnet til at flette sekvenser sammen. Her sætter man to eller flere sekvenser eller enkeltværdier sammen i et array, og `Place` veksler så mellem de forskellige kilder. Arrayet gennemløbes det antal gange, man angiver (herunder 4 gennemløb).

``` sc title="Sammenflettede sekvenser med Place"
(
Pbind(
    \degree, Place([
        [4, 3, 5, 4],
        [2, 1],
        -3,
        0
    ], 4).trace
).play;
)
// -> 4, 2, -3, 0, 3, 1, -3, 0, 5, 2, -3, 0, 4, 1, -3, 0

```

Der findes også en variant, som er endnu mere relevant i forhold til sammensætning af patterns, fordi den tillader, at man erstatter listerne i `Place` med patterns. `Ppatlace`, som denne variant hedder, er meget oplagt som ramme for indlejrede patterns og filtreret tilfældighed:

``` sc title="Sammenflettede patterns med Ppatlace"
Pbind(
    \degree, Ppatlace([
        Pshuf([2, 3, 4, -1], inf),
        Pwhite(4, 7).stutter(4),
    ], inf).trace,
    \dur, 0.25
).play;
```

![type:audio](../media/audio/03-ppatlace.ogg)

## Patterns som variererende argumenter

Man kan skabe interessante variationer ved at erstatte de faste værdier, vi ofte angiver som argumenter til patterns, med noget, som varierer. Som eksempel kan vi tage `Pseries`, der normalt giver lineære sekvenser ud fra tre argumenter - en startværdi, en trinstørrelse, og et antal:

```sc title="Pseries med faste argumenter"
Pseries(0, 1, 4)
// -> 0, 1, 2, 3
Pseries(6, -2, 5)
// -> 6, 4, 2, 0, -2
Pseries(5, 0.5, inf)
// -> 5, 5.5, 6, 6.5, 7, 7.5 ...
```

Hvis vi ønsker at varierere trinstørrelsen i `Pseries`, kan vi gøre det ved at *indlejre* noget, der varierer - fx et andet pattern! Det kræver, at vi konverterer det indlejrede pattern til en *stream*. Det lyder måske lidt teknisk, men bare rolig, streams er meget nært beslægtede med patterns - en stream er blot et objekt, der kan levere en strøm af værdier. Når patterns skal generere værdier, bliver de faktisk automatisk konverteret til streams - det sker blot under motorhjelmen. Det kan vi heldigvis også gøre manuelt:

```sc title="Pattern konverteret til stream"
// Først gemmer vi en Pseq som en stream
~stream = Pseq([1, 2, 3], inf).asStream;

// Derefter kan vi bede om en ny værdi fra strømmen gang efter gang med .next-method'en
~stream.next.postln;
// -> 1, 2, 3, 1, 2, 3, 1, 2, 3 ...
```

Det vil føre for vidt at uddybe den tekniske forskel mellem patterns og streams yderligere[^1], men for nuværende kan du blot huske på, at indlejrede patterns, der anvendes som argumenter til andre patterns, ofte skal konverteres til streams med den handy method `.asStream`.

[^1]: Teknisk nysgerrige læsere kan konsultere Fieldsteels [-@fieldsteel2021] [diskussion](https://www.youtube.com/watch?v=17uMs9HpMgE), som på ganske udmærket vis demonstrerer forbindelsen mellem patterns og streams.

For at vende tilbage til vores `Pseries` ovenfor: Hvis vi ønsker at variere trinstørrelsen fra tone til tone, kan vi eksempelvis vælge et tilfældigt tal mellem -1 og 1 på disse to måder:

```sc title="Varierende spring med indlejret Pwhite"
Pseries(0, Pwhite(-1, 1).asStream, 10);
// -> 0, -2, -1, 0, 1, -1, 1, 3, 2, 2
```

Her er et andet musikalsk eksempel, hvor vi bruger `Pseries` til at styre hvor mange tilfældige toner fra Pwhite, der bliver flettet ind i sekvensen - med flere og flere for hvert gennemløbg.

```sc title="Varieret fraselængde med indlejret Pseries"
Pbind(
    \degree, Pseq([
        -7,
        -7,
        Pwhite(0, 4, length: Pseries(0, 1).asStream)
    ], 8),
    \dur, 0.25,
).play;
```

![type:audio](../media/audio/03-pseries-indlejret.ogg)
