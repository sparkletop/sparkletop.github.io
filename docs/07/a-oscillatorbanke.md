---
tags:
    - Artikler
---

??? abstract "Introduktion til kapitlet"

    Dette kapitel ...

# Oscillatorbanke og multikanalslyd

En af de store styrker ved SuperColliders UGen-system er evnen til fleksibelt at arbejde med store banke af oscillatorer og lydkanaler. Men netop dette område kan samtidig være et lidt subtilt system at forstå og navigere, så det er værd at dvæle ved, blandt andet fordi det er et oplagt redskab til at arbejde med additiv syntese, detuning mm.

## Multikanalslyd med Multichannel Expansion

Vi har hidtil typisk arbejdet med monofone signaler, som så ved hjælp af UGen'en `Pan2` placeres i et stereofelt. Der findes `Pan4` og `PanAz`, som panorerer på tilsvarende vis med henholdsvis 4 eller et vilkårligt antal højttalere.

Men på et mere grundlæggende niveau understøtter de fleste UGens, at de på enkel vis kan "ekspanderes". Giver vi fx en `SinOsc` et array af frekvenser i stedet for blot en enkelt frekvens, kan vi høre, at der oprettes flere forskellige oscillatorer:

```sc title="Multichannel expansion"
{SinOsc.ar([100, 250, 719, 1682])}.play;
{SinOsc.ar([100, 250, 719, 1682]).sum * 0.1}.play;
{Splay.ar( SinOsc.ar([100, 250, 719, 1682]) )}.play;
```

På et stereosystem eller hovedtelefoner kan vi kun høre to kanaler ad gangen - i eksemplet ovenfor bliver det så på første linje 100Hz i venstre side, 250Hz i højre, og de højeste toner kan vi ikke høre. Men summerer vi signalet med `.sum`, er alle fire sinustoner hørbare, fordi de bliver lagt sammen og således kun udgør én kanal. Vi kan alternativt fordele et vilkårligt antal kanaler i et stereofelt med UGen'en `Splay`.

Ekspansionen videreføres til UGens, som ligger senere i signalkæden. I eksemplet herunder opretter vi først to tilfældighedsgeneratorer, den ene genererer 5 tilfældige værdier pr. sekund, den anden 10. Når `SinOsc` på næste linje modtager dette signal med to kanaler, ekspanderes der videre, så vi får to tilsvarende sinusbølge-oscillatorer.

```sc title="Stereosignal med arrays"
(
{
    var freqs LFNoise0.kr([5, 10]).exprange(200, 800);
    SinOsc.ar(freqs); // indeholder to sinusbølge-oscillatorer
}.play;
)
```

![type:audio](eksempel.ogg)

Brug af multikanalslyd kan være en særdeles effektiv teknik inden for lyddesign. Den mest "håndholdte" tilgang kan være at notere arrays direkte, som i eksemplerne ovenfor.

## Detuning

Oscillatorbanke er fx særdeles velegnede til at skabe "tykkere" klange gennem detuning. Her opretter vi med multichannel expansion fire forskellige oscillatorer, der klinger med næsten samme frekvens:

```sc title="Detuning med .midiratio"
(
{
    var freq = 220;
    var transposeFactors = [0, 0.10, -0.07, -0.08].midiratio;
    var sig = Saw.ar(freq * transposeFactors);
    sig = sig.sum;
    Pan2.ar(sig);
}.play;
)
```

## Algoritmisk oprettelse af oscillatorbanke

Computere er glimrende redskaber til at gentage de samme operationer mange gange, så længe vi beskriver præcist hvad der skal gøres. Vi kan beskrive hvad der skal gøres med [funktioner](../01/a-funktioner.md), som vi danner lister med ved hjælp af [iteration](../01/a-lister.md#iteration-over-lister). Genlæs evt. de relevante afsnit herom, før du læsere videre.

### Algoritmisk dannede oscillatorbanke

Her kan vi eksempelvis oprette en liste med grundtonen og frekvenserne for de 4 oktaver, som ligger over grundtonen:

```sc title="Grundtone og overtoner"
(
5.collect({
    arg num;
    var octave = (num * 12).midiratio;
    var freq = 110;
    freq * octave;
}).postln;
)
```

Vi kan omsætte dette til et klingende eksempel ved at lade tonerne fremstille sinusbølge-oscillatorer og blive fordelt jævnt i et stereofelt med `Splay`:

```sc title="Fordeling af overtoner i stereofeltet"
(
{
    var freq = 110;
    var sig = 5.collect({
        arg num;
        var octave = (num * 12).midiratio;
        SinOsc.ar(freq * octave);
    });
    Splay.ar(sig);
}.play;
)
```

![type:audio](eksempel.ogg)

Denne teknik ligger sammen med den beslægtede multichannel expansion-teknik til grund for [additiv syntese](a-additiv.md).
