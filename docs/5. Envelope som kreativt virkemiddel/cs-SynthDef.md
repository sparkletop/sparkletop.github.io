---
tags:
    - Cheat sheets
---


# Cheat sheet: SynthDef-skabeloner

SynthDefs kan indrettes på ganske mange forskellige måder, men hvis man skal fremstille lydkilder med tonalt indhold og en mono- eller stereofon lydkilde kan skabeloner herunder være et udmærket udgangspunkt.

Læs evt. nærmere om de [standard-argumentnavne](), der anvendes i skabelonerne.

Husk at ændre `\navn` til et deskriptivt navn for din SynthDef.

```sc title="Skabelon til monofone lydkilder"
(
SynthDef(\navn, {
	arg freq = 440, pan = 0,
	amp = 0.1, out = 0;
	var sig = SinOsc.ar(freq);



	// sig er et monofont signal
	Out.ar(out, Pan2.ar(sig, pan, amp));
}).add;
)
```

```sc title="Skabelon til stereofone lydkilder"
(
SynthDef(\navn, {
	arg freq = 440, pan = 0,
	amp = 0.1, out = 0;
	var sig = SinOsc.ar(freq).dup;



	// sig er et stereofont signal
	Out.ar(out, Balance2.ar(sig[0], sig[1] pan, amp));
}).add;
)
```
