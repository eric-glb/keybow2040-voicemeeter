# keybow2040-voicemeeter

### Keybow2040 tailored for my needs:

  - USB HID *and* Midi keys to pilot Voice Meeter Banana, OS media control, Meet and Teams mute switchs
  - Visual feedback when muting/unmuting mic
  - Standby mode (all leds off) if not used for a certain amount of time (15 min.)

https://user-images.githubusercontent.com/89578893/130957119-04bb56d3-d831-4dda-bfc8-a24a935e4dee.mp4


### Inspiration taken from:

- https://www.tomshardware.com/how-to/build-rp2040-powered-shortcut-keypad


### My installation relies on:

- [Pimoroni keybow2040](https://shop.pimoroni.com/products/keybow-2040)
- [VB-Audio Voice Meeter Banana](https://vb-audio.com/Voicemeeter/banana.htm) (worth the price)  
- VB-Audio Macro Buttons (installed with Voice Meeter; see [Voice Meeter Banana documentation](https://vb-audio.com/Voicemeeter/VoicemeeterBanana_UserManual.pdf), p. 37)
- [VB-Audio Virtual Audio Cable](https://vb-audio.com/Cable/index.htm) to route Spotify client to VoiceMeeter input #3, using the system mixer configuration 


### Libraries versions

- [CircuitPython 8.2.1](https://circuitpython.org/board/pimoroni_keybow2040/)
- [Adafruit CircuitPython IS31FL3731 release 3.3.9]( https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3731)
- [Adafruit CircuitPython bundle 8.x release tag 20230731](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20230731)


### Debug:

- Use PuTTY on Serial line COM4 (YMMV), speed 115200 bauds, or
- Use [Thonny](https://thonny.org/) (better)

**Note**: the [boot.py](./boot.py) contains information about how to re-enable the CircuitPython USB drive


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

Use [configs/MacroButtons-Midi-keybow](configs/MacroButtons-Midi-keybow) for the Voice Meeter MIDI config.


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


### Todo:

Add french keyboard support using [Neradoc/Circuitpython_Keyboard_Layouts](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts) and its [layout generator](https://www.neradoc.me/layouts/)
