Denne bog introducerer til grundlæggende musik- og lydprogrammering. Bogen er blevet til som et supplerende materiale til min undervisning på musikuddannelsen ved Aalborg Universitet. Mit ønske med bogen er, at studerende kan lære at bruge programmering som et kreativt redskab til komposition og lydproduktion, uanset om man på forhånd har kendskab til programmering. Alle kan lære at kode på grundlæggende niveau, og med musik som vores legeplads er det en fornøjelse!

Når man dykker ned i musik- og lydprogrammering, lærer man en masse om computermusik i bredere forstand. Bogen introducerer derfor også sekundært til digital klangdannelse og algoritmisk komposition. Den tekniske platform er [SuperCollider](https://supercollider.github.io), et fantastisk redskab, som tilmed er gratis og open source.

Sidst men ikke mindst: Bogen her udgør et \textit{supplerende} læringsmateriale. Det betyder, at man med fordel også kan studere andre materialer (hvoraf stort set alle dog er på engelsk). Her kan jeg særligt anbefale to glimrende ressourcer, som henvender sig til begyndere:


- Bruno Ruviaros e-bog *[A Gentle Introduction to SuperCollider](https://ccrma.stanford.edu/~ruviaro/texts/A_Gentle_Introduction_To_SuperCollider.pdf)*
- Eli Fieldsteels videoserie [SuperCollider Tutorials](https://www.youtube.com/playlist?list=PLPYzvS8A_rTaNDweXe6PX4CXSGq4iEWYC) 

I slutningen af bogen kommer jeg med yderligere anbefalinger til videre studier udi computermusik med SuperCollider.

## Sådan bruger du denne bog

Bogen er skrevet med henblik på studerende på de videregående uddannelser men kan bruges af alle, der har en forståelse af musikteori og musikteknologi på grundlæggende niveau.

Hvis man er begynder, er det en god idé at starte fra kapitel 1 og arbejde sig fremad. Man skal, som det gode gamle ordsprog lyder, kravle, før man kan gå. Al erfaring viser, at det er sjovest at tage fat på de mere avancerede emner, når man har godt styr på de grundlæggende færdigheder. Er man mere erfaren inden for programmering og computermusik, kan man i stedet bruge bogen som et opslagsværk.

Uanset hvilken baggrund man har, vil jeg anbefale, at man undervejs i læsningen selv indtaster og afprøver eksemplerne med kildekode.

- Man forstår og husker bedre hvordan koden fungerer, når man selv har indtastet den.
- Man lærer et nyt sprog bedst, når man bruger det i praksis.
- Og sidst, men bestemt ikke mindst: Det er sjovere at lege med eksemplerne på egen hånd! 

Prøv selv at [installere SuperCollider](https://supercollider.github.io/downloads), åbne programmet og indtaste nedenstående kildekode i tekst-editoren. Placer cursoren på én af de midterste linjer og tast Ctrl-Enter eller Cmd-Enter for at høre lyden. Stop lyden igen med Ctrl-Punktum eller Cmd-Punktum.


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
![type:audio](../docs/media/audio/sinus-random.ogg)

Du vil nu høre to sinustoner; en tone i hver stereo-kanal, som begge springer tilfældigt op og ned 10 gange i sekundet. 


### Om bogens indhold

Bogens kapitler indeholder sektioner med tre forskellige typer indhold, der kan bruges efter behov:

Artikler

:   Introducerer til hvordan man kan arbejde med generativ komposition og digital klangdannelse i SuperCollider.

Cheat sheets

:   Overskuelige, korte oversigter over centrale redskaber og teknikker. Oplagt at bruge som opslagsværk.

Øvelser

:   Praktiske opgaver, som giver mulighed for at øve sig i de forskellige teknikker.


Bogen kan også læses i en webudgave på \href{https://sparkletop.github.io}{sparkletop.github.io}, hvor også bogens lydeksempler findes.

## Licens

Bogen er skrevet af [Anders Eskildsen](https://vbn.aau.dk/en/persons/146493) og gjort tilgængelig for offentligheden under Creative Commons-licensen \textit{CC BY 4.0}. Det betyder, at bogen må deles og bearbejdes, så længe licensbetingelserne overholdes (herunder tydelig henvisning til forfatteren). Læs nærmere herom hos [Creative Commons](https://creativecommons.org/licenses/by/4.0/).