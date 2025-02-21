---
tags:
    - Artikler
---

# Pbind-nøgler

I SuperCollider kan man sammensætte længere forløb af musikalske "begivenheder" ved hjælp af `Pbind`. Det er ofte inden for Pbind, at vi specificerer musikalske parametre som tonehøjde, dynamik, rytmik og frasering. Det gør vi ved at sammensætte nøgler og værdier i formen `\nøgle, værdi`:

```sc title="Nøgler og værdier i Pbind"
(
~eksempel = Pbind(
    \degree, 4, // 5. skalatrin, et g (fordi udgangspunktet er C-dur)
    \dur, 0.5,  // varighed på et halvt taktslag (dvs. en ottendedel i almindelig musikterminologi)
    \db, -25,   // -25 decibel lydstyrke
).play;
)
~eksempel.stop;
```

Nøglen i Pbind'en ovenfor her er altså den tekstbid, der starter med \ - `\degree`, `\dur` eller `\db`, og de tilhørende værdier er henholdvis `4`, `0.5` og `-25`. Herunder gennemgås de mest almindelige standardnøgler, som det er værd at kende til [^1].

## Tonehøjde i Pbind

Til at notere tonehøjder bruger vi primært nøglerne

- `\degree` - skalatrin
- `\scale` - skala
- `\octave` - oktav
- `\root` - toneart

```sc title="Skalatrin, skala, oktav og grundtone"
( 
~eksempel = Pbind(
    \degree, [0, 2, 4, 6],   // en diatonisk firklang
    \scale, Scale.minor,     // mol-skala
    \octave, 5,              // oktav 5 er den oktav, som starter ved noglehuls-c
    \root, -3                // 3 halvtoner under nøglehuls-c (i dette tilfælde a)
).play;                         // tilsammen en A-mol7
)
~eksempel.stop;
```

For skalavalgmuligheder, kør `Scale.directory;`

Man kan også vælge at angive tonehøjde på andre abstraktionsniveauer - med MIDI-tal eller oscillatorfrekvens:

```sc title="Alternative nøgler til angivelse af tonehøjde"
~eksempel = Pbind(\midinote, 60).play;  // c
~eksempel = Pbind(\freq, 440).play;     // a, kammertonen
~eksempel.stop;
```

Kromatisk og modal transponering kan angives med:

- `\mtranspose` - modal transponering, dvs. parallelføring inden for skalaen
- `\ctranspose` - kromatisk transponering, dvs. halvtonetrin uafhængigt af skala

```sc title="Modal og kromatisk transponering"
(
~eksempel = Pbind(
    \degree, [0, 2, 4],
    \mtranspose, Pseq([0, 1, 2, 3]),
).play;
)
(
~eksempel = Pbind(
    \degree, [0, 2, 4],
    \ctranspose, Pseq([0, 1, 2, 3]),
).play;
)
~eksempel.stop;
```

## Varighed, frasering og timing

Til at notere rytmik bruger vi primært nøglerne `\dur` og `\legato`

- `\dur` - tidsinterval mellem på hinanden følgende anslag, målt i taktslag (ikke sekunder!)
- `\legato` - hvor længe en tone klinger, målt relativt i forhold til `\dur` (>1 giver legato, <1 giver staccato)

```sc title="Rytmik og frasering"
~eksempel = Pbind(\dur, 1).play;        // tidsinterval 1 taktslag, dvs. en 4.-del
~eksempel = Pbind(\dur, 0.25).play;     // tidsinterval 0.25 taktslag, dvs. en 16.-del
~eksempel = Pbind(\legato, 0.1).play;   // staccato
~eksempel = Pbind(\legato, 1.5).play;   // legato
~eksempel.stop;
```

For at justere timing relativt til beatet kan man bruge nøglen `\lag` (fx for at "humanisere" en ellers meget maskinel timing). For at forskyde timingen relativt til andre ellers samtidigt klingende toner kan vi bruge `\strum`-nøglen, som forskyder toneanslag i akkorder ligesom et guitar-strum.

```sc title="Rytmisk Forskydning"
~eksempel = Pbind(\lag, 1.5).play // giver kun mening relativt til fx et beat
(
~eksempel = Pbind(
    \degree, [0, 2, 4, 6],
    \strum, 0.05
).play;
)
~eksempel.stop;
```

### En note om rytmenotation

For at notere nodeværdier som vi kender dem fra almindelig musikteori, skal vi tage højde for, at SuperCollider tæller varigheder i *taktslag*. Når vi almindeligvis taler om et "taktslag" taler vi typisk om en fjerdedel (1/4) - og det vi mener er en fjerdedel af en takt. I SuperCollider tæller vi med `\dur`-nøglen ikke i takter, men i taktslag. Derfor skriver vi 1 og ikke 1/4, når vi ønsker en varighed på ét taktslag.

Hvad nu, hvis vi gerne vil bruge almindelige rytmeangivelser i SuperCollider? Jo, vi kan for det meste ganske enkelt gange med 4 for at omregne fra "varighed målt i andele af takt" til "varighed målt i taktslag". For at notere sekstendedele, ottendedele, fjerdele, halvnoder og helnoder kan vi således skrive:

```sc title="Traditionelle nodeværdier"
~eksempel = Pbind(\dur, 1/16 * 4).play;
~eksempel = Pbind(\dur, 1/8 * 4).play;
~eksempel = Pbind(\dur, 1/4 * 4).play;
~eksempel = Pbind(\dur, 1/2 * 4).play;
~eksempel = Pbind(\dur, 1/1 * 4).play;
~eksempel.stop;
```

## Lydstyrke

Til at notere volumen kan man vælge mellem nøglerne `\db` eller `\amp`. Med `\db` omregner SuperCollider automatisk fra decibel, hvor `0` er den maksimale værdi, `-20` svarer til, at lyden bliver opfattet halvt så kraftigt som ved maksimal lydstyrke, og så fremdeles. Med nøglen `\amp` angiver vi i stedet amplituden direkte, typisk som en værdi mellem 0 og 1.

```sc title="Lydstyrke"
~eksempel = Pbind(\db, -30).play
~eksempel = Pbind(\amp, 0.2).play
~eksempel.stop;
```

[^1]: Når man senere i kurset skriver sine egne SynthDefs, fungerer ovennævnte nøgler kun, når man anvender argumenterne `freq`, `amp` og `gate` korrekt i sin SynthDef. Se hertil afsnittet om [argumentnavne i SynthDef](../05/a-synthdef.md#argumentnavne-i-synthdef).
