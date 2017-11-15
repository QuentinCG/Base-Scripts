#!/usr/bin/env bash

#@brief Utility functions for user priviledge handling
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 25 February 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

WITHOUT_SHELL=0
WITH_NORMAL_SHELL=1

SHELLS_PATH="/etc/shells"
NOLOGIN_SHELL="/usr/sbin/nologin"
NORMAL_SHELL="/bin/bash"

#@brief Add a new linux user $1 with or without shell
#
#@param $1 User name
#@param $2 (boolean) $WITHOUT_SHELL or $WITH_NORMAL_SHELL
addNewLinuxUser() {
	if [ "$#" -eq 2 ]; then
		adduser $1
		if [ "$2" -eq $WITHOUT_SHELL ]; then
			removeUserShell $1
			echo "Added user '$1' with no shell"
		else
			echo "Added user '$1' with normal shell"
		fi
	else
		echo "Wrong parameters in addNewLinuxUser."
	fi
}
export -f addNewLinuxUser

#@brief Remove the shell of user $1
#
#@param $1 User name
removeUserShell() {
	if [ "$#" -eq 1 ]; then
		if ! [ grep -q "$NOLOGIN_SHELL" "$SHELLS_PATH" ]; then
			echo $NOLOGIN_SHELL >> $SHELLS_PATH
			echo "Adding a 'no login shell' $NOLOGIN_SHELL in $SHELLS_PATH"
		fi
		usermod -s $NOLOGIN_SHELL $1
	else
		echo "Wrong parameters in removeUserShell."
	fi
}
export -f removeUserShell

#Add shell for user $1
#$1: User name
addUserShell() {
	if [ "$#" -eq 1 ]; then
		if ! grep -q "$NORMAL_SHELL" "$SHELLS_PATH" ; then
			echo $NORMAL_SHELL >> $SHELLS_PATH
			echo "Adding a 'login shell' $NORMAL_SHELL in $SHELLS_PATH"
		fi
		usermod -s $NORMAL_SHELL $1
	else
		echo "Wrong parameters in addUserShell."
	fi
}
export -f addUserShell

#@brief List linux user names
listUsers() {
	cut -d: -f1 /etc/passwd
}
export -f listUsers
