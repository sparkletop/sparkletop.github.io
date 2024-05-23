---
tags:
    - Artikler
---

# Samples

Vi har indtil nu arbejdet med rent syntetisk dannede klange i SuperCollider. Men der er også gode muligheder for at arbejde med præindspillet lyd eller for den sags skyld live-lyd fra en mikrofon eller andet musikudstyr. Her koncentrerer vi os i første omgang om at arbejde med samples i form af lydfiler.

## Indlæsning af samples

For at arbejde med et sample/en lydfil, skal samplet indlæses i en såkaldt `Buffer`, som udgør et afgrænset område i lydserverens hukommelse. Det gør vi med `Buffer.read`, hvor første argument er lydserveren (i vores tilfælde `s`), og andet argument er stien til den lydfil, vi ønsker.

Her bruges et sample, der følger med SuperCollider, men man kan nemt arbejde med egne samples - erstat blot `Platform.resourceDir +/+ "sounds/a11wlk01.wav"` med stien til din egen lydfil. Stien kan genereres automatisk ved at trække filen ind i SuperCollider med musen, eller ved at copy-paste filen fra en mappe.

``` sc
(
// ~lydFilSti = "C:/lydfiler/minlydfil.wav";

~lydFilSti = Platform.resourceDir +/+ "sounds/a11wlk01.wav";

~sample = Buffer.read(s, ~lydFilSti);
)
```

Når samplet er indlæst i en `Buffer` under variabelnavnet `~sample`, kan vi bruge de forskellige instance methods, som knytter sig til buffere:

```sc
~sample.play;      // afspilning, anvendes kun til test

~sample.query;     // info om bufferens indhold
~sample.plot;      // visuel repræsentation
~sample.path;      // oprindelig sti
~sample.duration;  // længde i sekunder
```

## Afspilning med `PlayBuf`

Den mest enkle metode til afspilning af samples er at bruge UGen'en `PlayBuf`. Her vises hvordan vi kan styre afspilningen med argumenter til `PlayBuf.ar`:

```sc
(
{
	PlayBuf.ar(
		// antal kanaler
		numChannels: 1,

		// buffer nummer / Buffer objekt
		bufnum: ~sample,

		// afspilningshastighed - BufRateScale.kr tager højde for mismatch mellem serverens og lydfilens respektive samplerates
		rate: 1 * BufRateScale.kr(~sample),

		// reset-trigger, kan bruges til at angive spring til startposition
		trigger: 1,

		// startposition, målt i sample frames
		startPos: 0,

		// loop - start forfra, når vi rammer slutningen af bufferen (0 = nej, 1 = ja)
		loop: 0,

		// doneAction - hvad sker der, når vi rammer den sidste sample frame i bufferen?
		doneAction: Done.freeSelf
	)
}.play
)
```

Vi kan modulere flere af parametrene, fx afspilningshastighed, ved hjælp af andre UGens:

```sc
(
{
    PlayBuf.ar(1, ~sample,
        SinOsc.kr(2) * BufRateScale.kr(~sample)
    )
}.play;
)
(
{
    PlayBuf.ar(1, ~sample,
        LFNoise1.kr(0.5).range(0.5, 2) * BufRateScale.kr(~sample),
        loop: 1
    )
}.play;
```

Med et triggersignal, her skabt af UGen'en `Impulse`, kan vi springe hen til den position i bufferen, som er angivet med argumentet `startPos`.

```sc
(
// Fast startposition - midt i bufferen
{
	PlayBuf.ar(1, ~sample,
		trigger: Impulse.kr(5),
		startPos: 0.5 * BufFrames.kr(~sample),
    )
}.play;
)

(
// Dynamisk startposition, moduleret af en LFO
    PlayBuf.ar(1, ~sample,
		trigger: Impulse.kr(5),
		startPos: BufFrames.kr(~sample) * LFTri.kr(0.05).unipolar,
	)
}.play
)
```

## Ekstra fleksibilitet med `BufRd`

`BufRd` er mere fleksibel end `PlayBuf`, idet den tillader, at vi styrer læsningen af data fra bufferen direkte med en anden UGen. Det svarer lidt til når en pickupnål afspiller lyd fra en vinylplade, bortset fra at vi med et bredt udvalg af UGens kan flytte nålen rundt på meget forskellig vis. Til at styre afspilningspositionen angiver vi en UGen under `BufRead.ar`'s argument `phase`.

Ofte anvendes UGen'en `Phasor`, som skaber en lineær rampe fra start- til slutværdi (det er generelt sådan samples afspilles i digitale lydsystemer).

```sc
(
{
	BufRd.ar(
		numChannels: 2,
		bufnum: ~sample,
		// afspilningsposition i sample frames - en UGen, som angiver hvor i bufferen, vi læser data fra
		phase: Phasor.ar(0, BufRateScale.kr(~sample), 0, BufFrames.kr(~sample)),
		loop: 1
	)
}.play
)
```

Man kan anvende mange forskellige UGens som alternativ til `Phasor`. Her moduleres afspilningsposition i `BufRd` af henholdsvis en perkussiv envelope og lavfrekvent støj:

```sc
(
{
	// envelopes kan bruges til at gennemløbe en buffer
	var position = EnvGen.ar(Env.perc(0.1, 2)) * BufFrames.kr(~sample);
	BufRd.ar(1, ~sample, position, 1);
}.play;
)

(
{
	// interpoleringen mellem værdier i LFNoise1 (de lineære segmenter i outputtet) bliver til forskellige afspilningshastigheder
	var position = LFNoise1.ar(6).range(0, BufFrames.kr(~sample));
	BufRd.ar(1, ~sample, position, 1);
}.play;
)
```
