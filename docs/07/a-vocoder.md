---
tags:
    - Artikler
---

# Old school vocoder

En vocoder er en lydeffekt, der oftest bliver brugt til at skabe den efterhånden velkendte "robotstemme"-lyd. Vocoderen fungerer således, at man analyserer frekvensspektret for ét lydsignal og anvender resultatet af analysen til at justere på frekvensspektret for et andet lydsignal. Det analyserede lydsignal er ofte en menneskestemme, da menneskelig tale og sang er karakteriseret ved, at overtonespektret indeholder grupper af fremtrædende overtoner kaldet *formanter*, hvis konstante forskydning og afveksling danner stavelser, ord og sætninger [@berg2025, Steady-state waves | The human voice]. Vocoderen overfører variationerne i overtonespektret fra lydkilden til en ofte syntetisk dannet klang, eksempelvis en savtakket bølgeform, der indeholder et righoldigt overtonespektrum. Dette kan implementeres på forskellige måder, men her kigger vi på en digital emulering af den tidlige analoge vocoder fra 1930'erne, som beskrevet af Curtis Roads [-@roads2023, pp. 207-208].

## Den grundlæggende vocoder-teknik

Vi starter med den lydkilde, som skal udsættes for analyse. Den kalder vi for **kilde A**. Det er som sagt ofte den menneskelige stemme, som er rig på formanter, men alle signaler med et dynamisk spektralt indhold kan anvendes. Her anvender vi blot en støjgenerator, som vi senere erstatter med et vokalsample. For at analysere et lydsignals frekvensspektrum, kan man dele dette op i en række "bånd" og måle på lydstyrken inden for hvert af disse bånd. Lad os illustrere, hvordan man kan gøre dette for ét bånd med centerfrekvens på 200Hz ved at isolere båndet med et band pass-filter (`BPF.ar`) og måle amplituden med `Amplitude.ar`:

```sc title="Analyse af amplitudeenvelope i frekvensbånd"
{
    var kildeA = PinkNoise.ar;
    var amp = Amplitude.ar(BPF.ar(kilde, 200, 0.15));
    // amp indeholder amplituden for frekvensbåndet
}
```

Hvis vi ønsker at arbejde med en række bånd frem for blot ét, kan vi [bruge en algoritme til at danne en bank af signaler for os](a-oscillatorbanke.md#algoritmisk-oprettelse-af-oscillatorbanke). Her kan vi fx finde amplituderne ved 500Hz, 1000Hz, 2000Hz og 4000Hz:

```sc title="Spektral envelopeanalyse"
{
    var kilde = PinkNoise.ar;
    var amps = [500, 1000, 2000, 4000].collect({
        arg centerFreq;
        Amplitude.ar(BPF.ar(kilde, centerFreq, 0.15));
    });
    // amps indeholder amplituder for de fire frekvensbånd
}
```

Når vi nu har disse amplituder, kan vi bruge dem til at styre amplituden af tilsvarende frekvensbånd i et andet lydsignal, som vi kan kalde for **kilde B**. Her kan vi tage en savtakket bølgeform som eksempel. Den er velegnet, fordi den har et righoldigt overtonespektrum, hvor manipulationen med den spektrale envelope fra kilde A tydeligt vil kunne høres. Med en sinusbølge, som ikke har nogen overtoner, vil der ikke være nogen hørbar effekt.

```sc title="Basal vocoding"
{
    var kildeA = PinkNoise.ar;
    var kildeB = Saw.ar;
    var sig = [500, 1000, 2000, 4000].collect({
        arg centerFreq;
        var amp = Amplitude.ar(BPF.ar(kildeA, centerFreq, 0.15));
        amp * BPF.ar(kildeB, centerFreq, 0.15);
    }).sum;
    // sig indeholder den modificerede version af kildeB
}
```

## Sammensætning i SynthDef

For at udnytte ovenstående teknik til at fremstille den klassiske vocoder-lyd, kan vi anvende et vokalsample som kilde A. Derudover skal vi fremstille en liste med centerfrekvenser til vores frekvensbånd.

```sc title="Forberedelse til vocoder"
(
// Først indlæser vi et sample med noget tale
~speak = Buffer.readChannel(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");

// Centerfrekvenser
~bandFrequencies = 12.collect({
    arg num;
    num.linexp(0, 11, 50, 12000);
});
)
```

Når ovenstående kode er eksekveret, kan vi registrere nedenstående SynthDef.

```sc title="En old school vocoder-SynthDef"
(
SynthDef(\vocoder, {
    arg freq = 440, gate = 1, pan = 0, amp = 0.5, rq = 0.15, noiseThreshold = 0.1;
    var kildeA, kildeB, sig;
    kildeA = PlayBuf.ar(1, ~speak, loop: 1);
    kildeB = Saw.ar(freq);

    sig = ~bandFrequencies.collect({
        arg centerFreq;
        Amplitude.ar(BPF.ar(kildeA, centerFreq, rq)).lag(0.01)
        * BPF.ar(kildeB, centerFreq, rq);
    }).sum * 2;

    sig = sig * Env.asr(0.01, 1, 0.2).kr(2, gate);
    // En simpel noise gate
    sig = sig * (DetectSilence.ar(kildeA + Impulse.ar(0), amp: noiseThreshold, time: 0.05) - 0.7).fold(0, 1).round;
    sig = Pan2.ar(sig, pan, amp);
    Out.ar(0, sig);
}).add;
)
```

Når SynthDef'en er indlæst, kan vi bruge den til at spille et robotstemme-mønster i skiftende akkorder ved hjælp af patterns.

```sc title="Vi spiller på vocoderen med patterns"
(
TempoClock.tempo = 1;
Pbind(
    \instrument, \vocoder,
    \degree, [-7, 0, 2, 4],
    \octave, 5,
    \mtranspose, Pseq([0, 1, 2, -3], inf),
    \dur, ~speak.duration,
    \pan, Pgauss(0, 0.1),
    \db, 0,
    \legato, 1,
).play;
)
```

![type:audio](../media/audio/vocoder.ogg)

Det overlades til den nysgerrige læser at implementere en "keyboard og mikrofon"-udgave. Det kræver nogle få justeringer: Dels skal man anvende UGen'en `SoundIn` i stedet for `PlayBuf` som kilde A, dels skal man starte og slukke for enkelte `Synth`-instanser med `MIDIdef`. Der findes et udmærket eksempel herpå [i SuperColliders dokumentation](https://doc.sccode.org/Guides/UsingMIDI.html#Playing%20notes%20on%20your%20MIDI%20keyboard).
