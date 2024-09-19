---
tags:
    - Artikler
---

# Oscillatorbanke og multikanalslyd

En af de store styrker ved SuperColliders UGen-system er evnen til fleksibelt at arbejde med store banke af oscillatorer og lydkanaler. Men netop dette område kan samtidig være et lidt subtilt system at forstå og navigere, så det er værd at dvæle ved, blandt andet fordi det er et oplagt redskab til at arbejde med additiv syntese, detuning mm.

## Multikanalslyd med "Multichannel Expansion"

Vi har hidtil typisk arbejdet med monofone signaler, som så ved hjælp af UGen'en `Pan2` placeres i et stereofelt. Der findes `Pan4` og `PanAz`, som panorerer på tilsvarende vis med henholdsvis 4 eller et vilkårligt antal højttalere. 

Men på et mere grundlæggende niveau understøtter de fleste UGens, at de på enkel vis kan "ekspanderes". Giver vi fx en `SinOsc` et array af frekvenser i stedet for blot en enkelt frekvens, kan vi høre, at der oprettes flere forskellige oscillatorer: 

```sc
{SinOsc.ar([100, 250, 719, 1682])}.play;
{SinOsc.ar([100, 250, 719, 1682]).sum * 0.1}.play;
{Splay.ar( SinOsc.ar([100, 250, 719, 1682]) )}.play;
```

På et stereosystem eller hovedtelefoner kan vi kun høre to kanaler ad gangen - i eksemplet ovenfor bliver det så på første linje 100Hz i venstre side, 250Hz i højre, og de højeste toner kan vi ikke høre. Men summerer vi signalet med `.sum`, er alle fire sinustoner hørbare, fordi de bliver lagt sammen og således kun udgør én kanal. Vi kan alternativt fordele et vilkårligt antal kanaler i et stereofelt med UGen'en `Splay`.

Ekspansionen videreføres til UGens, som ligger senere i signalkæden. I eksemplet herunder opretter vi først to tilfældighedsgeneratorer, den ene genererer 5 tilfældige værdier pr. sekund, den anden 10. Når `SinOsc` på næste linje modtager dette signal med to kanaler, ekspanderes der videre, så vi får to tilsvarende sinusbølge-oscillatorer.

```sc
(
{
    var freqs LFNoise0.kr([5, 10]).exprange(200, 800);
    SinOsc.ar(freqs); // indeholder to sinusbølge-oscillatorer
}.play;
)
```

Brug af multikanalslyd kan være en særdeles effektiv teknik inden for lyddesign. Den mest "håndholdte" tilgang kan være at notere arrays direkte, som i eksemplerne ovenfor.

## Detuning

Oscillatorbanke er fx særdeles velegnede til at skabe "tykkere" klange gennem detuning. Her opretter vi fire forskellige oscillatorer, der klinger med næsten samme frekvens:

```sc
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

### Iteration med `.do` og `.collect`

Computere er glimrende redskaber til at gentage de samme operationer mange gange, så længe vi beskriver præcist hvad der skal gøres. Dette kaldes ofte *iteration*. Når vi beskriver i en såkaldt funktion (angivet med `{}`), hvad vi ønsker at generere, kan SuperCollider skabe ganske store oscillatorbanke samt mange andre samlinger og sekvenser. For at forstå iteration, kan vi se på method'en `.do`:

```sc
5.do({ "Hej!".postln; });

(
10.do({
    arg input;
    "Mit input var ".post; input.postln;
});
)
```

`X.do` udfører altså funktionen (dvs. den kodeblok, som er omkranset af { ... }) X antal gange. Funktionen modtager som første argument tallene fra 0 op til `X-1`.

Beslægtet med `.do` er `.collect`, som grundlæggende gør det samme, men samler resultaterne i en liste (et array). "Resultatet" af en funktion er blot det, der står på den sidste linje inde funktionen.

```sc
5.collect({ "Goddaw..."; });

(
10.collect({
    arg input;
    input * 100;
});
)
```


### Algoritmisk dannede oscillatorbanke

Her kan vi eksempelvis oprette et en liste med grundtonen og frekvenserne for de 4 oktaver, som ligger over grundtonen:

```sc
(
5.collect({
	arg num;
    var octave = (num * 12).midiratio;
    var freq = 110;
    freq * octave;
}).postln;
)
```

Med lyd - tonerne fremstilles af sinusbølge-oscillatorer og fordeles jævnt i et stereofelt med `Splay`:

```sc
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

Denne teknik ligger sammen med den beslægtede multichannel expansion-effekt til grund for [additiv syntese](Art2-Additive-bølger.md).
