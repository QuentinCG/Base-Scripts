#!/usr/bin/env bash

echo "Setting the bash profile to the current user"
mv bash_profile ~/.bash_profile

echo "Setting the bashrc to the current user"
mv bashrc ~/.bashrc

echo "Copying the aliases,commands and functions to /etc/utils/"
sudo mkdir /etc/utils
sudo mv ../utils/* /etc/utils/
