---
tags:
    - Artikler
---
# Synth og SynthDef

Hidtil har vores lyddesign været enkle og midlertidige - med `{}.play` kan vi hurtigt teste UGens og idéer. Men vi kan gøre vores lyddesign meget mere fleksibelt og anvendeligt til længere kompositionsforløb ved at samle vores UGens i en såkaldt `SynthDef`.

## Hvad er en `Synth`?

Bemærk først, hvad der bliver vist i SuperColliders post window, når vi kører nedenstående linje: 
```sc
{SinOsc.ar * 0.1}.play;
```

Vi får at vide, at vi har startet en såkaldt `Synth`. Hver gang vi producerer lyd på lydserveren, har vi gang i en eller flere Synths. Når vi fx afspiller toner med en `Pbind`, genererer vi en ny Synth for hver tone, der spiller. Kør fx nedenstående blok og se listen over Synths i plotTree-vinduet:  

```sc
(
s.plotTree;
Pbind(
	\degree, Pwhite(0, 4),
	\legato, Pwhite(2.0, 4.0)
).play;
)
```

Vi kan starte Synths direkte ved at bruge `Synth.new`:
```sc
Synth.new(\default);
Synth(\default);   // samme resultat, .new er implicit
```

Men hvad er mon `\default`? Jo, det er navnet på en bestemt `SynthDef`. 

## Hvad er en `SynthDef`?

Ordet SynthDef står, ikke overraskende, for **Synth-definition**. Med SynthDefs kan vi lave lyddesign-opskrifter og generere Synths på meget fleksibel vis.

En SynthDef adskiller sig fra de mere primitive `{}.play` på følgende måder:

- En ny SynthDef (`SynthDef.new`) skal registreres på lydserveren med `.add;`
- En SynthDef skal have et navn, så vi kan henvise til den senere, fx `\minSynthDef`
- Vores UGen-funktion angives lige efter navnet, som argument nr. 2 til `SynthDef.new()`
- For at høre lyd-outputtet skal vi inde i UGen-funktionen route det ønskede signal ud med den særlige UGen `Out`

Det kan eksempelvis se således ud:

```sc
(
// Vi skriver først SynthDef'en og registrerer den på lydserveren
SynthDef(\minSynthDef, {
	Out.ar(0, SinOsc.ar(440) * 0.1);
}).add;
)

// Start en Synth baseret på SynthDef'en
Synth(\minSynthDef);
```

## Interfacet mellem Synth, SynthDef og Pbind

Sammenhængen mellem `Synth`, `SynthDef` og `Pbind` er helt central i SuperCollider.

- `SynthDef` kan forstås som et instrument, der bestemmer klang og variationsmuligheder.
- `Synth`s kan forstås som de konkrete lyde, man skaber med instrumentet.
- `Pbind` udgør således kompositionen eller partituret.

Hvis man i denne analogi synes, at der mangler en musiker til at udføre kompositionen, kan man tænke på den `EventStreamPlayer`, som opstår, når vi bruger `Pbind().play` - det er dette objekt, som faktisk udfører partituret og starter/stopper Synths på lydserveren ud fra de instrukser, vi har angivet med `Pbind`.

### SynthDef og Synth

Lad os se på hvordan samspillet mellem `Synth`, `SynthDef` og `Pbind` fungerer i praksis.

SynthDef'en `\minSynthDef` ovenfor fungerer, men er ikke særligt fleksibel. Vi kan fx kun spille én tone med den, og vi er nødt til at stoppe den manuelt med Ctrl-/Cmd-punktum. For at kunne spille forskellige toner kan vi indføre et argument. Her vælger jeg at indføre argumentet `freq` ved hjælp af nøgleordet `arg`, og jeg angiver også en standardværdi på `440`:

