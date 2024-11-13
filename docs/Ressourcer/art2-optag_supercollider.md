# Optag lyd fra SuperCollider

På et tidspunkt i din rejse med musik- og lydprogrammering ved hjælp af SuperCollider bliver det relevant at kunne bruge lyd fra SuperCollider i andre programmer. Det kan fx være vi vil eksportere en atmosfærisk lydtekstur skabt med granular syntese eller en melodi, vi har genereret ved hjælp af subtraktiv syntese og patterns. Hertil findes der i SuperCollider flere metoder, som passer til forskellige scenarier. Den interne optagelse er mest enkel og anbefales til begyndere, men at route signalet fra SuperCollider til en DAW er en fleksibel og nyttig metode.

## Intern optagelse af SuperColliders lydserver

SuperCollider har ganske udmærkede metoder til at optage outputtet fra lydserveren og lagre det i en lydfil.

### Enkel optagelse

At optage outputtet fra SuperColliders lydserver er ganske enkelt:

```sc title="Enkel optagelse med s.record"

// Start optagelsen
s.record;

// Spil noget lyd
{ Pulse.ar([220, 222]) * Env.perc.kr(2) }.play;

// Afslut optagelsen
s.stopRecording;

// Tilgå mappen hvor lydoptagelsen er gemt
Platform.recordingsDir.openOS;
```

Efter ovenstående tre linjer er kørt, vil SuperColliders post window vise hvor på din harddisk, lydfilen med optagelsen er gemt. Som udgangspunkt gemmes optagelser i en mappe, der kan findes med `Platform.recordingsDir`, og lydfilen får tildelt et navn med et unikt timestamp (således at flere optagelser foretaget efter hinanden ikke overskriver eksisterende filer).

Vi kan selv angive filsti og -navn, antal kanaler, samt evt. en varighed. Her eksempelvis en fil, der hedder optagelse.wav og gemmes under C:/samples, har to lydkanaler (dvs. stereo) og varer tre sekunder:

```sc title="Argumenter til s.record"
s.record(
    path: "C:/samples/optagelse.wav",
    numChannels: 2,
    duration: 3
);
// s.stopRecording er ikke nødvendigt her
```

De sidste argumenter til s.record (bus og node) kan læseren selv undersøge nærmere i [SuperColliders dokumentation](https://docs.supercollider.online/Classes/Server.html#-record).

### Optagelse med "præcist" begyndelsestidspunkt

`s.record` starter optagelsen et kort stykke tid efter, at kodelinjen er kørt. Det er lidt upraktisk, hvis man gerne vil starte optagelsen, præcist når man sætter en lyd i gang. Derfor kan man forberede optagelsen, så den kan startes på et præcist tidspunkt:

```sc title="Forberedt optagelse"
// Forbered optagelsen
s.prepareForRecord; // her kan path og numChannels evt. specificeres

// Start optagelse og lydproduktion
(
s.record(duration: 1.1); // Optagelsen stopper automatisk efter 1.1 sekund
{ Pulse.ar([220, 222]) * Env.perc.kr(2) }.play;
)
```

### Superhurtig NRT-optagelse

Hvis man har lavet en algoritme, der kan fremstille lydoptagelser der er lange eller et stort antal, kan det være nyttigt at få SuperCollider til at generere lydfilerne i "non-realtime" - deraf tilnavnet NRT. Det er et lidt mere kompliceret emne, som læseren selv kan studere nærmere i [SuperColliders dokmentation](https://docs.supercollider.online/Guides/Non-Realtime-Synthesis.html) samt i [en udmærket blog-post af Mads Kjeldgaard](https://madskjeldgaard.dk/posts/2019-08-05-supercollider-how-to-render-patterns-as-sound-files-using-nrt/).

## Routing fra SuperCollider til DAW

I mange tilfælde er det nyttigt at route lyden fra SuperCollider over til et andet program, fx en DAW. Det kan man gøre på tre overordnede måder, som nævnt i [Abletons udmærkede oversigt](https://help.ableton.com/hc/en-us/articles/360010526359-How-to-route-audio-between-applications):

- Analog loopback
- Digital loopback
- Virtuel audio routing

Analog og digital loopback beror på, at der sendes lyd ud af et lydkorts udgange og direkte tilbage via lydkortets indgange. Nogle lydkort-drivere understøtter, at dette kan gøres uden fysiske kabler. Disse tilgange kræver typisk et eksternt lydkort.

Virtuel audio routing kan udføres uden særlig hardware (eksternt lydkort) og er derfor en meget anvendt tilgang. Det udføres som regel med tredjepartssoftware, der figurerer i styresystemet som en ekstra lydkortdriver. Denne kan så både bruges som in- og output. I den ovennævnte oversigt fra Ableton fremgår en række sådanne redskaber til Mac og Windows. På Linux findes der ganske glimrende redskaber som [jack](https://jackaudio.org/) og [pipewire](https://www.pipewire.org/).

### SuperCollider til Reaper via ReaRoute

Som eksempel på virtuel audio routing kan vi tage det scenarie, at en windows-bruger vil sende lyd fra SuperColliders lydserver til DAW'en Reaper. Dette kan gøres ved hjælp af systemet [ReaRoute](https://www.youtube.com/watch?v=OnfTq8EtluU), der følger med Reaper, hvis man vinger det af under installationen. Fremgangsmåden er som følger:

**Reaper**

:   - Start Reaper.
    - Armér et spor til optagelse og vælg ReaRoute som audio-input.
    ![Vælg ReaRoute som input i Reaper](media/rearoute.png)

**SuperCollider**

:   - Indstil SuperColliders lydserver til at bruge ReaRoute som output.
    - Start eller genstart SuperColliders lydserver.    
    ```sc title="Vælg ReaRoute som output i SuperCollider"
    // Angiv ReaRoute som audio device (lydkort) for lydserveren
    Server.default.options.device = "ASIO : ReaRoute ASIO (x64)"
    
    // Start eller genstart lydserveren
    s.boot; // eller s.reboot;
    
    // Test at lyden går igennem til Reaper
    { PinkNoise.ar * Env.perc.kr(2) }.play;
    ```

