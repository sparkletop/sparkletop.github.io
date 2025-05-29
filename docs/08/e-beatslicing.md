---
tags:
    - Øvelser
---

# Øvelse: Beatslicing

I denne øvelse producerer du beats ved hjælp af algoritmisk beatslicing.

## Klargøring

1. Indlæs først et eller flere trommeloops under variablen `~sample`til brug i nedenstående øvelse. Det er (for denne øvelse) vigtigt, at trommeloopet er metrisk underdelt i sekstendedele og varer præcis én takt.
1. Indlæs SynthDef'en `\slice` fra [afsnittet om beatslicing](a-beatslicing.md#en-synthdef).

## Algoritmiske beats

Skab et nyt beat ud af et eksisterende beat ved hjælp af SynthDef og loop fra Opgave 0 ovenfor. Beatet skal overholde følgende krav:

1. Slices skal vælge tilfældigt.
1. Klang skal varieres ved hjælp af `\drive` og de to filterparametre (`\cutoff` og `\rq`).
1. Mikrotimingen skal "humaniseres" ved hjælp af `\lag`-nøglen - vælg hertil selv et passende pattern og værdier.
1. Vælg selv yderligere parametre til justering.

```sc title="Beatslicing med patterns"
(
TempoClock.tempo = 115 / 60;
Pdef(\beat,
    Pbind(
        \instrument, \slice,
        \buf, ~sample,

        \numSlices, 16,
        \slice, Pseries(0, 1, 16).repeat,
        \dur, 1/16 * 4,
        \lag, 0,

        \pan, 0,
        \direction, 1,

        \release, 0.01,

        \drive, 0,
        \cutoff, 16000,
        \rq, 1,
        \amp, 0.5,
    )
).play;
)
```

## Synkretisme med to breakbeats

Tag afsæt i samme ressourcer som ovenfor plus mindst ét ekstra sample og fremstil et nyt beat. Opgaven her går ud på at få to breakbeats til at fungere sammen klangligt, rytmisk og evt. tonalt.

1. Ved nøglen `\buf` skiftes der vha. patterns mellem de indlæste samples.
1. Justér gerne på anvendte nøgler og på den SynthDef, som ligger til grund for kompositionen.
1. Fremstil mindst tre forskellige varianter af beatet, eksporter dem fra SuperCollider og indlæs i en DAW som trommebeat for en komposition.
