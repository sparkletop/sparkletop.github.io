---
tags:
    - Øvelser
---
# Øvelse: Grundlæggende programmering

Denne øvelse omhandler brug af SuperColliders IDE til at eksekvere kildekode, tilføje kommentarer, bruge variabler, samt identificere syntaksfejl i SuperCollider-kildekode.

## Forklar kildekoden

- Eksekvér nedenstående kodeblok på én gang. Forklar i kommentarer hvad hver enkelt kodelinje gør.

``` sc title="Hvad gør kildekoden?"
"Else Marie Pade".postln;

TempoClock.tempo.postln;

~akkord = [0, 3, 4];
~akkord.postln;

(3 + 4).postln;
3 + 4.postln;
```

## Yndlingstal og variabler

1. Post dit yndlingstal i SuperColliders post window.
1. Gem dit yndlingstal under en global variabel, fx `~mitYndlingstal`.
1. Post indholdet af din variabel.
1. Post indholdet af din variabel ganget med 200.

## Nu kører det

1. Eksekvér linjerne i kodeblokken herunder én for én.
1. Eksekvér linjerne i kodeblokken herunder [som én kodeblok](./a-eksekvering.md#flere-instrukser-ad-gangen).

```sc title="Eksekvering af kildekode"
"Bach is back".postln;
2.pow(24).postln;
[57, 69].midicps.postln;
```

## En funktionel funktionsforståelse

1. Læs nedenstående kildekode og beskriv hvad hver linje i funktionen gør.
1. Bekræft din forståelse af funktionen ved at køre den med `.value` et par gange.

```sc title="En funktion"
(
~myFunc = {
    arg root = 0;
    var chord = root + [0, 4, 6, 9];
    chord.reverse.mirror;
};
)
~myFunc.value(2);
~myFunc.value(4);
~myFunc.value(-3);
```

Boot eventuelt lydserveren med `s.boot` og brug funktionen til at spille en akkordbrydning: `Pbind(\degree, Pseq(~myFunc.value(-3))).play;`. Vi lærer mere om dette [i næste kapitel](../02/a-patterns-intro.md).

## Listige liste-methods

1. Undersøg ved hjælp af nedenstående kildekode, hvad de forskellige methods for lister gør.
1. Erstat `~liste` med en liste på mindst 5 tal, som du selv vælger.

Husk følgende:

- Den tekniske term for en "liste" i SuperCollider er `Array`. Du kan også i dokumentationen støde på klassen `ArrayedCollection`. For nuværende kan vi blot betragte disse som forskellige navne for lister.
- Listers indeks-tal [starter fra 0](a-lister.md). Det første element har derfor indeks 0, det næste indeks 1 og så fremdeles.

```sc title="Liste-methods"
~liste = [0, 1, 3, 4, 6, 7];

~liste.reverse;
~liste.mirror;
~liste.mirror1;
~liste.scramble;
~liste.size;
~liste.sum;
~liste.mean;
~liste.normalize(0, 100);
~liste.normalizeSum;
~liste.normalizeSum.sum;
~liste.at(4);
~liste[4];
~liste.put(4, -2);
~liste.plot;
~liste.do({ arg num; num.pow(2).postln; });
~liste.collect({ arg num; num * 10; });
~liste.dupEach(3);
~liste.sputter(0.5, 50);
~liste.rotate(1);
~liste.wrapExtend(15);
```

## Kan du finde alle de syntaktiske kategorier?

Du er i gang med at lære et nyt sprog. Nedenstående øvelse giver en god forudsætning for at undersøge og forstå kildekode, du ikke har set før.

1. Identificér følgende i kildekoden herunder:
    1. Alle klassenavne. *Hint: Det er dem, der [starter med stort begyndelsesbogstav](a-methods#class-methods).
    1. Alle methods, herunder også [implicit](./a-methods.md#class-methods) `.new`.
    1. Alle lister.
    1. Alle unikke [variabelnavne](./a-variabler.md#brug-af-variabler).
    1. Alle [funktioner](a-funktioner.md).
    1. Alle [argumenter](a-funktioner.md#input-til-funktioner-argumenter).
1. Undersøg ved hjælp af SuperColliders dokumentation følgende:
    1. Hvad dækker de forskellige klassenavne over?
    1. Hvilken funktionalitet knytter sig til de forskellige methods?
    1. Hvilken betydning har argumenterne i de to methods, hvor der er angivet eksplicitte argumenter?

Tip: Du kan slå op i SuperColliders indbyggede dokumentation ved at placere cursoren ved en method eller et klassenavn og taste Ctrl/Cmd-D.

```sc title="Find Holger"
~interval = 12;
440 * ~interval.midiratio;

Platform.userExtensionDir;
MIDIClient.init;

(
{
    arg input = 0;
    var output = (2 + input).pow(2);
    output.postln;
}.value(3);
)

s.boot;
{SinOsc.ar(880)}.play;

~trin = [0, 2, 4, 6].mirror;
~komp = Pbind(\degree, Pseq(~trin)).play;
~komp.stop;
```

Der findes i ovenstående kodeblok:

- 5 klassenavne.
- 14 methods (heraf 2 stk. implicit `.new`).
- 1 liste.
- 4 unikke variabelnavne (3 globale og 1 lokal).
- 2 funktioner.
- 6 argumenter.

## Find og ret syv fejl

1. Find og ret fejlene i de syv eksempler herunder.
1. Ryd SuperColliders post window (Cmd/Ctrl+Shift+p) inden du starter med et nyt eksempel.
1. Læs fejlmeddelelsen, før du retter fejlen.
1. Forklar i en kommentar for hver fejl hvad du har rettet og hvad problemet bestod i.

``` sc title="Find 7 fejl"
~alder = 32,5;
~skala = Scale.locrian; \\ her gemmer jeg min yndlingsskala
(
10.postln
20.postln
)
(
~Resultat = 4 * 10;
~Resultat.postln;
)
"57".midicps;
~svar = 10 * (4 + (2 * 1.5);
~svar.postln;
```
