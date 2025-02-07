---
tags:
    - Artikler
---

# Hvordan får vi SuperCollider til at gøre noget?

Alt hvad man kan *gøre* i SuperCollider er knyttet til noget, der hedder *methods*. Hvis vi forstår og kan anvende de forskellige methods, der findes, kan vi groft sagt bruge alle de redskaber, der findes i SuperCollider! Derfor er det relevant at lære hvordan methods fungerer. Samtidig er det vigtigt at forstå hvad *argumenter* er, da vi bruger argumenter for at angive, hvordan en method skal udføres.

## Methods er funktionalitet

Teknisk set er en method en særlig *funktion*, idet dens rolle er at udføre en bestemt handling, når den bliver aktiveret. I SuperCollider-kildekode ser man ofte methods noteret lige efter punktummer. I et fiktivt eksempel som `~car.drive`, er `drive` en method, som anvendes på det, der er gemt under variablen `~car` - antagelig for at få en bil til at køre. Men lad os kigge på nogle reelle methods i SuperCollider: 

```sc title="Tre methods med forskellig funktionalitet"
// method'en .postln viser objekter i post window, i dette tilfælde et stykke tekst
"Hello world".postln;
// method'en .minorPentatonic angiver (kombineret med Scale) en mol-pentaton skala
Scale.minorPentatonic;
// method'en .midicps omregner et tal fra MIDI-tonehøjde til frekvens, målt i Hertz
69.midicps;
```

Methods kaldes undertiden også for "messages". Det skyldes, at methods anvendes på "noget", og dette noget kalder man så en "receiver". I udtrykket `69.midicps` er `69` receiveren, som modtager vores message `midicps`. 

Alle methods hører til enten en *class* (klasse) eller en *instance* (forekomst). 

## Class methods

En klasse er blot en kategori af objekter. Klasser repræsenteres af ord, som er skrevet med stort begyndelsesbogstav, fx `Scale`, `Pbind` og `SinOsc`. Class methods er knyttet til, ja, klasser. For at aktivere en class method noterer man førstklassenavnet, derefter et punktum, og til sidst method-navnet. Det kan fx se sådan her ud:

``` sc title="Eksempler på class methods"
TempoClock.tempo; // finder eller angiver tempo
Scale.directory;  // viser alle indbyggede skalaer
SinOsc.ar;        // angiver en sinus-oscillator
Pbind.new;        // opretter en ny Pbind (ramme for komposition)
```

Der findes i SuperCollider en særlig class method, som vi bruger hele tiden: `.new`. Denne method skaber et nyt objekt - en "instance"/forekomst af den valgte klasse.

``` sc title="Eksempler på .new"
Pbind.new()     // opretter en ny Pbind
SynthDef.new()  // opretter en ny SynthDef
Scale.new()     // opretter en ny skala
```

`.new` har en særstatus, fordi det at oprette en ny forekomst af noget er så almindeligt, at der for rigtig mange klasser findes en genvej til at bruge method'en - nemlig helt at udelade `.new`. Derfor giver disse to udtryk samme resultat:

``` sc title="Eksplicit og implicit .new"
Pwhite.new(0, 10)   // .new fremgår eksplicit
Pwhite(0, 10)       // .new er underforstået
// Denne forekomst af Pwhite vil generere værdier mellem 0 og 10
```

Om man bruger eks- eller implicit `.new` er et spørgsmål om personlig præference. Den eksplicitte tilgang er mest tydelig at læse, men ofte vil den implicitte udgave give sig selv. Det er fx tilfældet, når vi i næste kapitel skal arbejde med [patterns](../02/a1-patterns-intro.md), hvor man konkret .

## Instance methods

Instance methods bruger vi på "instances", dvs. konkrete forekomster af bestemte klasser af objekter. Fx er `9` en forekomst af klassen `SimpleNumber`. `"kaffe"` er en forekomst af klassen `String`. Instance methods noteres ligesom class methods med et punktum først[^1], men de forekommer efter instances, ikke klassenavne. Her er nogle eksempler:

`.midicps`

:   En method, som blandt andet kan anvendes på tal (og [UGens](../04/a1-ugens.md)). Method'en omregner MIDI-tonetallet 69 til frekvens målt i Hz. `69.midicps` bliver altså til `440`.

`.dup`

:   Kopierer det objekt, den anvendes på. Det kan fx være en sinustone-oscillator: `SinOsc.ar.dup` giver to sinustone-oscillatorer.

`.play`

:   Kan bruges i flere forskellige sammenhænge. Med `Pbind.new().play` kan vi starte med at afspille en ny Pind.

Nogle methods kan styres med input i form af argumenter:

``` sc title="Styring af methods med argumenter"
SinOsc.ar(220)         // vi beder om en sinustone-oscillator, som svinger med 220 Hertz
SinOsc.ar.dup(10)      // vi beder om 10 ens sinustone-oscillatorer
Pwhite(0, 7)           // vi beder om et pattern, der kan generere tilfældige tal mellem 0 og 7
```

Mange methods kan bruges med forskellige slags objekter, fx `.play`:

``` sc title="Forskellige resultater med .play"
Pbind().play;
{SinOsc.ar * 0.1}.play;
Routine({"hej ".post; 1.wait; "med dig".postln;}).play;

// ... men .play kan ikke anvendes på alle objekter!
10.play       // giver en fejlmeddelelse (.play findes ikke som instance method for SimpleNumber)
Pbind.play    // giver en fejlmeddelelse (.play findes kun som instance method, ikke som class method for Pbind)
```

## Dokumentation for methods

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

[^1]: For nogle (men ikke alle) methods findes en syntaktisk variant, hvor instance methods noteres *før* objektet, adskilt med et simpelt mellemrum. Fx er `play {SinOsc.ar};` helt korrekt syntaks, der svarer til `{SinOsc.ar}.play;`. Jeg anbefaler, at man holder sig til den sidstnævnte form, da punktummet mellem method og objekt tydeliggør, hvad der er method og hvad denne method knytter sig til.
