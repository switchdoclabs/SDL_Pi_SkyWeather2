#!/bin/bash
USBNAME=RTL2838
LSUSB=$(lsusb | grep --ignore-case $USBNAME)
DEVICE="/dev/bus/usb/"$(echo $LSUSB | cut --delimiter=' ' --fields='2')"/"$(echo $LSUSB | cut --delimiter=' ' --fields='4' | tr --delete ":")
usbreset $DEVICE 2>&1 >/dev/null

