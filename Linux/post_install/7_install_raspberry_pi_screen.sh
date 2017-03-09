#!/usr/bin/env bash

#@brief Post install step 6:
#  - Install RPI LCD screen
#
# This script must be called by root user
#
#@note Inspired from http://www.waveshare.com/wiki/3.5inch_RPi_LCD_%28A%29
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 9 March 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

echo "---------Untar file----------"
cp ../files/LCD-show-161112.tar.gz /tmp/
cd /tmp/
extract LCD-show-161112.tar.gz
sudo chmod -R 777 LCD-show
cd LCD-show/
echo "The RPi will reboot soon..."
./LCD35-show
