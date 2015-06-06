#!/usr/bin/python

from evdev import InputDevice, categorize, ecodes, KeyEvent
from gopigo import *

speed=550

debug = 1	#Print raw values when debugging

joystick = InputDevice('/dev/input/event0')

set_speed(speed)
stop()
gamepad = InputDevice('/dev/input/event0')

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == 'BTN_A':
                print "Back"
                bwd()
            elif keyevent.keycode == 'BTN_Y':
                print "Forward"
                fwd()
            elif keyevent.keycode == 'BTN_B':
                print "Right"
                right()
            elif keyevent.keycode == 'BTN_X':
                print "Left"
                left()
            elif keyevent.keycode == 'BTN_TR":
                print "Stop"
                stop()

