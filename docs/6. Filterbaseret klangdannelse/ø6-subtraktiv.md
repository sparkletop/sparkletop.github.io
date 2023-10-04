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

Du kan finde hjælp og eksempler i [filter-cheat sheetet](cs-filtre.md).

```sc hl_lines="4"
(
{
	var source = WhiteNoise.ar;
	var sig =   ;
	sig * 0.1;
}.play;
)
```

## Opgave 2: Modulation af filtre

Brug følgende kilder til at modulere cutoff-frekvensen for et low pass-filter, så cutoff-frekvensen bevæger sig mellem 500Hz og 1000Hz (se evt. [artiklen om modulation af UGens](../4. Oscillatorer og modulation/A2-skalering.md) for relevante teknikker).

1. Den allerede noterede envelope
1. En `XLine`-envelope, vælg selv tidsinterval
1. En LFO (vælg selv bølgeform og passende frekvens)

```sc hl_lines="5"
(
{
	var source = PinkNoise.ar;
	var env = EnvGen.ar(Env.linen(0.5, 0.5, 2), doneAction: Done.freeSelf);
	var cutoff =     ;
	var sig = LPF.ar(source, cutoff);
	sig * env;
}.play;
)
```

## Opgave 3: Subtraktiv SynthDef

Omskriv kildekoden fra Opgave 2 til en SynthDef, som gør brug af subtraktiv syntese. Du kan evt. gøre brug af en [SynthDef-skabelon](../5. Envelope som kreativt virkemiddel/cs-SynthDef.md) som ramme for dit arbejde.

SynthDef'en skal overholde følgende krav:

1. Lydkilden ændres fra pink støj til en oscillator med en periodisk bølgeform og et righoldigt spektrum (fx en savtakket eller firkantet bølge)
1. Oscillatorens frekvens styres af et argument kaldet `freq` med default-værdi 440Hz
1. Filteret ændres til typen `RLPF`
1. Filterets cutoff-frekvens bevæger sig mellem 2 og 4 oktaver over oscillatorfrekvensen
i takt med envelope-generatoren
1. Filterets rq-værdi styres af et SynthDef-argument med default-værdi 0.5
1. Følgende envelope-parametre kan styres ved hjælp af SynthDef-argumenter:
    - `attackTime`, default-værdi 0.1
    - `curve`, default-værdi 0

Skriv en Pbind-komposition, som demonstrerer SynthDef'ens forskellige klangmuligheder, dvs. hvor nøglerne i kodeblokken herunder varieres ved hjælp af pattterns (husk at erstatte SynthDef-navnet med det navn, du selv har valgt):


```sc hl_lines="4 7 10 11 14"
(
Pbind(
    // Valg af SynthDef
    \instrument, \navnetPåMinFantastiskeSynthDef,
    
    // Tonehøjde
    \degree,     ,

    // Envelope
    \attackTime,        ,
    \curve,        ,
    
    // Filter
    \rq,    ,

).play;
)
```
