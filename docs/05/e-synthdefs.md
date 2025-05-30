---
tags:
    - Øvelser
---

# Øvelse: SynthDefs

SynthDef-skrivning er måske et lidt tørt, teknisk emne. Men med lidt øvelse er det nøglen til at åbne de mange fantastiske variationsmuligheder, som interfacet mellem `SynthDef` og `Pbind` [lægger op til](a-synthdef.md#interfacet-mellem-synth-synthdef-og-pbind). Du må i denne øvelse gerne skele til [cheat sheet'et om SynthDefs](c-synthdef.md) og [andre relevante afsnit](./a-synthdef.md#argumentnavne-i-synthdef), men du skal i denne øvelse skrive SynthDef-kildekoden selv. Det får du nemlig mest ud af.

## Min første SynthDef

1. Skriv en SynthDef, som overholder følgende krav:
    1. SynthDef'ens navn skal være `\hello`.
    1. Som lydkilde skal SynthDef'en indeholde [en oscillator](../04/a-ugens.md#oscillator-ugens) efter eget valg.
    1. Oscillatorens frekvens kan styres med et SynthDef-argument kaldet `freq`, defaultværdi `440`.
    1. Oscillatorens lydstyrke over tid styres af en envelope kaldet `Env.linen`.
1. Test, at `freq`-argumentet i din SynthDef fungerer.
    1. Brug en kommando som `Synth(\hello, [\freq, 1000]);`, hvor du ændrer på frekvensen.
1. Justér SynthDef'en, så der kan ændres på lydstyrken.
    1. Indfør et nyt SynthDef-argument kaldet `amp` med defaultværdi `0.1`.
    1. Sørg for, at amplituden for lydsignalet bliver ganget med `amp`, før det sendes ud med `Out`.
1. Test din SynthDef med nedenstående Pbind.

```sc title="Test af \hello-SynthDef"
Pbind(
    \instrument, \hello,
    \degree, Pwhite(0, 7),
    \octave, Pwhite(3, 6),
    \dur, 0.25,
).play;
```

## En SynthDef med firkantede bølgeformer

1. Skriv en SynthDef, som overholder følgende krav:
    1. SynthDef'ens navn skal være `\firkant`.
    1. Lydkilden er en `Pulse`-UGen hvis frekvens kan styres med et SynthDef-argument kaldet `freq`, defaultværdi `220`.
    1. Lydstyrken kan styres med et SynthDef-argument kaldet `amp`, defaultværdi `0.1`.
    1. Lydstyrken moduleres af en perkussiv envelope (`Env.perc`), hvor attack og release kan styres med SynthDef-argumenter `attack` og `release`.
    1. Bredden af firkanten i `Pulse`-oscillatoren (2. argument til `Pulse.ar`) kan styres med et SynthDef-argument kaldet `width`.
1. Test din SynthDef med nedenstående Pbind. Den bør give et resultat, der minder om lydeksemplet herunder.

```sc title="Test af \firkant-SynthDef"
TempoClock.tempo = 130 / 60;
Pbind(
    \instrument, \firkant,
    \degree, [0, 2, 4, 6],
    \scale, Scale.minor,
    \octave, 4,
    \mtranspose, Pwhite(-2, 2).stutter(Phprand(2, 20).asStream),
    \db, Pseries(-25, Pwhite(3, 4).asStream, 4).repeat,
    \attack, 0.001,
    \release, Pgeom(0.1, 1.03, 100),
    \dur, Pwrand([1/8, 1/4, Rest(1/8)], [0.8, 0.15, 0.05], inf) * 4,
    \strum, Pexprand(0.0001, 0.01),
    \width, Pseries(0.2, 0.005, 100)
).play;
```

![type:audio](../media/audio/05-komposition-firkant.ogg)

## SynthDef med vedvarende envelope

1. Justér nedenstående SynthDef, så den anvender en vedvarende envelope i stedet for en selv-afsluttende envelope. OBS: Dette kræver, at du [tilføjer et gate-argument](a-envelopes.md#vedvarende-envelopes-med-gate) til `EnvGen`.
1. Skriv en `Pmono`-baseret komposition, hvor du varierer `\degree`, `\lfoFreq` og `\lfoDepth` ved hjælp af patterns, fx [tilfældighedsgeneratorer](../02/a-random-patterns.md). Der findes en kodeblok herunder, som du kan tage udgangspunkt i.

Justér kun på de markerede linjer i kodeblokkene herunder.

```sc title="SynthDef med glissando" hl_lines="2 5"
SynthDef(\gliss, {
    arg freq = 440, pan = 0, amp = 0.1, out = 0,
    lfoFreq = 1, lfoDepth = 0.025;

    var env = EnvGen.kr(Env.perc, doneAction: Done.freeSelf);

    var sig = Pulse.ar(
        freq.lag(0.01) *
        LFTri.kr(lfoFreq).bipolar(lfoDepth).midiratio
    );
    
    sig = Pan2.ar(sig, pan, amp) * env;

    Out.ar(out, sig);
}).add;
```

Afsæt for komposition med `Pmono`:

```sc title="Glidende komposition med Pmono" hl_lines="2-4"
Pmono(\gliss,
    \degree,    ,
    \lfoFreq,    ,
    \lfoDepth,    ,
    \dur, 0.4,
).play;
```
