#!/usr/bin/python

import thunder_control as thunder
from evdev import InputDevice, categorize, ecodes, KeyEvent
import os
from gopigo import *

model_b_plus = True
next_move = "down"
event_time = 0
speed = 100
gamepad = InputDevice('/dev/input/event0')

thunder.setup()

# Enable USB to give supply upto 1.2A on model B+
if model_b_plus:
    os.system("gpio -g write 38 0")
    os.system("gpio -g mode 38 out")
    os.system("gpio -g write 38 1")

try:
    thunder.run_command(thunder.PARK, 1000)
    print "Parked"
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0X':
                if absevent.event.value == -1:
                    next_move = thunder.LEFT
                    event_time = absevent.event.timestamp()
                elif absevent.event.value == 1:
                    next_move = thunder.RIGHT
                    event_time = absevent.event.timestamp()
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
                if absevent.event.value == -1:
                    next_move = thunder.UP
                    event_time = absevent.event.timestamp()
                elif absevent.event.value == 1:
                    next_move = thunder.DOWN
                    event_time = absevent.event.timestamp()
        elif event.type == ecodes.EV_SYN:
            synevent = categorize(event)
            print synevent
            syntime = synevent.event.timestamp()
            move_duration = (syntime - event_time) * 1000
            print move_duration
            thunder.run_command(next_move, move_duration)
        elif event.type == ecodes.EV_KEY:
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
                elif keyevent.keycode == 'BTN_THUMBR':
                    print "Stop"
                    stop()
                elif keyevent.keycode == 'BTN_THUMBL':
                    thunder.run_command(thunder.FIRE, 250)
                elif keyevent.keycode == 'BTN_TR':
                    print "Faster"
                    speed += 20
                    if speed > 255:
                        speed = 255
                    set_speed(speed)
                elif keyevent.keycode == 'BTN_TL':
                    print "Slower"
                    speed -= 20
                    if speed < 50:
                        speed = 50
                    set_speed(speed)

except KeyboardInterrupt:
    # Disable hight current mode on USB before exiting
    if model_b_plus:
        os.system("gpio -g write 38 0")
