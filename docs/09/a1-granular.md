---
tags:
    - Artikler
---

# Granular syntese

Granular syntese er kort fortalt en teknik, der går ud på at danne komplekse klange og teksturer ved at sammensætte korte lydklip ("grains") til unikke strømme af lyd. Granular er en af de klangdannelsesteknikker, som hører til den digitale tidsalder, og SuperCollider indeholder glimrende redskaber til at arbejde med teknikken.

På den ene side er granular én blandt flere metoder til at adskille frekvens- og tidsdomænet (og derved fx undgå, at et vokalsample bliver til en musestemme, selvom tempoet sættes op). På den anden side kan granular syntese skabe unikke teksturer, klangflader og grooves, som ikke kan fremstilles på anden vis.

Granular er et komplekst emne med mange muligheder og parametre. Her introduceres grundlæggende teknikker og kompositionsmuligheder. For videregående teknikker henvises nysgerrige læsere til Eli Fieldsteels video nr. [25](https://youtu.be/WBqAM_94TW4) og [26](https://youtu.be/MnD8stNB5tE).

## Grundlæggende `GrainBuf`

Man kan i princippet danne grains af hvilken som helst lydkilde, men samples eller live-lydsignaler anvendes ganske ofte som kildemateriale. Herunder tager vi udgangspunkt i et sample, som er [indlæst i en buffer](../08/a1-samples.md). I den sammenhæng er det oplagt at anvende UGen'en `GrainBuf`, som netop læser grains fra en buffer (som skal indeholde et mono-sample).

### Argumenter til `GrainBuf`

Her hører vi 5 grains pr. sekund, placeret i midten af et stereofelt, hver med en varighed på 25ms, læst fra midten af den buffer, hvor vores sample er indlæst:

```sc
// Indlæs sample i mono (husk at erstatte med sti til lydfil på din egen computer)"
~sample = Buffer.readChannel(s, "C:/samples/minLydFil.wav", channels: [0]);

(
{
    GrainBuf.ar(
        // Antallet af output-kanaler
        numChannels: 2,

        // Et triggersignal, som udløser grains
        trigger: Impulse.ar(5),

        // Varigheden af grains
        dur: 0.025,

        // Den buffer, grains skal læses fra
        sndbuf: ~sample,

        // Afspilningshastighed for grains
        rate: BufRateScale.kr(~sample) * 1,

        // Læseposition i bufferen, hvor 0 er begyndelsen og 1 er slutningen
        pos: 0.5,

        // Position i stereofelt, ligesom ved Pan2 (når der arbejdes med 2 output-kanaler)
        pan: 0
    );
}.play;
)
```

Der findes yderligere argumenter til `GrainBuf`, men de er af mindre betydning for den grundlæggende anvendelse. Nysgerrige læsere henvises til [den relevante dokumentation](https://doc.sccode.org/Classes/GrainBuf.html).

### Triggere

Som argument til `GrainBuf.ar` angiver vi blandt andet et såkaldt triggersignal, som fortæller `GrainBuf`, hvornår der skal udløses et nyt grain. Man kan anvende et hvilket som helst signal som trigger, men typiske valg er `Impulse`, som udsender triggere med en fast frekvens, og `Dust`, som udsender triggere på tilfældige tidspunkter, men med et gennemsnitligt antal pr. sekund, groft svarende til frekvensen for `Impulse`.

![{ [Impulse.kr(50), Dust.kr(50)] }.plot(1)](../media/figures/triggere.png)

Hvorfor bruge den mere uregelmæssige og kaotiske `Dust` fremfor `Impulse`? Jo, med `Impulse` kan triggeren komme til at fungere som en form for amplitude-modulation, hvor frekvensen træder frem som et hørbart artefakt med særskilt pitch. For at modvirke dette kan man anvende `Dust`, der ikke resulterer i samme periodiske mønster. Hertil kommer selvfølgelig, at man kan have æstetisk præference for det mere tilfældighedsprægede udtryk, som også kendetegner `Dust`.

### Overlap eller luft i strømmen af grains

En central parameter i granular syntese er mængden af overlap mellem grains, dvs. om vi hører én kontinuerlig strøm af grains, eller om vi hører en masse korte lydbidder med "luft" imellem. Mængden af overlap afhænger af forholdet mellem to af de parametre, vi angiver som argumenter til `GrainBuf`: Grainvarighed og triggerfrekvens. Man kan ganske enkelt beregne mængden af overlap med følgende formel: `overlap = triggerfrekvens * grainvarighed`.

- Ved en triggerfrekvens på 100Hz og en grainvarighed på 1/100 sekund (0.010s) vil der hverken være overlap eller "luft" mellem de enkelte grains: `100Hz * 0.010s = 1`.
- Var triggerfrekvensen i stedet 50Hz, ville mængden af overlap være ½, dvs. der vil være stilhed 50% af tiden: `50Hz * 0.010s = 0.5`.
- Med en triggerfrekvens på 200Hz, vil der konstant være 2 samtidigt klingende grains: `200Hz * 0.010s = 2`.

Det er oplagt at styre overlap og grainvarighed kompositorisk, dvs. med LFO'er eller patterns. Vi kan i stedet udregne triggerfrekvensen automatisk ved at isolere den i formlen ovenfor: `triggerfrekvens = overlap / grainvarighed`.

Hvis vi eksempelvis styrer grainvarighed og overlap med en LFO (her simuleret med musens X- og Y-koordinater på skærmen), kan vi således kalkulere triggerfrekvensen automatisk:

```sc title="Automatisk beregning af triggerfrekvens"
(
{
    var grainDur = MouseX.kr(0.01, 0.2, \linear).poll(label: \grainDur);
    var overlap = MouseY.kr(0.5, 20, \exponential).poll(label: \overlap);
    var trigFreq = (overlap / grainDur).poll(label: \trigFreg);
    
    GrainBuf.ar(
        numChannels: 2,
        trigger: Dust.ar(trigFreq),
        dur: grainDur,
        sndbuf: ~sample,
        rate: 1,
        pos: LFSaw.ar(0.5, 1).unipolar,
        pan: 0
    );
}.play;
)
```

