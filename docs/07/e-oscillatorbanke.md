---
tags:
    - Øvelser
---

# Øvelse: Multikanalslyd og additiv syntese

I denne øvelse arbejdes der med multikanalslyd og additiv syntese. Det er i denne øvelse en fordel at [visualisere serverens lydlige output](../04/a-ugens.md#ugens-og-signalflow).

## Monofoni i to kanaler

Fremstil den samme sinustone i begge lydkanaler ved hjælp af `.dup`

```sc title="Monofoni i to kanaler" hl_lines="4"
(
{
    var sig = SinOsc.ar * 0.1;
    sig    ;
}.play;
)
```

## Stereofoni

Løs følgende opgaver ved hjælp af `Pan2`:

1. Fremstil en sinustone i venste side af stereofeltet
1. Fremstil en sinustone i højre side af stereofeltet
1. Fremstil en sinustone midt i stereofeltet
1. Fremstil en sinustone, der ved hjælp af modulation bevæger sig mellem højre og venstre side af stereofeltet

```sc title="Stereofoni med Pan2" hl_lines="4"
(
{
    var sig = SinOsc.ar * 0.1;
    Pan2.ar(sig,    );
}.play;
)
```

## Klangdannelse med additive elementer

Fremstil i nedenstående SynthDef en kompleks klang ved hjælp af additiv syntese med sinustoner (eksempler herpå kan findes i artiklen om [additiv syntese](a-additiv.md)). Klangen skal overholde følgende krav:

1. Klangen skal ud over grundtonen (`freq`) indeholde mindst tre forskellige overtoner (dvs. med et harmonisk forhold til `freq`)
1. Klangen skal derudover indeholde mindst to forskellige partialtoner (dvs. med et inharmonisk forhold til `freq`)
1. Hver tone har en unik amplitude, eventuelt tilfældigt genererede
1. Tonerne skal summeres før linjen, som starter med "env = ..."

```sc title="Additiv syntese" hl_lines="7-9"
(
SynthDef(\additivo, {
    arg freq = 440, pan = 0, amp = 0.1,
    attack = 0.01, release = 1, gate = 1;
    var env, sig;
    // udfyld herunder
    sig = 


    // udfyld ikke herunder
    env = EnvGen.kr(Env.asr(attack, 1, release), gate, doneAction: 2);
    sig = Pan2.ar(sig * env, pan, amp);
    Out.ar(0, sig);
}).add;
)
```

Afprøv din SynthDef med denne enkle komposition:

```sc title="Komposition til additiv SynthDef"
(
TempoClock.tempo = 125/60;
Pbind(
    \instrument, \additivo,
    \degree, Pshuf([0, 1, 3, 4], 4).repeat(4),
    \mtranspose, Pbrown(-2, 2, 1).stutter(16),
    \dur, Pseq([1/4, 1/8, 1/16, 1/16], inf) * 4,
    \attack, Pexprand(0.001, 0.02),
    \release, Pexprand(0.5, 1.5),
    \legato, Pgauss(1, 0.2),
).play;
)
```

### Bonusudfordring

Arbejd videre med SynthDef'en fra forrige opgave.

1. Tilføj et element af filtreret støj med egen amplitude-envelope, helt i begyndelsen af anslaget
1. Tilføj en sub-oktav, dvs. en tone, som klinger en oktav under freq
1. Gør mængden (lydstyrke) af anslagsstøj og sub-oktav justerbar ved at tilføje argumenter og varier disse ved at tilføje patterns og nøgler til Pbind-kompositionen
