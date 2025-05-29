---
tags:
    - Artikler
---

# Additive orgelklange

Orgelet - elektrisk eller akustisk - er et glimrende eksempel på additiv klangdannelse. Orgelets klang bestemmes af registertræk, som er fysiske lister, man trækker ud eller skubber ind (på engelsk kaldet *drawbars*). Registertrækkene styrer mængden og karakteren af overtonerne, hvilket vi kan simulere med simpel addition af sinusbølger.

## Emulering af et elektrisk orgel

Herunder fremgår en meget simpel emulering af et elektrisk orgel, løseligt baseret på [data om Hammond's B3-orgel fra Electric Druid](https://electricdruid.net/technical-aspects-of-the-hammond-organ/). Bortset fra de 8 overtoner, hvis amplitude bestemmes af registerudtræk, er særligt Hammond-orgeler også kendt for den lyd, som frembringes af en tilknyttet Leslie-højttaler med roterende horn, der kan justeres i rotationshastighed. Den kan vi implementere med et lavpasfilter, hvor [cutoff-frekvensen moduleres af en LFO](../06/a-filter-ugens.md#cutoff-frekvens).

```sc title="SynthDef til simpel emulering af Hammond-orgel"
SynthDef(\organ, {
    arg freq = 440, amp = 0.1, pan = 0, gate = 1,
    rotationSpeed = 0, drawbars = #[0.2, 0.4, 1, 0.2, 0.1, 0.1, 0, 0];
    var sig, env;

    env = EnvGen.kr(Env.adsr(0.05, 0.1, 0.8, 0.05), gate, doneAction: Done.freeSelf);

    sig = SinOsc.ar(freq * [0.5, 1.498823530, 1, 2, 2.997647060, 4, 5.040941178, 5.995294120, 8]);

    sig = sig * drawbars.lag(0.1);

    sig = sig.sum * 0.5;

    // Roterende horn i Leslie-højttaler
    rotationSpeed = rotationSpeed.clip(0, 1).round * 7;
    sig = LPF.ar(sig, SinOsc.kr(rotationSpeed).range(1600, 2000));

    sig = sig * env;

    sig = Pan2.ar(sig, pan, amp);

    Out.ar(0, sig);
}).add;
```

Med SynthDef'en kan vi indstille orgelets registertræk og hornets rotationshastighed:

```sc title="Test lyden af Hammond-orgel-SynthDef'en"
x = Synth(\organ);

// Tilfældige drawbar-positioner
x.set(\drawbars, Array.rand(8, 0.0, 1.0).postln);

// Hurtig/langsom rotation 
x.set(\rotationSpeed, 1);
x.set(\rotationSpeed, 0);

x.set(\gate, 0);
```

![type:audio](../media/audio/07-hammond-variation.ogg)

For at demonstrere én af de klanglige muligheder ved denne orgel-SynthDef kan vi skrive en lille algoritmisk komposition til en (eventuelt lettere beruset) baseball-organist.

```sc title="Algoritmisk komposition for baseball-orgel"
Pbind(
    \instrument, \organ,
    \drawbars, [[0.5, 0.2, 1, 0.2, 0.6, 0.1, 0.2, 0.9]],
    \rotationSpeed, 1,
    \degree, Pseq([0, -3, -2, -1], 10),
    \ctranspose, Pseries(0, Prand([-2, 0, 1, 2], inf).asStream).stutter(4),
    \dur, Pgeom(0.5, 0.85).stutter(4),
    \legato, Pexprand(1.3, 1.7),
).play;
```

![type:audio](../media/audio/07-komposition-beruset-baseball-orgel.ogg)
