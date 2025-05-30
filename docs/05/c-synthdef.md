---
tags:
    - Cheat sheets
---

# Cheat sheet: SynthDef-skabeloner

SynthDefs kan indrettes på mange forskellige måder. Men til mono- eller stereofone lyde, hvor en given tonehøjde er vigtig, kan skabelonerne herunder være et udmærket udgangspunkt. Begge skabeloner er i sig selv ret kedelige med en simpel sinustone, men det kan du nemt udbygge med et mere interessant lyddesign. Du bruger skabelonen på følgende måde:

- `\navn` skal ændres til et mere deskriptivt navn for din SynthDef.
- Du kan tilføje argumenter efter behov ved at følge den syntaks, der er anvendt på linje 3 og 4.
- Du kan tilføje lokale variabler ligesom på linje 5 til at definere signalflowet i SynthDef'en.
- Du kan ændre `SinOsc.ar(freq)` til noget andet, alt efter hvilken lydkilde du ønsker at arbejde med.
- Du kan tilføje yderligere indhold og lydlig transformation til SynthDef'en mellem linje 5 og 10 (tilføj gerne flere linjer).
- Linje 10 med `Out.ar` er oftest den sidste linje i en SynthDef, som sørger for, at signalet panoreres og volumenjusteres som ønsket, inden det sendes til de ønskede output-kanaler.

```sc title="SynthDef-skabelon til monofone lydkilder"
SynthDef(\navn, {
    arg freq = 440, pan = 0,
    amp = 0.1, out = 0;
    var sig = SinOsc.ar(freq);



    // sig er et monofont signal
    Out.ar(out, Pan2.ar(sig, pan, amp));
}).add;
```

I SynthDef'en herunder er lydkilden, en sinustone, blot dupliceret med `.dup`, så den klinger i to kanaler. Det er oplagt at foretage ændringer og tilføjelser her for at opnå et mere interessant steroe-lyddesign. Med `Balance2.ar` balanceres der til sidst mellem de to kanaler. Læs eventuelt nærmere om stereofoni og *multichannel expansion* i [kapitlet om oscillatorbanke](../07/a-oscillatorbanke.md).

```sc title="SynthDef-skabelon til stereofone lydkilder"
SynthDef(\navn, {
    arg freq = 440, pan = 0,
    amp = 0.1, out = 0;
    var sig = SinOsc.ar(freq).dup;



    // sig er et stereofont signal
    Out.ar(out, Balance2.ar(sig[0], sig[1], pan, amp));
}).add;
```
