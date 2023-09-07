# Eksekvering af kode

Brugerfladen i SuperCollider er primært kildekode, som noteres og eksekveres ved hjælp af tastaturet.

Man eksekverer kode ved at taste Ctrl+Enter på Windows eller Cmd+Enter på Mac.

Sæt cursoren på en af linjerne herunder og tast Ctrl+Enter (se outputtet i SuperCollider's "Post window"):     

``` sc
5 + 10
Scale.major
rrand(0, 100)
"Vekseldominant".postln
```

Hvis vi gerne vil gøre mere end én ting ad gangen, kan vi adskille vores instrukser (statements) til SuperCollider ved hjælp af `;` (semikolon)
``` sc
"Et fantastisk tal:".postln; rrand(0, 100).postln
```
Ofte er det en god idé at fordele instrukserne over flere linjer. Hvis vi vil have SuperCollider til at udføre flere linjer med instrukser umiddelbart efter hinanden, kan vi gøre dette ved hjælp parenteser og ; (semikolon). Læg mærke til hvordan begge linjer herunder bliver udført lige efter hinanden:
``` sc
(
"Endnu et fantastisk tal:".postln;
rrand(50, 100).postln;
)
```

Vi eksekverer ofte kode, som genererer lyd. I de tilfælde skal vi først starte SuperColliders lydserver. Dette kan gøres på flere måder, men det mest enkle er at køre denne linje:
``` sc
c.boot;
```
Bemærk, at tallene nederst i højre hjørne bliver grønne, når lydserveren er bootet.

Derefter kan vi afspille lyde:
``` sc
{ SinOsc.ar(440) * 0.1}.play
Pbind(\degree, [0, 2, 4]).play
```

For at slukke lyden: Tast Ctrl+Punktum på Windows eller Cmd+Punktum på Mac.

