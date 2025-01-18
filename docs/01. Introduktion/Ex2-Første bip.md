---
tags:
    - Øvelser
---
# Øvelse: Første bip

Nedenstående øvelse går ud på at producere lyde på SuperColliders lydserver og eksperimentere med at ændre på lyden ved at variere på parametrene.

Start først lydserveren med: `s.boot;`

## En uendelig sekvens

1. Overvej hvad de enkelte kodelinjer gør ved lyden.
1. Eksekvér kodeblokken og lyt til resultatet. Tryk Ctrl/Cmd-Punktum for at stoppe igen.
1. Prøv at ændre på tallene eller vælge en anden skala, og kør blokken igen for at lytte til resultatet.

``` sc title="Øvelse: Skalaudforskning"
(
Pbind(
	// prøv at vælge en anden skala, fx Scale.egyptian
	\scale, Scale.minor,

	// prøv at ændre på de forskellige tal herunder
	\degree, Pseq([0, 3, 2, 1, 4, 5, 6], inf),
	\root, 1,
	\octave, 4,
	\dur, 0.25,    // <-- denne værdi skal være større end 0
	\legato, 1.2,
).play;
)
```

Tip: Kør `Scale.directory;` for at få vist de forskellige indbyggede skalaer.

## Skøre oscillatorer

1. Overvej hvad de enkelte kodelinjer gør ved lyden.
1. Eksekvér kodeblokken og lyt til resultatet. Tryk Ctrl/Cmd-Punktum for at stoppe igen.
1. Prøv at ændre på tallene eller vælge andre oscillatorer, og kør blokken igen for at lytte til resultatet.

``` sc title="Øvelse: Oscillator-eksperiment"
(
{
	var sig, lfo, lfoFreq;

	// prøv at ændre på de forskellige tal herunder
	var freq = 330;

	var lfoFreqStart = 2;

	var lfoFreqEnd = 10;

	var duration = 7;

	lfoFreq = Line.kr(
		lfoFreqStart,
		lfoFreqEnd,
		duration,
		doneAction: Done.freeSelf
	);

	lfoFreq = lfoFreq.dup(2);

	lfo = LFNoise0.kr(lfoFreq);

	lfo = lfo.bipolar(24);

	lfo = lfo.round(4);

	// justér ikke herunder
	lfo = lfo.midiratio;
	sig = Pulse.ar(freq * lfo);
	sig = Splay.ar(sig);
	Limiter.ar(sig * 0.1);
}.play;
)
```