```sc title="SynthDef og Synth"
(
SynthDef(\tone, {
	arg freq = 440;  // <--- her erklærer vi argumentet og angiver standardværdien
	Out.ar(0, SinOsc.ar(freq) * 0.1); // <--- her bruger vi argumentet, ligesom en variabel
}).add;
)

Synth(\tone);
Synth(\tone, [\freq, 220]);
Synth(\tone, [\freq, 1000]);

// Vi kan også justere frekvensen efterfølgende ved at gemme Synth'en under en variabel og bruge .set
~tone = Synth(\tone, [\freq, 330]);
~tone.set(\freq, 220);
~tone.set(\freq, rrand(100, 800));
```

I mange SynthDefs er det nyttigt at bruge en [envelope](a-envelopes.md) til at styre volumen over tid. Med `doneAction` angiver vi, at Synth'en skal fjernes, når tonen er klinget ud (læs evt. nærmere om [automatisk oprydning med doneAction](a-envelopes.md#automatisk-oprydning-med-doneaction)).

### SynthDef og Pbind

Når vores SynthDef er sat op på denne måde, kan vi bruge `Pbind` til at generere sekvenser af Synths, helt automatisk. Vi fortæller Pbind, hvilken SynthDef, der skal anvendes, ved at bruge nøglen `\instrument`. Det betyder, at `Pbind(\instrument, \cool)` vil starte Synths baseret på en SynthDef med navnet `\cool`. Hvis ikke en sådan SynthDef er registreret på lydserveren, vil vi modtage en fejlmeddelelse.

```sc title="SynthDef og Pbind"
(
SynthDef(\simpel, {
	arg freq = 440;
	Out.ar(0, SinOsc.ar(freq) * 0.1
		* EnvGen.kr(Env.perc, doneAction: Done.freeSelf)
	);
}).add;
)

// Nu kan vi bruge Pbind til at "spille på" vores SynthDef, som om den er et instrument:
(
Pbind(
	// SynthDef-navnet angives under nøglen \instrument
	\instrument, \simpel,
	\degree, Pwhite(-7, 7),
).play;
)
```

