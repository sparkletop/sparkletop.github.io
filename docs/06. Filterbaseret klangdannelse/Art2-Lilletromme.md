---
tags:
    - Eksempler
---

# Lilletromme

Denne lilletrommelyd er inspireret af [*Sound on Sound*-artikler af Gordon Reid om syntetisk skabelse af percussion-lyde](https://www.soundonsound.com/techniques/practical-snare-drum-synthesis). Lyddesignet forsøger at simulere forskellige klangelementer i en "realistisk" lilletrommelyd.

SynthDef'en illustrerer hvordan man bruger forskellige [filtre](Cheat1-Filter-UGens.md) sammen med [envelopes](../05. Envelope som kreativt virkemiddel/Art1-Envelopes.md) til at modulere klangens forandring over tid.

```sc title="En SynthDef til syntetisk emuleret lilletrommelyd"
(
SynthDef(\snare,{
  arg pan = 0, amp = 0.1, out = 0,

  // Forskellige komponenter, angives i dB
  body = 0, harmonics = 0, click = 0,
  highNoise = 0, lowNoise = 0;

  var sig = [
    // Primært resonansrum
    SinOsc.ar([180, 330]).sum
    * EnvGen.ar(
      Env.perc(0.03, 0.2, (body - 3).dbamp)
    ),

    // Overtoner
    LFTri.ar(
      [286, 335] * EnvGen.ar(
        Env.new(
          [1, 1.5, 1],
          [0.01, 0.09],
          \sine
        )
      )
    ).sum * EnvGen.ar(
      Env.perc(0.01, Rand(0.09, 0.11), (harmonics + 2).dbamp)
    ),

    // Klik i begyndelsen af lyden
    LPF.ar(
      HPF.ar(WhiteNoise.ar, 300),
      8000
    ) * EnvGen.ar(
      Env.linen(0.001, 0.01, 0.001, * click.dbamp)
    ),

    // High noise (seiding)
    HPF.ar(
      BPeakEQ.ar(WhiteNoise.ar, 4000, 0.5, 3),
      300
    ) * EnvGen.ar(
      Env.perc(0.05, Rand(0.16, 0.19), (highNoise - 8).dbamp).delay(0.01),
      doneAction: Done.freeSelf
    ),

    // Low noise
    LPF.ar(
      HPF.ar(WhiteNoise.ar, 230),
      500
    ) * EnvGen.ar(
      Env.perc(0.1, Rand(0.09, 0.11))
    ) * (lowNoise-5).dbamp
  ].sum;

  // Distortion/compression
  sig = (sig * 1.5).tanh;

  Out.ar(out, Pan2.ar(sig, pan, amp));
}).add;
)
```

Vi kan med denne SynthDef fremhæve eller nedtone forskellige elementer i lyden. Vi kan fx skrue kraftigt ned for støjen for at simulere, at vi har slået den såkaldte "seiding" (metalbånd på undersiden af trommen) fra.

```sc title="To forskellige lilletrommelyde"
// Standardindstillinger
Synth(\snare);

(
// Mindre seiding/støj
Synth(\snare, [
  \body, 3,
  \harmonics, -2,
  \click, -15,
  \highNoise, -40,
  \lowNoise, -40,
]);
)
```

Lydeksempel: Standardindstillinger vs. lilletromme med seidingen slået fra
![type:audio](../media/audio/snare.ogg)
