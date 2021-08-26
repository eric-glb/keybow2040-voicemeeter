# French azerty mapping for Adafruit HID

See here:
  - https://github.com/adafruit/Adafruit_CircuitPython_HID/pull/54

Then:
  - https://github.com/usini/CircuitPython_Exemples/tree/main/clavier_fr_tweet/lib/adafruit_hid


Code:

    # Clavier et layout français
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid_fr.keyboard_layout_fr import KeyboardLayoutFR
