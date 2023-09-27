---
tags:
    - Cheat sheets
---
# Cheat sheet: Vigtige UGen-methods

Inden du prøver eksemplerne herunder, er det en god idé at køre disse to linjer, så du kan se en visualisering af SuperColliders lydlige output. Flyt evt. vinduerne, så du kan se både bølgeform og frekvensspektrum.

```sc
s.scope;
s.freqscope;
```

## 4 vigtige UGen-methods

Disse vigtige methods tillader os at justere output fra UGens på forskellige måder.

```sc
// .ar - generer lydsignal (audio rate), anvendes typisk til lydkilder, filtre og routing-UGens
{SinOsc.ar * 0.1}.play;

// .kr - generer kontrolsignal (control rate), anvendes typisk til LFO'er og envelopes.
{SinOsc.kr(1)}.plot(1);

// .range og .exprange - justerer outputtet fra en UGen, så det ligger mellem et nyt min og max
{SinOsc.ar.range(50, 1000)}.plot;     // bemærk Y-aksen
{SinOsc.ar.exprange(50, 1000)}.plot;  // bemærk Y-aksen og bølgeform

// .unipolar og .bipolar - genveje til at skrive .range(0, x) og .range(-x, x)
{SinOsc.ar.unipolar(100)}.plot;  // bemærk Y-aksen, signalet går fra 0 til 100
{SinOsc.ar.bipolar(100)}.plot;   // bemærk Y-aksen, signalet går fra -100 til 100

// .dup - kopierer et signal, så det bliver til et multikanals-signal
{SinOsc.ar(440).dup * 0.1}.play;
{SinOsc.ar(440).dup(10) * 0.1}.play;
```

