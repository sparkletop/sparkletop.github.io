---
tags:
    - Artikler
---

# Hvordan får vi SuperCollider til at gøre noget?

Alt hvad man kan gøre i SuperCollider er knyttet til konkrete *methods*. Hvis vi forstår og kan anvende de forskellige methods, der findes, kan vi groft sagt bruge alle de redskaber, der findes i SuperCollider!

## Methods indeholder funktionalitet

Teknisk set er en method en *funktion*. Methods udfører bestemte handlinger, når de bliver aktiveret. I SuperCollider-kildekode ser man ofte methods noteret lige efter punktummer. Fx sådan her:

```sc title="Tre methods"
"Hello world".postln;  // method'en .postln viser objekter i post window, i dette tilfælde et stykke tekst
Scale.minorPentatonic; // method'en .minorPentatonic angiver (kombineret med Scale) en mol-pentaton skala
69.midicps;            // method'en .midicps omregner et tal fra MIDI-tonehøjde til frekvens, målt i Hertz
```

Methods kaldes undertiden også for "messages". Det skyldes, at methods anvendes på "noget", og dette noget kalder man så en "receiver". I udtrykket `69.midicps` er `69` receiveren, som modtager vores message `midicps`. 

## Methods hører til klasser og instanser

En klasse er blot en kategori af objekter. Klasser repræsenteres af ord, som er skrevet med stort begyndelsesbogstav, fx `Scale`, `Pbind` og `SinOsc`. 

### Class methods

Class methods er knyttet til, ja, klasser. En class method noterer man direkte efter klassenavnet, adskilt med et punktum. Det kan fx se sådan her ud:

``` sc title="Eksempler på class methods"
TempoClock.tempo;      // finder eller angiver tempo
Scale.directory;       // viser alle indbyggede skalaer
SinOsc.ar;             // angiver en sinus-oscillator
Pbind.new;             // opretter en ny Pbind (kan udgøre ramme for generativ komposition)
```

Der findes i SuperCollider en særlig class method, som vi bruger hele tiden: `.new`. Den har en særstatus, fordi den er så udbredt. `.new` skaber et nyt objekt (en "instance" eller forekomst) af den klasse, man angiver før punktummet.

``` sc title="Eksempler på .new"
Pbind.new()     // opretter en ny Pbind
SynthDef.new()  // opretter en ny SynthDef
Scale.new()     // opretter en ny skala
```

`.new` er så almindeligt, at der for rigtig mange klasser findes en genvej til at bruge method'en - nemlig helt at udelade `.new`. Derfor giver disse to udtryk samme resultat:

``` sc title="Eksplicit og implicit .new"
Pwhite.new(0, 10)   // .new fremgår eksplicit
Pwhite(0, 10)       // .new er underforstået
// Denne forekomst af Pwhite vil generere værdier mellem 0 og 10
```

### Instance methods

Instance methods bruger vi på "instances", dvs. konkrete forekomster af bestemte typer af objekter. Fx er `9` en forekomst af klassen `SimpleNumber`. `"kaffe"` er en forekomst af klassen `String`.

Instance methods noteres ligesom class methods med et punktum først, men de forekommer efter instances, ikke klassenavne. Her er nogle eksempler:

``` sc title="Eksempler på instance methods"
69.midicps             // vi beder om at regne MIDI-tonetallet 69 om til Hz (69 er en forekomst/instance af klassen SimpleNumber)
"kaffe".dup            // vi duplicerer teksten "kaffe" (en forekomst/instance af klassen String)
Pbind.new().play       // vi afspiller en ny Pind (en forekomst/instance af klassen Pbind)
```

Nogle methods kan styres med input i form af argumenter:

``` sc title="Styring af methods med argumenter"
SinOsc.ar(220)         // vi beder om en sinustone-oscillator, som svinger med 220 Hertz
SinOsc.ar.dup(10)      // vi beder om 10 ens sinustone-oscillatorer
Pwhite(0, 7)           // vi beder om et pattern, der kan generere tilfældige tal mellem 0 og 7
```

Mange methods kan bruges med forskellige slags objekter, fx .play (start lydserveren for at høre lydeksemplerne med `s.boot;`):

``` sc title="Forskellige resultater med .play"
Pbind().play;
{SinOsc.ar * 0.1}.play;
Routine({"hej ".post; 1.wait; "med dig".postln;}).play;

// ... men `.play` kan ikke anvendes på alle objekter!
10.play       // giver en fejlmeddelelse (.play findes ikke som instance method for SimpleNumber)
Pbind.play    // giver en fejlmeddelelse (.play findes kun som instance method, ikke som class method for Pbind)
```

## Dokumentation af methods

I SuperColliders dokumentation kan man se hvilke methods, der passer til forskellige klasser.

- Slår man en klasse op (fx `Array`, `Pwhite`, `SinOsc` etc.), vil man kunne se hvordan de forskellige class og instance methods fungerer og anvendes.
- Slår man en method op (fx `.new`, `.play`, `.reverse` etc.), vil man kunne se de forskellige klasser, som har denne method tilknyttet (klik på klassenavnet for at se hvordan dokumentationen for den pågældende method inden for den specifikke klasse).

Placér cursoren sammen med et af kodeudtrykkene herunder og tast Ctrl/Cmd-D for at åbne dokumentationen. Læs selv nærmere om de forskellige methods, og bemærk hvilke resultater, der dukker op.

``` sc title="Undersøg selv dokumentation for methods"
// Hvilke class og instance methods knytter sig til henholdsvis Array, Pwhite og SinOsc?
Array
Pwhite
SinOsc

// På hvilke slags objekter kan vi bruge disse methods?
.new
.play
.trace
.ar
.reverse
```
