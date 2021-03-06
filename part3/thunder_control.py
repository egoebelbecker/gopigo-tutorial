#!/usr/bin/python

#
# This is a simple Python module for controlling the DreamCheeky Thunder Cannon.
# This code borrows quite heavily from Dexter Industries example script at
# https://github.com/DexterInd/GoPiGo/
#                                       
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#

import platform
import time
import usb.core
import usb.util

# Protocol command bytes
DOWN = 0x01
UP = 0x02
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20
PARK = 0x30
LED = 0x31

dev = None
dev_type = None


# Setup the Office Cannon
def setup():
    global dev
    global dev_type

    dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if dev is None:
        dev = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if dev is None:
            raise ValueError('Missile device not found')
        else:
            dev_type = "Original"
    else:
        dev_type = "Thunder"

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            dev.detach_kernel_driver(0)
        except Exception, e:
            pass  # already unregistered
    dev.set_configuration()
    print "Set up device!"


# Send command to the office cannon
def __cmd(cmd):
    if "Thunder" == dev_type:
        dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif "Original" == dev_type:
        dev.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])


# Send command to control the LED on the office cannon
def __led(cmd):
    if "Thunder" == dev_type:
        dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif "Original" == dev_type:
        print("There is no LED on this device")


# Send command to move the office cannon
def __move(cmd, duration_ms):
    __cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    __cmd(STOP)


def run_command(command, value):
    if command == RIGHT or command == LEFT or command == UP or command == DOWN:
        __move(command, value)
    elif command == PARK:
        # Move to bottom-left
        __move(DOWN, 2000)
        __move(LEFT, 8000)
    elif command == LED:
        if value == 0:
            __led(0x00)
        else:
            __led(0x01)
    elif command == FIRE:
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        __cmd(FIRE)
        time.sleep(4.5)
    else:
        print "Error: Unknown command: '%s'" % command
