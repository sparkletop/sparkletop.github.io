---
tags:
    - Artikler
---

# Pattern-komposition med MIDI-output

Når vi lærer at arbejde patterns som kompositionsredskab, er det oplagt at anvende en mere interessant lydkilde end den indbyggede standardlyd i SuperColliders lydserver. Vi kommer senere til at [designe vores egne lyde med SuperColliders lydserver](../05/a-synthdef.md), men for nuværende kan det give nogle lydligt interessante resultater at bruge vores patterns til MIDI-komposition.

## Opsætning og test af MIDI-kommunikation

For at sende MIDI-signaler fra SuperCollider til et andet program på samme computer, hvor SuperCollider kører, skal man [sætte en virtuel MIDI-port](https://help.ableton.com/hc/en-us/articles/209774225-Setting-up-a-virtual-MIDI-bus). Alternativt kan man bruge MIDI-output til et andet stykke hardware, fx en ekstern synthesizer. Jeg forudsætter herunder, at den virtuelle eller fysiske forbindelse er etableret, og at modtageren af vores MIDI-signal er klar til at modtage meddelelser.

Når DAW eller synthesizer er klar til at modtage MIDI-signal, kører man i SuperCollider først `MIDIClient.init`. Dette får SuperCollider til at kontakte computerens MIDI-system og vise i post window hvilke MIDI-porte der er tilgængelige. Derfra noterer man navnet på den ønskede port og bus. Dem angiver man så, når man med `MIDIOut.newByName` opretter et output og gemmer dette under en global variabel.

``` sc title="Opsætning af MIDI-output med MIDIClient og MIDIOut"
// Start MIDI-kommunikation
MIDIClient.init;

// Opret MIDIOut til DAW/synthesizer
~daw = MIDIOut.newByName("loopMIDI Port", "loopMIDI Port"); // Typisk portnavn på Windows
~daw = MIDIOut.newByName("IAC Driver", "Bus 1"); // Typisk portnavn på Mac
```

Så er vi klar til at sende MIDI-meddelelser fra SuperCollider. For at teste forbindelse kan vi sende en Note On- og en Note Off-meddelelse, hvorved vi kan se eller høre på modtageren, at der spilles en tone.

```sc title="Test MIDI-forbindelsen med toneanslag og -afslag"
~daw.noteOn(chan: 0, note: 64, veloc: 80);
~daw.noteOff(chan: 0, note: 64);
```

## Patterns og MIDI-begivenheder

For at bruge Pbind som MIDI-generator skal vi angive et par oplysninger under nogle særlige nøgler:

`\type`

:   Med denne nøgle angiver vi hvilken event-type, vores Pbind skal genererere. Vi har hidtil arbejdet med den event-type, som er default, nemlig den såkaldte `\note`-event. Når vi angiver `\midi` her, ved Pbind, at der skal produceres MIDI-meddelelser i stedet for meddelelser til lydserveren.

`\midiout`

:   Her angiver vi den `MIDIOut`, vi oprettede ovenfor, så Pbind ved, hvor de genererede MIDI-meddelelser skal sendes hen.

`\chan`

:   Her kan vi angive hvilken MIDI-kanal, der skal sendes på. Der er 16 tilgængelige kanaler, nummereret i SuperCollider fra 0 til 15.

Samler vi disse oplysninger, vil vi med nedenstående kildekode kunne høre en række toner blive spillet i DAW/synthesizer.

```sc title="Pbind med MIDI-output"
(
~komposition = Pbind(
    \type, \midi,
    \midiout, ~daw,
    \chan, 0,    
).play;
)
~komposition.stop;
```

## Begrænsninger ved MIDI-protokollen

Når vi komponerer med MIDI, er det væsentligt at notere sig dennes begrænsninger. Almindelige *Note On* og *Note Off*-meddeleser i MIDI indeholder blot information om hvilken MIDI-tone, det drejer sig om, samt en parameter, der kaldes *velocity*, hvilket ofte kobles med lydstyrke[^1]. Begge disse oplysninger befinder sig i intervallet 0-127. Samtidig kan vi styre, *hvornår* meddelelserne afsendes. Dermed har vi altså kontrol over følgende musikalske parametre:

- Tonehøjde, i form af MIDI-tonetal
- Lydstyrke, i form af MIDI-velocity
- Rytmik, i form af meddelelsernes timing

Vi har *ikke* kontrol over parametre som klang, envelope-parametre eller lignende. Dertil kan man alternativt anvende de såkaldte Control Change-meddelelser, som nysgerrige læsere kan undersøge nærmere [i SuperColliders dokumentation](https://doc.sccode.org/Tutorials/A-Practical-Guide/PG_08_Event_Types_and_Parameters.html#MIDI%20output).

[^1]: MIDI, der står for *Musical Instrument Digital Interface* blev oprindeligt udviklet af en sammenslutning af instrumentproducenter, som ønskede en fælles protokol for hvordan forskelligt musikudstyr kunne kommunikere med hinanden. Den prototypiske anvendelse af MIDI er således når man kobler et MIDI-keyboard sammen med en synthesizer for at kunne spille på denne via keyboardets tangenter. Deraf kom terminologien *velocity*, som oprindeligt vedrørte hvor hurtigt en tangent blev trykket ned og i dag stadig bruges, uagtet at der ikke altid er tale om en fysisk tangent, som trykkes ned.

## Automatisk Note On og Note Off

Når vi bruger Pbind til at sende MIDI-output, sendes der automatisk Note On- og Note Off-meddelelser i overensstemmelse med de værdier vi angiver med `\dur` og `\legato`-nøglerne, præcis som hvis vi brugte SuperColliders lydserver. Nedenstående eksempel demonstrerer dette ved at veksle fra legato- til staccatofrasering.

```sc title="Automatisk Note On og Note Off"
(
~komposition = Pbind(
    \type, \midi,
    \midiout, ~daw,
    \chan, 0,

    \degree, Pseries(0, 1, 8).repeat(2),
    \dur, 0.5,
    \legato, Pseq([1.5, 0.1]).stutter(8)
).play;
)
~komposition.stop;
```
