#!/usr/bin/env bash

#@brief Post install step 5:
#  - Install teamspeak
#
# This script must be called by root user
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 25 February 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/user_functions.sh
source ../utils/functions.sh

TEAMSPEAK_USERNAME="teamspeak"
TEAMSPEAK_SERVER_FOLDER_NAME="teamspeak3-server"
TEAMSPEAK_SERVER_VERSION="3.0.13.6"

echo "---------Adding teamspeak user----------"
addNewLinuxUser $TEAMSPEAK_USERNAME $WITH_NORMAL_SHELL

echo "---------Installing teamspeak----------"
cd /home/$TEAMSPEAK_USERNAME
wget http://teamspeak.gameserver.gamed.de/ts3/releases/$TEAMSPEAK_SERVER_VERSION/teamspeak3-server_linux_amd64-$TEAMSPEAK_SERVER_VERSION.tar.bz2
extract teamspeak3-server_linux_amd64-$TEAMSPEAK_SERVER_VERSION.tar.bz2
rm teamspeak3-server_linux_amd64-$TEAMSPEAK_SERVER_VERSION.tar.bz2
mv teamspeak3-server_linux_amd64 $TEAMSPEAK_SERVER_FOLDER_NAME
chmod -R 755 $TEAMSPEAK_SERVER_FOLDER_NAME

runuser -l $TEAMSPEAK_USERNAME -c "/home/$TEAMSPEAK_USERNAME/$TEAMSPEAK_SERVER_FOLDER_NAME/ts3server_startscript.sh start"

echo "---------Please SAVE the ID and TOKEN printed in the screen------------"
waitUserAction

echo "---------Please add this command to crontab:------------"
echo "@reboot cd /home/$TEAMSPEAK_USERNAME/$TEAMSPEAK_SERVER_FOLDER_NAME && ./ts3server_startscript.sh start"
waitUserAction
runuser -l $TEAMSPEAK_USERNAME -c 'crontab -e'
