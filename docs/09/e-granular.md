---
tags:
    - Øvelser
---

# Øvelse: Granular syntese

I denne øvelse arbejder du med granulering af samples ved hjælp af UGen'en `GrainBuf`.

## Valg og indlæsning af sample

Til brug i denne øvelse skal der indlæses et sample. Du kan bruge din egen lydfil, den skal blot:

- Vare maksimalt 10 sekunder.
- Være trimmet, så der ikke er stilhed i begyndelsen eller slutningen af samplet.
- Indlæses i mono.

Som forberedelse til de øvrige opgaver herunder:

1. Indlæs et sample i en buffer gemt under variablen `~buffer`.
1. Hvis din lydfil er i stereo, kan du indlæse den første kanal med `.readChannel` - se kodeblokken herunder.
1. Hvis du ikke har en lydfil klar selv, kan du bruge den nederste linje herunder, som indlæser et indbygget sample fra SuperCollider.

```sc title="Indlæsning af sample"
// Udfyld her med dit eget mono-sample
~buffer = Buffer.read(s,      );

// Brug .readChannel, hvis dit sample er i stereo
~buffer = Buffer.readChannel(s, channels: [0], path:   );

// Hvis du ikke har en lydfil klar, kan du bruge et indbygget sample i stedet:
~buffer = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");
```

## Grain-produktion med GrainBuf

Justér nedenstående kodeblok, således at:

1. Der kommer overlap mellem de enkelte grains.
1. Følgende parametre moduleres af LFO'er, fx `SinOsc`, `XLine`, `EnvGen`, `LFNoise`, `LFTri` etc.:
    1. `dur`
    1. `rate`
    1. `pos`
    1. `pan`
1. `Dust` anvendes som trigger i stedet for `Impulse`.

Hvordan påvirker disse parametre og modulationer lyden? Hvilke æstetiske muligheder kan du se i denne form for sample-manipulation?

```sc title="Modulation af GrainBuf-parametre"
(
{
    GrainBuf.ar(
        numChannels: 2,
        trigger: Impulse.ar(10),
        dur: 0.025,
        sndbuf: ~buffer,
        rate: BufRateScale.kr(~buffer) * 1,
        pos: MouseX.kr(0, 1),
        pan: 0
    )
}.play;
)
```
