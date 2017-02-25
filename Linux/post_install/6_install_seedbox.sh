#!/usr/bin/env bash

#@brief Post install step 6:
#  - Install a seedbox (transmission)
#  - TODO: Install a way to get/delete files from the server
#
# This script must be called by root user
#
#@note Inspired from https://www.guillaume-leduc.fr/la-seedbox-facile-sous-debian-avec-transmission.html
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 25 February 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/user_functions.sh
source ../utils/functions.sh

SEEDBOX_USERNAME="seedbox"
SEEDBOX_SERVER_FOLDER_NAME="download"
SEEDBOX_LOGIN="loginHere"
SEEDBOX_PASSWORD="myPasswordHere"
SEEDBOX_PORT=9001

echo "---------Adding seedbox user----------"
addNewLinuxUser $SEEDBOX_USERNAME $WITH_NORMAL_SHELL
cd /home/$SEEDBOX_USERNAME

echo "---------Installing seedbox----------"
fastInstall transmission-daemon sudo
sudo service transmission-daemon stop

sudo usermod -a -G debian-transmission $SEEDBOX_USERNAME
sudo mkdir /home/$SEEDBOX_USERNAME/incomplete
sudo chown -R $SEEDBOX_USERNAME:debian-transmission /home/$SEEDBOX_USERNAME

echo "---------Configuring seedbox----------"

echo '
{
  "alt-speed-down": 7000,            // KB/s
  "alt-speed-enabled": true,
  "alt-speed-time-day": 127,         // 127(10)=1111111(2) (one 1 for each day of the week)
  "alt-speed-time-enabled": true,
  "alt-speed-up": 7000              // KB/s
  "download-dir": "/home/$SEEDBOX_USERNAME",
  "incomplete-dir": "/home/$SEEDBOX_USERNAME/incomplete",
  "incomplete-dir-enabled": true,
  "rpc-authentication-required": true,
  "rpc-enabled": true
  "rpc-password": "$SEEDBOX_PASSWORD",
  "rpc-port": $SEEDBOX_PORT,
  "rpc-url": "/",
  "rpc-username": "$SEEDBOX_LOGIN",
  "ratio-limit": 20,
  "ratio-limit-enabled": false,
}' | sudo tee /etc/transmission-daemon/settings.json

echo "---------Restarting seedbox----------"
sudo service transmission-daemon reload
