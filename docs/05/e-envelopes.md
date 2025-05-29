---
tags:
    - Øvelser
---

# Øvelse: Envelopes

I denne øvelse arbejder du med at anvende og designe dine egne envelopes og LFO'er.

## Brug af indbyggede envelopes

1. Tag udgangspunkt i nedenstående kildekode, og brug følgende envelopes:
    1. Indbyggede envelopes med standardværdier for attack, release mm.
        1. `Env.perc`
        1. `Env.linen`
        1. `Env.sine`
        1. `Env.triangle`
    1. Indbyggede envelopes med specifikke indstillinger
        1. `Env.perc` med attack-tid på 200 milisekunder og release-tid på 3 sekunder
        1. `Env.linen` med sustain-**tid** på 2 sekunder
        1. `Env.sine` med varighed på 0.1 sekund
1. Modificér dernæst koden, således at vi også modulerer `Pulse`-oscillatorens frekvens med envelope-generatoren, skaleret med `.exprange` til intervallet 55-440.

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Øvelse med indbyggede envelopes" hl_lines="3"
(
{
    var env = EnvGen.kr(     , doneAction: Done.freeSelf);
    var freq = 440;
    Pulse.ar(freq) * env * 0.1;
}.play;
)
```

Husk, at `.plot` kan være en nyttig hjælp: `Env.perc(1, 3).plot`

## Simpel lilletrommelyd

Du skal her fremstille en simpel lilletrommelyd. De centrale lydlige egenskaber ved trommelyde varierer meget hurtigt over tid, hvilket du kan simulere ved hjælp af envelopes.

Skriv tre envelopes:

1. *body:* En `XLine`, som bevæger sig fra 220 til 110 over 275ms.
1. *sweep:* En `XLine`, som bevæger sig fra 8000 til 2500 over 10ms.
1. *vol:* En `Env.perc`, hvor attack-segmentet varer 0.5ms(!) og release-segmentet varer 150ms.

Prøv efterfølgende at justere på parametrene i de forskellige envelopes og bemærk hvordan selv mindre ændringer påvirker det lydlige resultat.

```sc title="Simpel lilletrommelyd" hl_lines="3-5"
(
{
    var body =     ;
    var sweep =     ;
    var vol =     ;

    // justér ikke herunder
    var resonance = VarSaw.ar(body);

    var seiding = WhiteNoise.ar;

    var sig = resonance + seiding;

    sig = LPF.ar(sig, sweep);

    sig = sig * EnvGen.ar(vol, doneAction: Done.freeSelf);
    Out.ar(0, sig.dup);
}.play;
)
```

Lilletrommen dannes på følgende måde [@pejrolo2017, p. 121-122]:

- Resonansen i trommens krop, dvs. dens "tone", simuleres med en trekantformet lydbølge. Vi kan således "stemme" trommen ved at justere start- og slutværdier for envelopen.
- Trommens seiding (metaltråde monteret på undersiden) simuleres med hvid støj.
- Med et dynamisk low pass filter simulerer vi trommens klanglige forandring over tid (mere højfrekvent støj i starten).

I næste kapitel gennemgås [et mere elaboreret bud på dannelse af lilletrommelyd](../06/a-lilletromme.md).

## En unik envelope til tonehøjde

Definér din egen envelope, som overholder følgende krav:

1. Envelopen skal bestå af mindst to segmenter.
1. Værdierne i envelopen (linje 3 i kodeblokken herunder) skal ligge mellem 220 og 880.
1. Tidsintervallerne (linje 4 i kodeblokken herunder) vælges frit (husk, at der skal være ét tidsinterval færre end antallet af trin).

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Unikke envelopes" hl_lines="3 4"
(
~frekvensEnvelope = Env(
    [   ],
    [   ],
    \exp
);
)
// Plot envelopen;
~frekvensEnvelope.plot;

// Test envelopen med lyd
(
{
    var freq = EnvGen.kr(~frekvensEnvelope);
    var vol = EnvGen.kr(
        Env.sine(~frekvensEnvelope.duration),
        doneAction: Done.freeSelf
    );
    SinOsc.ar(freq) * vol * 0.1;
}.play;
)
```

## Hjemmestrikket LFO

1. Modificér SynthDef'en, således at LFO'en modulerer mindst to forskellige, lydlige parametre (fx tonehøjde, panorering, lydstyrke, cutoff-frekvens etc.). Husk at [skalere outputtet fra LFO'en](../04/a-skalering.md), så det passer til modulationens formål.
1. Design din egen LFO ved hjælp af `Env.circle`. Du kan finde et eksempel herpå i [artiklen vedr. nye envelopes og LFO'er](a-nye-envelopes.md#envelope-som-lfo).
1. Skriv på egen hånd en komposition ved hjælp af `Pbind` eller `Pmono`, hvor du demonstrerer mulighederne i SynthDef'en.

```sc title="SynthDef med hjemmelavet LFO" hl_lines="7-8"
(
SynthDef(\lfo, {
    arg freq = 440, pan = 0, amp = 0.1, out = 0, gate = 1;

    var lfo = EnvGen.kr(
        Env.circle(
            [   ],
            [   ],
            \exp
        )
    );

    var env = EnvGen.kr(Env.asr, gate, doneAction: Done.freeSelf);
    var sig = Saw.ar(freq);

    // Lavpas-filter med cutoff-frekvens to oktaver over grundtonen
    sig = LPF.ar(sig, freq * 4);
    sig = Pan2.ar(sig, pan, amp) * env;
    Out.ar(out, sig);
}).add;
)
```
