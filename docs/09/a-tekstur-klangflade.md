---
tags:
    - Eksempler
---

# Granular lyddesign

Mulighederne i granular syntese er mange, men hvordan udnytter man et potentielt meget komplekst redskab?

I det følgende bruger vi følgende sample, som er indlæst i en buffer under variablen ~sample.

<!-- ![type:audio](file.ogg) -->

## Granular grooves

Ved hjælp af LFO'er kan vi skabe rytme og gentagelse, så resultatet bliver et abstrkt groove.

``` sc title="Modulation af GrainBuf-parametre med LFO"
(
var trin = Env.new([0, 4, 7, 2], [1, 1, 1, 2], curve: \step);
{
    var overlap = LFTri.kr(1).exprange(0.2, 25);
    var grainDur = 0.100;
    var trigFreq = overlap / grainDur;
    GrainBuf.ar(
        numChannels: 2,
        trigger: Impulse.ar(trigFreq),
        dur: grainDur,
        sndbuf: ~sample,
        /* rate: (
            LFPulse.kr(1).range(0, 7) +
            LFNoise0.kr(0.25).bipolar(2).round
        ).midiratio,*/
        rate: EnvGen.kr(trin.circle, timeScale: 1).midiratio,
        pos: SinOsc.ar(0.2).range(0, 0.3) + Line.kr(0, 0.3, 30, doneAction: 2),
        pan: SinOsc.kr(10).bipolar(0.5)
    ) * 0.1;
}.play;
)
```

## Aleatorisk tesktur

Med tilfældighedsgeneratorer som `TRand` eller `TIRand`.

``` sc title="Tilfældige værdier for hvert grain"
(
{
    var overlap = 5;
    var grainDur = 0.100;
    var trigFreq = (overlap / grainDur);
    var trigger = Dust.ar(trigFreq);

    GrainBuf.ar(
        numChannels: 2,
        trigger: trigger,
        dur: grainDur,
        sndbuf: ~sample,
        // variér evt. grænseværdierne herunder
        rate: TIRand.ar(-12, 12, trigger).poll.midiratio,
        pos: TRand.ar(0, 1, trigger),
        pan: TRand.ar(-1, 1, trigger)
    )
}.play
)
```
