# Opsætning af MIDI output fra SuperCollider

SuperCollider kan sende data afsted på mange forskellige måder - MIDI er én af dem.
Dette kræver, at man enten forbinder sin computer med en ekstern hardware-synthesizer eller [sætter en virtuel MIDI-port](https://help.ableton.com/hc/en-us/articles/209774225-Setting-up-a-virtual-MIDI-bus) op til at facilitere MIDI-kommunikation mellem forskellige programmer på computeren.

## MIDI-output fra SuperCollider

Når DAW eller synthesizer er klar til at modtage MIDI-signal og MIDI-forbindelsen er sat op, enten virtuelt eller ved hjælp af et MIDI-eller USB-kabel, kører man i SuperCollider først `MIDIClient.init`. Dette får SuperCollider til at kontakte computerens MIDI-system og vise i post window hvilke MIDI-porte der er tilgængelige. Derfra noterer man navnet på den ønskede port og angiver det, når man opretter en `MIDIOut`:

``` sc title="MIDIClient og MIDIOut"
// Start MIDI-kommunikation
MIDIClient.init;

// Opret MIDIOut til DAW/synthesizer
~daw = MIDIOut.newByName("loopMIDI Port", "loopMIDI Port"); // Typisk portnavn på Windows
~daw = MIDIOut.newByName("IAC Driver", "Bus 1"); // Typisk portnavn på Mac
```

Så er vi klar til at sende MIDI-meddelelser fra SuperCollider. For at teste forbindelse kan vi sende en Note On- og en Note Off-meddelelse, hvorved vi burde

```sc title="Test MIDI-forbindelsen med toneanslag og -afslag"
~daw.noteOn(chan: 0, note: 64, veloc: 80);
~daw.noteOff(chan: 0, note: 64);
```
