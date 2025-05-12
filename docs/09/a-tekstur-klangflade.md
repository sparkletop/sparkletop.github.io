---
tags:
    - Artikler
---

# Rytmik og tekstur

Granular syntese udgør en meget fleksibel måde at strække eller transponere lyd på, men denne teknik er også attraktiv på grund af dens evne til at skabe rytmiserede klangflader og abstrakte teksturer. Disse to kompositionsmuligheder udforsker vi herunder.

I det følgende bruger vi følgende sample, som er indlæst i en buffer under variablen `~sample`.

![type:audio](guit_em9.ogg)
/// caption
    attrs: {id: sample}
Sample til eksemplerne herunder. Kilde: Freesound user...
///

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
        rate: EnvGen.kr(trin.circle, timeScale: 1).midiratio,
        pos: SinOsc.ar(0.2).range(0, 0.3) + Line.kr(0, 0.3, 30, doneAction: 2),
        pan: SinOsc.kr(10).bipolar(0.5)
    ) * 0.1;
}.play;
)
```

![type:audio](eksempel.ogg)

## Aleatorisk tekstur

kan vi skabe mere abstrakte teksturer ved at tilføje lidt støj til pointeren og fordele grains tilfældigt over hele stereofeltet.
Med tilfældighedsgeneratorer som `TRand` eller `TIRand` kan vi generere tilfældige værdier for hvert enkelt grain. Derved opnår vi en form for lydlig tekstur, der er helt unik for granular klangdannelse. Dette kan blandt andet gøres ved hjælp af UGen'en `TRand`, som producerer tilfældige tal mellem et minimum og maksimum, hver gang den modtager en trigger. Denne tilfældige fordeling af grain-parametre kan vi kalde for jitter:

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

![type:audio](eksempel.ogg)

En anden tilgang...

```sc title="Tekstur og klangflade med TRand" hl_lines="4 16 18 26 27"
(
~sprinkler = {
    arg transpose = 0, moveRate = 1,
    jitter = 0.01, spread = 0.1;

    var buf = ~sample;
    var numFrames = BufFrames.kr(buf);
    var pointer = Phasor.ar(
        rate: rateScale * moveRate,
        start: 0,
        end: numFrames
    ) / numFrames;

    var trigger = Dust.kr(200);

    var jit = TRand.kr(jitter.neg, jitter, trigger) / BufDur.kr(buf);

    var pan = TRand.kr(spread.neg, spread, trigger);

    GrainBuf.ar(
        numChannels: 2,
        trigger: trigger,
        dur: 0.1,
        sndbuf: buf,
        rate: BufRateScale.kr(buf) * transpose.midiratio,
        pos: pointer + jit,
        pan: pan
    ) * 0.1;
}.play;
)

// Fordeling af grains i stereofelt (høres bedst i hovedtelefoner)
~sprinkler.set(\spread, 0)
~sprinkler.set(\spread, 1)

// Spring i grainposition
~sprinkler.set(\jitter, 0.1)
~sprinkler.set(\jitter, 1.5)

// Stillestående pointer, med spredning i grainposition
~sprinkler.set(\jitter, 1, \moveRate, 0)
```

![type:audio](eksempel.ogg)
