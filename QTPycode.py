import time
import board
import digitalio
import busio
import usb_hid
import neopixel
import supervisor

from adafruit_tla202x import TLA2024
from adafruit_tla202x.analog_in import AnalogIn

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keyboard import Keycode

button_pin = board.A1
power_pin = board.A2

time.sleep(1) #apparently necessary to avoid race condition

# Power stuff
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

power_on = digitalio.DigitalInOut(power_pin)
power_on.direction = digitalio.Direction.OUTPUT
power_on.value = True #turn on the power
time.sleep(1) # make sure the power is up
pixel.fill((255,255,255)) # white


button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

keyboard_started = False
time_to_start_keyboard = 15 # wait to start up keyboard

pixel.fill((255,255,0)) #yellow

button_is_pushed = False
button_is_held = False
time_push_began = 0.0
time_released = 0.0
debounce = 0.25
warn_delay = 2.0
hold_delay = 7.0


# i2c stuff

try:

    pixel.fill((10,255,255)) #cyan
    i2cbus = busio.I2C(board.SCL, board.SDA)
    tla = TLA2024(i2cbus)
except:
    print("no i2c")
    pixel.fill((255,0,0)) #red
    while True:
        time.sleep(2)
    #power_on.value = False

vdc = 0.0
vbatt = 0.0
temp_vdc = 0.0
temp_vbatt = 0.0
total_samples = 5
sample_count = 0

while True:

    if time.monotonic() > time_to_start_keyboard:
        if not keyboard_started:
            # Start up keyboard
            pixel.fill((150,150,0)) #yellow

            if supervisor.runtime.usb_connected:
                try:
                    keyboard = Keyboard(usb_hid.devices)
                    Keyboard_layout = KeyboardLayoutUS(keyboard)
                    keyboard_started = True
                except:
                    keyboard_started = False
            else:
                keyboard_started = False


    # Button monitoring
    if not button.value: # button is grounded, ie pushed
        if button_is_pushed: # button was previously being pushed, still being pushed
            if time_push_began + hold_delay < time.monotonic(): # hold delay has been surpassed
                if not button_is_held:
                    print("...and held...")
                    button_is_held = True
                    if keyboard_started == True:
                        keyboard.press(Keycode.CONTROL)
                        keyboard.press(Keycode.ALT)
                        keyboard.press(Keycode.F1)
                        keyboard.release_all()
                    # do long-press things
        else : # button was not previously being pushed
            if time_released + debounce < time.monotonic(): # only register new press once debounce has been surpassed
                print("button was pushed...")
                button_is_pushed = True
                time_push_began = time.monotonic() # store current time

    else: # button is not currently being pushed
        if button_is_pushed: # button was previously being pushed, so it has been released
            if time_push_began + hold_delay < time.monotonic(): # hold delay has not been surpassed
                print("...and released (long press)")
                pixel.fill((0,0,0))
                time.sleep(.1)
                pixel.fill((0,0,255)) # blue
                time.sleep(.1)
                pixel.fill((0,0,0))
                time.sleep(.1)
                pixel.fill((0,0,255)) # blue
                time.sleep(.1)
                power_on.value = False # turn off power
            else:
                print("...and released (short press)")
                # do shot-press things
                if keyboard_started == True:
                    keyboard.press(Keycode.CONTROL)
                    keyboard.press(Keycode.ALT)
                    keyboard.press(Keycode.ESCAPE)
                    keyboard.release_all()
                pixel.fill((0,0,0))
                time.sleep(.1)
                pixel.fill((0,255,0)) # green
                time.sleep(.1)
            button_is_pushed = False
            button_is_held = False
            time_released = time.monotonic()
            pixel.fill((255,0,0))
            
            
    # Power monitoring
    if sample_count < total_samples: # Smooth out samples
        tla.input_channel = 2
        temp_vdc += tla.voltage
        tla.input_channel = 0
        temp_vbatt += tla.voltage
        sample_count += 1
    else:
        vdc = temp_vdc / sample_count
        vbatt = temp_vdc / sample_count
        sample_count = 0
        

    if vdc > 1.0: # Running on DC power, not battery
        pixel.fill((0, 255, 0)) # green
    else: # Running on battery
        if vbatt > 4:
            pixel.fill((0, 0, 255)) # blue
        elif vbatt > 3.5:
            pixel.fill((255, 128, 0)) # orange
        else:
            pixel.fill((255, 0, 0)) # red

    time.sleep(0.01)
