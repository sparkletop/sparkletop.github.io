---
tags:
    - Artikler
---

# Enkle eksempler på subtraktiv klangdannelse

Subtraktiv klangdannelse er et omfattende emne. Udtrykket dækker ofte over forskellige teknikker, der anvendes til at emulere lyden af akustiske instrumenter. Dermed naturligvis ikke sagt, at resultatet altid klinger præcis som det akustiske forbillede; syntetiske blæser-, stryger- og trommelyde har fået deres egen genkendelige rolle inden for både den elektroniske musik og populærmusikken. Tænk blot på trommelydene fra en Roland TR-808, der indgår i utallige hiphop-tracks.

Nedenstående klarinet- og strygerlyde er løseligt baseret på Pejrolo og Metcalfes gennemgang af subtraktive klangdannelsesteknikker.

## Syntetisk klarinet

For at opnå en simpel, "klarinet"-lignende lyd, kan vi først og fremmest vælge en oscillator med en kvadratisk bølgeform (`Pulse`) som lydkilde. Dette skyldes, at den firkantede bølgeform udelukkende producerer "ulige" overtoner, dvs. den første, tredje, og femte overtone (og så fremdeles). Dette skaber en "hul" klang, som kan minde lidt om visse blæseinstrumenter. Vi kan blødgøre klangen ved at køre oscillatoren igennem et lavpas-filter med resonans, hvilket kan emulere den naturlige dæmpning af øvre frekvenser i et akustisk instrument [@pejrolo2017, p. 119].

Bemærk i kildekoden herunder, hvordan cutoff-frekvensen beregnes ud fra oscillatorens frekvens: Cutoff-frekvens beregnes til at ligge 18 halvtoner (dvs. cirka 1½ oktav) over oscillatorens frekvens. Genlæs eventuelt [afsnittet om skalering](../04/a-skalering.md), hvis du er i tvivl om, hvordan dette fungerer.

```sc title="SynthDef til syntetisk klarinet" hl_lines="7"
SynthDef(\clarinet, {
    arg freq = 440, gate = 1;

    // lydkilde: firkantet bølgeform med mulighed for glissando via .lag
    var oscillator = Pulse.ar(freq.lag(0.025));
    // resonant low pass-filter anvendes til klanglig justering
    var sig = RLPF.ar(oscillator, freq * 18.midiratio, 0.5);

    // lydstyrke styres med en envelope
    sig = sig * EnvGen.kr(Env.asr, gate, doneAction: Done.freeSelf) * 0.1;
    Out.ar(0, sig.dup);
}).add;
```

Hvis vi skal "spille på" denne SynthDef og ønsker at fastholde idéen om en klarinetlyd, er det værd at bemærke det måske indlysende faktum, at klarinetten er et *monofont* instrument. Det betyder, at der ikke kan være tidsligt overlappende toner som ved akkordinstrumenter som klaveret eller guitaren. Vi kan derfor oplagt bruge `Pmono` eller `PmonoArtic` til fx at spille et par skalaløb:

```sc title="Et par smidige skalaløb"
Pmono(\clarinet,
    \degree, Pseq([0, 1, 2, 3, 4, 5, 6, 7], 2),
    \octave, Pseq([4, 5], inf).stutter(2),
    \dur, 0.15,
).play;
```

![type:audio](../media/audio/06-clarinet.ogg)

## 1980'er-strings

Når man emulerer lyden af strygerinstrument, kan man bruge oscillatorer, der genererer savtakkede bølgeformer. Bortset fra den meget skarpe klang af savtakkede bølgeformer, som opstår på grund af høj intensitet i overtonespektret, giver de savtakkede bølgeformer en passende klang. Her kan vi også kombinere to oscillatorer, der er stemt meget tæt på hinanden, hvilket giver en slags chorus-effekt - som om der er to akustiske instrumenter, som spiller på samme tid og varierer i frekvens i meget små intervaller, som kendetegner akustiske instrumenter, sangstemmer osv. Til sammen kan dette skabe en klang, der minder om 1980'er-strings [@pejrolo2017, p. 120].

```sc title="SynthDef til firser-strings"
SynthDef(\stringz, {
    arg freq = 440, gate = 1;

    // lydkilde: to savtakkede bølgeformer, den ene med en smule detuning
    var oscillator = Saw.ar(freq) + Saw.ar(freq * 0.9971);

    // cutoff styres af oscillatorens frekvens samt af en envelope
    var cutoff = freq * EnvGen.kr(
        Env.adsr(0.2, 0.7),
        gate,
        levelBias: 1
    );
    var sig = RLPF.ar(oscillator, cutoff, 0.4);

    // lydstyrke styres med en separat ADSR-envelope
    sig = sig * EnvGen.kr(Env.adsr(0.2, 0.4), gate, doneAction: Done.freeSelf) * 0.1;
    Out.ar(0, sig.dup);
}).add;
```

For at få et indtryk af de fyldige lydmuligheder kan vi afspille et par akkorder med vores syntetiske strygerlyd:

```sc title="En akkordrække med firser-strings"
Pbind(
    \instrument, \stringz,
    \degree, [-7, 0, 2, 4, 6, 8],
    \mtranspose, Pseq([3, 1, 0]),
    \dur, 2,
).play;
```

![type:audio](../media/audio/06-strings.ogg)
