# Øvelse 2B: Forståelse og brug af Pattern-eksempler

Denne øvelse går ud på at læse, undersøge, forstå og variere nogle simple eksempler på patternbaseret komposition.

Når du løser opgaverne, kan du med fordel bruge disse tricks til at forstå hvad der foregår:

- Brug .trace til at tjekke outputtet fra forskellige patterns, fx `Pwhite(0, 5).trace`.
- Brug SuperColliders dokumentation - sæt cursoren ved et pattern-navn og tast Ctrl/Cmd-D. Scroll herefter ned til bunden af dokumentationsfilen for at se eksempler på hvordan det pågældende pattern fungerer.
- Eksperimentér med at ændre på nogle af værdierne for at få en fornemmelse af, hvordan teknikkerne fungerer.

## Eksempel 1: Nøgler

- Notér for hver linje i Pbind'en: Hvilken funktion har de enkelte nøgler (`\octave`, `\root` osv.)?
- Hvilken effekt opnår man ved at kombinere `Pwhite` og `.stutter`?

```sc title="Eksempel 1"
(
TempoClock.tempo = 120/60;

~trin = [0, 4, 3, 1, 2];
~nodevaerdier = [1/8, 1/8, 1/8, 1/16, 1/16];
Pbind(
	\octave, 5,
	\root, 2,
	\scale, Scale.lydian,
	\degree, Pseq(~trin, inf),
	\mtranspose, Pwhite(-3, 3).stutter(10),

	\dur, Pseq(~nodevaerdier, inf) * 4,
	\legato, 1.2,
	\lag, Pgauss(0, 0.005),

	\db, Pseq([-10, Pgauss(-15, 2, 4)], inf),
).play;
)
```

## Eksempel 2: Skala-udforskning med Pbrown

Besvar følgende spørgsmål:

- Hvad er forskellen på `Pbrown` og `Pwhite`?
- Hvilken funktion har nøglen `\ctranspose`?

```sc title="Eksempel 2"
(
TempoClock.tempo = 80 / 60;

Pbind(
	\degree, Pbrown(0, 21, 2),
	\octave, 4,
	\ctranspose, Pbrown(-5, 4, 1).stutter(32),
	\dur, 0.2
).play;
)
```

## Eksempel 3: Pentatone mønstre

Beskriv forholdet mellem tilfældighed og kompositorisk struktur i denne korte komposition.

```sc title="Eksempel 3"
(
TempoClock.tempo = 140 / 60;
Pbind(
	\scale, Scale.minorPentatonic,
	\octave, Pwhite(4, 5).stutter(4),
	\degree, Pshuf([0, 1, 2, 3, 4, 5], 4).repeat,
	\ctranspose, Pxrand([0, 1, 2]).repeat.stutter(32),

	\dur, 0.3,
	\legato, Pseq(Array.interpolation(160, 0.1, 3.5)),

	\db, Pbrown(-20, -17, 0.6)
).play;
)
```

## Eksempel 4: Korte, rytmiske sekvenser

I dette eksempel kan man argumentere for, at der arbejdes med en kombination af tilfældighed og genkendelighed. Hvilke teknikker resulterer i skabelsen af balance mellem det tilfældige og det genkendelige? 

```sc title="Eksempel 4"
(
TempoClock.tempo = 85 / 60;

~melodi = Pbind(
	\scale, Scale.dorian,
	\degree, Pshuf((0..7), 4).repeat,

	\legato, 1.3,
	\dur, Pwrand([
		Pseq( [1/4, 1/4] ),
		Pseq( [1/16, 1/16, 1/8] ),
		Pseq( [1/16, 1/8, 1/16] ),
		Pseq( [Pn(1/24, 6), 1/4] ), // 16.-dels-trioler
		Pseq( [1/2, Rest(1/2)] ),   // Rest angiver pause
	], [40, 40, 30, 5, 5].normalizeSum
	).repeat * 4,
);
~komp = ~melodi.play;
)
~komp.stop;

// Flerstemmig version med Ppar (parallelle Pbinds):
~komp = Ppar(~melodi ! 2).play;
~komp.stop;
```

## Eksempel 5: Rytmiserede og dynamiserede akkorder

Besvar følgende spørgsmål:
- Hvilken effekt har kombinationerne af .stutter og .repeat på outputtet fra de forskellige patterns?
- Hvad betyder `Array.interpolation(16, -20, -10)`?

```sc title="Eksempel 5"
(
TempoClock.tempo = 120 / 60;

Pbind(
	\degree, Pwrand([
		[-14, 0, 2, 4, 6],
		[-12, -1, 1, 4, 5]
	], [0.9, 0.1]).stutter(16).repeat,

	\mtranspose, Pxrand((-5..5)).repeat.stutter(16),

	\dur, 1/16 * 4,
	\legato, 0.7,

	\db, Pseq(Array.interpolation(16, -20, -10), inf),
).play;
)
```
