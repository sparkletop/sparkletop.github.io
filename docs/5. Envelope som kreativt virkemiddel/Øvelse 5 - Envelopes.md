---
tags:
    - Øvelser
---

# Øvelse 5. Envelopes og SynthDefs

## Opgave 1: Brug af envelopes til modulation af amplitude

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

## Opgave 2: Hjemmelavede envelopes

Definér din egen envelope, som overholder følgende krav:

- Envelopen skal bestå af mindst to segmenter
- Trinene i envelopen skal ligge mellem 220 og 880
- Tidsintervallerne vælges frit (husk, at der skal være ét tidsinterval færre end antallet af trin)

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Opgave 2" hl_lines="3 4"
(
~frekvensEnvelope = Env(
	[   ],
	[   ],
	\exp
);

{
	var freq = EnvGen.kr(~frekvensEnvelope);
	var env = EnvGen.kr(
		Env.sine(~frekvensEnvelope.duration),
		doneAction: Done.freeSelf
	);
	SinOsc.ar(freq) * env * 0.1;
}.play;
)
```

## Opgave 3: SynthDef med vedvarende envelope

1. Justér nedenstående SynthDef, så den anvender en vedvarende envelope i stedet for en selv-afsluttende envelope. OBS: Dette kræver tilføjelse af gate-argument - se hvordan i [artiklen om envelopes](Envelopes.md).
2. Skriv en `Pmono`-baseret komposition, hvor du varierer `\degree`, `\lfoFreq` og `\lfoDepth` ved hjælp af patterns, fx [tilfældighedsgeneratorer](../2. Generativ komposition med patterns/2.2-tilfældighedsgeneratorer.md).

Justér kun på de markerede linjer i kodeblokken herunder.

```sc title="Opgave 3" hl_lines="3 6 21-23"
(
SynthDef(\opgave3, {
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
Pmono(\opgave3,
    \degree,    ,
    \lfoFreq,    ,
    \lfoDepth,    ,
    \dur, 0.4,
).play;
)
```


## Bonusopgave til de ekstra nysgerrige: Hjemmelavede LFO'er med Env.circle

1. Design din egen LFO ved hjælp af `Env.circle`. Se et eksempel i SuperColliders dokumentation eller [artiklen vedr. envelopes](Envelopes.md).
1. Brug LFO'en til at modulere mindst to forskellige parametre (fx tonehøjde, panorering, lydstyrke, cutoff-frekvens etc.).
1. Skriv en komposition baseret på `Pbind` eller `Pmono`, hvor du demonstrerer mulighederne i SynthDef'en.

```sc
(
SynthDef(\opgave4, {
    arg freq = 440, pan = 0, amp = 0.1, out = 0, gate = 1;

    var lfo = EnvGen.kr(
		Env.circle(
			[   ],  // <-- udfyld trin/værdier her
			[   ],  // <-- udfyld varigheder af tidsintervaller her
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
