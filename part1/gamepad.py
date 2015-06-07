#!/usr/bin/python

###############################################################                                                                  
# This is the final script in the tutorial at
# http://wp.me/p5kNk-2u
#
# History
# ------------------------------------------------
# Author                Date      		Comments
# Eric Goebelbecker     Jun 5 2015 		Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
###############################################################
from select import select
from evdev import InputDevice, categorize, ecodes
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

