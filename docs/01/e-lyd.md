---
tags:
    - Øvelser
---
# Øvelse: De første bip

Denne øvelse går ud på at producere lyde på SuperColliders lydserver og eksperimentere med at ændre på lyden ved at variere på parametrene. På dette trin er det ikke vigtigt, at du forstår, hvad alle kodelinjerne gør. Til gengæld er det en god idé at eksperimentere med kildekoden for at få en fornemmelse af, hvordan det fungerer. Hvis du får ændret på koden, så den ikke længere fungerer, kan du bare kopiere koden herunder igen og starte forfra.

Start først lydserveren med `s.boot;`

## En uendelig sekvens

1. Overvej hvad de enkelte kodelinjer gør ved lyden.
1. Eksekvér kodeblokken og lyt til resultatet. Tryk Ctrl/Cmd-Punktum for at stoppe igen.
1. Prøv at ændre på tallene eller vælge en anden skala, og kør blokken igen for at lytte til resultatet.

```sc title="Skalaudforskning"
Pbind(
    // prøv at vælge en anden skala, fx Scale.egyptian
    \scale, Scale.minor,

    // prøv at ændre på de forskellige tal herunder
    \degree, Pseq([0, 3, 2, 1, 4, 5, 6], inf),
    \root, 1,
    \octave, 4,
    \dur, 0.25,    // <-- denne værdi skal være større end 0
    \legato, 1.2,
).play;
```

Tip: Kør `Scale.directory;` for at få vist de forskellige indbyggede skalaer. Det er også muligt [at definere sine egne skalaer](https://doc.sccode.org/Classes/Scale.html#*new) eller bruge alternative [stemningssystemer](https://doc.sccode.org/Classes/Tuning.html).

## Selvkørende oscillatorer

1. Overvej hvad de enkelte kodelinjer gør ved lyden.
1. Eksekvér kodeblokken og lyt til resultatet. Tryk Ctrl/Cmd-Punktum for at stoppe igen.
1. Prøv at ændre på tallene på linje 5-13 og kør blokken igen for at lytte til resultatet.
1. Prøv at ændre `LFNoise0` på linje 9 til `LFNoise1`, `LFNoise2`, `LFSaw` eller `LFPulse`. Hvordan forandrer det lyden?

```sc title="Sjov med LFO'er"
({
    var sig, lfo, lfoFreq;

    // prøv at ændre på de forskellige tal herunder
    var freq = 330;
    var lfoFreqStart = 2;
    var lfoFreqEnd = 10;
    var duration = 7;
    lfoFreq = Line.kr(lfoFreqStart, lfoFreqEnd, duration, doneAction: Done.freeSelf);
    lfoFreq = lfoFreq.dup(2);
    lfo = LFNoise0.kr(lfoFreq);
    lfo = lfo.bipolar(24);
    lfo = lfo.round(4);

    // justér ikke herunder
    lfo = lfo.midiratio;
    sig = Pulse.ar(freq * lfo);
    sig = Splay.ar(sig);
    Limiter.ar(sig * 0.1);
}.play;)
```
