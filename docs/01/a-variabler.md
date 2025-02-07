---
tags:
    - Artikler
---
# Brug af variabler

Vi kan opbevare forskellige former for data i computerens hukommelse ved hjælp af variabler. Man kan forestille sig en skuffe, som man sætter en seddel på med en kort beskrivelse af indholdet. Når man så skal finde indholdet frem igen eller putte noget nyt indhold i, finder man blot skuffen med den rette seddel frem. Variabler fungerer lidt på samme måde: Når man opretter en variabel, gemmer man et objekt under et bestemt navn. Når man så senere skal bruge objektet igen, henviser man blot til variablens navn. Og nu vi er ved variabelnavne: De starter altid med et lille begyndelsesbogstav[^1]. Hvis vi prøver at bruge variabelnavnet `~Kaffe`, vil vi derfor få en fejlmeddelelse. Brug i stedet `~kaffe`.

## Globale variabler

Der er to typer variabler: *Globale* og *lokale* variabler. Globale variabler kan anvendes (næsten) overalt i et SuperCollider-program. De noteres med tegnet tilde (`~`), direkte efterfulgt af et passende navn, fx sådan her:

```sc title="Globale variabler"
~trin;
~akkord;

// Alle enkeltbogstaver fra `a` til `z` udgør også globale variabler:
a;
b;
```

For at bruge variabler skal vi kunne tilgå og definere deres indhold.


For at tilgå variablen, dvs. finde dens indhold frem og bruge det til noget, bruger vi slet og ret variabelnavnet, fx `~trin`.
- For at definere eller ændre variablens indhold, bruger vi først variabelnavnet efterfulgt af et lighedstegn, og det nye indhold på højre side af lighedstegnet: `~trin = 2`. Dette kaldes også *assignment*, fordi vi i dette tilfælde "assigner" tallet 2 til variable med navnet `~trin`.

``` sc title="Grundlæggende brug af variabler"
~trin.postln; // tjek først variablens indhold
~trin = 5;    // gem et tal
~trin.postln; // tjek variablens indhold igen

//Vi kan efterfølgende tilgå og bruge variablens indhold blot ved at bruge dens navn:
~trin - 10;
```

En variabel kan efterfølgende let omdefineres ved at foretage en ny assignment:

``` sc title="At omdefinere indholdet af en variabel"
// Vi kan også omdefinere indholdet med endnu en assignment:
~trin = 50;
~trin.postln;

// Variablens nuværende indhold kan anvendes, når man regner en ny værdi ud og gemmer under samme variabelnavn:
~trin = ~trin * 10 + 7;
~trin.postln;
```

Der findes en mindre teknisk forskel på variabler som `~trin` og `t`, men på begynderniveau er det ikke nødvendigt at skelne mellem de to[^2].

## Lokale variabler

Vi bruger blandt andet lokale variabler til at gemme data som akkorder og rytmer, men også til at [definere signalflowet](../04/a-ugens.md#signalflow-med-lokale-variabler), når vi designer lyde.

Lokale variabler defineres med nøgleordet `var` i stedet for `~`. De kan udelukkende tilgås inden for en afgrænset kodeblok bestående af almindelige parenteser eller tuborg-parenteser, og de skal oprettes i begyndelsen af den kodeblok, de tilhører.

``` sc title="En lokal variabel"
(
var akkord = [0, 1, 4];
akkord.postln;
// Inden for kodeblokken: viser variablens indhold
)

akkord.postln;
// Uden for kodeblokken: giver en fejlmeddelelse
```

[^1]: Teknisk set skal variable begynde med småt begyndelsesbogstav fordi stort begyndelsesbogstav er forbeholdt de såkaldte [klassenavne](a-methods.md#class-methods).

[^2]: Rent teknisk udgør variabler som `~kaffe` og `~the` såkaldte *environment variables*, hvor variabler som `a`, `b` og `c` er globale variabler i mere klassisk forstand. Med environment variables kan man skifte mellem environments og dermed adskille det man i mere avanceret programmering kalder for [*namespaces*](https://en.wikipedia.org/wiki/Namespace). Som begynder skal man ikke bekymre sig om dette, da vi på grundlæggende niveau udelukkende arbejder inden for ét environment. Vi kan dermed for enkelhedens skyld betragte environment variables som globale variabler.
