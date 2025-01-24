---
tags:
    - Artikler
---
# Brug af variabler

Vi kan opbevare forskellige former for data i computerens hukommelse ved hjælp af variabler. Variabler kan forstås som en slags opbevaringsrum, hvor vi kan gemme ting og finde dem frem igen senere. Der er to typer variabler: *Globale* og *lokale* variabler.

## Globale variabler

Globale variabler kan tilgås (næsten) overalt i et SuperCollider-program. De noteres med tegnet tilde (`~`), direkte efterfulgt af et passende navn, fx sådan her:

```sc
~alder;
~kaffekop;
```

Alle enkeltbogstaver fra `a` til `z` udgør også globale variabler:

```sc
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

Der findes en mindre teknisk forskel på variabler som `~kaffe` og `k`, men på begynderniveau[^1] er det ikke nødvendigt at skelne mellem de to.

### Variabelnavne starter med et lille bogstav

Variabelnavne starter altid med et lille begyndelsesbogstav, fordi stort begyndelsesbogstav er forbeholdt klassenavne. Hvis vi prøver at bruge variabelnavnet `~Kaffe`, vil vi derfor få en fejlmeddelelse. Brug i stedet `~kaffe`.

## Lokale variabler

Kan udelukkende tilgås inden for en afgrænset kodeblok bestående af `()` eller `{}`. Lokale variabler defineres med nøgleordet `var` og anvendes uden `~`.

``` sc title="Lokale variabler"
(
var model = "Fabia";
model.postln; // inden for kodeblokken: viser variablens indhold
)

model.postln; // uden for kodeblokken: giver en fejlmeddelelse
```

Lokale variabler bruges blandt andet til at gemme data som akkorder og rytmer, men også til at definere signalflowet, når man designer lyde i en såkaldt SynthDef. Det vender vi tilbage til senere.

[^1]: Rent teknisk udgør variabler som `~kaffe` og `~the` såkaldte *environment variables*, hvor variabler som `a`, `b` og `c` er globale variabler i mere klassisk forstand. Med environment variables kan man skifte mellem environments og dermed adskille det man i mere avanceret programmering kalder for [*namespaces*](https://en.wikipedia.org/wiki/Namespace). Som begynder skal man ikke bekymre sig om dette, da vi på grundlæggende niveau udelukkende arbejder inden for ét environment. Vi kan dermed for enkelhedens skyld betragte environment variables som globale variabler.
