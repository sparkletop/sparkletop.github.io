---
tags:
    - Artikler
---
# Brug af variabler

Vi kan opbevare forskellige former for data i computerens hukommelse ved hjælp af variabler. Variabler kan forstås som en slags opbevaringsrum, hvor vi kan gemme ting og finde dem frem igen senere. Der er to typer variabler: *Globale* og *lokale* variabler.

## Globale variabler

Globale variabler kan tilgås (næsten) overalt i et SuperCollider-program. De noteres med "~", direkte efterfulgt af et passende navn, fx sådan her:

```sc
~alder;
~kaffekop;
```

Alle enkeltbogstaver (a-z) udgør også globale variabler:

``` sc
a;
q;
```

For at kunne bruge variabler skal vi kunne definere, tilgå og ændre deres indhold.

- For at tilgå variablen, dvs. finde dens indhold frem og bruge det til noget, bruger vi slet og ret variabelnavnet, fx `~alder`.
- For at definere eller ændre variablens indhold, bruger vi variabelnavnet på venstre side af et lighedstegn, og det nye indhold på højre side: `~alder = 10`. Dette kaldes også *assignment*.

``` sc title="Grundlæggende brug af variabler"
~alder.postln; // tjek først variablens indhold
~alder = 23;   // gem et tal (også kendt som "assignment")
~alder.postln; // tjek variablens indhold igen

//Vi kan efterfølgende tilgå og bruge variablens indhold blot ved at bruge dens navn:
~alder * 100;
```

En variabel kan efterfølgende let omdefineres:

``` sc title="At omdefinere indholdet af en variabel"
// Vi kan også omdefinere indholdet med endnu en assignment:
~alder = 50;
~alder.postln;

// Variablens nuværende indhold kan anvendes, når man regner en ny værdi ud og gemmer under samme variabelnavn:
~alder = ~alder * 10 + 7;
~alder.postln;
```

### Små begyndelsesbogstaver

OBS: Variabelnavne SKAL have lille begyndelsesbogstav (fordi klassenavne har stort begyndelsesbogstav). Se fx hvad der sker, når vi prøver at bruge variabelnavnet `~Kaffe`:

```sc
~Kaffe   // giver fejlmeddelelse
```

## Lokale variabler

Kan udelukkende tilgås inden for en afgrænset kodeblok bestående af `()` eller `{}`. Lokale variabler defineres med nøgleordet `var` og anvendes uden `~`.

``` sc title="Lokale variabler
(
var model = "Fabia";
model.postln; // inden for kodeblokken: viser variablens indhold
)

model.postln; // uden for kodeblokken: giver en fejlmeddelelse
```

Lokale variabler bruges blandt andet til at gemme data som akkorder, rytmer, men også til at definere signalflowet, når man designer lyde i en såkaldt SynthDef. Det vender vi tilbage til senere.
