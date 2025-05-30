---
tags:
    - Artikler
---

??? abstract "Introduktion til kapitlet"

    Vi har indtil nu arbejdet med rent syntetisk dannede klange i SuperCollider. Men der er også gode muligheder for at arbejde med præindspillet lyd eller for den sags skyld live-lyd fra en mikrofon eller andet musikudstyr. Her koncentrerer vi os i første omgang om at arbejde med samples i form af præeksisterende lydfiler, som vi først indlæser og derefter kan bearbejde i SuperCollider. Sample-manipulation er ganske fleksibelt i SuperCollider, men kræver en lille smule teknisk forberedelse, som gennemgås herunder. Derefter introducerer kapitlet til to kompositionsstrategier: Produktion af varierende og dynamiske trommebeats med "humaniseret" mikrorytmiske forskydninger samt abstrakt lydcollage.

# Afspilning af samples

Når vi arbejder med samples i SuperCollider, skal vi indlæse disse på lydserveren. Dette gør vi ved hjælp af `Buffer`-klassen, og vi kan derefter afspille vores samples med UGens som `PlayBuf` og den lidt mere avancerede `BufRd`. Dette introduceres herunder.

## Indlæsning af sample i Buffer

For at arbejde med et sample/en lydfil, skal samplet indlæses i en såkaldt `Buffer`, som udgør et afgrænset område i lydserverens hukommelse. Det gør vi med `Buffer.read`, hvor første argument er lydserveren (i vores tilfælde `s`), og andet argument er stien til den lydfil, vi ønsker.

Til at starte med kan vi bruge et sample, der følger med SuperCollider (linje 3). Men man kan nemt arbejde med egne samples (se linje 6 herunder) - erstat blot `C:/lydfiler/minlydfil.wav` med stien til din egen lydfil. Stien kan genereres automatisk ved at trække filen ind i SuperCollider med musen, eller ved at copy-paste filen fra en mappe på din computer. Når du slipper en fil med musen eller taster Cmd-/Ctrl-V på tastaturet for at sætte filen ind, vil SuperColliders IDE skrive filens sti, der hvor musemarkøren eller cursoren befinder sig.

```sc title="Indlæsning af lydfil i Buffer"
// Et indbygget sample indlæses i buffer
~sample = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");

// En ekstern lydfil indlæses i buffer
~sample = Buffer.read(s, "C:/lydfiler/minlydfil.wav");
```

Ønsker vi blot at indlæse én af flere kanaler i en lydfil, kan vi i stedet for `Buffer.read` bruge `Buffer.readChannel` og under argumentet `channels` angive en liste med et tal for hver af de kanaler, vi ønsker at indlæse. Her er 0 typisk den venstre og 1 typisk den højre kanal.

```sc title="Indlæsning af lydfil i mono-buffer"
// En ekstern lydfil indlæses i mono-buffer
~sample = Buffer.readChannel(s, "C:/lydfiler/minlydfil.wav", channels: [0]);
```

Når lydfilen er indlæst i en `Buffer` under variabelnavnet `~sample`, kan vi bruge de forskellige instance methods, som knytter sig til buffere, til at vise noget grundlæggende information om samplet:

```sc title="Nyttige info-methods til buffere"
~sample.play;      // afspilning, anvendes kun til test

~sample.query;     // info om bufferens indhold
~sample.plot;      // visuel repræsentation
~sample.path;      // samplets oprindelig sti i filsystemet
~sample.duration;  // længde i sekunder
```

## Sample-afspilning med PlayBuf

Den mest enkle metode til afspilning af samples er at bruge UGen'en `PlayBuf`. Her er der to tekniske forhold, det er værd at huske på:

- **Sampleraten** i en given lydfil matcher ikke nødvendigvis lydserverens samplerate. Hvis lydserverens samplerate er 44.1 kHz, men lydfilen er produceret ved 48 kHz, vil afspilningen ske for langsomt, og tonehøjde, tempo osv. vil ikke passe. Derfor har vi en særlig UGen, der kan tage højde for sådanne mismatch, nemlig `BufRateScale`.
- **Antal samples:** Et lydsample eller en lydfil består af et bestemt antal "målinger", der med et lidt uheldigt terminologisk sammenfald også kaldes *samples* på engelsk (deraf betegnelsen "samplerate"). Med `PlayBuf` måler vi samplets varighed ud fra antallet af disse samples, sammenholdt med samplerate, dvs. hvor hurtigt vi skal læse disse samples. Vi kan imidlertid ikke gå ud fra antallet af samples i en Buffer, da en buffer kan indeholde data fra lydfiler med et variabelt antal kanaler (oftest arbejder vi dog med mono- eller stereofiler). For at finde varigheden af en indlæst lydfil, målt i enkeltsamples, kan vi i stedet bruge UGen'en `BufFrames`. Den giver os antallet af såkaldte sample frames, der er fast, uanset hvor mange kanaler, bufferen indeholder.

