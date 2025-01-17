# Om denne bog

Denne bog indeholder læringsmaterialer inden for grundlæggende musik- og lydprogrammering med redskabet [SuperCollider](https://supercollider.github.io), som er gratis og open source. Man kan lære at arbejde med programmering som et værktøj til musikalsk kreativitet, uanset om man har tidligere erfaring med at programmere.

Bogen udgør ikke en enkeltstående introduktion og bør suppleres med anden litteratur. Her kan særligt Bruno Ruviaros *[A Gentle Introduction to SuperCollider](https://ccrma.stanford.edu/~ruviaro/texts/A_Gentle_Introduction_To_SuperCollider.pdf)* og Eli Fieldsteels videoserie *[SuperCollider Tutorials](https://www.youtube.com/playlist?list=PLPYzvS8A_rTaNDweXe6PX4CXSGq4iEWYC)* anbefales.

## Sådan bruger du denne bog

Bogen er opbygget i 10 kapitler. Det anbefales, at begyndere starter fra kapitel 1 og arbejder sig fremad, da det er vigtigt at tilegne sig grundlæggende færdigheder, før man tager hul på mere avancerede emner.

Det anbefales kraftigt, at man undervejs i læsningen selv indtaster og afprøver eksemplerne med kildekode. Årsagerne hertil er mange:

- Det er sjovere at lege med eksemplerne på egen hånd
- Man forstår og husker bedre hvordan koden fungerer, når man selv har indtastet den
- Man lærer et nyt sprog bedst ved at bruge det

Prøv selv at indtaste nedenstående kildekode i SuperColliders tekst-editor. Placer cursoren på én af de midterste linjer og tast Ctrl-Enter eller Cmd-Enter for at høre lyden. Stop lyden igen med Ctrl-Punktum eller Cmd-Punktum.

```sc title="En tilfældig LFO styrer en sinustone-oscillator"
(
s.waitForBoot({
{
    SinOsc.ar(
        LFNoise0.kr(10.dup).exprange(220, 880)
    )
}.play;
})
)
```

## Tre indholdstyper

Bogen har tre forskellige typer indhold:

- *Artikler*: Korte tekster, som introducerer til generativ komposition og digital klangdannelse med SuperCollider
- *Cheat sheets*: Overskuelige, korte oversigter over centrale redskaber og teknikker
- *Øvelser*: Praktiske udfordringer, som giver mulighed for at arbejde hands on med emnerne

## Licens

Bogen er skrevet af [Anders Eskildsen](https://vbn.aau.dk/en/persons/146493) og gjort tilgængelig for offentligheden under Creative Commons-licensen [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
