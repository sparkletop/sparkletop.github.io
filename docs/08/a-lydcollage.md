---
tags:
    - Artikler
---

# Lydcollage

En lydcollage bestående af samples, sammensat på kryds og tværs uden skelen til gængse konventioner for beatproduktion, er en interessant kompositionstilgang. Ved at fremstille en fleksibel SynthDef til sample-afspilning og anvende den til komposition med patterns, kan vi skabe lydcollager med forskellige sammensætninger af samples. Lad os udforske denne teknik herunder.

## SynthDef til sample-afspilning

Når vi skal skabe en lydcollage, er det nyttigt at indrette vores SynthDef, således at den passer til de teknikker, vi vil bruge i vores collage-komposition. Særligt drejer det sig om følgende egenskaber:

- Det er en central del af kompositionsteknikken at kunne styre, hvor mange samtidigt klingende samples, der afspilles. Med andre ord bør vi kunne styre, hvor meget *overlap*, der vil være, hvilket vi som tidligere nævnt kan gøre med [Pbind-nøglen](../02/a-pbind.md#varighed-frasering-og-timing) `\legato`. Det kræver imidlertid, at vi er nødt til at indrette vores SynthDef således, at afspilningen indhegnes af en [vedvarende envelope](../05/a-envelopes.md#vedvarende-envelopes-med-gate). Samplets varighed styres dermed af en envelope. Som udgangspunkt indstiller vi `PlayBuf` til at loope samplet, så det klinger i hele envelopens tidsrum.
- I stedet for at styre afspilningshastigheden direkte, er det mere relevant at kunne transponere et antal halvtoner op eller ned. Derfor bruger SynthDef'en `.midiratio` på argumentet `transpose` til dette formål, samt et argument `direction`, der styrer afspilningsretningen.
- Der er dog én ulempe ved at angive en transponeringsafstand frem for direkte at angive afspilningshastigheden er, at vi mister evnen til at afspille samplet *baglæns* (idet transponering blot går ud på at skalere afspilningshastigheden op eller ned). For at kunne afspille baglæns, opretter vi et argument `direction`, hvor vi i SynthDef'en ved hjælp af method'en `.sign` registrerer, om der er tale om et negativt eller et positivt tal. Negative tal fører til baglæns afspilning, positive tal giver forlæns afspilning, og tallets størrelse gør ingen forskel.
- For at kunne variere de valgte samples klangligt, anvender vi to teknikker:
    - Et lavpas-filter med resonans, som kan forme klangens af de valgte sample.
    - En simpel form for waveshaping[^1], der implementeres med `.htan` og kan styres med argumentet `drive`, for om ønskeligt at skabe en mere rå klang.

[^1]: [Waveshaping](https://en.wikipedia.org/wiki/Waveshaper) er en digital form for distortion. Kort fortalt fungerer den typisk ved at tilføje overtoner ved hjælp af en såkaldt transfer-funktion. Jo kraftigere et signal, der fødes ind i transfer-funktionen, desto mere udtalte bliver overtonerne/forvrængningen (frem for at overstyre eller "clippe"). Derfor skaleres drive-argumentet her til en faktor mellem 1 og 100.

Dertil kommer egenskaber som argumentet `startPos`, der angiver en position i bufferen (som tal fra 0 til 1), hvor læsningen af et sample skal starte. Samlet set bliver SynthDef'en indrettet således:

```sc title="SynthDef til sampleafspilning"
(
SynthDef(\sampleM, {
    arg amp = 0.1, out = 0, pan = 0,
    transpose = 0, startPos = 0, direction = 0,
    buf, loop = 1, t_reset = 1,
    drive = 0, cutoff = 20000, rq = 1,
    atk = 0.005, sus = 1, rel = 0.2, gate = 1;
    var env = EnvGen.kr(Env.asr(atk, sus, rel), gate, doneAction: 2);
    var sig = PlayBuf.ar(
        numChannels: 1,
        bufnum: buf,
        rate: transpose.midiratio * BufRateScale.kr(buf) * direction.sign,
        trigger: t_reset,
        startPos: startPos.linlin(0, 1, 0, BufFrames.kr(buf) - 2),
        loop: loop
    );
    sig = (sig * drive.linexp(0, 1, 1, 100)).tanh; // drive/distortion
    sig = RLPF.ar(sig, cutoff, rq) * env;
    sig = Pan2.ar(sig, pan, amp);
    Out.ar(out, sig);
}).add;
)
```

## Collage med patterns

Med ovenstående SynthDef indlæst, kan vi nu koncentrere os om at skabe en samplebaseret collage med patterns. Hertil skal vi naturligvis bruge ét eller flere samples. For enkelhedens skyld kan vi i dette tilfælde nøjes med ét sample. Det valgte sample her indeholder en stabil tonal sekvens, er kontinuerlig i sit relative lydniveau, og varer flere sekunder. Dette gør smplet relevant til æstetikken i en lydcollage, hvor vi kan lægge lag på lag.

![type:audio](../media/audio/guit_em9.ogg)

Med dette sample [indlæst i en buffer](a-samples.md#indlæsning-af-sample-i-buffer) under variabelnavnet `~guitar` kan vi med nøje udvalgte patterns og indstillinger fremstille en komposition, der udnytter SynthDef'en til at skabe en algoritmisk genereret lydcollage. Undersøg selv effekten af de forskellige patterns herunder - bemærk, at det samlede antal sampleafspilninger afhænger af den sekvensen, som defineres under `\drive`-nøglen.

```sc title="Lydcollage med patterns"
( TempoClock.tempo = 60/60;
Pbind(
    \instrument, \sampleM,

    // PlayBuf-indstillinger
    \buffer, ~guitar,
    \transpose, Prand([12, 7, 0, -12], inf).clump(3),
    \direction, -1,
    \startPos, Pbrown(0.0, 1.0, 0.2),
    \loop, 1,

    // Rytmik/timing
    \strum, 0.25,
    \dur, Pwhite(1.0, 3.0),
    \legato, Pexprand(2.5, 3.5),

    // Klang
    \cutoff, Pexprand(500, 3000),
    \drive, Pseq(Array.interpolation(10, 0.1, 0.8).mirror),

    // Panorering, envelope, amplitude
    \pan, Pgauss(0, 0.4),
    \atk, 2, \rel, 3,
    \db, -30,
).play;)
```

![type:audio](../media/audio/eksempel.ogg)