Her kan du se, hvordan man indstiller argumenterne til `PlayBuf` og bruger `BufRateScale` samt `BufFrames`:

```sc title="PlayBuf-argumenter"
{
    PlayBuf.ar(
        // antal kanaler
        numChannels: 1,

        // buffer nummer / Buffer objekt
        bufnum: ~sample,

        // afspilningshastighed - BufRateScale tager højde for mismatch mellem serverens og lydfilens respektive samplerates
        rate: 1 * BufRateScale.kr(~sample),

        // reset-trigger, kan bruges til at angive spring til startposition
        trigger: 1,

        // startposition, målt i sample frames - BufFrames er det samplede antal sample frames i bufferen/lydfilen 
        startPos: 0 * BufFrames.kr(~sample),

        // loop - start forfra, når vi rammer slutningen af bufferen (0 = nej, 1 = ja)
        loop: 0,

        // doneAction - hvad sker der, når vi rammer den sidste sample frame i bufferen?
        doneAction: Done.freeSelf
    )
}.play
```

Vi kan modulere flere af `PlayBuf`s parametre ved hjælp af andre UGens. For eksempel afspilningshastighed:

```sc title="Modulation af sampleafspilning med LFO"
{
    PlayBuf.ar(1, ~sample,
        SinOsc.kr(2) * BufRateScale.kr(~sample)
    )
}.play;
)
(
{
    PlayBuf.ar(1, ~sample,
        LFNoise1.kr(0.5).range(0.5, 2) * BufRateScale.kr(~sample),
        loop: 1
    )
}.play;
```

![type:audio](eksempel.ogg)

Med et triggersignal, her skabt af UGen'en `Impulse`, kan vi springe hen til den position i bufferen, som er angivet med argumentet `startPos`.

```sc title="Spring til position i sample"
// Fast startposition - midt i bufferen
{
    PlayBuf.ar(1, ~sample,
        trigger: Impulse.kr(5),
        startPos: 0.5 * BufFrames.kr(~sample),
    )
}.play;
)

(
// Dynamisk startposition, moduleret af en LFO
{
    PlayBuf.ar(1, ~sample,
        trigger: Impulse.kr(5),
        startPos: BufFrames.kr(~sample) * LFTri.kr(0.05).unipolar,
    )
}.play
```

![type:audio](eksempel.ogg)

## Ekstra fleksibilitet med BufRd

`BufRd` er mere fleksibel end `PlayBuf`, fordi den tillader, at vi styrer læsningen af data fra bufferen direkte med en anden UGen. Det svarer lidt til, at en pickupnål aflæser den lyd, som er indpræget i en vinylplade - bortset fra at vi med et bredt udvalg af UGens kan flytte nålen rundt på meget forskellig vis. Til at styre afspilningspositionen angiver vi en UGen under `BufRd.ar`'s argument `phase`.

Ofte anvendes UGen'en `Phasor`, som skaber en lineær rampe fra start- til slutværdi (det er generelt sådan samples afspilles i digitale lydsystemer).

```sc title="Sample-afspilning med BufRd og Phasor"
{
    BufRd.ar(
        numChannels: 2,
        bufnum: ~sample,
        // phase-argumentet er afspilningspositionen, målt i sample frames
        phase: Phasor.ar(0, BufRateScale.kr(~sample), 0, BufFrames.kr(~sample)),
        loop: 1
    )
}.play
```

Man kan anvende mange forskellige UGens som alternativ til `Phasor`. Her moduleres afspilningsposition i `BufRd` af henholdsvis en perkussiv envelope og lavfrekvent støj:

```sc title="Envelope og tilfældighedsgenerator som pickupnål"
{
    var position = EnvGen.ar(Env.perc(0.1, 2)) * BufFrames.kr(~sample);
    BufRd.ar(1, ~sample, position, 1);
}.play;
)

(
{
    var position = LFNoise1.ar(6).range(0, BufFrames.kr(~sample));
    BufRd.ar(1, ~sample, position, 1);
}.play;
```

![type:audio](eksempel.ogg)
