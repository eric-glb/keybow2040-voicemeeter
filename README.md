# keybow2040-voicemeeter

### Keybow2040 tailored for my needs:
  - USB HID *and* Midi keys to pilot Voice Meeter Banana, OS media control, Meet and Teams mute switchs;
  - Visual feedback when muting/unmuting mic;
  - standby mode (all leds off) if not used for a certain amount of time (10 min).

### Demonstration

https://user-images.githubusercontent.com/89578893/131130065-ba3a7a3c-cb5e-4299-a4bc-061b160bbfd6.mp4

### What it does control 

![voicemeeter-keybow](https://user-images.githubusercontent.com/89578893/131132043-4670462a-669e-4495-9d9d-ae1357e7f5e8.png)

And also:
- Speakers and Headphones presets;
- Mute switch for Google Meet;
- Multimedia: Previous, Next Track and Play/Pause; Volume keys (hooked to A1 output level in Voice Meeter).

NB:  
As Mute switch for Teams is keyboard layout dependend (CTRL+SHIFT+M), I use a french AZERTY mapping for adafruit_hid.  
Please read the specific [README.md](lib/adafruit_hid_fr/README.md) for details.

### Inspiration taken from:
- https://www.tomshardware.com/how-to/build-rp2040-powered-shortcut-keypad

### My installation relies on:
- Pimoroni keybow2040-circuitpython:  
    https://github.com/pimoroni/keybow2040-circuitpython
- VB-Audio Voice Meeter Banana (worth the price):  
    https://vb-audio.com/Voicemeeter/banana.htm
- VB-Audio Macro Buttons (installed with Voice Meeter):  
    See [Voice Meeter Banana documentation](https://vb-audio.com/Voicemeeter/VoicemeeterBanana_UserManual.pdf), p. 37.
- VB-Audio Virtual Audio Cable to route Spotify client to VoiceMeeter input #3, using the system mixer configuration:  
    https://vb-audio.com/Cable/index.htm

### Debug:
- Use PuTTY on Serial line COM4 (YMMV), speed 115200 bauds.

### My VB-Audio Voice Meeter Banana settings:

    Input #1 -> USB Blue Yeti Mic            -> to B1
    Input #2 -> Laptop Mic (unused)
    Input #3 -> VB-Audio Virtual Audio Cable -> to A1 and A2
    A1       -> Laptop jack output           -> speakers
    A2       -> USB soundcard                -> headphones

    Hook Volumes Keys (For Level Output A1)

Use [configs/VoiceMeeter-Midi-keybow.xml](configs/VoiceMeeter-Midi-keybow.xml) MIDI map for the Voice Meeter MIDI config.  
Basically:

    MIDI Mapping for CircuitPython Audio:
    Mute Strip #1 -> Note on C1 (36)
    Mute Strip #3 -> Note On E1 (40)
    Mute BUS A2   -> Note On G#1 (44)

### My VB-Audio Macro Buttons settings:

Use [configs/MacroButtons-Midi-keybow.xml](configs/MacroButtons-Midi-keybow.xml) for the Voice Meeter MIDI config.

### Key mapping:

    ┌─┬────────────┬─┬───────────┬──┬────────────────┬──┬──────────────┐
    │3│Google Meet │7│Previous   │11│Next            │15│Play/Pause    │
    │ │Mute        │ │Track      │  │Track           │  │              │
    ├─┼────────────┼─┼───────────┼──┼────────────────┼──┼──────────────┤
    │2│Headphones  │6│MIDI Cable │10│MIDI Headphones │14│Speakers      │
    │ │Preset      │ │Volume Up  │  │Volume Up       │  │Volume Up     │
    ├─┼────────────┼─┼───────────┼──┼────────────────┼──┼──────────────┤
    │1│Speakers    │5│MIDI Cable │ 9│MIDI Headphones │13│Speakers      │
    │ |Preset      │ │Volume Down│  │Volume Down     │  │Volume Down   │
    ├─┼────────────┼─┼───────────┼──┼────────────────┼──┼──────────────┤
    │0│MIDI Mic    │4│MIDI Cable │ 8│MIDI Headphones │12│Speakers      │
    │ │Mute        │ │Mute       │  │Mute            │  │Mute          │
    └─┴────────────┴─┴───────────┴──┴────────────────┴──┴──────────────┘
