# Keybow2040 tailored for my needs:
#   - USB HID *and* Midi keys to pilot Voice Meeter Banana
#   - Visual feedback when muting/unmuting mic
#                                  eric_glb - 2021/08/26
#

import time
import board
from keybow2040 import Keybow2040
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

# QWERTY: from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid_fr.keyboard_layout_fr import KeyboardLayoutFR

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard
keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)

# Set up the layout
keyboard = Keyboard(usb_hid.devices)
# QWERTY: layout = KeyboardLayoutUS(keyboard)
layout = KeyboardLayoutFR(keyboard)

# Set up USB MIDI up on channel 0.
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Map reminder on debug console
print("""
┌─┬────────────┬─┬───────────┬──┬────────────────┬──┬──────────────┐
│3│Google Meet │7│Previous   │11│Next            │15│Play/Pause    │
│ │Mute        │ │           │  │                │  │              │
├─┼────────────┼─┼───────────┼──┼────────────────┼──┼──────────────┤
│2│Teams       │6│MIDI Cable │10│MIDI Headphones │14│Speakers      │
│ │Mute        │ │Volume Up  │  │Volume Up       │  │Volume Up     │
├─┼────────────┼─┼───────────┼──┼────────────────┼──┼──────────────┤
│1│Reset Voice │5│MIDI Cable │ 9│MIDI Headphones │13│Speakers      │
│ |Meeter conf │ │Volume Down│  │Volume Down     │  │Volume Down   │
├─┼────────────┼─┼───────────┼──┼────────────────┼──┼──────────────┤
│0│MIDI Mic    │4│MIDI Cable │ 8│MIDI Headphones │12│Speakers      │
│ │Mute        │ │Mute       │  │Mute            │  │Mute          │
└─┴────────────┴─┴───────────┴──┴────────────────┴──┴──────────────┘
""")

# Keys categories
blank = []
reset = [1]
mic = [0]
teams = [2]
meet = [3]
cable = [4]
headphones = [8]
speakers = [12]
volume = [5,6,9,10,13,14]
control = [7,11]
playpause = [15]


# Sleep mode for keys
keybow.led_sleep_enabled = True
keybow.led_sleep_time = 900

# Colors
black = (0,0,0)
grey = (128,128,128)
white = (255,255,255)
weak_red = (85,0,0)
red = (255,0,0)
weak_blue = (0,0,85)
blue = (0,0,255)
weak_orange = (85,34,0)
orange = (255,102,0)
weak_green = (0,85,0)
green = (0,255,0)
weak_purple = (42,0,42)
purple = (128,0,128)
weak_yellow = (128,128,0)
yellow = (255,255,0)



#mic_muted = True
#cable_muted = False
#speakers_muted = False
#headphones_muted = True


#mic_blink = False

# Function for send Midi keypress
def midi_send(key):
    start_note = 36
    velocity = 127
    note = start_note + key
    midi.send(NoteOn(note, velocity))
    midi.send(NoteOff(note, 0))

def reset_config():
    # mute led status when starting (need to config things accordingly...)
    global mic_muted
    global cable_muted
    global speakers_muted
    global headphones_muted
    # bolean to get the mic key blinking when mic is unmuted
    global mic_blink
    # Values at boot time    
    mic_muted = True
    cable_muted = False
    speakers_muted = False
    headphones_muted = True
    mic_blink = False
    # Reset Voice Meeter config
    midi_send(1)

# Small animation when starting
keybow.set_all(*black)
for i in range(5):
    for key in keys:
        key.set_led(*grey)
    for key in keys:
        key.set_led(*white)

reset_config()

