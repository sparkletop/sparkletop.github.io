---
tags:
    - Artikler
---

# Adskil tempo og tonehøjde

Én af de særligt nyttige egenskaber ved granular syntese er evnen til at adskille varighed og tonehøjde - eller mere teknisk - tids- og frekvensdomænet. Når vi normalvis skruer afspilningshastigheden for et sample op, bevæger tonehøjden sig også op. Men med granular kan vi imidlertid let skille disse dimensioner ad.

Dette skyldes, at vi kan læse de enkelte grains med én hastighed, mens vi bevæger os igennem et sample med en anden hastighed.

## En pointer til at styre tempo

Til at styre bevægelsen gennem en buffer kan vi genere et signal, som vi kalder en "pointer". Pointerens funktion minder om en pickup-nål, som læser information ved at bevæge sig rundt på en vinylplade. Pointeren angiver så hvor i bufferen, grains skal læse fra.

Som pointer er det oplagt at bruge UGen'en `Phasor`, der generer en lineær bevægelse fra én værdi til en anden. Når vi så justerer den hastighed hvormed Phasor bevæger sig, justerer vi dermed tempoet i sample-afspilningen.

```sc title="Fleksibelt tempo med Phasor som pointer"
(
{
    arg moveRate = 1;

    // ~sample er en Buffer, der indeholder et indlæst mono-sample
    var buf = ~sample;
    var numFrames = BufFrames.kr(buf);
    
    // Pointeren implementeres med Phasor
    var pointer = Phasor.ar(
        rate: BufRateScale.kr(buf) * moveRate,
        start: 0,
        end: numFrames
    ) / numFrames;

    GrainBuf.ar(
        numChannels: 2,
        trigger: Dust.kr(100),
        dur: 0.100,
        sndbuf: buf,
        rate: BufRateScale.kr(buf),
        pos: pointer,
        pan: 0
    ) * 0.1;
}.play;
)

// Afspilningshastighed påvirker ikke tonehøjde
~granulator.set(\moveRate, 0.5)   // halvering af tempo
~granulator.set(\moveRate, 3)     // tredobling af tempo
```

## Fleksibel tonehøjde

Modificerer vi ovenstående med et argument til transponering, kan vi ændre afspilningshastigheden for de enkelte grains og dermed tonehøjden:

```sc title="Fleksibel tonehøjde"
(
~granulator = {
    arg moveRate = 1, transpose = 0;

    var buf = ~sample;
    var numFrames = BufFrames.kr(buf);
    
    // Pointeren implementeres med Phasor
    var pointer = Phasor.ar(
        rate: BufRateScale.kr(buf) * moveRate,
        start: 0,
        end: numFrames
    ) / numFrames;

    GrainBuf.ar(
        numChannels: 2,
        trigger: Dust.kr(100),
        dur: 0.1,
        sndbuf: buf,
        rate: BufRateScale.kr(buf) * transpose.midiratio,
        pos: pointer,
        pan: 0
    ) * 0.1;
}.play;
)

// Transponering påvirker ikke tempo
~granulator.set(\transpose, 7)    // en kvint op
~granulator.set(\transpose, -12)  // en oktav ned

// Tonehøjde og varighed/tempo kan justeres som adskilte parametre!
~granulator.set(\moveRate, 0.25, \transpose, 12)  // kvart tempo, en oktav op
```



### Tekstur og klangflade (flyttes til Art3)

Hvor ovenstående giver en meget fleksibel måde at strække eller transponere lyd på, kan vi skabe mere abstrakte teksturer ved at tilføje lidt støj til pointeren og fordele grains tilfældigt over hele stereofeltet. Dette kan blandt andet gøres ved hjælp af UGen'en `TRand`, som producerer tilfældige tal mellem et minimum og maksimum, hver gang den modtager en trigger. Denne tilfældige fordeling af grain-parametre kan vi kalde for jitter:

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
