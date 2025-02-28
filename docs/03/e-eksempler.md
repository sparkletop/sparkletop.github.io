---
tags:
    - Øvelser
---

# Øvelse: Analyse og videreudvikling af kompositioner

I denne øvelse skal du analysere og viderudvikle en række eksempler på pattern-baseret komposition. Øvelsen skal gøre dig fortrolig med de teknikker, der er omtalt tidligere i bogen, da vi her anvender de introducerede teknikker i en kompositorisk sammenhæng.

Når du undersøger, hvordan teknikkerne fungerer, kan disse tricks være en god hjælp til at forstå hvad der foregår:

- Brug method'en `.trace` til at vise outputtet fra forskellige patterns i post window, fx `Pwhite(0, 5).trace`.
- Brug SuperColliders dokumentation - sæt cursoren ved et pattern-navn og tast Ctrl-/Cmd-D. Scroll herefter ned til bunden af den pågældende dokumentationsside for at se eksempler på hvordan det pågældende pattern fungerer.
- Eksperimentér med at ændre på nogle af værdierne for at få en fornemmelse af, hvordan teknikkerne fungerer.

Lydeksemplerne her under er realiseret ved at bruge den angivne Pbind til at sende MIDI-meddelelser til en DAW og generere lyden med instrumentplugins. Det fremgår under hvert eksempel hvilket plugin, der er anvendt. De kodelinjer, som skal til for at realisere kompositionerne på denne måde, fremgår af [et tidligere afsnit om pattern-baseret MIDI-komposition](a-patterns-midi.md).

## Sammensætning af nøgler og patterns

- Undersøg følgende:
  - Hvordan fungerer de enkelte nøgler (`\octave`, `\root`, `\mtranspose` osv.)? Slå evt. op i [forrige kapitel](../02/a-pbind.md).
  - Hvordan kombineres tilfældighed og repetition under nøglerne `\mtranspose` og `\db`?
- Eksperimentér med følgende:
  - Alternative skalaer, nodeværdier, tonesekvenser og patterns

```sc title="Sammensætning af nøgler og patterns"
(
TempoClock.tempo = 120/60;

~trin = [0, 4, 3, 1, 2];
~nodevaerdier = [1/8, 1/8, 1/8, 1/16, 1/16];
Pbind(
    \octave, 5,
    \root, 2,
    \scale, Scale.lydian,
    \degree, Pseq(~trin, inf),
    \mtranspose, Pwhite(-3, 3).stutter(~trin.size + 2),

    \dur, Pseq(~nodevaerdier, inf) * 4,
    \legato, 1.2,
    \lag, Pgauss(0, 0.005),

    \db, Pseq([-10, Pgauss(-15, 2, 4)], inf),
).play;
)
```

## Skala-udforskning med Pbrown

Bemærk her forskellen på `Pbrown` og `Pwhite` (sidsnævnte blev anvendt ovenfor) samt anvendelsen af nøglen `\ctranspose`.

```sc title="Skala-udforskning med Pbrown"
(
TempoClock.tempo = 80 / 60;

Pbind(
    \degree, Pbrown(0, 21, 2),
    \octave, 4,
    \ctranspose, Pbrown(-5, 4, 1).stutter(32),
    \dur, 0.2
).play;
)
```

Afledte kompositioner kan eksperimentere med andre skalaer og patterns.

## Pentatone mønstre

Denne korte søger også en kombination af tilfældighed og struktur.

1. Skriv to variationer af kompositionen:
    1. Én version, som har en højere grad af tilfældighed
    1. Én version, som har en højere grad af struktur og gentagelse

```sc title="Pentatone mønstre"
(
TempoClock.tempo = 140 / 60;
Pbind(
    \scale, Scale.minorPentatonic,
    \octave, Pwhite(4, 5).stutter(4),
    \degree, Pshuf([0, 1, 2, 3, 4, 5], 4).repeat,
    \ctranspose, Pxrand([0, 1, 2]).repeat.stutter(32),

    \dur, 0.3,
    \legato, Pseq(Array.interpolation(160, 0.1, 3.5)),

    \db, Pbrown(-20, -17, 0.6)
).play;
)
```

## Rytmiserede og dynamiske akkorder

1. Besvar: Hvilken effekt har kombinationerne af `.stutter` og `.repeat` på outputtet fra de forskellige patterns?
1. Besvar: Hvad betyder `Array.interpolation(16, -20, -10)`?
1. Justér kildekoden på følgende vis:
    1. Tilføj mindst én akkord til `Pwrand` (husk, at sandsynlighederne `[0.9, 0.1]` skal svare til antallet af valgmuligheder og tilsammen skal give 1)
    1. Erstat `Pxrand` med et [listebaseret pattern](../02/a-random-patterns.md#listebaserede-generatorer) efter eget valg, og notér hvilken forskel dette gør

```sc title="Rytmiserede og dynamiske akkorder"
(
TempoClock.tempo = 120 / 60;

Pbind(
    \degree, Pwrand([
        [-14, 0, 2, 4, 6],
        [-12, -1, 1, 4, 5]
    ], [0.9, 0.1]).stutter(16).repeat,

    \mtranspose, Pxrand((-5..5)).repeat.stutter(16),

    \dur, 1/16 * 4,
    \legato, 0.7,

    \db, Pseq(Array.interpolation(16, -20, -10), inf),
).play;
)
```

## Korte, rytmiske sekvenser

I dette eksempel kan man argumentere for, at der arbejdes med en kombination af tilfældighed og genkendelighed. Undersøg hvilke teknikker, der i dette tilfælde skaber balance mellem det tilfældige og det genkendelige.

Skriv en ny komposition, som er inspireret af kildekoden her samt din besvarelse af opgaverne ovenfor.

```sc title="Korte, rytmiske sekvenser"
(
TempoClock.tempo = 85 / 60;
~melodi = Pbind(
    \scale, Scale.dorian,
    \degree, Pshuf((0..7), 4).repeat,

    \legato, 1.3,
    \dur, Pwrand([
        Pseq( [1/4, 1/4] ),
        Pseq( [1/16, 1/16, 1/8] ),
        Pseq( [1/16, 1/8, 1/16] ),
        Pseq( [Pn(1/24, 6), 1/4] ), // 16.-dels-trioler
        Pseq( [1/2, Rest(1/2)] ),   // Rest angiver pause
    ], [40, 40, 30, 5, 5].normalizeSum
    ).repeat * 4,
);
~komp = ~melodi.play;
)
// Flerstemmig variation med Ppar (parallelle Pbinds):
~komp = Ppar(~melodi ! 2).play;

~komp.stop;
```
