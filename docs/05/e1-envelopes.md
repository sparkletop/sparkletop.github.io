---
tags:
    - Øvelser
---

# Øvelse: Envelopes og SynthDefs

I denne øvelse arbejder du med envelopes. Som et element i nogle af opgaverne, indgår disse envelopes i SynthDefs.

## Brug af envelopes til modulation af amplitude

1. Tag udgangspunkt i nedenstående kildekode, og brug følgende envelopes til at modulere amplituden for en firkantet bølgeform:
    1. Indbyggede envelopes med standardværdier for attack, release mm.
        - `Env.perc`
        - `Env.linen`
        - `Env.sine`
        - `Env.triangle`
    1. Indbyggede envelopes med specifikke indstillinger
        - `Env.perc` med attack-tid på 200 milisekunder og release-tid på 3 sekunder
        - `Env.linen` med sustain-**tid** på 2 sekunder
        - `Env.sine` med varighed på 0.1 sekund
2. Modificér dernæst koden, således at vi også modulerer `Pulse`-oscillatorens frekvens med envelope-generatoren, skaleret med `.exprange` til intervallet 55-440.

Husk, at `.plot` kan være en nyttig hjælp: `Env.perc(1, 3).plot`

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Opgave 1" hl_lines="3 4"
(
{
	var env = EnvGen.kr(    , doneAction: Done.freeSelf);
    var freq = 440;
	Pulse.ar(freq) * env * 0.1;
}.play;
)
```

## Unikke envelopes

Definér din egen envelope, som overholder følgende krav:

1. Envelopen skal bestå af mindst to segmenter
1. Trinhøjderneene i envelopen skal ligge mellem 220 og 880
1. Tidsintervallerne vælges frit (husk, at der skal være ét tidsinterval færre end antallet af trin)

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Opgave 2" hl_lines="3 4"
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

## Simpel lilletrommelyd

Vi skal her fremstille en simpel lilletrommelyd. De centrale lydlige egenskaber ved trommelyde varierer meget hurtigt over tid, og det kan vi simulere ved hjælp af envelopes.

Skriv tre envelopes:

1. *body:* En `XLine`, som bevæger sig fra 220 til 110 over 275ms
1. *sweep:* En `XLine`, som bevæger sig fra 8000 til 2500 over 10ms
1. *vol:* En `Env.perc`, hvor attack-segmentet varer 0.5ms(!) og release-segmentet varer 150ms

Prøv efterfølgende at justere på parametrene i de forskellige envelopes og bemærk hvordan selv mindre ændringer påvirker det lydlige resultat.

```sc hl_lines="3-5" title="Opgave 3"
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

Forklaring:

- Resonansen i trommens krop, dvs. dens "tone", simuleres med en trekantformet lydbølge. Vi kan således "stemme" trommen ved at justere start- og slutværdier for envelopen.
- Trommens seiding (metaltråde monteret på undersiden) simuleres med hvid støj.
- Med et dynamisk low pass filter simulerer vi trommens klanglige forandring over tid (mere højfrekvent støj i starten).

Denne klangdannelsesopskrift stammer fra s. 121-122 i [*Creating Sounds from Scratch*](https://global.oup.com/academic/product/creating-sounds-from-scratch-9780199921898) af Andrea Pejrolo & Scott B. Metcalfe.

Se i øvrigt [et mere elaboreret bud på syntetisk dannelse af lilletrommelyd](../06/a3-lilletromme.md).

## SynthDef med vedvarende envelope

1. Justér nedenstående SynthDef, så den anvender en vedvarende envelope i stedet for en selv-afsluttende envelope.
    - OBS: Dette kræver tilføjelse af gate-argument - se hvordan i [artiklen om envelopes](a1-envelopes.md).
2. Skriv en `Pmono`-baseret komposition, hvor du varierer `\degree`, `\lfoFreq` og `\lfoDepth` ved hjælp af patterns, fx [tilfældighedsgeneratorer](../02/a2-random-patterns.md).

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Opgave 4" hl_lines="3 6 21-23"
(
SynthDef(\opgave4, {
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
)

(
Pmono(\opgave4,
    \degree,    ,
    \lfoFreq,    ,
    \lfoDepth,    ,
    \dur, 0.4,
).play;
)
```


## Hjemmelavede LFO'er med `Env.circle`

1. Modificér SynthDef'en, således at LFO'en modulerer mindst to forskellige, lydlige parametre (fx tonehøjde, panorering, lydstyrke, cutoff-frekvens etc.). Husk at [skalere outputtet fra LFO'en](../04/a2-skalering.md), så det passer til modulationens formål.
1. Design din egen LFO ved hjælp af `Env.circle`. Du kan finde et eksempel herpå i [artiklen vedr. nye envelopes og LFO'er](a3-nye-envelopes.md#envelope-som-lfo).
1. Skriv en komposition baseret på `Pbind` eller `Pmono`, hvor du demonstrerer mulighederne i SynthDef'en.

```sc title="Hjemmelavet LFO" hl_lines="7-8"
(
SynthDef(\opgave5, {
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
