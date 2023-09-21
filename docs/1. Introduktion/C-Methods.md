---
tags:
    - Artikler
---
# Hvad er "methods"?

Start lydserveren for at høre lydeksemplerne herunder
`s.boot;`

Alt hvad man kan gøre i SuperCollider, altså SuperColliders funktionalitet, er knyttet til "methods". I kode kan man typisk se disse methods lige efter punktummer. Fx sådan her:

``` sc
"Hello world".postln;  // method'en .postln viser objekter i post window, i dette tilfælde et stykke tekst
Scale.minorPentatonic; // .minorPentatonic angiver (kombineret med Scale) en mol-pentaton skala
69.midicps;            // method'en .midicps omregner fra MIDI-tonehøjde til frekvens, målt i Hertz
```

Methods kaldes undertiden også for "messages". Det skyldes, at methods anvendes på "noget", og dette noget kalder man så en "receiver". I udtrykket `69.midicps` er `69` receiveren, som modtager vores message `midicps`. 

## To slags methods

### Class methods 

Class methods er knyttet til det, der kaldes klasser. En klasse er blot en kategori af objekter. Klasser repræsenteres af ord, som er skrevet med stort begyndelsesbogstav, fx `Scale`, `Pbind` og `Pulse`.

Class methods noteres direkte efter klassenavnet, kun adskilt med et punktum. Det kan fx se sådan her ud:

``` sc
Pbind.new;             // opretter en ny Pbind
TempoClock.tempo;      // finder eller angiver tempo
SinOsc.ar;             // opretter en audio-rate sinus-oscillator
SinOsc.kr;             // opretter en control-rate sinus-oscillator
Scale.directory;       // viser alle indbyggede skalaer
```

#### Den (lidt) hemmelige method .new

Der findes i SuperCollider en særlig class method, som vi bruger hele tiden: `.new`. Den har en slags særstatus, fordi den er så udbredt.

`.new` skaber et nyt objekt (en "instance" eller forekomst) af den klasse, man angiver før punktummet.

`.new` er så almindeligt, at der for rigtig mange klasser findes en genvej til at bruge method'en - nemlig helt at udelade `.new`. Derfor giver disse to udtryk samme resultat:

``` sc
Pwhite.new(0, 10, 5)   // .new fremgår eksplicit
Pwhite(0, 10, 5)       // .new er underforstået
```

### Instance methods

Instance methods bruger vi på "instances", dvs. konkrete forekomster af bestemte typer af objekter. Fx er `9` en forekomst af klassen `SimpleNumber`, og `"kaffe"` er en forekomst af klassen `String`.

Instance methods noteres ligesom class methods med et punktum først, men de forekommer lige efter instances, ikke klassenavne. Her er nogle eksempler:

``` sc
69.midicps             // vi beder om at regne MIDI-tonetallet 69 om til Hz (69 er en forekomst/instance af klassen SimpleNumber)
"kaffe".dup            // vi duplicerer teksten "kaffe" (en forekomst/instance af klassen String)
Pbind.new().play       // vi afspiller en ny Pind (en forekomst/instance af klassen Pbind)
```

Nogle methods kan styres med input i form af argumenter:

``` sc
SinOsc.ar(220)         // vi beder om en sinustone-oscillator, som svinger med 220 Hertz
SinOsc.ar.dup(10)      // vi beder om 10 ens sinustone-oscillatorer
Pwhite(0, 7)           // vi beder om et pattern, der kan generere tilfældige tal mellem 0 og 7
```

Mange methods kan bruges med forskellige slags objekter, fx .play:

``` sc
Pbind().play;
{SinOsc.ar * 0.1}.play;
Routine({"hej ".post; 1.wait; "med dig".postln;}).play;
```

... men ikke alle objekter!

``` sc
10.play       // giver en fejlmeddelelse (.play findes ikke som instance method for SimpleNumber)
Pbind.play    // giver en fejlmeddelelse (.play findes kun som instance method, ikke som class method for Pbind)
```

## Dokumentation af methods

I SuperColliders dokumentation kan man se hvilke methods, der passer til forskellige klasser.

- Slår man en klasse op (fx `Array`, `Pwhite`, `SinOsc` etc.), vil man kunne se de forskellige class methods og instance methods samt hvordan de bruges.
- Slår man en method op (fx `.new`, `.play`, `.reverse` etc.), vil man kunne se de forskellige klasser, som har denne method tilknyttet (klik på klassen for at se hvordan fx .new anvendes inden for den specifikke klasse).

Placér cursoren sammen med et af kodeudtrykkene herunder og tast Ctrl/Cmd-D for at åbne den dokumentationen.

``` sc
Array
Pwhite
SinOsc
.new
.play
.reverse
```
