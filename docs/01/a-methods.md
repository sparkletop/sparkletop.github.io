---
tags:
    - Artikler
---

# Indbygget funktionalitet i methods

Al indbygget funktionalitet i SuperCollider er knyttet til en særlig gruppe af funktioner, der kaldes *methods*. Hvis vi forstår og kan anvende de forskellige methods, der findes, kan vi groft sagt bruge alle de redskaber, der findes i SuperCollider! Derfor er det relevant at lære hvordan methods fungerer.

## Funktionalitet er knyttet til methods

Når vi skal have SuperCollider til at udføre en handling, som fx at sætte en lyd i gang, bruger vi en eller flere konkrete *methods*. En method er en *funktion*, hvis rolle er at udføre en bestemt handling, når den bliver aktiveret.

Lyder det abstrakt? Okay, lad os se på hvordan methods optræder i kildekode: Methods noteret typisk lige efter punktummer. I et fiktivt eksempel som `~car.drive`, er `drive` altså en method. Methods kaldes undertiden også for "messages". Det skyldes, at methods altid anvendes på "noget", og dette noget kalder man så en "receiver" - i det fiktive eksempel her er receiveren det, der er gemt under variablen `~car`. Men lad os kigge på nogle reelle methods i SuperCollider:

```sc title="Tre methods med forskellig funktionalitet"
// method'en .postln viser objekter i post window, i dette tilfælde et stykke tekst
"Hello world".postln;

// method'en .minorPentatonic angiver (kombineret med receiveren Scale) en mol-pentaton skala
Scale.minorPentatonic;

// method'en .midicps omregner et tal fra MIDI-tonehøjde til frekvens, målt i Hertz
69.midicps;
```

Vi kan ikke gennemgå alle methods i SuperCollider her, da der er alt for mange til at det rent praktisk giver mening. Men vi kommer løbende i bogen til at gå i dybden med hvordan man bruger konkrete methods. Dog er det vigtigt at forstå, at alle methods hører til enten en *class* (klasse) eller en *instance* (forekomst).

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

Om man bruger eks- eller implicit `.new` er et spørgsmål om personlig præference. Den eksplicitte tilgang er mest tydelig at læse, men ofte vil den implicitte udgave give sig selv. Det er fx tilfældet, når vi i næste kapitel skal arbejde med [patterns](../02/a-patterns-intro.md), hvor man konkret .

## Instance methods

Instance methods bruger vi på "instances", dvs. konkrete forekomster af bestemte klasser af objekter. Fx er `9` en forekomst af klassen `SimpleNumber`. `"kaffe"` er en forekomst af klassen `String`. Instance methods noteres ligesom class methods med et punktum først[^1], men de forekommer efter instances, ikke klassenavne. Her er nogle eksempler:

`.dup`

:   Kopierer det objekt, den anvendes på. Det kan fx være en sinustone-oscillator: `SinOsc.ar.dup` giver to sinustone-oscillatorer.

`.play`

:   Kan bruges i flere forskellige sammenhænge. Med `Pbind.new().play` kan vi starte med at afspille en ny Pind.

`.midicps`

:   En method, som blandt andet kan anvendes på tal (og [UGens](../04/a-ugens.md)). Method'en omregner MIDI-tonetallet 69 til frekvens målt i Hz. `69.midicps` bliver altså til `440`. Bemærk, at dette er præcist det samme som vi så ifm. [indbyggede funktioner](a-funktioner.md#indbyggede-funktioner), altså `midicps(69)`.

[^1]: For nogle (men ikke alle) methods findes en syntaktisk variant, hvor instance methods noteres *før* objektet, adskilt med et simpelt mellemrum. Fx er `play {SinOsc.ar};` helt korrekt syntaks, der svarer til `{SinOsc.ar}.play;`. Jeg anbefaler, at man holder sig til den sidstnævnte form, da punktummet mellem method og objekt tydeliggør, hvad der er method og hvad denne method knytter sig til.

Flere gængse methods kan heldigvis bruges med mange forskellige slags objekter[^3]. Det gælder eksempelvis for `.play`, som vi bruger jævnligt. Her er nogle eksempler (for at høre resultatet af de første to linjer skal lydserveren først bootes):

[^3]: Særligt programmeringsteknisk interesserede læsere kan notere sig, at dette med et fancy udtryk fra det såkaldt objektorienterede programmeringsparadigme kaldes for ["polymorfisme"](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)).

``` sc title="Forskellige resultater med .play"
Pbind().play;
{SinOsc.ar * 0.1}.play;
Routine({"hej ".post; 1.wait; "med dig".postln;}).play;
```

Det er dog ikke alt, der kan "afspilles" med `.play`. Begge instrukser herunder resulterer derfor i fejlmeddelelser:

```sc title=".play kan ikke anvendes på alle objekter!"
10.play
// Det giver ikke mening at afspille et tal

Pbind.play
// .play findes som instance method for forekomster af Pbind, ikke som class method
```

## Argumenter

I mange tilfælde kan vi styre hvordan en given method fungerer. Det gør vi ved hjælp af *argumenter*. Men argumenter - hvad er nu det for noget? Vi har ovenfor set en række tilfælde, hvor en method er blevet efterfulgt af et sæt parenteser, nogle gange med nogle tal eller anden tekst noteret mellem parenteserne. Det, der står mellem parenteserne, kalder vi for argumenter. Med vores fiktive eksempel ovenfor kunne man forestille sig, at `~car.drive(50)` og `~car.drive(100)` ville få en bil til at køre med henholdsvis 50 km/t og 100 km/t. Her er nogle reelle eksempler på

``` sc title="Styring af methods med argumenter"
// vi beder om en sinustone-oscillator, som svinger ved 220 Hertz audio rate
SinOsc.ar(220)

// vi beder om 10 kopier af en sinustone-oscillator
SinOsc.ar.dup(10)

// vi beder om et pattern, der kan generere tilfældige tal mellem 0 og 7
Pwhite.new(0, 7)
```

- Navngivne argumenter.

- Standardværdier.

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
