---
tags:
    - Eksempler
---

# Additiv orgellyd

Orgelet - elektrisk eller akustisk - er et glimrende eksempel på additiv klangdannelse. Her er en meget simpel simulering af et Hammond-orgel, løseligt baseret på [data fra Electric Druid](https://electricdruid.net/technical-aspects-of-the-hammond-organ/).

```sc
(
SynthDef(\organ, {
    arg freq = 440, amp = 0.1, pan = 0, gate = 1,
    rotationSpeed = 0, drawbars = #[0.2, 0.4, 1, 0.2, 0.1, 0.1, 0, 0];
    var sig, env;

    env = EnvGen.kr(Env.adsr(0.05, 0.1, 0.8, 0.2), gate, doneAction: Done.freeSelf);

    sig = SinOsc.ar(freq * [0.5, 1.498823530, 1, 2, 2.997647060, 4, 5.040941178, 5.995294120, 8]);

    sig = sig * drawbars;

    sig = sig.sum * 0.5;

    // Simulering af roterende horn i Leslie-højttaler
    rotationSpeed = rotationSpeed.clip(0, 1).round.linlin(0, 1, 1, 7);
    sig = LPF.ar(sig, SinOsc.kr(rotationSpeed).range(1600, 2000));

    sig = sig * env;

    sig = Pan2.ar(sig, pan, amp);

    Out.ar(0, sig);
}).add;
)

// Test lyden 
x = Synth(\organ);

// Tilfældige drawbar-positioner
x.set(\drawbars, Array.rand(8, 0.0, 1.0).postln);

// Hurtig/langsom rotation 
x.set(\rotationSpeed, 1);
x.set(\rotationSpeed, 0);

x.set(\gate, 0);

(
// En lille komposition for orgel
Pbind(
    \instrument, \organ,
    \drawbars, [[0.5, 0.2, 1, 0.2, 0.6, 0.1, 0.2, 0.9]],
    \rotationSpeed, 1,
    \degree, Pwalk((-7..14), Prand([-4, 1, 3], inf), 1, 7),
    \dur, 0.5,
    \legato, Pexprand(1.3, 1.9),
).play;
)
```

