---
tags:
    - Øvelser
---

# Øvelse 6: Anvendelse af filtre

Denne øvelse går ud på at anvende og modulere gængse filter-UGens.

## Opgave 1: Valg og indstilling af filtre

Brug følgende filtre til at modificere klangen af hvid støj:

1. Et low pass-filter med cutoff-frekvens på 1000hz
1. Et high pass-filter med cutoff-frekvens på 800hz
1. Et band pass-filter med centerfrekvens på 500hz
1. Et resonerende low pass-filter med cutoff-frekvens på 800hz og rq-værdi på 0.1

```sc
(
{
	var source = WhiteNoise.ar;
	var sig =   ; // <-- udfyld her
	sig * 0.1;
}.play;
)
```

## Opgave 2: Modulation af filtre

Brug følgende kilder til at modulere cutoff-frekvensen for et low pass-filter, så cutoff-frekvensen bevæger sig mellem 500hz og 1000hz (brug fx `.range` eller `.exprange`):

1. Den allerede noterede envelope
1. En `XLine`-envelope, vælg selv tidsinterval
1. En LFO (vælg selv bølgeform og passende frekvens)

```sc
(
{
	var source = WhiteNoise.ar;
	var env = EnvGen.ar(Env.linen(0.5, 0.5, 2), doneAction: Done.freeSelf);
	var cutoff =     ; // <-- udfyld her
	var sig = LPF.ar(source, cutoff);
	sig * env * 0.1;
}.play;
)
```

## Opgave 3: Fleksibel, subtraktiv SynthDef

Skriv en SynthDef, som gør brug af subtraktiv syntese. SynthDef'en skal overholde følgende krav:

1. Lydkilden er en oscillator med en periodisk bølgeform og et righoldigt spektrum (fx en savtakket eller firkantet bølge)
1. Oscillatorens frekvens styres af et argument (`freq`) med default-værdi 440hz
1. Lydkildens lydstyrke styres af en envelope-generator - vælg selv en passende envelope med `doneAction: Done.freeSelf`
1. Lydkildens klang modificeres af et resonant low pass filter (`RLPF`)
1. Filterets cutoff-frekvens er automatisk 2 oktaver højere end oscillatorfrekvensen
1. Filterets rq-værdi er 0.5

### Ekstra forslag til de særligt nysgerrige

1. Justér koden, således at filterets cutoff-frekvens bevæger sig i takt med envelope-generatoren, fra 2 til 3 oktaver over oscillatorfrekvensen (og tilbage igen)
1. Justér koden, så du kan styre envelopens parametre (segment-tider) vha. SynthDef-argumenter
1. Justér koden, således at filterets rq-værdi gøres fleksibel vha. et SynthDef-argument

```sc
(
SynthDef(\subtraktor, { // udfyld herunder ⬇

	Out.ar(0, sig);
}).add;
)

Skriv en Pbind-komposition, hvor ovenstående variationsmuligheder demonstreres
(
Pbind(
	\instrument, \subtraktor, // udfyld herunder ⬇

).play;
)
```
