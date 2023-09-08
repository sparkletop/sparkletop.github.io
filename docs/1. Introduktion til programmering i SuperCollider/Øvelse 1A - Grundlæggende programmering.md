# Øvelse 1A: Grundlæggende programmering

Nedenstående øvelser omhandler brug af variabler og eksekvering af kildekode.

## Opgave 1: Forklar kildekoden

Eksekvér nedenstående kodeblok på én gang. Forklar i kommentarer hvad hver enkelt kodelinje gør.

``` sc
(
"Else Marie Pade".postln;

TempoClock.tempo.postln;

~akkord = [0, 3, 4];
~akkord.postln;

(3+4).postln;
)
```

## Opgave 2: Yndlingstal og variabler

- Post dit yndlingstal i SuperColliders post window
- Gem dit yndlingstal under en global variabel, fx ~mitYndlingstal
- Post indholdet af din variabel
- Post indholdet af din variabel ganget med 200

## Opgave 3: Find (og ret) syv fejl

Find og ret fejlene i de syv eksempler herunder.

Vigtigt: Læs altid fejlmeddelelsen, før du retter fejlen!

Forklar i en kommentar for hvert eksempel hvad du har rettet og hvad problemet bestod i

Ryd SuperColliders post window (Cmd/Ctrl+Shift+p) inden du starter med et nyt eksempel           

``` sc
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
