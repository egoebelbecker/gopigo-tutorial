#!/usr/bin/python

import thunder_control as thunder
import time

model_b_plus=False


thunder.setup_usb()

#Enable USB to give supply upto 1.2A on model B+
#if model_b_plus:
#    os.system("gpio -g write 38 0")
#    os.system("gpio -g mode 38 out")
#    os.system("gpio -g write 38 1")

thunder.run_command("zero", 1000)
print "Zeroed"
thunder.run_command("left", 1000)
print "Left"
thunder.run_command("right", 1000)
print "Right"
thunder.run_command("up", 1000)
print "Up"
#thunder.run_command("fire", 500)
#print "Fire"
thunder.run_command("down", 1000)
print "Down"
thunder.run_command("led", 1)
time.sleep(5)
print "LED"
thunder.run_command("led", 0)
print "LED"
thunder.run_command("zero", 1000)
print "Zeroed"




#except KeyboardInterrupt:
#	#Disable hight current mode on USB before exiting
#	if model_b_plus:
#		os.system("gpio -g write 38 0")
	
