---
tags:
    - Øvelser
---
# Øvelse: Generativ komposition

Denne øvelse handler om at bruge patterns til generativ komposition.

## Aleatorik ud over det hele

Skriv en komposition med `Pbind`, hvor alle parametre genereres tilfældigt, dvs. de faste værdier skal erstattes med patterns. Se evt. [artiklen om patterns og tilfældighed](a-random-patterns.md).

```sc title="Aleatorik ud over det hele"
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

## Sekvens og generativitet

1. Erstat teksten `Lunken kaffe` herunder med et udtryk efter eget valg og kør derefter den første kodeblok. Du har nu den `~sekvens`, som skal være grundlag for din komposition.
1. Skriv ved hjælp af `Pbind` og listebaserede patterns som `Pseq`, `Pshuf`, `Prand`, `Pxrand`, `Pwrand` og `Pser` en generativ komposition, der lever op til følgende krav:
    1. Kompositoriske parametre (tonehøjde, rytmik/frasering, lydstyrke, panorering osv.) skal så vidt muligt baseres på listen, som er gemt under variablen `~sekvens`.
    1. Forsøg at tilstræbe en balance mellem gentagelse og variation. Hertil kan det være en god idé at bruge pattern-methods som `.stutter`, `.repeat` og `.clump`.

```sc title="Sekvens og generativitet"
(
~sekvens = "Lunken kaffe".ascii % 10;
~sekvens.postln;
)

(
Pbind(




).play;
)
```
