---
tags:
    - Artikler
---

# Sammensætning af event patterns

Hidtil har vi betragtet patterns som opskrifter på strømme af værdier. Men hvis vi ser på `Pbind`, er det tydeligt, at den ikke producerer strømme af enkeltværdier, men i stedet producerer såkaldte *events* ud fra de nøgler og værdier/patterns, den knytter sammen. I denne terminologi svarer én event til én tone. `Pbind` er dermed et *event pattern*, i modsætning til *value patterns* som `Pwhite` og `Pbrown`, der producerer enkeltværdier. Man kan bruge event patterns som moduler, der kan sættes sammen og varieres på forskellig vis, og et par teknikker hertil demonstreres herunder.

## Sekvenser af Pbinds

Den mest åbenlyse måde at sammensætte Pbinds er at afvikle dem sekventielt, altså den ene efter den anden. Lad os eksempelvis definere to Pbinds, den ene med et rodet udtryk og den anden med et mere roligt udtryk. Bemærk, at vi ikke afspiller disse Pbinds med `.play` men i stedet gemmer dem under deskriptive variabelnavne.

```sc title="Tre simple Pbinds"
~op = Pbind(
    \degree, Pseries(0, 2, 4),
    \db, Pseries(-20, 2, 4)
);
~ned = Pbind(
    \degree, Pseries(1, -2, 4),
    \db, Pseries(-14, -2, 4)
);
~rundt = Pbind(
    \degree, Pseq([0, 1, 0, -1]),
    \db, Pgauss(-16, 2)
);
```

![type:audio](pbind-kombination.ogg)

Med ovenstående tre Pbinds gemt under variabelnavne kan vi afspille dem i en sekvens med velkendte, listebaserede patterns som `Pseq`, `Prand` m.fl.:

```sc title="Sekvensering af Pbinds"
~sekvenser = [~op, ~ned, ~op, ~rundt];

Pseq(~sekvenser).play;
Prand(~sekvenser, 4).play;
Pxrand(~sekvenser, 4).play;
Pshuf(~sekvenser, 4).play;
```

## Begrænsning af Pbind-output med Pfin og Pfindur

Nogle gange er det mere relevant at definere Pbinds, som ikke har en begrænset varighed (dvs. hvor ingen af de anvendte value patterns har et endeligt antal output), og derefter begrænse, hvor mange events, de producerer. På den måde kan den samme Pbind anvendes i forskellige sammenhænge. Lad os eksempelvis definere to forskellige Pbinds, hvor den ene er lidt rodet i sin timing, dynamik og rytmik, mens den anden er mere regulært opbygget.

```sc title="To forskellige Pbinds"
(
~drunk = Pbind(
    \degree, Pbrown(-3, 7, 7),
    \ctranspose, Pwrand([0, -1], [0.9, 0.1], inf),
    \scale, Scale.minor,
    \dur, Pexprand(0.2, 0.8),
    \legato, 0.25,
    \db, Pwhite(-25, -10),
);
~sober = Pbind(
    \degree, Pbrown(-3, 6, 3),
    \scale, Scale.minorPentatonic,
    \dur, Prand([0.5, 1, 1.5], inf),
    \legato, Pexprand(1.3, 1.5),
    \db, Pgauss(-20, 2),
);
)```

Hvis vi kun ønsker tre events fra en af ovenstående Pbinds, kan vi bruge et pattern, der hedder `Pfin`. Vi kan også sekvensere `Pfin` med fx `Pseq`:

```sc title="Begrænsning af event-antal med Pfin"
TempoClock.tempo = 115/60;
Pfin(10, ~drunk).play;
Pfin(10, ~sober).play;

Pseq([ Pfin(8, ~drunk), Pfin(8, ~sober) ], 4).play;
```

Da disse to pbinds har varierende `\dur`-værdier, er det umuligt at forudsige hvor mange events vi skal vælge med `Pfin` for eksempelvis at spille én takt med den ene Pbind, én takt med den anden, og så fremdeles. Hertil kan vi i stedet bruge et nært beslægtet pattern, der hedder `Pfindur(varighedsgrænse, pattern, tolerance)`, som kan begrænse *varigheden* af en Pbind.

