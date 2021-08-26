# Keybow2040 tailored for my needs:
#   - USB HID *and* Midi keys to pilot Voice Meeter Banana
#   - Visual feedback when muting/unmuting mic
#                                  eric_glb - 2021/08/24
#
# From:
#   https://www.tomshardware.com/how-to/build-rp2040-powered-shortcut-keypad
#
# My installation relies on:
#   Pimoroni keybow2040-circuitpython for this code:
#     https://github.com/pimoroni/keybow2040-circuitpython
#   VB-Audio Voice Meeter Banana:
#     https://vb-audio.com/Voicemeeter/banana.htm
#   VB-Audio Virtual Audio Cable:
#     https://vb-audio.com/Cable/index.htm
#   Audio Router to route Spotify to Virtual Audio Cable:
#     https://github.com/audiorouterdev/audio-router
#
# Debug: 
#   Use PuTTY on Serial line COM4, speed 115200 bauds
# 
# My Voice Meeter Banana settings:
#   Input #1 -> USB Blue Yeti Mic            -> to B1
#   Input #2 -> Laptop Mic (unused)
#   Input #3 -> VB-Audio Virtual Audio Cable -> to A1 and A2
#   A1       -> Laptop jack output           -> speakers
#   A2       -> USB soundcard                -> headphones
#
#   Hook Volumes Keys (For Level Output A1)
#   Hook Ctrl+F10,F11,F12 (For Level Input #1)
#
#   MIDI Mapping for CircuitPython Audio:
#     Mute Strip #3 -> Note On G#1 (44)
#     Mute BUS A2   -> Note On C#2 (49)
#
# Key mapping: see below

import time
import board
from keybow2040 import Keybow2040
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

# Map reminder on debug console
print("""
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
""")

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard
keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)

# Set up USB MIDI up on channel 0.
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
start_note = 36
velocity = 127

# Keys categories
blank = [1,4,5,6,9,10,14]
mic = [0]
cable = [8]
speakers = [12]
headphones = [13]
mute = [12,13]
volume = [2,3]
control = [7,11]
playpause = [15]

# Sleep mode for keys
keybow.led_sleep_enabled = True
keybow.led_sleep_time = 300

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

# mute led status when starting (need to config Voice accordingly)
mic_muted = True
cable_muted = False
speakers_muted = False
headphones_muted = True

# bolean to get the mic key blinking when mic is unmuted
mic_blink = False

# Small animation when starting
keybow.set_all(*black)
for i in range(5):
    for key in keys:
        key.set_led(*grey)
    for key in keys:
        key.set_led(*white)

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
            
        for i in playpause:
            keybow.keys[i].set_led(*weak_green)
 
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
        print('Mic Mute key pressed')
        keyboard.send(Keycode.CONTROL, Keycode.F10)   # Voicemeter shortcut for input #1
        keybow.set_all(*white)
        keyboard.release_all()
        time.sleep(0.2)
        mic_muted = not mic_muted

    elif keys[1].pressed:
        pass
 
    elif keys[2].pressed: 
        print('Volume Down key pressed')
        keybow.keys[2].set_led(*blue)
        consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        keyboard.release_all()

    elif keys[3].pressed:
        print('Volume Up key pressed')
        keybow.keys[3].set_led(*blue)
        consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        keyboard.release_all()
        
    elif keys[4].pressed:
        pass

    elif keys[5].pressed:
        pass

    elif keys[6].pressed:
        pass
          
    elif keys[7].pressed:
        print('Previous Track key pressed')
        keybow.keys[7].set_led(*orange)
        consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        keyboard.release_all()
        time.sleep(0.1)
          
    elif keys[8].pressed:
        print('MIDI Cable Mute key pressed')
        keybow.keys[8].set_led(*red)
        note = start_note + 8
        midi.send(NoteOn(note, velocity))
        midi.send(NoteOff(note, 0))
        keyboard.release_all()
        time.sleep(0.1)
        cable_muted = not cable_muted

    elif keys[9].pressed:
        pass

    elif keys[10].pressed:
        pass

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
        keyboard.release_all()
        time.sleep(0.1)
        speakers_muted = not speakers_muted

    elif keys[13].pressed:
        print('MIDI Headphones Mute key pressed')
        keybow.keys[13].set_led(*red)
        note = start_note + 13
        midi.send(NoteOn(note, velocity))
        midi.send(NoteOff(note, 0))
        keyboard.release_all()
        time.sleep(0.1)
        headphones_muted = not headphones_muted        

    elif keys[14].pressed:
        pass
        
    elif keys[15].pressed:
        print('Play/Pause key pressed')
        keybow.keys[15].set_led(*green)
        consumer.send(ConsumerControlCode.PLAY_PAUSE)
        keyboard.release_all()
        time.sleep(0.1)
