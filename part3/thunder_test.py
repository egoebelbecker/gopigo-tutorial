#!/usr/bin/python

import thunder_control as thunder
import time
from evdev import InputDevice, categorize, ecodes, KeyEvent
import os

model_b_plus=True
next_move = "down"
event_time = 0

gamepad = InputDevice('/dev/input/event0')

thunder.setup_usb()

#Enable USB to give supply upto 1.2A on model B+
if model_b_plus:
    os.system("gpio -g write 38 0")
    os.system("gpio -g mode 38 out")
    os.system("gpio -g write 38 1")

try:
    thunder.run_command("zero", 1000)
    print "Zeroed"
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0X':
                if absevent.event.value == -1:
                    next_move = "left"
                    event_time = absevent.event.timestamp()
                elif absevent.event.value == 1:
                    next_move = "right"
                    event_time = absevent.event.timestamp()
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
                if absevent.event.value == -1:
                    next_move = "up"
                    event_time = absevent.event.timestamp()
                elif absevent.event.value == 1:
                    next_move = "down"
                    event_time = absevent.event.timestamp()
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RZ':
                thunder.run_command("fire", 250)
        if event.type == ecodes.EV_SYN:
            synevent = categorize(event)
            print synevent
            syntime = synevent.event.timestamp()
            move_duration = (syntime - event_time) * 1000
            print move_duration
            thunder.run_command(next_move, move_duration)
    
#thunder.run_command("fire", 500)
#print "Fire"
#thunder.run_command("led", 1)




except KeyboardInterrupt:
	#Disable hight current mode on USB before exiting
	if model_b_plus:
		os.system("gpio -g write 38 0")
	