```sc title="Begrænsning af Pbind-varighed med Pfindur"
TempoClock.tempo = 115/60;
Pfindur(8.01, ~sober, 0.01).play;

(
Pseq([
    Pfindur(4.01, ~drunk, 0.01),
    Pfindur(4.01, ~sober, 0.01),
], 4).play;
)
```

## At kombinere Pbinds med Pbindf

Som [tidligere nævnt](../01/a-funktioner.md) kan det i programmering være fornuftigt med en vis portion strategisk dovenhed - forstået således, at det ofte er nyttigt at undgå at skulle skrive den samme kildekode flere gange. Dette princip kan også bruges i forbindelse med patterns, og det viser sig at være meget nyttigt til at skabe variationer og sammensætninger, hvis vi som nævnt ovenfor bygger vores patterns op i mindre moduler, der så kan sammensættes på nye måder.

Hertil kan vi bruge `Pbindf` (bemærk f'et til sidst i klassenavnet), som skaber en nye Pbind baseret på en anden, foruddefineret Pbind. Det betyder, at vi kan definere én Pbind, som kan varieres og lægges til grund for en række andre Pbinds, hvilket åbner mange muligheder for at arbejde med variation og musikalsk elaborering.

Vi bruger `Pbindf` ved at angive en eksisterende Pbind som det første argument. De efterfølgende argumenter fungerer præcis som ved Pbind. Her kan vi eksempelvis definere et enkelt melodisk motiv i én Pbind og i en anden lave en "overstemme" gennem modal transponering, dvs. parallelføring inden for skala.

```sc title="Overstemme med Pbindf"
(
~melodi = Pbind(
    \degree, Pseq([2, 1, 3, 2], 4),
    \dur, 0.5
);
~overstemme = Pbindf(~melodi,
    // Læg enten en terts eller en sekst til
    \mtranspose, Prand([2, 5], inf)
);

~melodi.play; ~overstemme.play;
)
```

![type:audio](overstemme.ogg)

Bemærk her, at vi i stedet for at omdefinere `\degree`-nøglen i Pbindf'en anvender `\mtranspose`. Havde vi brugt `\degree`, ville den eksisterende information om skalatrin fra `~melodi`-Pbind'en blive overskrevet. I stedet fungerer den oprindelige `Pseq` og den nye `Prand` sammen, så "stemmerne" kan følges ad.

## En minimalistisk kompositionsidé

Et mere interessant eksempel kan være en algoritme inspireret af det minimalistiske værk [*Piano Phase*](https://stevereich.com/composition/piano-phase/) fra 1967 af komponisten Steve Reich. I dette værk for to klaverer spiller hver pianist den samme melodiske frase igen og igen. Værkets særkende er, at den ene pianist spiller motivet i en lille smule højere tempo end den anden. Resultatet er, at frasens forskellige tonehøjder og rytmer konstant går ind og ud af "fase" med hinanden. Dette kan vi på simpel vis simulere med Pbindf, hvor vi sætter `\dur`-nøglen i to forskellige versioner af en `~basis`-Pbind til næsten ens nodeværdier.

```sc title="Forenklet udgave af Steve Reichs Piano Phase"
// Tempo 115 BPM
(
TempoClock.tempo = 115/60;

// Trinsekvenser
~trin = [0, 1, 4, 5, 6, 1, 0, 5, 4, 1, 6, 5];

~basis = Pbind(
    \root, 4,
    \octave, 4,
    \scale, Scale.dorian,
    \degree, Pseq(~trin, inf),
    \legato, 0.5,
);
~left = Pbindf(~basis, \dur, 0.250, \pan, -1).play;
~right = Pbindf(~basis, \dur, 0.252, \pan, 1).play;
)
~left.stop; ~right.stop;
```

![type:audio](piano-phase.ogg)

Dette er blot en forsimplet illustration af, hvordan *Piano Phase* fungerer. I slutningen af dette kapitel kan man øve sig i at skrive egne minimalistiske kompositioner, hvor lignende processer med gradvis udvikling gør sig gældende.
