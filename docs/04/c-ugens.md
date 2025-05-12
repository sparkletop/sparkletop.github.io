---
tags:
    - Cheat sheets
---
# Cheat sheet: Centrale UGens

Start med at lære UGens fra dette cheat sheet at kende. Brug SuperColliders dokumentation samt [oscilloskop og spektrogram](./a-ugens.md#ugens-og-signalflow) til at nærstudere de forskellige UGens.

Se eventuelt også [Eli Fieldsteels liste med "essential UGens"](https://uofi.app.box.com/s/1bfva2kan3ntmgey2345goc73snjzpwt) samt dokumentet [*Tour of UGens* fra SuperColliders dokumentation](https://doc.sccode.org/Guides/Tour_of_UGens.html), der begge har tjent som inspiration til nedenstående.

## Almindelige oscillatorer og støjgeneratorer

Fire almindelige bølgeformer: Sinusbølge, savtakket, firkantet og trekantet[^2].

[^2]: `SinOsc`, `Saw` og `Pulse` er (i modsætning til fx `LFTri`) "band limited". Det betyder, at de ikke skaber "aliasing" (en form for digital støj), når de anvendes ved høje frekvenser.

```sc title="Basale bølgeformer"
// Sinusbølger, savtakkede og firkantede bølger:
{SinOsc.ar(440) * 0.1}.play;
{Saw.ar(440) * 0.1}.play;
{Pulse.ar(440) * 0.1}.play;
{LFTri.ar(440) * 0.1}.play;
```

`Pulse` og den beslægtede UGen `VarSaw` kan begge indstilles med hensyn til duty cycle, dvs. symmetri/assymmetri i bølgeformen.

```sc title="Bølgeformer med variabel duty cycle"
{VarSaw.ar(440, 0.1) * 0.1}.play;
{VarSaw.ar(440, 0.5) * 0.1}.play;
{Pulse.ar(440, 0.1) * 0.1}.play;
{Pulse.ar(440, 0.5) * 0.1}.play;
```

Der findes også forskellige støjgeneratorer, hvoraf vi primært bruger disse to:

```sc title="Hvid og pink støj"
{WhiteNoise.ar * 0.01}.play;
{PinkNoise.ar * 0.1}.play;
```

## LFO-egnede UGens

Disse UGens (samt `SinOsc`) er velegnede som LFO'er. Men de kan sagtens benyttes over 20Hz.

```sc title="LFO-egnede UGens"
// Savtakket, trekantet/pyramideformet og firkantede bølgeformer. 
{LFSaw.kr(10)}.plot(0.2);
{LFTri.kr(10)}.plot(0.2);
{LFPulse.kr(10)}.plot(0.2);

// Lavfrekvent støj, velegnede som tilfældighedsgeneratorer.
{LFNoise0.kr(10)}.plot(1);
{LFNoise1.kr(10)}.plot(1);
{LFNoise2.kr(10)}.plot(1);
```

## Envelope-generatorer

```sc title="Envelope-generatorer"
// Line og XLine er nok de mest enkle envelopes, bestående af ét segment, lige eller eksponentiel linje.
{Line.kr(0, 1, 4, doneAction: 2) * PinkNoise.ar * 0.1}.play;
{XLine.kr(0.01, 1, 4, doneAction: 2) * PinkNoise.ar * 0.1}.play;

// EnvGen er den bredest anvendelige envelope-generator, bruges sammen med forskellige envelopes:
{EnvGen.kr(Env.perc, doneAction: 2) * PinkNoise.ar * 0.1}.play;
{EnvGen.kr(Env.sine, doneAction: 2) * PinkNoise.ar * 0.1}.play;
{EnvGen.kr(Env.triangle, doneAction: 2) * PinkNoise.ar * 0.1}.play;
```

## Filtre

```sc title="Filtre"
// Low-, high-, og band pass-filtre.
{LPF.ar(PinkNoise.ar, 440) * 0.1}.play;
{HPF.ar(PinkNoise.ar, 440) * 0.1}.play;
{BPF.ar(PinkNoise.ar, 440) * 0.1}.play;

// Low- og high pass-filtre med resonans.
{RLPF.ar(PinkNoise.ar, 440, 0.01) * 0.1}.play;
{RHPF.ar(PinkNoise.ar, 440, 0.01) * 0.1}.play;

// Shelf-filtre.
{BLowShelf.ar(PinkNoise.ar, 440, db: 20) * 0.05}.play;
{BHiShelf.ar(PinkNoise.ar, 440, db: 20) * 0.05}.play;

// Low pass-filter inspireret af filtrene i de klassiske Moog-synthesizere
{MoogFF.ar(PinkNoise.ar, 440) * 0.1}.play;
```

## Triggere og delays

Triggere genererer impulser. En impuls bruges typisk til at udløse noget, fx igangsætning af en envelope-generator, spring i afspilningsposition eller lignende.

```sc title="Triggere og delays"
// Impulse og Dust genererer impulser, regelmæssigt eller tilfældigt fordelt i tid.
{Impulse.ar(10) * 0.1}.play;
{Dust.ar(10) * 0.1}.play;

// DelayN, DelayL, DelayC er delaylinjer uden feedback, dvs. de forsinker blot lydsignalet.
{DelayL.ar(Impulse.ar(0), 1, 1) * 0.1}.play;

// CombN, CombL, CombC - såkaldt "comb filter", fungerer som delay med feedback.
{CombL.ar(Impulse.ar(0), decaytime: 10) * 0.1}.play;
```

## Buffer/Samples

```sc title="Buffere og samples"
// Kør først denne linje for at indlæse et sample i en buffer:
~sample = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");

// PlayBuf og BufRd - afspiller indholdet af en buffer:
{PlayBuf.ar(1, ~sample, doneAction: 2)}.play;
{BufRd.ar(1, ~sample, SinOsc.ar(0.1).range(0, BufFrames.kr(~sample)))}.play;
```

## Routing og stereofoni

```sc title="Routing og stereofoni"
// Pan2 - placerer et signal i et stereofelt.
{Pan2.ar(SinOsc.ar, 0.5) * 0.1}.play;

// Balance2 - justerer forholdet mellem to kanaler (venstre og højre).
{Balance2.ar(SinOsc.ar(440), SinOsc.ar(443)) * 0.1}.play;

// Splay - fordeler et vilkårligt antal kanaler ligeligt i et stereofelt
{Splay.ar(SinOsc.ar([220, 440, 660, 880])) * 0.1}.play;

// Out - sender signal ud af en Synth.
{Out.ar(1, SinOsc.ar * 0.1)}.play;
```
