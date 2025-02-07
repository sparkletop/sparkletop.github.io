---
tags:
    - Øvelser
---
# Øvelse: Grundlæggende programmering

Denne øvelse omhandler brug af SuperColliders IDE til at eksekvere kildekode, tilføje kommentarer, bruge variabler, samt identificere syntaksfejl i SuperCollider-kildekode.

## Forklar kildekoden

- Eksekvér nedenstående kodeblok på én gang. Forklar i kommentarer hvad hver enkelt kodelinje gør.

``` sc title="Hvad gør kildekoden?"
(
"Else Marie Pade".postln;

TempoClock.tempo.postln;

~akkord = [0, 3, 4];
~akkord.postln;

(3 + 4).postln;
3 + 4.postln;
)
```

## Yndlingstal og variabler

- Post dit yndlingstal i SuperColliders post window
- Gem dit yndlingstal under en global variabel, fx `~mitYndlingstal`
- Post indholdet af din variabel
- Post indholdet af din variabel ganget med 200

## Find og ret syv fejl

- Find og ret fejlene i de syv eksempler herunder
- Ryd SuperColliders post window (Cmd/Ctrl+Shift+p) inden du starter med et nyt eksempel         
- Læs fejlmeddelelsen, før du retter fejlen
- Forklar i en kommentar for hver fejl hvad du har rettet og hvad problemet bestod i

``` sc title="Find 7 fejl"
~alder = 32,5;

~skala = Scale.locrian; \\ her gemmer jeg min yndlingsskala

(
10.postln
20.postln
)

(
~resultat = 4 * 10;
~Resultat.postln;
)

(
var Rytme = [1/4, 1/8, 1/8];
Rytme.postln;
)

"57".midicps;

(
~svar = 10 * (4 + (2);
~svar.postln;
)
```
