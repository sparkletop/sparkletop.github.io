---
tags:
    - Artikler
---

# Simulering af strenge

En kerne af teknikker inden for subtraktiv syntese går ud på at sende en støjimpuls igennem en feedbackløkke med delay og filtrering. Dette simulerer på sin vis den fysiske filtrering af lydbølger, som dæmpes, når de bevæger sig igennem et materiale.

## Karplus-Strong

Et centralt eksempel er her den berømte Karplus-Strong-algoritme, som har til formål at generere en klang, der minder om lyden af en streng, der bliver slået an [@karplus1983]. Der findes i SuperCollider en særlig UGen, der implementerer Karplus-Strong kaldet `Pluck`, som vi kigger på om lidt. Men det kan være interessant at se, hvordan algoritmen fungerer, så et eksempel er inkluderet herunder. Hertil bruger vi et par UGens, som vi ikke har set hidtil, blandt andet `LocalIn` og `LocalOut`, som definerer feedbackløkken, og `DelayC`, som forsinker lydsignalet (med feedback). Decay-tiden og `OnePole`-filterets koefficient er afgørende for tonehøjde og klang.

```sc title="Manuel Karplus-Strong"
(
{
    var freq = 440, coef = 0.2;
    var sig = LocalIn.ar(1); // Feedback-løkke starter
    var noise = Impulse.ar(0); // Støjimpuls
    var sound = DelayC.ar(
        noise + (sig * 0.99), // 0.99 styrer decay-tiden
        20.reciprocal,
        freq.reciprocal - ControlRate.ir.reciprocal
    );
    // Filter
    sound = OnePole.ar(sound, coef);

    LocalOut.ar(sound); // Feedback-løkke slutter
    sig;
}.play
)
```

En tilsvarende lyd kan opnås mere effektivt med `Pluck`, som vi anvender herefter:

```sc title="Karplus-Strong med Pluck"
(
{
    var freq = 440, coef = 0.2;
    Pluck.ar(
        in: WhiteNoise.ar,
        trig: Impulse.ar(0),
        maxdelaytime: 0.1,
        delaytime: freq.reciprocal,
        decaytime: 0.99,
        coef: coef
    );
}.play;
)
```

![type:audio](eksempel.ogg)

## Inkorporering i SynthDef

Vi kan inkorporere ovenstående i en SynthDef med argumenter for frekvens, decay-tid og filter-koefficient. Herunder er der også inkluderet et argument til simulering af vibrato. Derudover anvendes UGen'en `DetectSilence` til at fjerne Synth'en fra lydserveren, når lyden har klinget ud (hvilket er nødvendigt, da vi ikke styrer lydstyrken med en envelope, som ellers ville kunne udføre denne funktion).

```sc title="Karplus-Strong SynthDef"
(
SynthDef(\karplus, {
    arg freq = 440, decay = 1, coef = 0.1,
    pan = 0, amp = 0.1, out = 0, vibrato = 0.05;

    var freqScale = SinOsc.ar(
        XLine.kr(7, 1, decay)
    ).bipolar(vibrato).midiratio;

    var sig = Pluck.ar(
        in: WhiteNoise.ar,
        trig: Impulse.kr(0),
        maxdelaytime: freq.reciprocal * vibrato.midiratio,
        delaytime: freq.reciprocal * freqScale,
        decaytime: decay,
        coef: coef
    );

    DetectSilence.ar(sig, doneAction: 2);
    sig = Pan2.ar(sig, pan, amp);
    Out.ar(out, sig);
}).add;
)
```

Med ovenstående SynthDef indlæst kan vi prøve klangmulighederne af:

```sc title="Klanglige variationsmuligheder"
Synth(\karplus, [\coef, 0.1, \decay, 1])
Synth(\karplus, [\coef, 0.4, \decay, 1])
Synth(\karplus, [\coef, 0.7, \decay, 1])
Synth(\karplus, [\freq, 110, \coef, 0.005, \decay, 10, \vibrato, 0.25])
```

![type:audio](../media/audio/karplus-variation.ogg)

## Kompositionseksempel

Vi kan selvfølgelig også skrive en lille komposition med patterns:

```sc title="Komposition med Karplus-Strong"
(
TempoClock.tempo = 110/60;

~komp = Pbind(
    \instrument, \karplus,
    
    // Streng-indstillinger
    \decay, Pgauss(5, 1).clip(0, 100),
    \coef, Pgauss(0.55, 0.05),
    \vibrato, Pexprand(0.1, 0.02),
    
    // Tonehøjde
    \degree, Pseries(
        start: 0,
        step: Pwhite(1, 4).asStream
        * Prand([-1, 1], inf).asStream,
        length: 4
    ).repeat,
    \mtranspose, Pwhite(-4, 4).stutter(3),
    \root, -3,
    \scale, Scale.minorPentatonic,
    
    // Rytmik
    \dur, Pseq([
        Prand([1/16, 1/32, 1/8, 3/16] * 4, Pwhite(3, 12).asStream),
        Prand([Rest(2.5), Rest(2), Rest(3)])
    ], inf),
    \lag, Pgauss(0, 0.003),
    
    // Panorering og lydstyrke
    \pan, Pbrown(-0.3, 0.3, 0.2),
    \db, Pgauss(-20, 1),
).play;
)
~komp.stop;
```

![type:audio](../media/audio/karplus-komp.ogg)
