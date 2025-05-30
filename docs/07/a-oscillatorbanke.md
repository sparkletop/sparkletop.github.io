---
tags:
    - Artikler
---

??? abstract "Introduktion til kapitlet"

    Dette kapitel introducerer til multikanalslyd i SuperCollider. Vi kigger også på additiv klangdannelse, der netop baseres på banke af lydsignaler. Den grundlæggende idé i additiv klangdannelse er, at vi kan sammensætte et overtonespektrum, præcist som vi ønsker det. Her kigger vi blandt andet på algoritmer til at danne standardbølgeformer, simulering af elektrisk orgel og dannelse af klokkelyde.

# Oscillatorbanke og multikanalslyd

En af de store styrker ved SuperColliders UGen-system er evnen til fleksibelt at arbejde med store banke af oscillatorer og lydkanaler. Men netop dette område kan samtidig være et lidt subtilt system at forstå og navigere, da det notationsmæssigt kan være vanskeligt at få øje på. Det er værd at dykke ned i, fordi det er et oplagt redskab til at arbejde med additiv klangdannelse, detuning, chorus-effekter, multikanalslyd og lignende.

## Duplikering

Den mest simple måde at skabe et lydsignal med flere kanaler er ved at duplikere en UGen. Det kan vi gøre med method'en `.dup`, der også gælder for duplikering af andre objekter. Som argument til `.dup` kan vi angive, hvor mange kopier, vi ønsker - defaultværdien er 2.

```sc title="Duplikering med .dup"
10.dup; // -> [10, 10]
10.dup(5); // -> [10, 10, 10, 10, 10]
SinOsc.ar.dup; // -> [ a SinOsc, a SinOsc ]
SinOsc.ar.dup(7); // -> [ a SinOsc, a SinOsc, a SinOsc, a SinOsc, a SinOsc, a SinOsc, a SinOsc ]
```

Der findes en syntaktisk genvej, som kan være nyttig at kende, nemlig operatoren `!`, der blot gør det samme som `.dup` med argument:

```sc title="Operatoren !"
\kaffe ! 3; // -> [ kaffe, kaffe, kaffe ]
Pulse.ar ! 4; // -> [ a Pulse, a Pulse, a Pulse, a Pulse ]
```

Når vi kører ovenstående kodelinjer, kan vi i post window se, at SuperCollider skaber *lister*, som indeholder kopier af det duplikerede objekt. Hertl kan man eventuelt genlæse [afsnittet om lister](../01/a-lister.md). Men når vi bruger `.dup` på oscillatorer i en UGen-funktion, kan man sige, at *listen udgør et lydsignal med mere end én kanal*. Duplikering er altså én simpel teknik til at skabe multikanalslyd. Her kan man dog sige, at der egentlig ikke er tale om stereofoni, hvis signalet i de to kanaler er helt identisk - så er det nærmere en slags fordoblet monofoni.

```sc title="Dobbelt monofoni"
{ SinOsc.ar.dup * 0.1; }.play;
```

![type:audio](../media/audio/07-dobbelt-monofoni.ogg)

## Panorering og stereofoni

Vi har hidtil typisk arbejdet med monofone signaler. Ved hjælp af UGen'en `Pan2` kan vi placere et monofont signal i et stereofelt. UGen'en har tre argumenter: `Pan2.ar(sig, pan, amp)`, hvor `sig` indeholder det monofone signal, som placeres i et stereofelt ud fra argumentet `pan` (hvor -1 er helt til venstre og 1 helt til højre) med lydstyrken `amp`. `Pan2` indgår ofte som det sidste trin i en UGen-funktion, fordi den både inkorporerer panorering og justering af lydstyrke.

```sc title="Panorering med Pan2"
// Pink støj i midten af stereofeltet
{ Pan2.ar(PinkNoise.ar, 0, 0.1) }.play;

// Pink støj helt til venstre af stereofeltet
{ Pan2.ar(PinkNoise.ar, -1, 0.1) }.play;

// Pink støj i midten af stereofeltet
{ Pan2.ar(PinkNoise.ar, 1, 0.1) }.play;
```

![type:audio](../media/audio/07-pan2-positioner.ogg)

Panoreringensargumentet kan selvfølgelig moduleres af en anden UGen. Her er det væsentligt at sikre sig, at modulatoren er [korrekt skaleret](../04/a-skalering.md), da panoreringsværdier skal ligge mellem -1 og 1. `LFTri` bevæger sig, som de fleste andre oscillatorer, netop i dette interval:

```sc title="Modulation af panorering"
{
    var pan = LFTri.kr(0.5);
    var sig = Pulse.ar;
    Pan2.ar(sig, pan, 0.1)
}.play;
```

![type:audio](../media/audio/07-pan2-lfo.ogg)

Der findes `Pan4` og `PanAz`, som panorerer på tilsvarende vis med henholdsvis 4 eller et vilkårligt antal højttalere. Skal man panorere et signal, som allerede er i stereo, er `Pan2` ikke det rette valg - i stedet kan man anvende `Balance2`, som i stedet for at lave et monofont signal til stereo justerer balancen mellem to input-kanaler.

## Multikanalslyd med Multichannel Expansion

Som vi så ovenfor med duplikering, har vi faktisk ikke brug for specielle UGens som `Pan2` for at kunne arbejde med multikanalslyd. På et grundlæggende niveau understøtter de fleste UGens, at de på enkel vis kan "ekspanderes" med en teknik, der kaldes *Multichannel Expansion*. Dette er et lidt tricky emne at forstå, men det er egentlig ganske enkelt. Giver vi fx `SinOsc.ar` en liste med frekvenser i stedet for blot en enkelt frekvens, kan vi høre, at der oprettes flere forskellige oscillatorer:

