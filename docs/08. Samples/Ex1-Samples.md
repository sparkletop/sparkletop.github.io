---
tags:
    - Øvelser
---

# Øvelse 8: Samples

I denne øvelse arbejder du med sample-afspilning ved hjælp af `PlayBuf`.

## Opgave 0: Klargøring af sample

Til brug i denne øvelse skal der indlæses et sample. Du kan bruge din egen lydfil, den skal blot:

- Vare maksimalt 10 sekunder
- Være trimmet, så der ikke er stilhed i begyndelsen eller slutningen af samplet
- Indlæses i mono

Som forberedelse til de øvrige opgaver herunder:

1. Indlæs et sample i en buffer gemt under variablen `~buffer`
1. Hvis din lydfil er i stereo, kan du indlæse den første kanal med `.readChannel` - se kodeblokken herunder
1. Hvis du ikke har en lydfil klar selv, kan du bruge den nederste linje herunder i stedet med et indbygget sample fra SuperCollider

OBS: Til denne øvelse skal der anvendes et mono-sample.


```sc
// Udfyld her med dit eget sample
~buffer = Buffer.read(s,      );

// Brug .readChannel, hvis dit sample er i stereo
~buffer = Buffer.readChannel(s, channels: [0], path:   );

// Hvis du ikke har en lydfil klar, kan du bruge et indbygget sample i stedet:
~buffer = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");
```

## Opgave 1: Afspilning med PlayBuf

1. Afspil dit sample ved dobbelt hastighed
1. Afspil dit sample ved halv hastighed
1. Afspil den sidste halvdel af dit sample
1. Afspil dit sample baglæns (bemærk, kræver justering af enten `startPos` eller `loop` og `doneAction`)   

```sc hl_lines="6 8 9"
(
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
)
```

## Opgave 2: Afspilningshastighed

1. Modulér afspilningshastigheden ved at fjerne `//`'erne for en række forskellige LFO'er herunder.
1. Notér i kommentarer, hvilken effekt de forskellige modulatorer har på den æstetiske oplevelse.

```sc 
(
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
)
```

## Opgave 3: Lydcollage-komposition

Fremstil en abstrakt lydcollage med minimalistiske træk. Kompositionen skal baseres på ét sample og realiseres ved at bruge patterns sammen med nedenstående `SynthDef`.

1. Vælg og indlæs et sample, som...
    1. indeholder en vedvarende lyd (dvs. uden lange pauser i lyden)
    1. varer mellem 2 og 10 sekunder
    1. tonalt set er relativt enkel og stabil
    1. indeholder én monokanal (brug evt. `Buffer.readChannel` som ved opgave 1, hvis din ønskede fil er stereo-format)
1. Modificér `Pbind`'en herunder ved at erstatte faste værdier med patterns, således at vi hører en klangligt varieret lydcollage baseret på det valgte sample.

```sc title="SynthDef til sampleafspilning"
// Erstat stien med en sti til din egen lydfil
~vedvarendeLyd = Buffer.readChannel(s, "C:/lydfiler/minSejeLydfil.wav", [0]);

(
SynthDef(\sampleM, {
    arg amp = 0.1, out = 0, pan = 0,
    transpose = 0, startPos = 0, direction = 0,
    buffer, loop = 0, t_reset = 1,
    drive = 0, cutoff = 20000, rq = 0.1,
    atk = 0.005, sus = 1, rel = 0.2, gate = 1;

    var sig, env;

    env = EnvGen.kr(
        Env.asr(atk, sus, rel),
        gate,
        doneAction: Done.freeSelf
    );

    sig = PlayBuf.ar(
        numChannels: 1,
        bufnum: buffer,
        rate: transpose.midiratio * BufRateScale.kr(buffer) * direction.sign,
        trigger: t_reset,
        startPos: startPos.linlin(0, 1, 0, BufFrames.kr(buffer) - 2),
        loop: loop
    );

    sig = (sig * drive.linexp(0, 1, 1, 100)).tanh; // drive/distortion

    sig = RLPF.ar(sig, cutoff, rq);

    sig = sig * env;

    sig = Pan2.ar(sig, pan, amp);

    Out.ar(out, sig);
}).add;
)
```



```sc title="Samplecollage genereret med patterns" hl_lines="4 9-18"
(
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
)
```
