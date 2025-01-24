---
tags:
    - Øvelser
---
# Øvelse 2B: Generativ komposition

Denne øvelse handler om at bruge patterns til generativ komposition.

## Opgave 1: Aleatorik ud over det hele

Skriv en komposition med `Pbind`, hvor alle parametre genereres tilfældigt, dvs. de faste værdier skal erstattes med patterns. Se evt. [artiklen om patterns og tilfældighed](a2-random-patterns.md).

```sc title="Opgave 1"
(
Pbind(
    // Tonehøjde
    \degree, 0,
    \octave, 4,
    \mtranspose, 0,
    
    \dur, 1,
    \legato, 1,

    \db, -20,
).play;
)
```

## Opgave 2: Sekvens og generativitet

1. Erstat teksten `Lunken kaffe` herunder med et udtryk efter eget valg og kør derefter den første kodeblok. Du har nu den `~sekvens`, som skal være grundlag for din komposition.
1. Skriv ved hjælp af `Pbind` og listebaserede patterns som `Pseq`, `Pshuf`, `Prand`, `Pxrand`, `Pwrand` og `Pser` en generativ komposition, der lever op til følgende krav:
    - Kompositoriske parametre (tonehøjde, rytmik/frasering, lydstyrke, panorering osv.) skal så vidt muligt baseres på listen, som er gemt under variablen `~sekvens`.
    - Forsøg at tilstræbe en balance mellem gentagelse og variation. Hertil kan det være en god idé at bruge pattern-methods som `.stutter`, `.repeat` og `.clump`.

```sc title="Opgave 2"
(
~sekvens = "Lunken kaffe".ascii % 10;
~sekvens.postln;
)

(
Pbind(




).play;
)
```
