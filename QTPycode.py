# Write your code here :-)
import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keyboard import Keycode

button_pin = board.A1

time.sleep(1) #apparently necessary to avoid race condition
keyboard = Keyboard(usb_hid.devices)
Keyboard_layout = KeyboardLayoutUS(keyboard)

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

button_is_pushed = False
button_is_held = False
time_push_began = 0.0
hold_delay = 5.0

led = digitalio.DigitalInOut(board.NEOPIXEL)
led.direction = digitalio.Direction.OUTPUT

print("waiting for button press...")

while True:
    if not button.value: # button is grounded, ie pushed
        if button_is_pushed: # button was previously being pushed, still being pushed
            if time_push_began + hold_delay < time.monotonic(): # hold delay has been surpassed
                if not button_is_held:
                    print("...and held...")
                    button_is_held = True
                    keyboard.press(Keycode.GUI)
                    keyboard.press(Keycode.TWO)
                    keyboard.release_all()
                    # do long-press things
        else : # button was not previously being pushed
            print("button was pushed...")
            button_is_pushed = True
            led.value = True
            time_push_began = time.monotonic() # store current time
            
    else: # button is not currently being pushed
        if button_is_pushed: # button was previously being pushed, so it has been released
            if time_push_began + hold_delay < time.monotonic(): # hold delay has not been surpassed
                print("...and released (long press)")
            else:
                print("...and released (short press)")
                # do shot-press things
                keyboard.press(Keycode.GUI)
                keyboard.press(Keycode.ONE)
                keyboard.release_all()
            button_is_pushed = False
            button_is_held = False
            led.value = False
            
    time.sleep(0.01)