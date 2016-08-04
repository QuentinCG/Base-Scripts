#!/usr/bin/env bash

#@brief Set the bash profile and bashrc in path $1
#@arg $1 path Path where bashrc and bash profile will be stored

BASEDIR=$(dirname "$0")

echo "Copying the aliases,commands and functions to /etc/utils/"
sudo rm -rf /etc/utils/
sudo mkdir /etc/utils
sudo cp "$BASEDIR"/../utils/* /etc/utils/

echo "Setting the bash profile to the current user"
sudo cp "$BASEDIR"/bash_profile "$1"/.bash_profile

echo "Setting the bashrc to the current user"
sudo cp "$BASEDIR"/bashrc "$1"/.bashrc