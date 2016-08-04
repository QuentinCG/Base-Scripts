#!/usr/bin/env bash

#@brief Post install step 2: Install and configure main software
#
# This script must be called by a sudoer user
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 4 August 2016
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2016 Quentin Comte-Gaz

source ../utils/functions.sh

echo "-------------- Install Text editors -------------"
fastInstall vim gedit

echo "------- Install Secure shell file system --------"
fastInstall sshfs

echo "-------- Install Brute force protection ---------"
fastInstall fail2ban
echo "Edit '/etc/fail2ban/jail.conf' in order to change checked software"
echo "Use '/etc/init.d/fail2ban restart' to restart fail2ban"

echo "---------- Install security NMAP check ----------"
fastInstall nmap
echo "Use 'nmap -sT -0 localhost' to check open port"

echo "---------- Install htop (memory check) ----------"
fastInstall htop

echo "------------- Install Files explorer ------------"
fastInstall xfe

echo "-------------- Install Web Browsers -------------"
fastInstall elinks links links2 dillo iceweasel

echo "------------ Install picture display ------------"
fastInstall feh gwenview gpicview

echo "--------- Install compression utilitary ---------"
fastInstall zip p7zip p7zip-full unrar rar

echo "------------ Install Screen utilitary -----------"
fastInstall screen

echo "----------- Install dos2unix utilitary ----------"
fastInstall dos2unix

#echo "--------------- Install IRC client --------------"
#fastInstall irssi

echo "--------------- Install compilers ---------------"
fastInstall cmake make

echo "--------------- Install cmd jokes ---------------"
fastInstall fortune

echo "--------------- Project Management --------------"
fastInstall git-core git git-gui gitk mercurial
echo "In git gui, the 'Loose Object' popup will never be displayed."
git config --global gui.gcwarning false

echo "---------------- FTP Management -----------------"
fastInstall lftp

echo "---------------- Torrent clients ----------------"
fastInstall transmission deluge rtorrent

echo "---------------- Install X-server ---------------"
fastInstall xauth
if [ -e "$X11CONFIG" ]; then
  replaceLineOrAddEndFile $X11CONFIG "AllowTcpForwarding " "AllowTcpForwarding yes"
  replaceLineOrAddEndFile $X11CONFIG "X11Forwarding " "X11Forwarding yes"
  replaceLineOrAddEndFile $X11CONFIG "X11DisplayOffset " "X11DisplayOffset 10"
  replaceLineOrAddEndFile $X11CONFIG "X11UseLocalhost " "X11UseLocalhost yes"
  replaceLineOrAddEndFile $X11CONFIG "AddressFamily " "AddressFamily inet"
  fastInstall x11-apps
  echo "X-Server created, please launch X11-client in your computer"
  waitUserAction
  echo "A clock should soon appear in your screen. If not, something went wrong"
  xclock &
  waitUserAction
else
  echo "ERROR: IMPOSSIBLE TO CONFIGURE X11 SERVER!"
fi

echo "---------- End of the installation step ---------"
