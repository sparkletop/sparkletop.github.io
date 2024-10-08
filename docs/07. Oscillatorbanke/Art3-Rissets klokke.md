---
tags:
    - Eksempler
---

# Rissets klokke

Jean-Claude Risset var en fransk komponist, der bl.a. arbejdede med additiv syntese og derved skabte en særlig klokkelyd. Nedenstående SynthDef er en SuperCollider-implementering, som er baseret på [Miller Puckettes gennemgang af Rissets klokke](http://msp.ucsd.edu/techniques/v0.11/book-html/node71.html#fig04.17). Der gøres flittig brug af [multichannel expansion](Art1-Oscillatorbanke.md#multikanalslyd-med-multichannel-expansion).

```sc
(
SynthDef(\risset,{
	arg freq = 440, atk = 0.01, rel = 3, pan = 0, amp = 0.1, out = 0;
	var ampRatios = [1, 0.67, 1, 1.8, 2.67, 1.67, 1.46, 1.33, 1.33, 1, 1.33];
	var durRatios = [1, 0.9, 0.65, 0.55, 0.325, 0.35, 0.25, 0.2, 0.15, 0.1, 0.075];
	var freqRatios = [0.56, 0.56, 0.92, 1.19, 1.7, 2, 2.74, 3, 3.76, 4.07];
	var detune = [0, 1, 0, 1.7, 0, 0, 0, 0, 0, 0, 0];

	var sig = SinOsc.ar((freq * freqRatios) + detune);

	sig = sig * ampRatios * 0.05;

	sig = sig * EnvGen.kr(
		Env.perc(atk, rel),
		timeScale: durRatios
	);

	sig = sig.sum;

    DetectSilence.ar(sig, doneAction: Done.freeSelf);    

	sig = Pan2.ar(sig, pan, amp);

	Out.ar(out, sig);
}).add;
)

(
Pbind(
	\instrument, \risset,
	\scale, Scale.minorPentatonic,
	\degree, Pwhite(0, 10),
	\rel, Pexprand(4, 12),
	\dur, Pexprand(0.2, 3),
	\pan, Pgauss(0, 0.3),
).play;
)
```
