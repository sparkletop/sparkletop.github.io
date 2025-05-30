---
tags:
    - Artikler
---

# Funktioner for den dovne programmør

Vi er nu nået til et emne, som er en gave til den dovne programmør, der ikke gider at skrive det samme sæt af instrukser mere end én gang. Heldigvis er det faktisk ofte en god idé at være doven på denne måde, fordi det er effektivt at indkapsle og genbruge sæt af instrukser, da det gør os i stand til at gøre mange ting med meget lidt kildekode. I programmering er *funktioner* et grundlæggende koncept, som er væsentligt at forstå. I SuperCollider og de fleste andre programmeringssprog er en funktion en defineret række af instrukser, der fungerer lidt ligesom de kodeblokke, vi kiggede på [ovenfor](a-eksekvering.md#flere-instrukser-ad-gangen). De er nyttige, hvis vi gerne vil gøre det samme mange gange, da vi i stedet for at skrive den samme kodeblok mange gange blot kan "kalde" funktionen.

## Hjemmelavede funktioner

Funktioner fungerer som sagt næsten ligesom de kodeblokke vi har set, hvor flere instrukser er omkranset af parenteser. Med funktioner bruger vi blot tuborgklammer (`{}`) i stedet for parenteser. Kører man linjen `{};` i SuperCollider, vil post window således vise `a Function`. For at gøre brug af funktioner, kan vi gøre følgende:

- Vi skriver mellem tuborgklammerne de instrukser, funktionen skal udføre, adskilt med semikolon.
- Dernæst [gemmer vi funktionen under en global variabel](a-variabler.md#globale-variabler), så vi kan referere til den igen andre steder i kildekoden.
- Hvis vi vil *kalde* funktionen, dvs. eksekvere de instrukser, som er indeholdt i funktionen, kan vi koble noget ekstra kode på variabelnavnet, nemlig `.value`. Dette er en *method*, hvilket bliver forklaret mere indgående [nedenfor](a-methods.md).

```sc title="En funktion"
// Vi gemmer funktionen under en variabel
~minFunktion = { "Hej fra funktionen".postln; };

// Vi kan henvise til funktionen
~minFunktion;

// Og vi kan kalde funktionen med .value
~minFunktion.value;
// -> se i post window, at instruksen bliver udført
```

## Output fra funktioner

Vi bruger ofte funktioner, fordi vi ønsker at producere "noget". Med andre ord er vi ofte interesserede i at opfange og bruge en funktions output. Outputtet fra en funktion er altid det, der fremgår i den sidste instruks/kodelinje i funktionen. Som eksempel kan vi lave en funktion, der trækker et tal fra et andet tal. Når vi eksekverer funktionen med `.value` vil vi derfor få resultatet af udregningen, som vi så kan bruge til det formål vi ønsker - herunder bliver den blot gemt under et andet variabelnavn og derefter vist i SuperColliders post window.

```sc title="En funktion til addition"
~minFunktion = {
    10 - 5;
};

~resultat = ~minFunktion.value;
~resultat.postln;
// -> 5
```

Fordi der kun er én kodelinje i funktionen, vil resultatet af denne kodelinje være funktionens output. I dette tilfælde er funktionen selvfølgelig ikke særligt nyttig, da den altid vil give samme resultat. Lad os derfor se på, hvordan vi kan bruge funktioner mere fleksibelt ved hjælp af det, der hedder *argumenter*.

## Input til funktioner: Argumenter

Funktioner kan også have en slags input, som vi kalder for *argumenter*. Lad os sige, at i stedet for at lægge de samme to tal sammen, hver gang funktionen kører, ønsker at angive de to tal og så få funktionen til at regne summen ud for os. I dette tilfælde kan vi indføre to argumenter, hvilket vi gør på den første kodelinje i funktionen ved hjælp af nøgleordet `arg`. Derefter kan vi angive værdier til argumenterne i parenteser, når vi bruger `.value`:

```sc title="Argumenter til funktioner"
~minFunktion = {
    arg kaffe, the;
    kaffe - the;
};

~minFunktion.value(100, 20);
// -> 80
```

### Standardværdier

Vi giver ofte argumenter nogle standardværdier, så funktionen kan fungere, selv hvis vi ikke angiver en værdi, når vi kalder den. På den måde får vi mulighed for at arbejde med en standardudgave og variationer derover.

```sc title="Argumenter og standardværdier"
~minFunktion = {
    arg kaffe = 10, the = 5;
    kaffe - the;
};

~minFunktion.value;
// -> 5
```

Angiver vi værdier, når vi kalder funktionen med `.value`, regner SuperCollider med, at vi skriver dem i den rækkefølge, de er indført i funktionens første linje. I vores tilfælde ovenfor betyder det, at vi skal angive `kaffe`, før vi kan angive `the`. Men med standardværdier kan vi vælge at springe et eller flere argumenter over og i stedet fortælle SuperCollider hvilket argument, vi ønsker at specificere.

```sc title="Navngivet argument ved funktionskald"
~minFunktion = {
    arg kaffe = 10, the = 5;
    kaffe - the;
};

~minFunktion.value(the: 20);
// -> -20
```

Når vi ikke angiver en værdi til et argument (ovenfor er `kaffe`-argumentet ikke specificeret), bruger funktionen i stedet standardværdien.

## Mellemregninger med lokale variabler

I praksis arbejder vi typisk med mere komplekse funktioner end de eksempmler vi har set ovenfor. I den sammenhæng er det særligt nyttigt at anvende [lokale variabler](a-variabler.md#lokale-variabler) til at holde styr på data i vores mellemregninger. Lad os eksempelvis tilføje en udregning til vores lille eksempel:

```sc title="Lokale variabler i funktioner"
~minFunktion = {
    arg kaffe = 10, the = 5;
    var drik = kaffe - the;
    drik * kaffe;
};

~minFunktion.value;
// -> 50
```

Indtil videre har vores funktioner ikke været musikalske, da de primært har skullet illustrere på enkel vis, hvordan vi bruger funktioner. Men én af anvendelserne af funktioner har at gøre med klangdannelse, hvor vi bruger en særlig funktionstype: UGen-funktioner.

## UGen-funktioner

Hidtil har funktionerne ovenfor kørt i SuperColliders [fortolker](a-brugerflade.md#brugerflade-fortolker-og-lydserver). Men den særlige funktionstype *UGen-funktioner* kører på lydserveren. Den noteres grundlæggende på samme måde som i eksemplerne ovenfor, men indeholder primært såkaldte UGens, som vi skal se nærmere på [i et senere kapitel](../04/a-ugens.md).

Før vi kan lave lyd med UGen-funktioner skal vi [boote lydserveren](a-eksekvering.md#fut-i-lydserveren). Derefter noterer vi `.play` umiddelbart efter funktionens afsluttende tuborgklamme. Her et eksempel med en sinustone, der svinger ved 440Hz (stop lyden igen med Ctrl/Cmd+Punktum):

```sc title="En UGen-funktion"
{ SinOsc.ar(440) }.play;
```

Ligesom ved almindelige funktioner er det sidste linje, der udgør outputtet, altså det vi hører[^1]. På samme måde som ovenfor kan vi bruge lokale variabler til at håndtere vores data, som UGen-funktioner svarer til signaler. Vi kan eksempelvis assigne vores sinustonegenerator til en lokal variabel, definere en anden lavfrekvent oscillator unden en anden variabel, og bruge sidstnævnte til at styre lydstyrken for førstnævnte:

[^1]: Når vi senere arbejder med [SynthDefs](../05/a-synthdef.md), er det værd at notere sig, at outputtet i stedet skal angives med en særlig UGen.

```sc title="Lokale variabler i UGen-funktioner"
{
    var tone = SinOsc.ar(440);
    var lfo = SinOsc.ar(2);
    tone * lfo;
}.play;
```

Bemærk i øvrigt hvad der sker, hvis vi øger frekvensen for LFO'en - så er vi i gang med en klangdannelsesteknik, der kaldes amplitudemodulation (AM).

```sc title="Simpel AM-syntese"
{
    var tone = SinOsc.ar(440);
    var lfo = SinOsc.ar(200);
    tone * lfo;
}.play;
```

Vi vender grundigt tilbage til UGen-funktioner [senere i bogen](../04/a-ugens.md).

## Indbyggede funktioner

Der findes en række indbyggede funktioner, som det kan være nyttigt at kende til. Dem kalder vi ikke ved at bruge `.value`, i stedet bruger vi et sæt parenteser efter funktionsnavnet. Her kan vi eksempelvis bruge funktionen `rrand` til at generere et tilfældigt tal eller funktionen `midicps` til at omregne fra MIDI-tonetal til frekvens:

```sc title="Indbyggede funktioner"
rrand(0, 10);
rrand(100, 200);

midicps(69);
midicps(57);

// En tilfældig MIDI-tone, omregnet til frekvens:
midicps(rrand(0, 127));
```

I det sidste eksempel her bliver den "inderste" funktion udført først, dvs. `rrand` vælger først sit tal, og derefter omregner `midicps` dette tal til en frekvens. Dette kaldes med et fancy udtryk "order of execution", hvilket såmænd blot betyder, at SuperCollider udregner de "inderste" funktionskald og matematiske operationer først, når vores kode eksekveres.
