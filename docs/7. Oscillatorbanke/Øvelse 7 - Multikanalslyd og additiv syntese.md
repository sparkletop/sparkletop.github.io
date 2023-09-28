# Øvelse 6A: Additiv syntese og multikanalslyd

Start først et par visuelle redskaber - spektrumanalyse og VU-meter
(
s.options.numOutputBusChannels = 8;
s.reboot;
s.meter.window.alwaysOnTop = true;
FreqScope(server: s).window.alwaysOnTop = true;
)

 6A.1: Monofoni - fordoblet

## Fremstil den samme sinustone i begge lydkanaler ved hjælp af .dup eller ! 
(
{
	var sig = SinOsc.ar * 0.1;
	sig    ;  // <-- udfyld her
}.play;
)

 6A.2: Stereofoni med Pan2

Løs følgende opgaver vha. Pan2
## Fremstil en sinustone i venste side af stereofeltet
## Fremstil en sinustone i højre side af stereofeltet
## Fremstil en sinustone midt i stereofeltet
## Fremstil en sinustone, der ved hjælp af modulation bevæger sig mellem højre og venstre side af stereofeltet

(
{
	var sig = SinOsc.ar * 0.1;
	Pan2.ar(sig,    );  // <-- udfyld
}.play;
)

 6A.3: Additiv syntese

OBS: Nedenstående SynthDef er en udmærket skabelon som kan udvides og udfyldes med eget lyddesign.

Fremstil en kompleks klang ved hjælp af additiv syntese med sinustoner:
## Klangen skal bestå af mindst tre forskellige overtoner (harmonisk forhold til freq)
## Klangen skal derudover indeholde mindst to forskellige partialtoner (inharmonisk forhold til freq)
## Hver tone skal tildeles sin egen unikke envelope (med forskellige attack- og release-tider)
## Hver tone skal tildeles sin egen max-amplitude
## Tonerne skal summeres (dette kan gøres automatisk, hvis man anvender Mix.fill)

Bonus:
## Tilføj et element af filtreret støj helt i begyndelsen af anslaget
## Tilføj en sub-oktav, dvs. en tone, som klinger en oktav under freq
## Gør mængden (lydstyrke) af anslagsstøj og sub-oktav justerbar ved at tilføje argumenter og varier disse ved at tilføje patterns og nøgler til Pbind-kompositionen

(
SynthDef(\additivo, {
	arg freq = 440, pan = 0, amp = 1,
	attack = 0.01, release = 1, gate = 1;
	var env = EnvGen.kr(Env.asr(attack, 1, release), gate, doneAction: Done.freeSelf);
	// udfyld herunder
	var sig = Pulse.ar(freq);

	sig = Pan2.ar(sig * env, pan, amp);
	Out.ar(0, sig);
}).add;
)

(
Afprøv din SynthDef med denne enkle komposition
TempoClock.tempo = 125/60;
Pbind(
	\instrument, \additivo,
	\degree, Pshuf([0, 1, 3, 4], 4).repeat(4),
	\mtranspose, Pbrown(-2, 2, 1).stutter(16),
	\dur, Pseq([1/4, 1/8, 1/16, 1/16], inf) * 4,
	\attack, Pexprand(0.001, 0.02),
	\release, Pexprand(0.5, 1.5),
	\legato, Pgauss(1, 0.2),
).play;
)