SynthDefs bliver i øvrigt meget lettere at læse, hvis vi bruger [lokale variabler](../01/a-variabler.md#lokale-variabler). Koden herunder fungerer præcis som ovenfor, men er markant mere læsbar, da vi kan følge signalflowet gennem de lokale variabler (hvis ellers variabelnavnene er tilstrækkeligt deskriptive):

```sc title="Signalflow i SynthDef med lokale variabler"
(
SynthDef(\simpel, {
	arg freq = 440;
	// 'sig' er variabelnavnet for vores hovedsignal
	var sig = SinOsc.ar(freq);
	// 'env' er variabelnavnet for vores envelope
	var env = EnvGen.kr(Env.perc, doneAction: Done.freeSelf);
	sig = sig * env * 0.1;
	Out.ar(0, sig);
}).add;
)
```

Med et par ekstra argumenter og en `Pan2`-UGen kan vi styre volumen og stereo-panorering. De argumenter, vi angiver i begyndelsen af en SynthDef, kan vi nemlig anvende som nøgler i `Pbind`. Dette interface mellem `SynthDef`/`Synth` og `Pbind`, danner grundlag for de utroligt righoldige, generative muligheder i SuperCollider.

```sc title="Komposition og lyddesign med variabel tonehøjde, panorering og volumen" hl_lines="3 7"
(
SynthDef(\fleksibel, {
	arg freq = 440, pan = 0, amp = 0.1;
	var sig = SinOsc.ar(freq);
	var env = EnvGen.kr(Env.perc, doneAction: Done.freeSelf);
	sig = sig * env;
    sig = Pan2.ar(sig, pan, amp);
	Out.ar(0, sig);
}).add;
)

(
Pbind(
	\instrument, \fleksibel,
	\degree, Pwhite(-7, 7).stutter(2),
	\pan, Prand([1, 0, -1], inf),
	\amp, Pexprand(0.01, 0.2),
	\dur, 0.4,
).play;
)
```

## Legato og staccato med vedvarende envelopes

`Pbind` kan også afslutte vedvarende envelopes for os, og vi kan dermed få adgang til at komponere med legato- og staccatofrasering. Det kræver dog, at SynthDef'en indrettes på følgende måde:

- Vi indfører et argument kaldet `gate` med standardværdi 1
- Vi bruger en vedvarende envelope, fx `Env.asr`
- Vi angiver `gate` som argument nr. 2 til `EnvGen.kr`

```sc title="Legato og staccato med vedvarende envelopes" hl_lines="3 5 16 24"
(
SynthDef(\vedvarende, {
	arg freq = 440, pan = 0, amp = 0.1, gate = 1;
	var sig = SinOsc.ar(freq);
	var env = EnvGen.kr(Env.asr, gate, doneAction: Done.freeSelf);
	sig = sig * env;
    sig = Pan2.ar(sig, pan, amp);
	Out.ar(0, sig);
}).add;
)
```

```
( // Legato-frasering
Pbind(
	\instrument, \vedvarende,
	\degree, Pwhite(-7, 7),
    \sustain, 3,
).play;
)

( // Staccato-frasering
Pbind(
	\instrument, \vedvarende,
	\degree, Pwhite(-7, 7),
    \sustain, 0.1,
).play;
)
```

### Vedvarende `Synth` med `Pmono` og `PmonoArtic`

Som vi har set, er Pbind god til sekvenser, der starter mange Synths. Men til gengæld kan Pbind ikke ændre på indstillingerne for Synths, fx tonehøjde eller panorering, når de er startet. Det kan vi gøre manuelt ved hjælp af `.set`-metoden:

```sc title="Synth og method'en .set"
~tone = Synth(\default);

~tone.set(\freq, 1000);
~tone.set(\freq, 500);
```

Hvis vi vil gøre noget lignende med patterns, kan vi i stedet for Pbind bruge `Pmono` eller `PmonoArtic`. Begge disse kusiner til Pbind starter blot én Synth ad gangen og justerer efterfølgende parametrene ved hjælp af de sædvanlige koblinger af nøgler og patterns, som vi kender fra Pbind. SynthDef-navnet angives som første argument, uden `\instrument`-nøglen (herunder genbruger vi en let justeret SynthDef fra eksemplet ovenfor):

```sc hl_lines="4 14" title="Glidende arpeggio med Pmono"
(
SynthDef(\glissando, {
	arg freq = 440, pan = 0, amp = 0.1, gate = 1;
	// .lag giver en glidende overgang mellem skiftende værdier (her glissando)
	var sig = SinOsc.ar(freq.lag(0.01));
	var env = EnvGen.kr(Env.asr, gate, doneAction: Done.freeSelf);
	sig = sig * env;
    sig = Pan2.ar(sig, pan, amp);
	Out.ar(0, sig);
}).add;
)

(
s.plotTree;  // vis Synths på serveren - Pmono starter kun én Synth
Pmono(\glissando,
    \degree, Pseq([0, 2, 4, 6], inf),
    \mtranspose, Pwhite(0, 7).stutter(4),
    \dur, 0.15,
).play;
)
```

Hvis vi har brug for at lave pauser mellem de strømme af værdier, der bliver skiftet imellem ved hjælp af `Pmono`, kan vi bruge `PmonoArtic`.

På patterns-iden styres artikulationen med `\sustain`- eller `\legato`-nøglen; når `\sustain` er mindre end `\dur`, afsluttes Synthen, og der startes en ny ved næste event. Den mest praktiske tilgang er at bruge nøglen `legato`, hvor vi angiver en værdi, som er mindre end 1, når vi ønsker at lave ophold, og en værdi der er højere end eller lig med 1, når vi ønsker en sammenhængende tone.

```sc title="Glidende arpeggio med luft mellem fraserne - med PmonoArtic" hl_lines="2 7"
(
PmonoArtic(\glissando,
    \degree, Pseq([0, 2, 4, 6], inf),
    \mtranspose, Pwhite(0, 7).stutter(4),
    \dur, 0.4,
    \legato, Pseq([1, 1, 1, 0.1], inf),
).play;
)
```

## Argumentnavne i SynthDef

Argumenterne i vores SynthDefs kan i princippet have de navne vi gerne vil give dem (dog skal de starte med små bogstaver, ligesom variabler). Argumentnavne kunne fx være `kaffe`, `the`, `mario`, `luke` eller `leia`. Men sædvanligvis kan det være en god idé at give argumenterne nogle deskriptive navne som fx `cutoffFreq`, `release`, `drive`, `delayTime` eller lignende, så man kan regne ud hvad de betyder, når man vender tilbage til koden efter noget tid.

Men vedrørende SynthDef-argumentnavne findes der nogle få undtagelser som er værd at kende, og de gennemgås herunder. Der er tale om konventioner, som gør vores SynthDefs fleksible i sammenspil med andre dele af SuperCollider. Herunder gives et par anbefalinger for argument-navngivning:

### Vigtige argumentnavne

Disse argumentnavne er nødvendige for at fungere med centrale dele af SuperCollider såsam patterns, events, live coding-klasser mm.:

`freq`

:   Anvendes til at angive tonefrekvens i SynthDefs, hvor det giver mening at forstå frekvensen som en tonehøjde, fx et højt c eller et lavt gis. Dette giver os mulighed for at bruge nøgler som `\degree`, `\midinote`, `\octave`, `\scale` osv. og automatisk få disse informationer omregnet til oscillatorfrekvens, når vi arbejder med `Pbind`.
    Standardværdi er ofte 440 (kammertonen).

`gate`

:   Anvendes typisk til at afslutte vedvarende envelopes og arbejde med legato og staccato-frasering, som vist ovenfor.
    Standardværdien er typisk 1.

`amp`

:   Bruges til at angive lydstyrke. Giver mulighed for at omregne automatisk fra `\db`, når vi arbejder med `Pbind`.
    Standardværdien er ofte 0.1, som svarer til -20Db.

`out`

:   Anvendes til at route et signal fra en Synth til en bestemt `Bus` - særligt relevant, hvis man skal arbejde med livecoding og [JITLib](http://doc.sccode.org/Overviews/JITLib.html).
    Standardværdien er ofte 0, den første hardware-outputkanal.

### Anbefalede argumentnavne

Disse argumentnavne er ikke så vidt vides strengt nødvendige. Men der er tale om meget udbredte konventioner, som gør kildekoden sammenlignelig og kompatibel med andres kildekode.

`pan`

:   Bruges til at angive panorering, ofte i et stereofelt mellem -1 og 1. Standardværdien er ofte 0, i midten af et stereofelt.

`buf`

:   Anvendes til at angive en `Buffer` på lydserveren. Dette er fx relevant, når [der arbejdes med samples](../08/a-samples.md), wavetables og lignende.

### Argumentnavne, som i mange tilfælde bør undgås

`dur`, `scale`, `sustain`, `stretch`, `midinote` med flere

:   Disse navne bruges til automatiske omregninger, når vi komponerer med `Pbind` (qua SuperColliders såkaldte **default Event**). Hvis man bruger dem som SynthDef-argumentnavne uden at være klar over dette, kan der hurtigt opstå mærkelige konsekvenser, som kan være svære at gennemskue.
    
    Man kan se den samlede liste over termer, der bruges til automatisk udredning af tonehøjde, timing og amplitude i [James Harkins' udmærkede oversigt](http://doc.sccode.org/Tutorials/A-Practical-Guide/PG_07_Value_Conversions.html).

    Tommelfingerregelen er at lade pattern/event-systemet foretage de automatiske udregninger:
    
    - Brug `freq`, `amp` og `gate` til SynthDef-argumentnavne som anbefalet ovenfor.
    - Brug `\scale`, `\degree`, `\mtranspose`, `\sustain`, `\legato`, `\db` osv. i forbindelse med patterns og events, og ikke direkte som argumentnavne i SynthDefs.
