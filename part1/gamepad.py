#!/usr/bin/python

from evdev import InputDevice, categorize, ecodes, KeyEvent
gamepad = InputDevice('/dev/input/event0')

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == 'BTN_A':
                print "Back"
            elif keyevent.keycode == 'BTN_Y':
                print "Forward"
            elif keyevent.keycode == 'BTN_B':
                print "Right"
            elif keyevent.keycode == 'BTN_X':
                print "Left"

