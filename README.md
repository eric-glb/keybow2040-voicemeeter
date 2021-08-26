# keybow2040-voicemeeter

### Keybow2040 tailored for my needs:
  - USB HID *and* Midi keys to pilot Voice Meeter Banana and OS media control
  - Visual feedback when muting/unmuting mic

https://user-images.githubusercontent.com/89578893/130957119-04bb56d3-d831-4dda-bfc8-a24a935e4dee.mp4

### From:
- https://www.tomshardware.com/how-to/build-rp2040-powered-shortcut-keypad

### My installation relies on:
- Pimoroni keybow2040-circuitpython:
    https://github.com/pimoroni/keybow2040-circuitpython
- VB-Audio Voice Meeter Banana:
    https://vb-audio.com/Voicemeeter/banana.htm
- VB-Audio Virtual Audio Cable:
    https://vb-audio.com/Cable/index.htm

### Debug:
- Use PuTTY on Serial line COM4, speed 115200 bauds

### My Voice Meeter Banana settings:

    Input #1 -> USB Blue Yeti Mic            -> to B1
    Input #2 -> Laptop Mic (unused)
    Input #3 -> VB-Audio Virtual Audio Cable -> to A1 and A2
    A1       -> Laptop jack output           -> speakers
    A2       -> USB soundcard                -> headphones

    Hook Volumes Keys (For Level Output A1)
    Hook Ctrl+F10,F11,F12 (For Level Input #1)

    MIDI Mapping for CircuitPython Audio:
    Mute Strip #3 -> Note On G#1 (44)
    Mute BUS A2   -> Note On C#2 (49)

### Key mapping:

    ┌─┬────────────┬─┬───────────┬──┬─────────────┬──┬────────────────┐
    │3│Volume Up   │7│Previous   │11│Next         │15│Play/Pause      │
    │ │            │ │           │  │             │  │                │
    ├─┼────────────┼─┼───────────┼──┼─────────────┼──┼────────────────┤
    │2│Volume Down │6│           │10│             │14│                │
    │ │            │ │           │  │             │  │                │
    ├─┼────────────┼─┼───────────┼──┼─────────────┼──┼────────────────┤
    │1│            │5│           │ 9│             │13│MIDI            │
    │ │            │ │           │  │             │  │Headphones Mute │
    ├─┼────────────┼─┼───────────┼──┼─────────────┼──┼────────────────┤
    │0│Mic Mute    │4│           │ 8│MIDI         │12│Speakers Mute   │
    │ │            │ │           │  │Cable Mute   │  │                │
    └─┴────────────┴─┴───────────┴──┴─────────────┴──┴────────────────┘
