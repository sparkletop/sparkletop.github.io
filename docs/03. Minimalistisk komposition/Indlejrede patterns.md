---
tags:
    - Artikler
---

# Indlejrede patterns

Det er relativt let at lave en simpel, algoritmisk komposition ved hjælp af patterns. Men det kan være mere vanskeligt at bevæge sig videre fra det meget simple eller meget tilfældighedsprægede udtryk. Her kan en teknik, som kaldes indlejring af patterns, være med til at give et mere nuanceret og subtilt udtryk.

## Indlejring af patterns

Generativ eller algoritmisk komposition indebærer, at man i et vist omfang overlader dele af det kompositoriske arbejde til et system eller en algoritme. Her spiller [tilfældighedsgeneratorer](../02. Generativ komposition med patterns/2.2-tilfældighedsgeneratorer.md) ofte (men ikke altid) en central rolle.

Total tilfældighed er imidlertid sjældent specielt interessant. Derfor kan man med fordel indlejre tilfældighed som et begrænset element i en ellers fastlagt struktur.

### En sekvens af patterns

Vi har tidligere set, [hvordan `Pseq` kan generere sekvenser af værdier](../02. Generativ komposition med patterns/2.1-Patterns.md). Men `Pseq` er fleksibel og kan lige så vel bruges til sekvenser af patterns. Her eksempelvis en sekvens med en blanding af faste og tilfældigt genererede skalatrin:

```sc
(
Pbind(
    \degree, Pseq([
        0,
        Pwhite(0, 7, 2),
        Pshuf([-1, -3]),
        -3
    ], 2),
).play;
)
```

### Variererende argumenter

Man kan skabe interessante variationer ved at erstatte de faste værdier, vi ofte angiver som argumenter til patterns, med noget, som varierer. Som eksempel kan vi tage `Pseries`, der normalt giver lineære sekvenser ud fra tre argumenter - en startværdi, en trinstørrelse, og et antal:

```sc
Pseries(0, 1, 4)      // -> 0, 1, 2, 3
Pseries(6, -2, 5)     // -> 6, 4, 2, 0, -2
Pseries(5, 0.5, inf)  // -> 5, 5.5, 6, 6.5, 7, 7.5 ...
```

Hvis vi ønsker at varierere trinstørrelsen 1 i `Pseries(0, 1, 10)`, kan vi gøre det ved at indlejre en funktion eller et pattern (konverteret til en stream). Det vil føre for vidt at forklare nuancerne her, men se gerne [Eli Fieldsteels udmærkede forklaring](https://www.youtube.com/watch?v=17uMs9HpMgE). Hvis trinstørrelsen skal være et tilfældigt tal mellem -1 og 1, kan vi således gøre det på disse to måder:

```sc
Pseries(0, {rrand(-1, 1)}, 10)
Pseries(0, Pwhite(-1, 1).asStream, 10)
```

Her er et musikalsk eksempel, hvor vi bruger `Plprand` til at variere antallet af toner i fraser.

```sc
(
Pbind(
    \degree, Pwhite(0, 4),
    \dur, Pseq([
        Prand([1/8, 1/4], Plprand(2, 8).asStream),
        Rest(1)
    ], inf),
).play;
)
```

## Automatisk sammenflettede sekvenser

Der findes et særligt pattern, som er velegnet til at flette sekvenser sammen - `Place`. Her sætter man to eller flere sekvenser eller enkeltværdier sammen i et array, og `Place` veksler så mellem de forskellige kilder. Arrayet gennemløbes det antal gange, man angiver (herunder 4 gennemløb).

```sc
(
Pbind(
	\degree, Place([
		[4, 3, 5, 4],
		[2, 1],
		-3,
		0
	], 4).trace
).play;
)
```

Der findes også en variant, som i stedet tillader, at man erstatter sekvenserne med patterns, nemlig `Ppatlace`. Det er meget oplagt som ramme for indlejrede patterns og filtreret tilfældighed:

```sc
(
Pbind(
	\degree, Ppatlace([
		Pshuf([2, 3, 4, -1], inf),
		Pwhite(4, 7).stutter(4),
	], inf).trace,
	\dur, 0.25
).play;
)
```
