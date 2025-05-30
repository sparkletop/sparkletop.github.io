---
tags:
    - Øvelser
---

# Øvelse: Samples

I denne øvelse arbejder du med sample-afspilning ved hjælp af `PlayBuf`.

## Klargøring af sample

Til brug i denne øvelse skal der indlæses et sample. Du kan bruge din egen lydfil, den skal blot have disse egenskaber:

- Samplet skal vare maksimalt 10 sekunder.
- Samplet skal være trimmet (brug hertil evt. [Audacity](https://www.audacityteam.org/)), så der ikke er stilhed i begyndelsen eller slutningen af samplet.
- Samplet skal indlæses i mono.

Som forberedelse til de øvrige opgaver herunder:

1. Indlæs et sample i en buffer gemt under variablen `~buffer`.
1. Hvis din lydfil er i stereo, kan du indlæse den første kanal med `.readChannel` (se kodeblokken herunder).
1. Hvis du ikke har en lydfil klar selv, kan du bruge den nederste linje herunder i stedet med et indbygget sample fra SuperCollider.

```sc title="Indlæsning af sample"
// Udfyld her med dit eget sample
~buffer = Buffer.read(s,      );

// Brug .readChannel, hvis dit sample er i stereo
~buffer = Buffer.readChannel(s, channels: [0], path:   );

// Hvis du ikke har en lydfil klar, kan du bruge et indbygget sample i stedet:
~buffer = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");
```

## Afspilning med PlayBuf

1. Afspil dit sample ved dobbelt hastighed.
1. Afspil dit sample ved halv hastighed.
1. Afspil den sidste halvdel af dit sample.
1. Afspil dit sample baglæns (bemærk, at dette kræver justering af enten `startPos` eller `loop` og `doneAction`).

```sc title="Sampleafspilning med PlayBuf" hl_lines="6 8 9"
{
    PlayBuf.ar(
        numChannels: 1,
        bufnum: ~buffer,
        rate: BufRateScale.kr(~buffer) * 1,
        trigger: 1,
        startPos: BufFrames.kr(~buffer) * 0,
        loop: 0,
        doneAction: Done.freeSelf
    )
}.play;
```

## Afspilningshastighed

1. Modulér afspilningshastigheden ved at fjerne `//`'erne for en række forskellige LFO'er herunder.
1. Notér i kommentarer, hvilken effekt de forskellige modulatorer har på den æstetiske oplevelse.

```sc title="Modulation af afspilningshastighed"
{
    var rate = 1; // afkommentér linjerne herunder for eksempler
    // rate = LFPulse.kr(1).range(0.5, 2);
    // rate = SinOsc.kr(1).range(-1, 1);
    // rate = SinOsc.kr(1).range(0.5, 2);
    // rate = SinOsc.kr([1, 1.02]).range(1, 1.5);
    // rate = LFNoise1.kr(2.dup).exprange(0.5, 4);
    // rate = Line.kr(-5, 5, 10, doneAction: 2);

    PlayBuf.ar(
        1,
        ~buffer,
        BufRateScale.kr(~buffer) * rate,
        loop: 1,
        doneAction: Done.none
    );
}.play;
```

## Lydcollage-komposition

Fremstil en abstrakt lydcollage. Kompositionen skal baseres på ét sample og realiseres ved at bruge patterns sammen med SynthDef'en fra [tidligere afsnit om lydcollage](a-lydcollage.md).

1. Vælg og indlæs et sample, som...
    1. ... indeholder en vedvarende lyd (dvs. uden lange pauser i lyden).
    1. ... varer mellem 2 og 10 sekunder.
    1. ... tonalt set er relativt enkel og stabil.
    1. ... indeholder én monokanal (brug evt. `Buffer.readChannel` som ved opgave 1, hvis din ønskede fil er stereo-format).
1. Modificér `Pbind`'en herunder ved at erstatte faste værdier med patterns, således at vi hører en klangligt varieret lydcollage baseret på det valgte sample.

```sc title="Indlæs sample"
// Erstat stien med en sti til din egen lydfil
~vedvarendeLyd = Buffer.readChannel(s, "C:/lydfiler/minSejeLydfil.wav", [0]);
```

```sc title="Samplecollage genereret med patterns" hl_lines="7 12-21"
TempoClock.tempo = 60/60;
Pdef(\collage,
    Pbind(
        \instrument, \sampleM,

        // PlayBuf-indstillinger
        \buffer, ~vedvarendeLyd,
        \startPos, 0,
        \transpose, 0,
        \loop, 1,
        \direction, 1,

        // Timing og overlap
        \dur, 1,
        \legato, 1,

        // Klang
        \drive, 0.1,
        \cutoff, 1000,
        \rq, 0.5,

        // Panorering og lydstyrke
        \pan, 0,
        \db, -20,
        \atk, 0.1, \rel, 1,
    )
).play;
```