while True:
    keybow.update()

    # keys colors
    if not keybow.sleeping:
        for i in blank:
            keybow.keys[i].set_led(*black)

        for i in volume:
            keybow.keys[i].set_led(*weak_blue)

        for i in control:
            keybow.keys[i].set_led(*weak_orange)

        for i in teams:
            keybow.keys[i].set_led(*weak_purple)

        for i in meet:
            keybow.keys[i].set_led(*weak_purple)

        for i in playpause:
            keybow.keys[i].set_led(*weak_green)

        for i in reset:
            keybow.keys[i].set_led(*weak_yellow)

        for i in mic:
            if mic_muted:
                keybow.keys[i].set_led(*weak_red)
            else:
                mic_blink = not mic_blink
                if mic_blink:
                    keybow.keys[i].set_led(*green)
                else:
                    keybow.keys[i].set_led(*weak_green)

        for i in cable:
            if cable_muted:
                keybow.keys[i].set_led(*weak_red)
            else:
                keybow.keys[i].set_led(*weak_green)

        for i in speakers:
            if speakers_muted:
                keybow.keys[i].set_led(*weak_red)
            else:
                keybow.keys[i].set_led(*weak_green)

        for i in headphones:
            if headphones_muted:
                keybow.keys[i].set_led(*weak_red)
            else:
                keybow.keys[i].set_led(*weak_green)

    # Actions
    if keys[0].pressed:
        print('MIDI Mic Mute key pressed')
        keybow.set_all(*white)
        midi_send(0)
        time.sleep(0.2)
        mic_muted = not mic_muted

    elif keys[1].held:
        print('Reset Voice Meeter Banana Config key pressed')
        keybow.keys[1].set_led(*yellow)
        midi_send(1)
        reset_config()
        time.sleep(0.5)
        keyboard.release_all()

    elif keys[2].pressed:
        print('Teams Mute key pressed')
        keybow.keys[2].set_led(*purple)
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, layout.keycodes("m")[0])
        keyboard.release_all()
        time.sleep(0.1)

    elif keys[3].pressed:
        print('Google Meet Mute key pressed')
        keybow.keys[3].set_led(*purple)
        keyboard.send(Keycode.CONTROL, Keycode.D)
        keyboard.release_all()
        time.sleep(0.1)

    elif keys[4].pressed:
        print('MIDI Cable Mute key pressed')
        keybow.keys[4].set_led(*red)
        midi_send(4)
        time.sleep(0.1)
        cable_muted = not cable_muted

    elif keys[5].pressed:
        print('MIDI Cable Volume Down key pressed')
        keybow.keys[5].set_led(*blue)
        midi_send(5)
        time.sleep(0.1)

    elif keys[6].pressed:
        print('MIDI Cable Volume Up key pressed')
        keybow.keys[6].set_led(*blue)
        midi_send(6)
        time.sleep(0.1)

    elif keys[7].pressed:
        print('Previous Track key pressed')
        keybow.keys[7].set_led(*orange)
        consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        keyboard.release_all()
        time.sleep(0.1)

    elif keys[8].pressed:
        print('MIDI Headphones Mute key pressed')
        keybow.keys[8].set_led(*red)
        midi_send(8)
        time.sleep(0.1)
        headphones_muted = not headphones_muted

    elif keys[9].pressed:
        print('MIDI Headphones Volume Down key pressed')
        keybow.keys[9].set_led(*blue)
        midi_send(9)
        time.sleep(0.1)

    elif keys[10].pressed:
        print('MIDI Headphones Volume Up key pressed')
        keybow.keys[10].set_led(*blue)
        midi_send(10)
        time.sleep(0.1)

    elif keys[11].pressed:
        print('Next Track')
        keybow.keys[11].set_led(*orange)
        consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        keyboard.release_all()
        time.sleep(0.1)

    elif keys[12].pressed:
        print('Speakers Mute key pressed')
        keybow.keys[12].set_led(*red)
        consumer.send(ConsumerControlCode.MUTE)
        time.sleep(0.1)
        speakers_muted = not speakers_muted

    elif keys[13].pressed:
        print('Control Volume Down key pressed')
        keybow.keys[13].set_led(*blue)
        consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        keyboard.release_all()

    elif keys[14].pressed:
        print('Control Volume Up key pressed')
        keybow.keys[14].set_led(*blue)
        consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        keyboard.release_all()

    elif keys[15].pressed:
        print('Control Play/Pause key pressed')
        keybow.keys[15].set_led(*green)
        consumer.send(ConsumerControlCode.PLAY_PAUSE)
        keyboard.release_all()
        time.sleep(0.1)
