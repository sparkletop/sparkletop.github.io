Denne bog introducerer til grundlæggende musik- og lydprogrammering. Bogen er blevet til som et supplerende materiale til min undervisning på musikuddannelsen ved Aalborg Universitet. Mit ønske med bogen er, at studerende kan lære at bruge programmering som et kreativt redskab til komposition og lydproduktion, uanset om man på forhånd har kendskab til programmering. Alle kan lære at kode på grundlæggende niveau, og med musik som vores legeplads er det en fornøjelse!

Når man dykker ned i musik- og lydprogrammering, lærer man en masse om computermusik i bredere forstand. Bogen introducerer derfor også sekundært til digital klangdannelse og algoritmisk komposition. Den tekniske platform er [SuperCollider](https://supercollider.github.io), et fantastisk redskab, som tilmed er gratis og open source.

Sidst men ikke mindst: Bogen her udgør et *supplerende* læringsmateriale. Det betyder, at man med fordel også kan studere andre materialer (hvoraf det meste er på engelsk). Her kan jeg særligt anbefale to glimrende ressourcer, som henvender sig til begyndere:

- Bruno Ruviaros e-bog *[A Gentle Introduction to SuperCollider](https://ccrma.stanford.edu/~ruviaro/texts/A_Gentle_Introduction_To_SuperCollider.pdf)*
- Eli Fieldsteels videoserie *[SuperCollider Tutorials](https://www.youtube.com/playlist?list=PLPYzvS8A_rTaNDweXe6PX4CXSGq4iEWYC)*

## Sådan bruger du denne bog

Bogen kan bruges af alle, der ønsker at lære musik- og lydprogrammering på grundlæggende niveau.

Hvis man er begynder, er det en god idé at starte fra kapitel 1 og arbejde sig fremad. Man skal kravle, før man kan gå, og det er min erfaring, at det er sjovest at tage fat på de mere avancerede emner, når man har godt styr på de grundlæggende færdigheder. Er man mere erfaren inden for programmering og computermusik, kan man bruge bogen som et opslagsværk.

Uanset hvilken baggrund man har, vil jeg kraftigt anbefale, at man undervejs i læsningen selv indtaster og afprøver eksemplerne med kildekode.

- Det er sjovere at lege med eksemplerne på egen hånd
- Man forstår og husker bedre hvordan koden fungerer, når man selv har indtastet den
- Man lærer et nyt sprog bedst ved at bruge det

Prøv selv at installere SuperCollider og indtaste nedenstående kildekode i SuperColliders tekst-editor. Placer cursoren på én af de midterste linjer og tast Ctrl-Enter eller Cmd-Enter for at høre lyden. Stop lyden igen med Ctrl-Punktum eller Cmd-Punktum.

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

Du vil nu høre en ...

## Tre indholdstyper

Bogens kapitler indeholder forskellige afsnit, der kan bruges alt efter behov og erfaring.

- *Artikler*: Korte tekster, som introducerer til generativ komposition og digital klangdannelse med SuperCollider
- *Cheat sheets*: Overskuelige, korte oversigter over centrale redskaber og teknikker
- *Øvelser*: Praktiske udfordringer, som giver mulighed for at arbejde hands on med emnerne

Bogen her kan også læses i en webudgave på [sparkletop.github.io](https://sparkletop.github.io).

## Licens

Bogen er skrevet og gjort tilgængelig for offentligheden af [Anders Eskildsen](https://vbn.aau.dk/en/persons/146493) under Creative Commons-licensen [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Det betyder, at bogen må deles og bearbejdes, så længe licensbetingelserne overholdes - læs nærmere herom hos Creative Commons.

