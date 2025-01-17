---
tags:
    - Øvelser
---

# Øvelse 3: Minimalistisk komposition

Denne øvelse går ud på at anvende patterns til at skabe en enkel, minimalistisk komposition.

På dette trin i kurset kan øvelsen oplagt udføres som en komposition, der bliver realiseret over MIDI. På den måde kan man fx lade en standalone-synthesizer eller en DAW udføre klangdannelsen og koncentrere sig om de kompositionsmæssige aspekter som tonehøjde, rytmik og dynamik i SuperCollider. Se evt. [guiden til MIDI-output fra SuperCollider](../Ressourcer/art1-MIDI-output.md).

Alternativt kan øvelsen sagtens udføres med standardlyden i SuperCollider. Senere i kurset designer vi egne lyde med [SynthDefs](../05. Envelope som kreativt virkemiddel/Art2-Synth og SynthDef.md), som kan erstatte den lidt kedelige standardlyd.

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

=== "Mulighed 1: Med MIDI-output til DAW"

    Følg først [vejledning til MIDI-output fra SuperCollider](../Ressourcer/art1-MIDI-output.md).

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

=== "Mulighed 2: Med SuperColliders standardlyd"
    
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