```sc title="Multichannel expansion"
{SinOsc.ar([100, 250, 719, 1682]) * 0.1}.play;
{SinOsc.ar([100, 250, 719, 1682]).sum * 0.1}.play;
{Splay.ar( SinOsc.ar([100, 250, 719, 1682]) ) * 0.1}.play;
```

![type:audio](../media/audio/07-multichannel-expansion.ogg)

Hvad hører vi i dette eksempel? På et stereosystem eller hovedtelefoner kan vi kun høre to kanaler ad gangen:

- På første linje hører vi en sinustone ved 100Hz i venstre side og én ved 250Hz i højre. De højeste toner kan vi ikke høre[^1].
- På 2. linje summerer vi signalet med method'en `.sum`, og her er alle fire sinustoner hørbare, fordi de bliver lagt sammen og således kun udgør én kanal - den venstre.
- På 3. linje fordeler vi et vilkårligt antal kanaler jævnt i et stereofelt med UGen'en `Splay`.

Det tricky her er den subtile notation: Selvom vi kun noterer én `SinOsc`, bliver der automatisk oprettet 3 ekstra `SinOsc`-UGens, svarende til det antal frekvenser, som fremgår af listen.

[^1]:Vi kan forvisse os om, at der faktisk produceres mere end to kanaler, ved at indstille SuperColliders lydserver til at arbejde med fx 8 outputkanaler og vise lydstyrken på disse. Det gør vi med `s.options.numOutputBusChannels = 8;`. Efter `s.reboot;` kan vi så køre `s.meter;`, som viser signalets amplitude på de 8 kanaler (hvoraf vi dog stadig kun kan høre to, hvis vi lytter på et almindeligt stereosetup med højttalere eller hovedtelefoner).

### Videreførelse af ekspansion

Ekspansionen videreføres til UGens, som ligger senere i signalkæden. I eksemplet herunder opretter vi først to tilfældighedsgeneratorer, den ene genererer 5 tilfældige værdier pr. sekund, den anden 10. Når `SinOsc` på næste linje modtager dette signal med to kanaler, ekspanderes der videre, så vi får to tilsvarende sinusbølge-oscillatorer.

```sc title="Stereosignal med arrays"
{
    var freqs = LFNoise0.kr([5, 10]).exprange(200, 800);
    SinOsc.ar(freqs); // skaber to sinusbølge-oscillatorer
}.play;
```

![type:audio](../media/audio/07-stereo-array.ogg)

Dette betyder også, at vi med en ganske begrænset mængde kildekode kan oprette et væld af oscillatorer og, fx ved hjælp af `Splay`, samle dem igen til et meget fyldigt lydbillede. Her kan vi eksempelvis bruge duplikering [som vist ovenfor](a-oscillatorbanke.md#duplikering) til at generere et signal med 30 oscillatorer:

```sc title="Mange oscillatorer med duplikering og multichannel expansion"
{
    var freqs = LFNoise2.kr(0.25.dup(30)).exprange(110, 1760);
    var amps = LFNoise1.kr(2.dup(30)).exprange(0.01, 0.1);
    var sig = SinOsc.ar(freqs) * amps;
    Splay.ar(sig);
}.play;
```

![type:audio](../media/audio/07-30-oscillatorer-scifi.ogg)

Dette kan vi også kalde en *oscillatorbank*. Her kan vi forhåbentlig begynde at ane, hvordan brug af multikanalslyd kan være en effektiv teknik inden for lyddesign.

## Detuning

Oscillatorbanke er fx særdeles velegnede til at skabe "tykkere" klange gennem detuning. Her opretter vi med multichannel expansion fire forskellige oscillatorer, der klinger med næsten samme frekvens, lægger dem sammen med `.sum` og panorerer til sidst med `Pan2`:

```sc title="Detuning med .midiratio"
{
    var freq = 220;
    var transposeFactors = [0, 0.10, -0.07, -0.08].midiratio;
    var sig = Saw.ar(freq * transposeFactors);
    sig = sig.sum * 0.1;
    Pan2.ar(sig);
}.play;
```

![type:audio](../media/audio/07-detuning.ogg)

## Algoritmisk oprettelse af oscillatorbanke

Computere er glimrende redskaber til at gentage de samme operationer mange gange, så længe vi beskriver præcist hvad der skal gøres. Vi kan danne oscillatorbanke ved at beskrive hvad der skal skabes med en [funktion](../01/a-funktioner.md), der så udføres og skaber oscillatorbanken ved hjælp af [iteration](../01/a-lister.md#iteration-over-lister). Genlæs evt. de relevante afsnit herom, før du læsere videre.

### Algoritmisk dannede oscillatorbanke

Hvis vi eksempelvis vil skabe en klang med de første toner i den naturlige overtonerække, kan vi oprette en liste med grundtonen og frekvenserne for de 4 oktaver, som ligger over grundtonen. Her lægger vi 1 til, fordi vi som bekendt tæller fra 0:

```sc title="Grundtone og overtoner"
5.collect({
    arg num;
    var octave = num + 1;
    var freq = 110;
    freq * octave;
}); // -> [ 110, 220, 330, 440, 550 ]
```

Vi kan omsætte dette til et klingende eksempel ved at lade tonerne fremstille sinusbølge-oscillatorer og blive fordelt jævnt i et stereofelt med `Splay`:

```sc title="Fordeling af overtoner i stereofeltet"
{
    var freq = 110;
    var sig = 5.collect({
        arg num;
        var octave = num + 1;
        SinOsc.ar(freq * octave);
    });
    Splay.ar(sig);
}.play;
```

![type:audio](../media/audio/07-simpel-oscillatorbank.ogg)

Dette princip kan udfoldes og danne rammen for mange forskellige lyddesign, heriblandt først og fremmest additiv klangdannelse.
