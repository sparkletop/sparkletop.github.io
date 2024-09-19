---
tags:
    - Øvelser
---

# Øvelse 3: Minimalistisk komposition

Denne øvelse går ud på at anvende patterns til at skabe en enkel, minimalistisk komposition.

På dette trin i kurset kan øvelsen oplagt udføres som en komposition, der bliver realiseret over MIDI. På den måde kan man fx lade en standalone-synthesizer eller en DAW udføre klangdannelsen og koncentrere sig om de kompositionsmæssige aspekter som tonehøjde, rytmik og dynamik i SuperCollider.

Alternativt kan øvelsen sagtens udføres med standardlyden i SuperCollider. Senere i kurset designer vi egne lyde med [SynthDefs](../05. Envelope som kreativt virkemiddel/Art2-Synth og SynthDef.md), som kan erstatte den lidt kedelige standardlyd.

??? note "Opsætning af MIDI output fra SuperCollider"

    Dette kræver, at man enten bruger en ekstern hardware-synthesizer eller [sætter en virtuel MIDI-port](https://help.ableton.com/hc/en-us/articles/209774225-Setting-up-a-virtual-MIDI-bus) op til at facilitere MIDI-kommunikation mellem SuperCollider og det instrument eller den DAW, der skal producere lyden. Linket ovenfor henviser til ableton.com, men den virtuelle MIDI-forbindelse hverken kræver eller er særligt knyttet til Ableton Live.

    Når DAW eller synthesizer er klar til at modtage MIDI-signal og MIDI-forbindelsen er sat op, enten virtuelt eller ved hjælp af et MIDI-eller USB-kabel, kører man i SuperCollider først `MIDIClient.init`. Dette får SuperCollider til at kontakte computerens MIDI-system og vise i post window hvilke MIDI-porte der er tilgængelige. Derfra noterer man navnet på den ønskede port og angiver det, når man opretter en `MIDIOut`:

    ``` sc
    // Start MIDI-kommunikation
    MIDIClient.init;

    // Opret MIDIOut til DAW/synthesizer
    ~daw = MIDIOut.newByName("loopMIDI Port", "loopMIDI Port"); // Typisk portnavn på Windows
    ~daw = MIDIOut.newByName("IAC Driver", "Bus 1"); // Typisk portnavn på Mac
    ```

    Så er vi klar til at sende MIDI-meddelelser fra SuperCollider. For at teste forbindelse kan vi sende en Note On- og en Note Off-meddelelse, hvorved vi burde 

    ```sc
    ~daw.noteOn(chan: 0, note: 64, veloc: 80);
    ~daw.noteOff(chan: 0, note: 64);
    ```

## Opgave 1: En minimalistisk komposition

Skriv en komposition ved hjælp af `Pbind`. Kompositionen skal:

- Udvikle sig langsomt og gradvist, jævnfor minimalismen
- Tage udgangspunkt i et yderst begrænset rytmisk og tonalt materiale
- Anvende mindst to forskellige listebaserede patterns samt mindst ét tilfældighedsgenererende pattern

Toner og nodeværdier vælges først og noteres i lister under `~toner` og `~varigheder`

Der kan eksempelvis gøres brug af følgende virkemidler:

- Gentagelser med subtil variation
- Gradvis dynamisk udvikling og variation (lydstyrke)
- Skiftende oktavering
- Modaltransponering
- Minimal rytmisk udvikling
- Små forskelle på samtidigt klingende sekvenser

=== "Med MIDI"

    ```sc title="En minimalistisk kompositionsopgave"
    (
    // Vælg nogle få toner og nodeværdier
    ~toner = [   ];
    ~varigheder = [   ];

    Pbind(
        // MIDI-konfiguration
        \type, \midi,
        \midiout, ~daw,
        \chan, 0,

        // Tilføj egne patterns herunder
        \degree,   ,
        \octave,   ,
        \mtranspose,   ,

        \db,   ,
        
        \dur,   ,
        \legato,   ,
    ).play;
    )
    ```

=== "Uden MIDI"
    
    ```sc title="En minimalistisk kompositionsopgave"
    (
     // Vælg nogle få toner og nodeværdier
    ~toner = [   ];
    ~varigheder = [   ];

    Pbind(
        // Tilføj egne patterns herunder
        \degree,   ,
        \octave,   ,
        \mtranspose,   ,

        \db,   ,
        
        \dur,   ,
        \legato,   ,
    ).play;
    )
    ```

