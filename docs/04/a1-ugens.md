---
tags:
    - Artikler
---

Dannelse og transformation af lyd er en central del af musik- og lydprogrammering. Redskaber som SuperCollider tillader os at arbejde meget fleksibelt med lyd på et detaljeret niveau. Dette kan give os unikke lyddesign til brug i musikalsk komposition, interaktive systemer, musikinstrumenter, lydkunst mm. Samtidig giver arbejdet med lyddesign på dette niveau en glimrende forståelse af principperne bag digital musik- og lydteknologi.

Når vi i det følgende tager hul på dannelse og transformation af lyd ved hjælp af oscillatorer, filtre, envelopes og så videre, arbejder vi med SuperColliders lydserver. Husk derfor at boote lydserveren med `s.boot;` inden du kører nedenstående eksempler. Det er også en god idé at starte et oscilloskop og en spektrumanalyse, så du kan se en grafisk repræsentation af SuperColliders lydlige output. Flyt evt. vinduerne på din skærm, så du kan se både bølgeform og frekvensspektrum på én gang.

```sc title="Start lydserver og visuelle redskaber"
s.boot;
// Når serveren er bootet
(
s.scope;
s.freqscope;
)
```

# UGens og signalflow

Det grundlæggende redskab for musikalsk lyddesign i SuperCollider og lignende platforme som puredata, Max/MSP, Csound m.fl. er såkaldte [UGens](https://en.wikipedia.org/wiki/Unit_generator), Unit Generators. UGens dækker over oscillatorer, filtre, analyseenheder, envelope-generatorer og ganske mange andre lydtekniske moduler. De kan sammenlignes med komponenterne i et elektronisk kredsløb eller modulerne i en modulær synthesizer. I kildekode kan vi kombinere UGens på mange forskellige måder med et fleksibelt signalflow og på den måde skabe unikke lyddesign.

### Fra patterns til UGens

Vi har hidtil primært arbejdet med SuperColliders patterns. Patterns kører i SuperColliders **fortolker** - det program, som fortolker den kildekode, vi eksekverer. `Pbind` har været den primære ramme om kompositionsarbejdet med patterns.

UGens kører i modsætning til patterns på SuperColliders **lydserver**, som er et andet program end fortolkeren. Det betyder, at syntaksen og logikken i UGens er en smule anderledes end den kode, vi hidtil har set. Rammen for vores arbejde med UGens er UGen-funktioner, som vi ofte noterer med `{}.play`:
 Kodelinjerne mellem disse tuborg-parenteser kører på SuperColliders lydserver, når de efterfølges af `.play`, dvs. `{}.play`.

```sc title="En ydmyg sinustone"
{ SinOsc.ar }.play;
```

Man kan ikke bruge patterns inde i UGen-funktioner. Men lidt senere i kurset kommer vi til at kombinere patterns og UGens ved at registrere vores UGen-funktioner som såkaldte `SynthDef`s. Så kan vi spille på UGen-funktioner ved hjælp af patterns.

Forholdet mellem patterns og UGens er nemlig lidt ligesom forholdet mellem en musiker (patterns) og et instrument (UGens); Man kan godt komponere med patterns uden at bruge UGens (fx ved at spille på et andet instrument via MIDI). Man kan også godt komponere udelukkende ved hjælp af UGens (ligesom en selvkørende, modulær synthesizer). Men den særlige fordel ved platforme som SuperCollider er kombinationen af de to niveauer: Når vi bruger det righoldige [pattern](../02/a1-patterns-intro.md)-bibliotek sammen med vores egne UGen-lyddesign får vi utroligt mange kompositionsmuligheder. Mere herom i [næste kapitel](../05/a2-synthdef.md).

## Første trin med `SinOsc`

Den mest enkle UGen er `SinOsc` - en ydmyg sinustone-oscillator. Vi afspiller den her ved audio rate (`.ar`):

```sc title="Sinusbølger - amplitude og frekvens"
{SinOsc.ar}.play;

// Vi kan angive oscillatorens frekvens med et argument lige efter .ar
{SinOsc.ar(220)}.play;

// Vi kan skrue ned for lydstyrken ved at gange med 0.1
{SinOsc.ar(220) * 0.1}.play;

// Vi kan plotte outputtet med .plot i stedet for .play
// Her frekvenser på 220Hz, 440Hz og 2000Hz
{SinOsc.ar([220, 440, 2000])}.plot;
```
![Sinusbølger ved 220Hz, 440Hz og 2kHz](../media/figures/tre_frekvenser.png){ width="70%" }

## Modulation

Sinostonen ovenfor bliver hurtigt lidt monoton, så lad os skabe lidt udvikling ved hjælp af modulation. Der findes grundlæggende to parametre, man kan manipulere ved en oscillator: *Tonehøjde* (frekvens) og *lydstyrke* (amplitude).

Der findes også en tredje parameter, nemlig fase, men den udelader vi her for enkelhedens skyld.

### Modulation af amplitude

Lad os først modulere sinustonens amplitude (lydstyrke). Det gør vi ganske enkelt ved *at gange med en anden UGen*. I dette eksempel bruger vi UGen'en `LFPulse`, som blot bevæger sig mellem 0 og 1 og dermed regelmæssigt tænder og slukker for lyden.

```sc title="Amplitudemodulation"
{SinOsc.ar(440) * LFPulse.kr(2) * 0.1}.play;
```

Dette ligger til grund for de klangdannelsesteknikker, som kaldes amplitude modulation (AM) og ring modulation (RM).

### Modulation af frekens

Vi kan også modulere frekvensen. Her erstatter vi den fast angivne frekvens på 440hz med en anden SinOsc. Det er her nødvendigt at skalere outputtet fra den anden SinOsc, så vi får hørbare frekvenser (over 20hz) - det gør vi med .range, her fra 200hz til 400hz.

```sc title="Frekvensmodulation"
{SinOsc.ar(SinOsc.kr(5).range(200, 400)) * 0.1}.play;
```

Dette ligger til grund for den klangdannelsesteknik som kaldes frequency modulation (FM).

## Signalflow med lokale variabler

Koden begynder nu at blive for kompliceret til at stå på én linje. For at gøre signalflowet mellem de forskellige UGens mere overskueligt og fleksibelt, kan vi derfor dele koden op, så den står på flere forskellige linjer. Dette indebærer, at vi indfører lokale variabler, så vi kan henvise til de forskellige signaler i vores UGen-funktion.

```sc title="Mere logisk og læsbar kildekode med lokale variabler"
(
{ // Samme lyd som ovenfor, men kildekoden er lettere at læse og justere
	var modulator = SinOsc.kr(5).range(200, 400);
	var sig = SinOsc.ar(modulator);
	sig * 0.1;
}.play;
)
```

Vi kan oprette lige så mange lokale variabler, som vi har lyst til, de skal blot erklæres i begyndelsen af funktionen. Her er et eksempel med LFO-modulation, hvor der er en del forskellige UGens på spil. Men koden bliver overskuelig, når vi bruger lokale variabler (gæt i øvrigt selv hvordan lyddesignet fungerer):

```sc title="Eksempel på signalflow med lokale variabler"
(
{
    var source = PinkNoise.ar;
    var lfo = LFSaw.kr(5);
    var env = EnvGen.ar(Env.triangle(5));
    var sig = LPF.ar(source, lfo.exprange(220, 880));
    sig = sig * env;
    sig * 0.1;
}.play;
)
```

