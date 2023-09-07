# Variabler

Vi kan opbevare forskellige former for data i computerens hukommelse ved hjælp af variabler.

Variabler kan forstås som en slags opbevaringsrum, hvor vi kan gemme ting og finde dem frem igen senere.

Der er to typer variabler: Globale og lokale variabler

## Globale variabler

Kan tilgås (næsten) overalt i et SuperCollider-program
Noteres med "~", direkte efterfulgt af et passende navn    
```sc
~alder;
~kaffekop;
```

Alle enkeltbogstaver (a-z) udgør også globale variabler
``` sc
a;
q;
```

For at kunne bruge variabler skal vi kunne definere, tilgå og ændre deres indhold.
Indholdet på højre side af lighedstegnet gemmes under variablen ~alder:

``` sc
~alder.postln; // tjek først variablens indhold
~alder = 23;   // gem et tal (også kendt som "assignment")
~alder.postln; // tjek variablens indhold igen
```

Vi kan tilgå og bruge variablens indhold blot ved at bruge dens navn:

``` sc
~alder * 100;
```

Vi kan omdefinere indholdet med endnu en assignment:

``` sc
~alder = 50;
~alder.postln;
```

Variablens nuværende indhold kan anvendes, når man regner en ny værdi ud og gemmer under samme variabelnavn

~alder = ~alder * 10 + 7;
~alder.postln;

### Store og små beg

OBS: Variabelnavne SKAL have lille begyndelsesbogstav (fordi klassenavne har stort begyndelsesbogstav)
~Kaffe   // giver fejlmeddelelse

## Lokale variabler
Kan tilgås inden for en afgrænset kodeblok bestående af () eller {}.
Lokale variabler defineres med nøgleordet "var" og anvendes uden tilde (~)   
``` sc
(
var model = "Fabia";
model.postln; // inden for kodeblokken: viser variablens indhold
)

model.postln; // uden for kodeblokken: giver en fejlmeddelelse
```
