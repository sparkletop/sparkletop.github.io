---
tags:
    - Artikler
---

# Simple blæser- og strygerlyde

Subtraktiv syntese anvendes ofte til at emulere lyden af akustiske instrumenter. Dermed naturligvis ikke sagt, at resultatet altid klinger præcis som det akustiske forbillede; syntetiske blæser-, stryger- og trommelyde har fået deres egen genkendelige rolle inden for både den elektroniske musik og populærmusikken. Tænk blot på trommelydene fra en Roland TR-808, der indgår i utallige hiphop-tracks.

Nedenstående klarinet- og strygerlyde er løseligt baseret på Pejrolo og Metcalfes gennemgang af subtraktive klangdannelsesteknikker[@pejrolo2017, pp. 119-120].

## Syntetisk klarinet

En simpel "klarinet"-lyd, hvor lydkilden udgøres af en kvadratisk bølgeform, der sendes gennem et lavpas-filter med resonans.

```sc title="SynthDef til syntetisk klarinet"
(
SynthDef(\clarinet, {
    arg freq = 440, gate = 1;

    // lydkilde: firkantet bølgeform med mulighed for glissando via .lag
    var oscillator = Pulse.ar(freq.lag(0.025));
    // resonant low pass-filter anvendes til klanglig justering
    var sig = RLPF.ar(oscillator, 1200, 0.5);

    // lydstyrke styres med en envelope
    sig = sig * EnvGen.kr(Env.asr, gate, doneAction: Done.freeSelf) * 0.1;
    Out.ar(0, sig.dup);
}).add;
)
```

Hvis vi skal "spille på" denne SynthDef og ønsker at fastholde idéen om en klarinetlyd, er det værd at bemærke - hvilket måske er indlysende - at klarinetten er et *monofont* instrument. Det betyder, at der ikke kan være tidsligt overlappende toner som ved et klaver eller en guitar. Vi kan derfor oplagt bruge `Pmono` eller `PmonoArtic` til fx at spille et par skalaløb:

```sc title="Et par hoppende skalaløb"
(
Pmono(\clarinet,
    \degree, Pseq([0, 1, 2, 3, 4, 5, 6, 7], 2),
    \octave, Pseq([4, 5], inf).stutter(2),
    \dur, 0.15,
).play;
)
```

## Firser-strings

Simpel 80'er-strings.

```sc title="SynthDef til firser-strings"
(
SynthDef(\stringz, {
    arg freq = 440, gate = 1;

    // lydkilde: to savtakkede bølgeformer, den ene med en smule detuning
    var oscillator = Saw.ar(freq) + Saw.ar(freq * 0.9971);

    // cutoff styres af oscillatorens frekvens samt af en envelope
    var cutoff = freq * EnvGen.kr(
        Env.adsr(0.2, 0.7),
        gate,
        levelBias: 1
    );
    var sig = RLPF.ar(oscillator, cutoff, 0.4);

    // lydstyrke styres med en separat ADSR-envelope
    sig = sig * EnvGen.kr(Env.adsr(0.2, 0.4), gate, doneAction: Done.freeSelf) * 0.1;
    Out.ar(0, sig.dup);
}).add;
)
```

For at få et indtryk af de fyldige lydmuligheder kan vi afspille et par akkorder med vores syntetiske strygerlyd:

```sc title="En akkordrække med firser-strings"
(
Pbind(
    \instrument, \stringz,
    \degree, [-7, 0, 2, 4, 6, 8],
    \mtranspose, Pseq([3, 1, 0]),
    \dur, 2,
).play;
)
```
