# Øvelse 1B: Første bip

Nedenstående øvelse går ud på at producere lyde på SuperColliders lydserver og eksperimentere med at ændre på lyden ved at variere på parametrene.

Start først lydserveren:

``` sc
s.boot;
```

## Lav noget lyd!

Herunder fremgår to kodeblokke - Eksempel 1 og 2. Leg med eksemplerne på følgende måde:

1. Eksekvér kodeblokken og lyt til resultatet.

2. Prøv løbende at ændre på kompositionen og eksekvér kodeblokken igen. Dette kaldes live coding!

3. Overvej hvad de enkelte kodelinjer gør ved lyden.

### Generativ komposition

Tip: Kør `Scale.directory;` for at få vist de forskellige indbyggede skalaer:

``` sc title="Eksempel 1: Pattern-baseret komposition"
(
Pdef(\eksempel1,
	Pbind(
		// prøv at vælge en anden skala, fx Scale.egyptian
		\scale, Scale.minor,

		// prøv at ændre på de forskellige tal herunder
		\degree, Pseq([0, 1, 2, 3, 4], inf),
		\root, 1,
		\octave, 4,
		\dur, Pwhite(0.25, 1.0).round(0.5),
		\legato, 1.2,
	)
).play;
)
Pdef(\eksempel1).stop;
```

### Oscillatorer

``` sc title="Eksempel 2: Komposition med oscillatorer"
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
