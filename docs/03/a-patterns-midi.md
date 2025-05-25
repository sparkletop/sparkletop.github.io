---
tags:
    - Artikler
---

# Pattern-komposition med MIDI-output

Når vi lærer at arbejde med patterns som kompositionsredskab, er det oplagt at anvende en mere interessant lydkilde end den indbyggede standardlyd i SuperColliders lydserver. Vi kommer senere til at [designe vores egne lyde med SuperColliders lydserver](../05/a-synthdef.md), men for nuværende kan det være mere inspirerende at bruge vores patterns til MIDI-komposition. Det gøres på følgende måde:

- Opret en virtuel MIDI-port til kommunikation mellem SuperCollider og DAW
- Indstil DAW til at modtage MIDI-meddelelser på et spor med et virtuelt instrument
- Indstil SuperCollider til at sende MIDI-meddelelser med `MIDIClient.init` og `MIDIOut.newByName`
- Spil på instrument-plugin'et i DAW'en ved hjælp af `Pbind`

Herunder kigger vi nærmere på disse trin.

## Opsætning og test af MIDI-kommunikation

### Virtuel MIDI-port og opsætning af DAW

For at sende MIDI-signaler fra SuperCollider til en DAW på samme computer, skal man sætte en virtuel MIDI-port op til at skabe forbindelse mellem de to programmer. Dette er heldigvis enkelt - på Windows kan man bruge programmet *loopMIDI* og på Mac kan man opsætte en virtuel port med den såkaldte *IAC Driver*. Dette forklares ganske fint i [en guide fra Ableton](https://help.ableton.com/hc/en-us/articles/209774225-Setting-up-a-virtual-MIDI-bus).

Man sætter derefter DAW'en op, så den modtager MIDI-meddelelser fra den virtuelle MIDI-port på et spor, hvor man har sat et instrument-plugin op. Det vil føre for vidt at introducere til dette for alle tænkelige DAW-programmer her. Men1 denne funktionalitet er heldigvis dokumenteret grundigt andre steder, da det svarer til hvordan man tilslutter et MIDI-keyboard. Se eksempelvis instrukserne for [Reaper](https://youtu.be/LmEy49PH9p8?feature=shared&t=225), [Ableton Live](https://help.ableton.com/hc/en-us/articles/360011853159-MIDI-controllers-FAQ), [Logic Pro](https://support.apple.com/guide/logicpro/connect-midi-keyboards-and-modules-lgcpebe6b756/10.7/mac/11.0), [Ardour](https://youtu.be/ACJ1suTVouw?feature=shared&t=778) og så videre.

Alternativt kan man sende MIDI-meddelelser fra SuperCollider til et stykke hardware som er tilsluttet computeren via MIDI, fx en ekstern synthesizer. For enkelhedens skyld omtaler vi dog her modtageren af MIDI-meddelelser som en [DAW](https://en.wikipedia.org/wiki/Digital_audio_workstation). Jeg forudsætter herunder, at den virtuelle eller fysiske forbindelse er etableret, og at modtageren af vores MIDI-signal er klar til at modtage meddelelser.

### Opsætning af MIDI-output fra SuperCollider

Når DAW er klar til at modtage MIDI-signal via en virtuel MIDI-port, starter man i SuperCollider med at køre linjen `MIDIClient.init`. Dette får SuperCollider til at kontakte computerens MIDI-system og vise i post window hvilke MIDI-porte der er tilgængelige. Derfra noterer man navnet på den ønskede port og bus. Dem angiver man så, når man med klassen `MIDIOut` og method'en `.newByName` opretter en forbindelse til  output og gemmer dette under en global variabel.

``` sc title="Klargøring af MIDI med MIDIClient"
// Start MIDI-kommunikation
MIDIClient.init;

// I post window ses nu bl.a. to nyttige lister, MIDI Sources og MIDI Destinations
// På Windows kan det fx se sådan ud:
MIDI Sources:
    MIDIEndPoint("loopMIDI Port", "loopMIDI Port")
MIDI Destinations:
    MIDIEndPoint("Microsoft GS Wavetable Synth", "Microsoft GS Wavetable Synth")
    MIDIEndPoint("loopMIDI Port", "loopMIDI Port")
```

Da vi skal sende MIDI ud af SuperCollider, kigger vi på listen over `MIDI Destinations` i post window for at identificere den ønskede destination. Vi noterer os det, der står mellem parenteserne efter `MIDIEndPoint`:

```sc title="Opret MIDIOut til DAW/synthesizer"
// Typisk portnavn på Windows
~daw = MIDIOut.newByName("loopMIDI Port", "loopMIDI Port");

// Typisk portnavn på Mac
~daw = MIDIOut.newByName("IAC Driver", "Bus 1");
```

### Test forbindelsen

Så er vi klar til at sende MIDI-meddelelser fra SuperCollider. For at teste forbindelse kan vi sende en Note On- og en Note Off-meddelelse, hvorved vi kan se eller høre på modtageren, at der spilles en tone.

```sc title="Test MIDI-forbindelsen med toneanslag og -afslag"
~daw.noteOn(chan: 0, note: 64, veloc: 80);
~daw.noteOff(chan: 0, note: 64);
```

Hvis der ikke spiller en tone, kan du tjekke i SuperColliders post window om der skulle være nogen fejlmeddelelser, samt i den DAW/synthesizer, der skal modtage meddelelserne.

## Patterns og MIDI-begivenheder

### Særlige nøgler til MIDI-kommunikation

For at bruge `Pbind` som MIDI-generator skal vi angive et par oplysninger under nogle særlige nøgler:

`\type`

:   Med denne nøgle angiver vi hvilken event-type, vores Pbind skal genererere. Vi har hidtil arbejdet med den event-type, som er default, nemlig den såkaldte `\note`-event. Når vi angiver `\midi` her, fortæller vi Pbind, at der skal produceres MIDI-meddelelser i stedet for meddelelser til lydserveren.

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

### Automatisk Note On og Note Off

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

Når man arbejder med patterns som MIDI-generator til at spille på et andet stykke software eller hardware, vil det hurtigt blive tydeligt, hvis vi stopper kompositionen i utide med Ctrl-/Cmd-punktum. Derved stopper vi nemlig SuperCollider i at afsende den sidste Note Off-meddelelse, hvilket betyder, at den sidste tonen vil blive hængende i DAW/synth (medmindre der er tale om et instrument, som ignorerer Note Off-meddelelser). For at undgå dette, gemmer vi `Pbind().play` under en variabel, og vi kan så efterfølgende stoppe forløbet med `.stop`, som vist ovenfor.

### Automatisk opsætning af MIDI-nøgler med Pbindf

Som vi har set [tidligere](a-sammensaetning.md#at-kombinere-pbinds-med-pbindf), kan vi bruge `Pbindf` til at genbruge en tidligere defineret `Pbind`. På den måde kan vi definere vores MIDI-nøgler én gang for alle og derefter undgå at skrive dem igen.

```sc title="Genbrug af MIDI-nøgler med Pbindf"
(
~midi = Pbind(
    \type, \midi,
    \midiout, ~daw,
    \chan, 0,
);

~klaver = Pbindf(~midi,
    \degree, Pbrown(-2, 4, 3),
    \dur, Prand([0.5, 1], inf),
).play;
~bas = Pbindf(~midi,
    // Vi sender her på en anden MIDI-kanal
    // ved at overskrive \chan-nøglen 
    \chan, 1,
    \octave, 3,
    \degree, Pseq([1, -3], inf),
).play;
)
```

## Begrænsninger ved MIDI-protokollen

Når vi komponerer med MIDI, er det væsentligt at notere sig dennes begrænsninger. Almindelige *Note On* og *Note Off*-meddeleser i MIDI indeholder blot information om hvilken MIDI-tone, det drejer sig om, samt en parameter, der kaldes *velocity*, hvilket ofte kobles med lydstyrke[^1]. Begge disse oplysninger befinder sig i intervallet 0-127, så hvis vi manuelt skal sende disse beskeder (fx med `~daw.noteOn`), skal værdierne befinde sig inden for dette interval. Bruger vi Pbind, kan vi heldigvis anvende de fleste af de nøgler, vi kender, som `\degree`, `\octave`, `\db` osv. Samtidig kan vi styre, *hvornår* meddelelserne afsendes, og med `\legato`-nøglen hvor længe besemte toner skal "holdes". Dermed har vi altså kontrol over følgende musikalske parametre:

- Tonehøjde, i form af MIDI-tonetal
- Lydstyrke, i form af MIDI-velocity
- Rytmik og frasering, i form af meddelelsernes timing

Vi har *ikke* kontrol over parametre som klang, envelope-parametre eller lignende. Dertil kan man evt. anvende de såkaldte Control Change-meddelelser, som nysgerrige læsere kan undersøge nærmere [i SuperColliders dokumentation](https://doc.sccode.org/Tutorials/A-Practical-Guide/PG_08_Event_Types_and_Parameters.html#MIDI%20output).

[^1]: MIDI, der står for *Musical Instrument Digital Interface* blev oprindeligt udviklet af en sammenslutning af instrumentproducenter, som ønskede en fælles protokol for hvordan forskelligt musikudstyr kunne kommunikere med hinanden. Den prototypiske anvendelse af MIDI er således når man kobler et MIDI-keyboard sammen med en synthesizer for at kunne spille på denne via keyboardets tangenter. Deraf kom terminologien *velocity*, som oprindeligt vedrørte hvor hurtigt en tangent blev trykket ned og i dag stadig bruges, uagtet at der ikke altid er tale om en fysisk tangent, som trykkes ned.
