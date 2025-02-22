# Musik- og lydprogrammering

Dette website indeholder supplerende materialer til et grundlæggende kursus i musik- og lydprogrammering. Redskabet i kurset, [SuperCollider](https://supercollider.github.io), er gratis og open source. Websitet her er ikke en enkeltstående introduktion og bør suppleres med anden litteratur, fx Bruno Ruviaros udmærkede *[A Gentle Introduction to SuperCollider](https://ccrma.stanford.edu/~ruviaro/texts/A_Gentle_Introduction_To_SuperCollider.pdf)* og Eli Fieldsteels udmærkede videoserie *[SuperCollider Tutorials](https://www.youtube.com/playlist?list=PLPYzvS8A_rTaNDweXe6PX4CXSGq4iEWYC)*.

## Brug af dette site

Denne side er opbygget i 11 moduler, som tilgås via menuen. Det anbefales, at begyndere starter fra modul 1 og arbejder sig fremad. Det anbefales kraftigt, at man undervejs i læsningen selv indtaster og afprøver eksemplerne med kildekode, da dette giver den bedst mulige erfaring og indlæring.

Blokke af kildekode her på siden kan let kopieres og indsættes i SuperColliders tekst-editor - prøv selv med nedenstående kildekode. Placer cursoren på én af de midterste linjer og tast Ctrl-Enter eller Cmd-Enter for at høre lyden. Stop lyden igen med Ctrl-Punktum eller Cmd-Punktum.

```sc title="En tilfældig LFO styrer en sinustone-oscillator"
(
{
    SinOsc.ar(
        LFNoise0.kr(10.dup).exprange(220, 880)
    )
}.play;
)
```

![type:audio](media/audio/sinus-random.ogg)

## Licens

Indholdet på disse sider er fremstillet af [Anders Eskildsen](https://vbn.aau.dk/en/persons/146493) og gjort tilgængelig for offentligheden under Creative Commons-licensen [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
