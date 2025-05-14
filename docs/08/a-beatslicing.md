---
tags:
    - Artikler
---

# Beatslicing med patterns

Beatslicing er en teknik, som kan udvide det kreative potentiale i loop-biblioteker. Teknikken indebærer at skære et beat eller en lydsekvens op i mindre dele, som derefter kan arrangeres på nye måder.

Ved for eksempel at skære et trommebeat op i et antal slices, kan vi omarrangere disse slices for at skabe et nyt beat. Dette kan give loops et unikt udtryk og hjælpe med at skille din musik ud fra mængden.

Beatslicing kan implementeres på forskellige måder, blandt andet ved hjælp af såkaldt "onset detection", som vi kigger nærmere på i næste modul. Denne artikel fremstiller en SynthDef, som afspiller et enkelt slice baseret på argumenter. Dernæst bruger vi patterns til at afspille disse slices på forskellig vis.

## Kildemateriale og slice-varighed

Med beatslicing er det afgørende, hvordan kildematerialet er organiseret. I denne artikel bruger vi som eksempel et sample, der indeholder et trommebeat af præcis én takts varighed. Beatet er metrisk velorganiseret og underdelt i sekstendedele. Det giver således mening at dele beatet op i 16 lige lange slices.

Vi kan beregne en startposition i bufferen ud fra hvilket nummer det ønskede slice har (her fra 0 til 15). Vi kan også fremstille en envelope med en fikseret varighed, der udregnes således at den sidste halvdel af envelopens release-segment ganske kort overlapper med begyndelsen af det efterfølgende slice.

Her kan vi således afspille det første slice i en buffer på følgende vis (justér evt. hvilket af de 16 slices der skal afspilles med variablen `slice`):

```sc title="Afspilning af et enkelt slice med PlayBuf"
~sample = Buffer.read(s, "C:/lydfiler/loop.wav");

(
{
    var buf = ~sample, slice = 0, numSlices = 16,
    attack = 0.002, release 0.010;

    // Beregner startpositionen for det aktuelle slice
    var startPos = (slice % numSlices) / numSlices;

    // Beregner varigheden af et slice og derefter envelopens sustain-tid
    var duration = BufDur.kr(buf) / numSlices;
    var sustainTime = duration - attack - (release * 0.5);
    
    var env = EnvGen.kr(
        Env.linen(attack, sustainTime, release),
        doneAction: Done.freeSelf
    );

    PlayBuf.ar(
        numChannels: 2,
        bufnum: buf,
        rate: BufRateScale.kr(buf),
        startPos: BufFrames.kr(buf) * startPos
    ) * env;
}.play;
)
```

### En SynthDef

Ovenstående kan omskrives til en SynthDef, hvor de første variabler laves om til argumenter, så vi kan styre dem med patterns. Hvis vi tilføjer transponering og afspilningsretning, klanglig manipulation med drive og low pass-filter samt panorering, amplitude og output-routing (alt sammen med tilhørende argumenter), får vi nedenstående resultat.

```sc title="SynthDef til beatslicing"
(
SynthDef(\slice, {
    arg buf, slice = 0, numSlices = 16,
    attack = 0.002, release = 0.010,
    transpose = 0, direction = 1,
    drive = 0, cutoff = 20000, rq = 1,
    amp = 0.1, out = 0, pan = 0;

    // Udregn startposition ud fra det specificerede slice og samlede antal slices
    var startPos = (slice % numSlices) / numSlices;

    // Udregn varighed baseret på varighed af hele samplet og antallet af slices
    var duration = BufDur.kr(buf) / numSlices;
    var sustainTime = duration - attack - (release * 0.5);

    // Simpel envelope med tre segmenter - attack, sustain og release
    var env = EnvGen.kr(
        Env.linen(attack, sustainTime, release),
        doneAction: Done.freeSelf
    );

    // Afspil slice med transponering og retning (1 = forlæns, -1 = baglæns)
    var sig = PlayBuf.ar(
        numChannels: 2,
        bufnum: buf,
        rate: BufRateScale.kr(buf) * transpose.midiratio * direction.sign,
        startPos: BufFrames.kr(buf) * startPos
    );

    // Distortion/waveshaping
    sig = (sig * drive.linexp(0, 1, 1, 100)).tanh;
    sig = sig * drive.lincurve(0, 1, 1, 0.1, -2);

    // Filter
    sig = RLPF.ar(sig, cutoff.clip(20, 20000), rq.clip(0.0001, 1));

    // Kompressor
    sig = Compander.ar(sig, sig, 0.1, 1.0, 0.25, 0.01, 0.01) * 10.dbamp;

    sig = sig * env;

    sig = Balance2.ar(sig[0], sig[1], pan, amp);

    Out.ar(out, sig);
}).add;
)

// Tilfældige slices
Synth(\slice, [\buf, ~sample, \slice, rrand(0, 15)]);
```

## Algoritmisk sammensætning af slices

Med ovenstående SynthDef kan vi fleksibelt sammensætte slices ved hjælp af patterns.

En enkelt overvejelse vi skal have med angår forholdet mellem to tempi: Originalsamplets tempo versus tempoet i vores nye beat. Mere specifikt kan der opstå huller i strømmen af slices, hvis vores nye tempo er langsommere end tempoet i det oprindelige, da ét slice nødvendigvis vil vare kortere end den tid, det er tænkt til at udfylde.

``` sc title="Pattern-baseret beatslicing"
(
TempoClock.tempo = 130 / 60;
Pdef(\test,
    Pbind(
        \instrument, \slice,
        \buf, ~sample,
        
        // Slice-valg og -info
        \dur, 1/16 * 4,
        \numSlices, 16,
        \slice, Pseq([
            0,
            Pwhite(1, 3, 4)
        ], inf),

        // Transponering og retning
        \transpose, Prand([-12, -7, 0], inf) + 2,
        \direction, Pwrand([1, -1], [0.9, 0.1], inf),
        
        // Klanglig manipulation
        \drive, 0.1,
        \cutoff, Pexprand(1000, 12000),
        \rq, 0.8,

        // Panorering og volumen
        \amp, 1,
        \pan, Pgauss(0, 0.2),
    )
).play;
)
```
