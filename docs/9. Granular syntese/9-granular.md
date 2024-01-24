---
tags:
    - Artikler
---

# Granular syntese

Granular syntese er kort fortalt en teknik, der går ud på at danne komplekse klange og teksturer ved at sammensætte korte lydklip ("grains") til unikke strømme af lyd. Granular er en af de klangdannelsesteknikker, som hører til den digitale tidsalder, og SuperCollider indeholder glimrende redskaber til at arbejde med granular syntese. På den ene side er granular én blandt flere metoder til at adskille frekvens- og tidsdomænet (og derved fx undgå, at et vokalsample bliver til en musestemme, selvom tempoet sættes op), men på den anden side kan granular syntese skabe unikke teksturer og klangflader, som ikke kan fremstilles på anden vis.

Granular er et komplekst emne med mange muligheder og parametre. Her introduceres blot et par grundlæggende idéer og teknikker - for videregående teknikker henvises nysgerrige læsere til Eli Fieldsteels video nr. [25](https://youtu.be/WBqAM_94TW4) og [26](https://youtu.be/MnD8stNB5tE).

## Triggering og grainvarighed med `GrainBuf`

Man kan i princippet danne grains af hvilken som helst lydkilde, men samples eller live-lydsignaler anvendes ganske ofte. Her tager vi udgangspunkt i et sample, som [er indlæst i en buffer](../8. Samples/8.1-samples.md), og i den sammenhæng er det oplagt at anvende UGen'en `GrainBuf`. Man skal dog være opmærksom på, at `GrainBuf` kun fungerer med mono-samples (hertil kan der indlæses blot én kanal, hvis man har en stereo-lydfil).

Her hører vi 5 grains pr. sekund, placeret i midten af et stereofelt, hver med en varighed på 25ms, læst fra midten af den buffer, hvor vores sample er indlæst:

```sc
// Erstat stien herunder med en relevant sti til en lydfil på din computer
~sample = Buffer.readChannel(s, "C:/lydfiler/minLydFil.wav", channels: [0]);

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

Alle argumenterne ovenfor kan moduleres med andre UGens, hvilket typisk er tilfældet, da lyddesignet ellers bliver helt statisk. Der findes yderligere argumenter til `GrainBuf`, og nysgerrige læsere henvises til [den relevante dokumentation](https://doc.sccode.org/Classes/GrainBuf.html).

### Triggere

Som argument til `GrainBuf.ar` angiver vi blandt andet et såkaldt triggersignal, som fortæller `GrainBuf`, hvornår der skal udløses et nyt grain. Man kan anvende et hvilket som helst signal som trigger, men det typiske valg er `Impulse`, som udsender triggere med en fast frekvens, eller `Dust`, som udsender triggere på tilfældige tidspunkter, men med et gennemsnitligt antal triggere pr. sekund, svarende til frekvensen for `Impulse`.

![{ [Impulse.kr(50), Dust.kr(50)] }.plot(1)](media/triggere.png)

Hvorfor bruge den mere uregelmæssige og kaotiske `Dust` fremfor `Impulse`? Jo, med `Impulse` kan triggeren komme til at fungere som en form for amplitude-modulation, hvor frekvensen træder frem som et hørbart artefakt med særskilt pitch. For at modvirke dette kan man anvende `Dust`. Hertil kommer selvfølgelig æstetisk præference for det mere tilfældighedsprægede udtryk, som kendetegner `Dust`.

### Overlap, triggerfrekvens og grainvarighed

En central parameter i granular syntese er mængden af overlap mellem grains, som afhænger af forholdet mellem grainvarigheder og triggerfrekvens, givet følgende formel: `triggerfrekvens * grainvarighed = overlap`.

Ved en triggerfrekvens på 100Hz og en grainvarighed på 1/100 sekund (0.010s) vil der hverken være overlap eller "luft" mellem de enkelte grains: `100 * 0.010 = 1`.

Man kan styre disse tre parametre på forskellig vis, men det kan være en god idé at styre overlap og grainvarighed med LFO'er eller patterns, og derfra udregne triggerfrekvensen automatisk. Her styres grainvarighed og overlap således med musen:


``` sc
(
{
    var grainDur = MouseX.kr(0.01, 0.2, \linear).poll(label: \grainDur);
    var overlap = MouseY.kr(0.5, 20, \exponential).poll(label: \overlap);
    var trigFreq = (overlap / grainDur).poll(label: \trigFreg);
    
    GrainBuf.ar(
        numChannels: 2,
        //trigger: Impulse.ar(trigFreq),
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

## Adskillelse af varighed og frekvens

Én af de særligt nyttige egenskaber ved granular syntese er evnen til at adskille varighed og frekvens - eller mere teknisk - tids- og frekvensdomænet.

### En pointer til at styre grainposition

I dette eksempel bruger vi UGen'en `Phasor` til at definere en "pointer", som vi kan bruge til at angive hvor i bufferen, grains skal læses fra. Vi kan styre pointerens bevægelseshastighed og transponere grains op og ned vha. argumenter:

``` sc
(
~granulator = {
    arg transpose = 0, moveRate = 1;

    var buf = ~sample;
    var numFrames = BufFrames.kr(buf);
    var pointer = Phasor.ar(
        rate: rateScale * moveRate,
        start: 0,
        end: numFrames
    ) / numFrames;

    var trigger = Dust.kr(200);
    
    GrainBuf.ar(
        numChannels: 2,
        trigger: trigger,
        dur: 0.1,
        sndbuf: buf,
        rate: BufRateScale.kr(buf) * transpose.midiratio,
        pos: pointer,
        pan: 0
    ) * 0.1;
}.play;
)

// Transponering påvirker ikke afspilningshastighed
~granulator.set(\transpose, 7)
~granulator.set(\transpose, -12)

// Afspilningshastighed påvirker ikke tonehøjde
~granulator.set(\moveRate, 0.5)
~granulator.set(\moveRate, 3)

// Tonehøjde og varighed/tempo kan justeres som adskilte parametre!
~granulator.set(\moveRate, 0.25, \transpose, 12)
```

### Tekstur og klangflade med tilfældighed

Hvor ovenstående giver en meget fleksibel måde at strække eller transponere lyd på, kan vi skabe mere abstrakte teksturer ved at tilføje lidt støj til pointeren og fordele grains tilfældigt over hele stereofeltet. Dette kan blandt andet gøres ved hjælp af UGen'en `TRand`, som producerer tilfældige tal mellem et minimum og maksimum, hver gang den modtager en trigger:

``` sc hl_lines="4 16 18 26 27"
(
~sprinkler = {
    arg transpose = 0, moveRate = 1,
    jitter = 0.01, spread = 0.1;

    var buf = ~sample;
    var numFrames = BufFrames.kr(buf);
    var pointer = Phasor.ar(
        rate: rateScale * moveRate,
        start: 0,
        end: numFrames
    ) / numFrames;

    var trigger = Dust.kr(200);

    var jit = TRand.kr(jitter.neg, jitter, trigger) / BufDur.kr(buf);

    var pan = TRand.kr(spread.neg, spread, trigger);

    GrainBuf.ar(
        numChannels: 2,
        trigger: trigger,
        dur: 0.1,
        sndbuf: buf,
        rate: BufRateScale.kr(buf) * transpose.midiratio,
        pos: pointer + jit,
        pan: pan
    ) * 0.1;
}.play;
)

// Fordeling af grains i stereofelt (høres bedst i hovedtelefoner)
~sprinkler.set(\spread, 0)
~sprinkler.set(\spread, 1)

// Spring i grainposition
~sprinkler.set(\jitter, 0.1)
~sprinkler.set(\jitter, 1.5)

// Stillestående pointer, med spredning i grainposition
~sprinkler.set(\jitter, 1, \moveRate, 0)
```
