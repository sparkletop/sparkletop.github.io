---
tags:
    - Øvelser
---

# Øvelse: Analyse og videreudvikling af kompositionseksempler

I denne øvelse skal du analysere udvalgte aspekter af fem eksempler på pattern-baseret komposition. Øvelsen skal gøre dig fortrolig med de teknikker, der er omtalt tidligere i bogen, da vi her anvender de introducerede teknikker i en kompositorisk sammenhæng. Du skal nemlig også videreudvikle kompositionerne med dit eget kreative bidrag.

**Redskaber til analyse:** Når du undersøger, hvordan teknikkerne fungerer, kan disse tricks være en god hjælp til at forstå hvad der foregår:

- Brug method'en `.trace` til at vise outputtet fra forskellige patterns i post window, fx `Pwhite(0, 5).trace`.
- Brug SuperColliders dokumentation - sæt cursoren ved et pattern-navn og tast Ctrl-/Cmd-D. Scroll herefter ned til bunden af den pågældende dokumentationsside for at se eksempler på hvordan det pågældende pattern fungerer.
- Eksperimentér med at ændre på nogle af værdierne for at få en fornemmelse af, hvordan teknikkerne fungerer.

**Lydeksempler:** Lydeksemplerne herunder er realiseret ved at sende MIDI-meddelelser til en DAW og generere lyden med instrumentplugins, som vist i [det foregående afsnit om pattern-baseret MIDI-komposition](a-patterns-midi.md). Det fremgår under hvert eksempel hvilket konkret plugin, der er anvendt.

## Sammensætning af nøgler og patterns

1. Analyse
    1. Hvordan fungerer de enkelte nøgler (`\octave`, `\root`, `\mtranspose`, `\lag` osv.)? Slå evt. op i [forrige kapitel](../02/a-pbind.md).
    1. Hvordan kombineres tilfældighed og repetition under nøglerne `\mtranspose` og `\db`? Se evt. [afsnittet om sekvenser af patterns](./a-indlejring.md#sekvenser-af-patterns).
1. Kreativ opgave
    1. Eksperimentér med alternative skalaer, nodeværdier og trinsekvenser

```sc title="Sammensætning af nøgler og patterns"
(
TempoClock.tempo = 120 / 60;

~trin = [0, 4, 3, 1, 2];
~nodevaerdier = [1/8, 1/8, 1/8, 1/16, 1/16];
Pbind(
    \octave, 5,
    \root, 2,
    \scale, Scale.lydian,
    \degree, Pseq(~trin, 16),
    \mtranspose, Pwhite(-3, 3).stutter(~trin.size + 2),

    \dur, Pseq(~nodevaerdier, inf) * 4,
    \legato, 1.2,
    \lag, Pgauss(0, 0.005),

    \db, Pseq([-10, Pgauss(-15, 2, 4)], inf),
).play;
)
```

![type:audio](../media/audio/03-komposition-keys.ogg)

Lydeksemplet er realiseret med instrument-plugin'et [Helm](https://tytel.org/helm/) og preset'et *Old Factory Presets > CM Pluck Time* med portamento slået til.

## Skala-udforskning med Pbrown

1. Analyse
    1. Hvilken funktion har nøglen `\ctranspose`?
    1. Hvad sker der, hvis du ændrer nøglen `\ctranspose` til `\mtranspose`?
    1. Hvad er forskellen på `Pbrown` og `Pwhite`?
1. Kreativ opgave
    1. Skab en mere interessant rytmik ved at erstatte den faste værdi 0.2 ved `\dur`-nøglen med et pattern efter eget valg

```sc title="Skala-udforskning med Pbrown"
(
TempoClock.tempo = 85 / 60;

Pbind(
    \degree, Pbrown(0, 21, 3),
    \octave, 4,
    \ctranspose, Pbrown(-5, 4, 1, 4).stutter(32),
    \db, Pbrown(-15, -5, 2).trace,
    \dur, 0.25,
).play;
)
```

![type:audio](../media/audio/03-komposition-pbrown.ogg)

Lydeksemplet er realiseret med instrument-plugin'et [sforzando](https://www.plogue.com/products/sforzando.html) og sfz-instrumentet *Marimba* fra [Versilian Studios Chamber Orchestra 2 Community Edition](https://versilian-studios.com/vsco-community/).

## Pentatone mønstre

1. Analyse
    1. Hvilke teknikker anvendes her til at opnå en balance mellem struktur/repetition og tilfældighed?
    1. Hvilket pattern styrer kompositionens storform, altså hvor mange toner vi samlet hører?
    1. Hvilken funktion har `Array.interpolation`? Se evt. [afsnittet om lister](../01/a-lister.md#automatiske-talrkker).
1. Kreativ opgave
    1. Skriv to variationer af kompositionen:
        1. Én version, som har en højere grad af tilfældighed
        1. Én version, som har en højere grad af struktur og gentagelse

```sc title="Pentatone mønstre"
(
TempoClock.tempo = 130 / 60;
Pbind(
    \scale, Scale.minorPentatonic,
    \octave, Pwhite(4, 5).stutter(4),
    \degree, Pshuf([0, 1, 2, 3, 4, 5], 4).repeat,
    \root, Pxrand([0, 2, 3]).repeat.stutter(24),

    \dur, 0.25,
    \legato, Pseq(Array.interpolation(24, 0.1, 3), 8),

    \db, Pbrown(-20, -12, 0.5)
).play;
)
```

![type:audio](../media/audio/03-komposition-pentaton.ogg)

Lydeksemplet er realiseret med instrument-plugin'et [Vital](https://vital.audio/) med en let justeret udgave af preset'et *Super Pluck*.

## Rytmiserede og dynamiske akkorder

1. Analyse
    1. Hvilken effekt har kombinationerne af `.stutter` og `.repeat` på outputtet fra de forskellige patterns?
    1. Hvad betyder `Array.interpolation(16, -20, -10)`?
1. Kreativ opgave
    1. Tilføj mindst én akkord til `Pwrand` (husk, at sandsynlighederne `[0.9, 0.1]` skal svare til antallet af valgmuligheder og tilsammen skal give 1).
    1. Erstat `Pxrand` med et andet [listebaseret tilfældighedspattern](../02/a-random-patterns.md#listebaserede-stokastiske-patterns) efter eget valg, og notér hvilken forskel dette gør.

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

![type:audio](../media/audio/03-komposition-akkorder.ogg)

Lydeksemplet er realiseret med instrument-plugin'et [sforzando](https://www.plogue.com/products/sforzando.html) og sfz-instrumentet *Uprigt Piano* fra [Versilian Studios Chamber Orchestra 2 Community Edition](https://versilian-studios.com/vsco-community/).

## Rytmiske motiver

1. Analyse
    1. Undersøg hvilke teknikker, der i dette tilfælde skaber balance mellem det tilfældige og det genkendelige.
    1. Undersøg hvad method'en `.normalizeSum` gør.
1. Kreativ opgave
    1. Skriv en ny komposition, som er inspireret af kildekoden herunder samt opgaverne ovenfor.

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
~komp = Ppar(~melodi ! 3).play;

~komp.stop;
```

![type:audio](../media/audio/03-komposition-pwrand.ogg)

Lydeksemplet er realiseret med instrument-plugin'et [Spitfire LABS](https://labs.spitfireaudio.com/) og [sample pack'en *Charango - Charango Ensemble*](https://labs.spitfireaudio.com/packs/charango).
