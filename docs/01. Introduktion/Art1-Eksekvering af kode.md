---
tags:
    - Artikler
---

Når man første gang åbner SuperCollider, mødes man af en umiddelbart noget minimalistisk brugerflade. Med mindre man har arbejdet med programmering i anden sammenhæng, vil det i begyndelsen være lidt uvant, at brugerfladen først og fremmest består i et tekstdokument, hvor man noterer og eksekverer kildekode. Men det ændrer sig hurtigt, når man kommer i gang, og inden længe kommer man til at sætte pris på den enkelhed, brugerfladen også repræsenterer.

# Eksekvering af kode

Man eksekverer kode ved at taste Ctrl+Enter på Windows/Linux eller Cmd+Enter på Mac. Prøv det selv:

- Kopiér eller indtast linjerne herunder i et SuperCollider-dokument.
- Sæt cursoren på en af linjerne herunder og tast Ctrl+Enter (PC) eller Cmd+Enter (Mac).
- Iagttag derefter outputtet i SuperCollider's "Post window" (som ved et nyinstalleret setup vil befinde sig til højre i skærmbilledet).

```sc title="Eksekvering af kode"
5 + 10
Scale.major
rrand(0, 100)
"Vekseldominant".postln
```

## Mere end én handling ad gangen

Hvis vi gerne vil gøre mere end én ting ad gangen, kan vi adskille vores instrukser (statements) til SuperCollider ved hjælp af semikolon:

``` sc title="Flere statements på én kodelinje"
"Et fantastisk tal:".postln; rrand(0, 100).postln
```

Hvis vi udelader semikolon, kan SuperCollider ikke forstå hvor den ene instruks stopper og hvornår den næste starter.

### Kodeblokke hjælper os med at udføre flere instrukser ad gangen

Ofte er det en god idé at fordele instrukserne over flere linjer. Hvis vi vil have SuperCollider til at udføre flere linjer med instrukser umiddelbart efter hinanden, kan vi gøre dette ved at afslutte de enkelte linjer med semikolon og omkranse linjerne med parenteser. Læg mærke til hvordan begge linjer herunder bliver udført så hurtigt efter hinanden, at det stort set sker samtidigt, når vi sætter cursoren på en af linjerne og trykker Ctrl/Cmd-Enter:

``` sc title="Kodeblokke med parenteser"
(
"Endnu et fantastisk tal:".postln;
rrand(50, 100).postln;
)
```

## Sæt gang i lydserveren

For at kunne bruge programmering som et musikalsk redskab til komposition og lyddesign skriver vi ofte kildekode, som genererer lyd.
I de tilfælde skal vi først starte SuperColliders lydserver. Dette kan gøres på flere måder, men det mest enkle er at køre denne linje:

``` sc title="Start af SuperColliders lydserver"
s.boot;
```

Bemærk, at når lydserveren er bootet, blvier tallene nederst i højre hjørne grønne. Derefter kan vi afspille lyde:

``` sc title="Et par simple lyde"
{ SinOsc.ar(440) * 0.1 }.play
Pbind(\degree, [0, 2, 4]).play
```

For at slukke lyden: Tast Ctrl+Punktum på Windows eller Cmd+Punktum på Mac.

