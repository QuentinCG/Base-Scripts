#!/usr/bin/env bash

#@brief Post install step 12:
#  - Install Mosquitto server with default config as secured with login/password
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 11 July 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

MOSQUITTO_PATH="/etc/mosquitto"

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "--------------- Install MQTT server and client ---------------"
fastInstall mosquitto mosquitto-clients

echo "--------- Add a login and a password to access mosquitto server ---------"
echo "--------- You'll be asked to set a MQTT login and a password (please press a key) ------------"
waitUserAction
sudo mosquitto_passwd -U "$MOSQUITTO_PATH/password"

echo "--------- Copy and edit mosquitto config into mosquitto folder ---------"
mv "$MOSQUITTO_PATH/mosquitto.conf" "$MOSQUITTO_PATH/mosquitto.conf.old"
sudo cp ../files/mosquitto.conf "$MOSQUITTO_PATH/mosquitto.conf"
echo "--------- You'll be asked to edit mosquitto config file (please press a key) ------------"
waitUserAction
sudo vim "$MOSQUITTO_PATH/mosquitto.conf"

echo "--------- Set proper rights to mosquitto config file and password ---------"
sudo chown mosquitto:mosquitto $MOSQUITTO_PATH/mosquitto.conf
sudo chown mosquitto:mosquitto $MOSQUITTO_PATH/password
sudo chmod -R 775 /home/$MOSQUITTO_PATH

echo "Restarting Mosquitto"
sudo service mosquitto reload
