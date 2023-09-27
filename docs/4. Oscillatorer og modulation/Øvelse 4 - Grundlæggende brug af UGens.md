---
tags:
    - Øvelser
---
# Øvelse 4: Grundlæggende brug af UGens

Denne øvelse går ud på at bruge UGens på grundlæggende niveau.

## Opgave 1: Blip båt

Afspil følgende lyde med peak-amplitude på 0.1:

1. Sinustone med frekvens på 220Hz
1. Savtakket bølgeform med frekvens på 100Hz
1. En firkantet bølgeform med frekvens på 350Hz   

```sc
{SinOsc.ar(   ) * 0.1}.play;
{     * 0.1}.play;
{     * 0.1}.play;
```

## Opgave 2: Visualisering af bølgeform

SuperCollider kan plotte lyd-outputtet i en graf. Dette viser eksempelvis outputtet fra en `SinOsc` og en `LFTri`, målt over et tidsrum på 10 millisekunder:

```sc
(
{[
    SinOsc.ar(440),
    LFTri.ar(440)
]}.plot(0.010);
)
```

Brug `{}.plot`-teknikken ligesom ovenfor til at overveje følgende spørgsmål:

1. Hvad er forskellen på `Pulse.ar(width: 0.5)` og `Pulse.ar(width: 0.1)`?
1. Hvad er forskellen på `LFNoise0.kr(2)` og `LFNoise1.kr(2)`? (Husk at vi har med LFO at gøre, plot derfor over fx 3 sekunder)                               

## Opgave 3: Visualisering af frekvensspektrum

Vi kan vise SuperColliders lydlige output i frekvensdomænet med `s.freqscope;`
                                        
Brug `s.freqscope` til at besvare følgende spørgsmål:

1. Hvad kendetegner overtonespektrene for de forskellige bølgeformer fra opgave 1 og 2?
1. Hvad styrer bevægelse af musen fra venstre til højre i nedenstående eksempel?

```sc
{ Blip.ar(220, MouseX.kr(1,50)) * 0.1 }.play
```

Har du mange ekstra vinduer åbne (fx fra ovenstående øvelse med plots), kan de lukkes på én gang med `Window.closeAll`.

## Opgave 4: Modulation af lydstyrke (amplitude)

Anvend følgende UGens, [skaleret med methoden'en '.unipolar'](A2-skalering.md), til at modulere amplituden i intervallet 0-1 for en savtakket bølgeform. Modulatorens frekvens vælges frit i intervallet 0-20Hz:

1. `LFSaw` (savtakket bølgeform)
1. `LFPulse` (firkantet bølgeform)
1. `SinOsc` (sinusbølge)         

```sc
{Saw.ar *   }.play;
{Saw.ar *   }.play;
{Saw.ar *   }.play;
```

## Opgave 5: Modulation af tonehøjde (frekvens)

Når vi modulerer frekvens, er det typisk nødvendigt at justere modulatorens frekvens og outputrækkevidde. `.range` og `.exprange` er oplagte redskaber at styre en absolut modulation, og .midiratio (evt. kombineret med .unipolar eller .bipolar) er oplagt til at styre en relativ modulation af tonehøjde. Læs evt. nærmere herom i artiklen om [modulation af UGens](A2-skalering.md).

Modulér frekvensen for en savtakket oscillator med følgende UGens og på følgende måder:

1. Rutsjebane
    - Brug `LFTri` som modulator
    - Tonens frekvens skal bevæge sig mellem 440Hz og 880Hz
    - Valgfri modulatorfrekvens under 20Hz
1. Tonespring
    - Brug `LFPulse` som modulator
    - Tonens frekvens skal bevæge sig mellem 220Hz og 330Hz
    - Valgfri modulatorfrekvens under 20Hz
1. Vibrato
    - Brug `SinOsc` som modulator
    - Tonens frekvens på 660Hz skal moduleres 15 cent op og ned
    - Modulatorfrekvensen skal være 15Hz
1. Tilfældige frekvenser
    - Brug `LFNoise0` som modulator
    - Tonens frekvens på 440Hz skal moduleres i halvtonetrin op til en oktav op og ned
    - Modulatorfrekvensen skal være 8Hz

Vælg selv en passende frekvens mellem 0Hz og 20Hz til modulatoren.

```sc hl_lines="3"
(
{
	var modulator =   ;
	Saw.ar(modulator) * 0.1;
}.play;
)
```

## Bonusopgave: FM, AM, RM

1. Eksperimentér med eksemplerne på AM (Amplitude Modulation), RM (Ring Modulation) og FM (Frequency Modulation) i Thor Magnussons [*Scoring Sound*, kapitel 7](https://leanpub.com/ScoringSound/read#leanpub-auto-chapter-7---modulation).
1. Eksperimentér med eksemplerne på FM fra [Eli Fieldsteels glimrende video om emnet](https://www.youtube.com/watch?v=UoXMUQIqFk4&list=PLPYzvS8A_rTaNDweXe6PX4CXSGq4iEWYC&index=22). Kildekoden fra videoen findes på [github](https://github.com/elifieldsteel/SuperCollider-Tutorials/blob/master/full%20video%20scripts/21_script.scd).


