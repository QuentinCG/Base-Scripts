#!/usr/bin/env bash

#@brief Post install step 1:
#  - Install sudo
#  - Add new user with sudo/bashrc/bash_profile and normal access rights
#  - Disable root SSH connection
#  - Update/upgrade the system
#  - Add weekly cron to update/upgrade the system
#
# This script must be called by root user
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 3 August 2016
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2016 Quentin Comte-Gaz

source ../utils/functions.sh

echo "---------- Check we have root privilege ---------"
isRoot
retval=$?
if [ "$retval" == 1 ]
then
  exit 1
fi

echo "---------------- Add source.list ----------------"
cp ../files/sources.list /etc/apt/sources.list

echo "----------------- Install sudo ------------------"
fastInstall sudo
echo "If you want to not write your password all the time when"
echo "using sudo, do : 'sudo visudo' and edit the right line:"
echo "USERNAME_HERE ALL=(ALL:ALL) NOPASSWD:ALL"
waitUserAction

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "----------------- Add new user ------------------"
echo "Add a new user (please specify a name):"
read username
sudo adduser --home /home/"$username" "$username"
sudo chown "$username":"$username" /home/"$username"
sudo chmod 755 /home/"$username"

echo "Add $username user to sudoers"
sudo bash -c 'echo "$username ALL=(ALL:ALL) NOPASSWD:ALL" | (EDITOR="tee -a" visudo)'

echo "Add bashrc and bash_profile to $username user"
sudo chmod 755 ../bash/install.sh
../bash/install.sh /home/"$username"

echo "------------ Disable ssh root access ------------"
replaceLineOrAddEndFile /etc/ssh/sshd_config "#PermitRootLogin" "PermitRootLogin no"

echo "-----Use port 50555 for SSH connexion-------"
replaceLineOrAddEndFile /etc/ssh/sshd_config "Port " "Port 50555"

/etc/init.d/ssh restart

echo "- Install automatic update and upgrade (weekly) -"
echo "apt-get -y update
apt-get -y upgrade" | sudo tee /etc/cron.weekly/update_and_upgrade
sudo chmod 755 /etc/cron.weekly/update_and_upgrade

echo "---------- End of the installation step ---------"
