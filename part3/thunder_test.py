#!/usr/bin/python

import thunder_control as thunder
import time
from evdev import InputDevice, categorize, ecodes, KeyEvent

model_b_plus=True

gamepad = InputDevice('/dev/input/event0')

thunder.setup_usb()

#Enable USB to give supply upto 1.2A on model B+
if model_b_plus:
    os.system("gpio -g write 38 0")
    os.system("gpio -g mode 38 out")
    os.system("gpio -g write 38 1")

thunder.run_command("zero", 1000)
print "Zeroed"
for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print ecode.bytype[absevent.event.type][absevent.event.code], absevent.event.value
        if ecode.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0X':
            if absevent.event.value == -1:
                thunder.run_command("down", 1000)
            else:
                thunder.run_command("up", 1000)
        if ecode.bytype[absevent.event.type][absevent.event.code] == 'ABS_HAT0Y':
            if absevent.event.value == -1:
                thunder.run_command("left", 1000)
            else:
                thunder.run_command("right", 1000)
    if event.type == ecodes.EV_SYN:
        synevent = categorize(event)
        print synevent

#thunder.run_command("fire", 500)
#print "Fire"
#thunder.run_command("led", 1)
#thunder.run_command("zero", 1000)
#print "Zeroed"




except KeyboardInterrupt:
	#Disable hight current mode on USB before exiting
	if model_b_plus:
		os.system("gpio -g write 38 0")
	

