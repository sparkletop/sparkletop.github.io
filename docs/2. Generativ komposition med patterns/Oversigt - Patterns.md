# Oversigt: Patterns

## 11 primære patterns

Start med at lære disse patterns at kende!

```sc
// Pseq - en fleksibel sequencer
Pbind(\degree, Pseq([0, -3, 1], 2)).play;

// Pser - endnu en fleksibel sequencer, med begrænsning af antal events
Pbind(\degree, Pser([0, -3, 1], 4)).play;

// Prand - vælger tilfældige elementer fra en liste
Pbind(\degree, Prand([0, 1, 2], inf)).play;

// Pxrand - vælger tilfældige elementer fra en liste, dog uden gentagelser
Pbind(\degree, Pxrand([0, 3, 4, 7], inf)).play;

// Pwrand - vælger tilfældige elementer fra en liste, med vægtede sandsynligheder
Pbind(\degree, Pwrand([0, -1, 1, 4], [0.6, 0.1, 0.1, 0.2], inf), \dur, 0.5).play;

// Pshuf - en fætter/kusine til Pseq, gentager en sekvens i tilfældig rækkefølge
Pbind(\degree, Pshuf([0, 1, 4, 6], 2), \dur, 0.5).play;

// Pwhite - tilfældige tal, ligeligt fordelt mellem min og max
Pbind(\degree, Pwhite(-7, 7)).play;

// Pexprand - tilfældige tal, eksponentielt fordelt mellem min og max
Pbind(\freq, Pexprand(400, 800)).play;

// Pgauss - tilfældige tal, normalfordelt omkring en middelværdi
Pbind(\pan, Pgauss(0, 0.5)).play; // brug evt. hovedtelefoner for at høre panorering

// Pbrown - en "fordrukken" stifinder
Pbind(\degree, Pbrown(-7, 7, 2), \dur, 0.2).play;

// Pseries - en trinvis udvikling med startværdi, interval og antal
Pbind(\degree, Pseries(7, -2, 8)).play;
```

## 3 vigtige Pattern-methods

Disse tre methods tillader os at arbejde mere fleksibelt med outputtet fra patterns.

```sc
// .repeat - gentager hele sekvenser
Pbind(\degree, Pshuf([0, 1, 3, 4], 2).repeat(2), \dur, 0.5).play; // bemærk ændring efter 1. gentagelse

// .stutter - gentager de enkelte værdier som genereres
Pbind(\degree, Pwhite(0, 9).stutter(3), \dur, 0.5).play;

// .clump - samler enkelte værdier til "akkorder"
Pbind(\degree, Pshuf([0, 1, 2, 4, 6, 8, 9], inf).clump(2)).play;
```

## 4 nyttige meta-Patterns

Disse patterns bruges ikke til at generere værdier, men til at sætte rammen om kompositioner.

```sc
// Pbind - knytter nøgler og patterns sammen i strømme af begivenheder (Events)
Pbind().play;

// Pmono og PmonoArtic - afspiller en enkelt tone, skifter løbende mellem værdier
Pmono(\default, \degree, Pwhite(-10, 10), \dur, Pexprand(0.1, 0.5)).play;

// Pdef - yderst handy til synkronisering og dynamisk udskiftning af patterns
Pdef(\melodi, Pbind(\degree, Pshuf([0, 1, 3, 4], inf), \dur, 0.5)).play; // kør linjen flere gange

// Pfindur - begrænser varigheden af en Pbind
Pfindur(3, Pbind(\degree, Pwhite(0, 7), \dur, Prand([0.25, 0.5, 0.125], inf))).play;
```
