---
tags:
    - Artikler
---

# Skalering af signaler

Ofte ønsker vi, at forskellige parametre ved UGens forandrer sig over tid. Som vist ovenfor kan vi gøre dette hjælp af [modulation](./a-ugens.md#modulation). Vi kan altid modulere outputtet fra UGens, og i mange tilfælde kan input/argumenter til UGens også moduleres på forskellig vis. I den forbindelse er det vigtigt at skalere signalerne korrekt og holde tungen lige i munden.

## Skalering med henblik på styring af amplitude

Vi kan behandle outputtet fra en UGen på forskellige måder, blandt andet med filtre, delay-effekter, distortion med mere. I første omgang fokuserer vi her på at styre amplituden for outputtet fra en oscillator-UGen. Når vi ønsker at justere outputtet fra en UGen på denne måde, kan vi ganske enkelt gange outputtet med modulatoren. Hvis vi eksempelvis ganger outputtet fra en `SinOsc` med 0.1, nedskalerer vi amplituden:

```sc title="Modulation af UGen-output"
{[
    SinOsc.ar(440),
    SinOsc.ar(440) * 0.1
]}.plot;
```

![En umodificeret sinusbølge og en sinusbølge med nedskaleret amplitude](../media/figures/to_amplituder.png){ width="60%" }

For et hørbart lydsignals amplitude er det væsentligt at bemærke, at vi bevæger os mellem -1 og 1. Udsving uden for dette interval vil skabe en uønsket, skrattende lyd. Når vi modulerer amplitude for hørbare UGens, skalerer vi derfor oftest amplituden **ned**. Det gør man ved at gange med en faktor mellem 0 og 1:

{==

**Tommelfingerregel:** Outputtet fra en LFO eller envelope, der *modulerer et hørbart signals amplitude*, bør som udgangspunkt bevæge sig i intervallet 0-1.

==}

### Skalering fra 0 til maksimum med .unipolar

Hvis vi ønsker at modulere amplituden for outputtet fra en oscillator-UGen, kan vi bruge en anden UGen til dette. Vi kalder denne anden UGen for en modulator, som modulerer amplituden. Hvis vi tager udgangspunkt i tommelfingerreglen ovenfor, skal outputtet fra denne modulator bevæge sig i intervallet mellem 0 og 1. Hertil har vi en handy UGen-method, der hedder `.unipolar(maksimum)`. Den skalerer nemlig outputtet fra en UGen, så det ligger i intervallet fra 0 til et givet maksimum (default-værdien er 1).

Som eksempel kan vi tage UGen'en `LFTri`, der giver en trekantet bølgeform og er velegnet som lavfrekvent oscillator.

- Uden skalering bevæger `LFTri.ar` sig mellem -1 og 1, ligesom `SinOsc` og de fleste andre oscillatorer.
- Med `LFTri.ar.unipolar` uden argumenter bevæger vi os i stedet mellem 0 og 1.
- Med `LFTri.ar.unipolar(0.5)` bevæger vi os mellem 0 og ½.

Bemærk hvor outputtet befinder sig på Y-aksen:

```sc title="En trekantet bølgeform udsat for .unipolar"
{[
    LFTri.ar,
    LFTri.ar.unipolar
    LFTri.ar.unipolar(0.5)
]}.plot;
```

![Brug af UGen-method'en .unipolar](../media/figures/unipolar.png){ width="80%" }

Hvis vi eksempelvis gerne vil modulere amplituden for et signal med pink støj med en trekantformet modulator, kan det gøres på følgende vis:

```sc title="Pulserende, pink støj"
{ PinkNoise.ar * LFTri.kr(0.5).unipolar }.play;
```

![type:audio](../media/audio/04-pulserende-pink-noise.ogg)

Udforsk ved hjælp af [SuperColliders dokumentation](https://doc.sccode.org/Classes/UGen.html#-bipolar) på egen hånd hvad den tilsvarende method `.bipolar` .

## Skalering med henblik på justering af tonehøjde

Ofte kan det være interessant at modulere inputs til en UGen, altså at argumenter vi anvender til method'en `.ar` består af signaler fra andre UGens og dermed forandrer sig over tid. Her bør man overveje hvilke input, der giver mening for den UGen, man modulerer. Som eksempel kigger vi her på tonehøjde.

Ved en UGen, der generer en tone, skal frekvens-argumentet typisk ligge inden for den menneskelige hørelse, dvs. et sted mellem 20Hz og 20kHz. Noget lignende gælder cutoff-frekvenser til filtre. Her skal det signal, der modulerer inputtet, bevæge sig i et interval, der ligger inden for dette spænd.

{==

**Tommelfingerregel:**: Et signal, der *modulerer en oscillators frekvens/tonehøjde*, bør typisk bevæge sig inden for intervallet 20 til 20000. Det samme gælder typisk for modulation af cutoff-frekvenser ved filter-UGens.

==}

### Skalering fra minimum til maksimum med .range og .exprange

Her kan vi med fordel bruge to UGen-methods, som hedder `.range` og `.exprange`. I begge tilfælde angiver man et minimum og et maksimum, og oscillatorens output skaleres så henholdsvis lineært og eksponentielt til at bevæge sig mellem disse to værdier. Bemærk her Y-aksen:

```sc title="Skalering af output med .range"
{ SinOsc.ar(3).range(100, 200) }.plot(1);
```

![Brug af UGen-method'en `.range`](../media/figures/range.png){ width="80%" }

Det er vigtigt, at vi bruger disse methods på frekvensmodulatoren (i modsætning til lydkildens amplitude). Hertil kan vi med fordel anvende [lokale variabler](../01/a-variabler.md#lokale-variabler) til at organisere kildekoden, så det er tydeligt, hvad der modulerer hvad:

```sc title="Skalering af output med .exprange"
{
    var freq = SinOsc.ar(3).exprange(100, 400);
    Pulse.ar(freq);
}.play;
```

![type:audio](../media/audio/04-skalering-exprange.ogg)

### Intervaltransponering med .midiratio

Sitationer hvor man ønsker at modulere en tonefrekvens, så den bevæger sig op og ned på en tonalt velklingende måde, kan være lidt tricky. Vi tænker nemlig normalt toner i intercaller som sekunder, tertser, kvarter, kvinter, oktaver osv. Skal vi flytte et a, der klinger ved 440Hz, en oktav op, skal vi gange med 2 - så får vi a'et ved 880Hz. Men hvad hvis vi skal flytte en terts op? En kvarttone ned? Eller et antal [cent](https://en.wikipedia.org/wiki/Cent_(music)) op eller ned?

Her kommer omregnings-method'en `.midiratio` os til undsætning. Her kan vi omregne et interval målt i halvtoner til den faktor, vi skal gange en frekvens med, for at modulere det antal halvtoner op eller ned:

```sc title="Intervaltransponering med .midiratio"
// Prim, ingen skalering
0.midiratio;     // --> 1

// Oktav op
12.midiratio;    // --> cirka 2

// Oktav ned
(-12).midiratio; // --> cirka 0.5

// Lille terts op
3.midiratio;     // --> 1.189207...

// Kvint op
7.midiratio;     // --> cirka 1.5

// Kvarttone op
0.5.midiratio;   // --> 1.02902...

// 15 cent op
0.15.midiratio;  // --> 1.008702...
```

Her er et eksempel, hvor vi anvender `.midiratio` sammen med `.unipolar` til at modulere en lille terts op:

```sc title=".midiratio kombineret med .unipolar"
{
    var freq = 440;
    var modulator = LFSaw.kr(1).unipolar(3).midiratio;
    Pulse.ar(freq * modulator);
}.play;
```

![type:audio](../media/audio/04-unipolar-midiratio.ogg)
