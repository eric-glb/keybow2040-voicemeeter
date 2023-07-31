import storage
import usb_hid

# Disable the CIRCUITPY USB drive
storage.disable_usb_drive()

# To re-enable the CIRCUITPY USB drive, in REPL:
# >>> import storage
# >>> storage.remount("/", readonly=False)
# Then comment out the storage.disable_usb_drive()
# And finally save boot.py + restart board

print("boot finished OK")
