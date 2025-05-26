---
tags:
    - Artikler
---

# Syntetisk lilletromme

Her udvikler vi en lilletrommelyd, som er inspireret af Gordon Reids [artikel](https://www.soundonsound.com/techniques/practical-snare-drum-synthesis) fra magasinet *Sound on Sound*[@reid2002] om syntetisk dannelse af lilletrommelyd. Lad os med lydproduktionen her simulere forskellige klangelementer i en "realistisk" lilletrommelyd, fra trommens "krop" og resonans til seiding og anden støj. Strategien går ud på at bruge støj og simple oscillatorer moduleret af envelopes, sendt gennem forskellige [filtre](c-filtre.md), der også moduleres af [envelopes](../05/a-envelopes.md). Dette skal samlet set simulere lilletrommelydens klanglige forandring over (kort) tid - hvad Denis Smalley har kaldt lydens *spektromorfologi* [@smalley1997].

## Elementerne i en lilletrommelyd

Resonansrummet inde i en lilletromme kan vi simulere med to sinustoner ved hhv. 180 Hz og 330 Hz, der klinger ud efter godt 200 millisekunder.

```sc title="Primært resonansrum"
(
{
    SinOsc.ar([180, 330]).sum
    * EnvGen.ar(Env.perc(0.03, 0.2))
}.play;
)
```

Der vil typisk også være en række overtoner, hvis frekvens bevæger sig op og ned over de første 10 millisekunder. Disse simuleres herunder af et par `LFTri`-UGens, hvor både amplitude og frekvens moduleres af envelopes. Når man spiller på en fysisk tromme, vil der altid være en smule variation i klangen, og dette simuleres blandt andet ved, at varigheden af overtonernes volumen-envelope gøre tilfældig (100-120ms).

```sc title="Overtoner"
(
{
    LFTri.ar(
      [286, 335] *
      EnvGen.ar(Env.new([1, 1.5, 1], [0.01, 0.09], \sine))
    ).sum * EnvGen.ar(
      Env.perc(0.01, Rand(0.09, 0.11))
    ),
}.play;
)
```

Når en trommestik rammer trommeskindet, genereres en støjimpuls, som både sætter hele trommen i svingninger og genererer en kort, støjende lyd, som ofte omtales som et "klik".

```sc title="Klik"
(
{
    LPF.ar(
      HPF.ar(WhiteNoise.ar, 300),
      8000
    ) * EnvGen.ar(
      Env.linen(0.001, 0.01, 0.001)
    )
}.play;
)
```

Derudover er der på undersiden af lilletrommen monteret en såkaldt "seiding" - et metalbånd med små tråde, som vibrerer og skaber en karakteristisk raslende lyd, som er essentiel i lilletrommens klang. Her filtrerer vi den spektralt righoldige hvide støj, og volumen-envelopen er den længste, som derfor styrer, hvornår Synth'en fjernes fra lydserveren igen. Dette simulerer, at lyden fra seidingen er den sidste, der klinger ud i det korte forløb, en lilletrommelyd er.

```sc title="Lilletrommens seiding"
(
{
HPF.ar(
    BPeakEQ.ar(WhiteNoise.ar, 4000, 0.5, 3),
    300
    ) * EnvGen.ar(
      Env.perc(0.05, Rand(0.16, 0.19)).delay(0.01),
      doneAction: Done.freeSelf
    )
}.play;
)
```

Trommen kan også have en dybere støjlyd, som simuleres på en lignende måde, blot med dybere cutoff-frekvenser.

```sc title="Dyb støj"
(
{
    LPF.ar(
      HPF.ar(WhiteNoise.ar, 230),
      500
    ) * EnvGen.ar(
      Env.perc(0.1, Rand(0.09, 0.11))
    )
}.play;
)
```

## En lilletromme-SynthDef

Herunder sættes de ovenfor omtalte komponenter sammen i en liste, som summeres til sidst. Vi indfører desuden nogle argumenter, så vi kan styre lydstyrken for de enkelte komponenter og på den måde fintune vores lilletromme. Hertil anvendes method'en `.dbamp`, som omregner fra dB-skalaen til en skaleringsfaktor, vi kan bruge til at styre lydstyrke. For at have en balance i lydniveauerne mellem de enkelte lydkilder indeholder SynthDef'en nogle forudprogrammerede lydniveauer, som sammen med argumenterne styrer lydstyrkerne. Sidst men ikke mindst foretages der lidt distortion/komprimering med `.tanh`, som er en form for *waveshaping*[^1].
[^1]: Waveshaping er en digital form for klanglig manipulation med distortion, som det vil føre for vidt at introducere her. Se evt. Curtis Roads' udmærkede introduktion til emnet [-@roads2023, p. 273].

```sc title="En SynthDef til syntetisk emuleret lilletrommelyd"
SynthDef(\snare,{
    arg pan = 0, amp = 0.1, out = 0,
    body = 0, harmonics = 0, click = 0,
    highNoise = 0, lowNoise = 0;

    var sig = [
        // Resonansrum
        SinOsc.ar([180, 330]).sum
        * EnvGen.ar( Env.perc(0.03, 0.2))
        * (body - 3).dbamp,

        // Overtoner
        LFTri.ar([286, 335] *
          EnvGen.ar(Env.new([1, 1.5, 1], [0.01, 0.09], \sine))
        ).sum * EnvGen.ar(Env.perc(0.01, Rand(0.09, 0.11)))
         * (harmonics + 2).dbamp,

        // Klik
        LPF.ar(HPF.ar(WhiteNoise.ar, 300), 8000)
        * EnvGen.ar(Env.linen(0.001, 0.01, 0.001))
        * click.dbamp,

        // Seiding
        HPF.ar(BPeakEQ.ar(WhiteNoise.ar, 4000, 0.5, 3),300)
        * EnvGen.ar(
          Env.perc(0.05, Rand(0.16, 0.19)).delay(0.01),
          doneAction: Done.freeSelf)
        * (highNoise - 8).dbamp,

        // Dyb støj
        LPF.ar(HPF.ar(WhiteNoise.ar, 230),500)
        * EnvGen.ar(Env.perc(0.1, Rand(0.09, 0.11)))
        * (lowNoise-5).dbamp
      ].sum;

    sig = (sig * 1.5).tanh;  // Distortion/komprimering
  Out.ar(out, Pan2.ar(sig, pan, amp));
}).add;
```

Med denne SynthDef kan vi producere forskelligt klingende lyde, blandt andet en version, hvor seidingen er slået fra.

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

![type:audio](../media/audio/snare.ogg)
