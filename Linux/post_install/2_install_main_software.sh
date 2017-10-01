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

echo "-------------- Install anacron (cron) -------------"
fastInstall vim gedit

echo "------ Install basic file transfer (curl) -------"
fastInstall curl

echo "------- Install Secure shell file system --------"
fastInstall sshfs

echo "-------- Install Brute force protection ---------"
fastInstall fail2ban
echo "Edit '/etc/fail2ban/jail.conf' in order to change checked software"
echo "Use '/etc/init.d/fail2ban restart' to restart fail2ban"

echo "---------- Install security NMAP check ----------"
fastInstall nmap
echo "Use 'nmap -sT -O localhost' to check open port"

echo "---------- Install clock synch ----------"
fastInstall ntp

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
fastInstall cmake make gcc

echo "------------ Install Perl, Ruby and Python ------------"
fastInstall perl python python2.7 python3 ruby-full

echo "--------------- Install cmd jokes ---------------"
fastInstall fortune

echo "--------------- Project Management --------------"
fastInstall git-core git git-gui gitk mercurial
echo "In git gui, the 'Loose Object' popup will never be displayed."
git config --global gui.gcwarning false
echo "Git email and username will be set"
read -p 'Specify Git email address (quentin@comte-gaz.com): ' GIT_EMAIL
read -p 'Specify Git name (Quentin Comte-Gaz): ' GIT_NAME
git config --global user.email $GIT_EMAIL
git config --global user.name $GIT_NAME

echo "---------------- FTP Management -----------------"
fastInstall lftp filezilla ftp

echo "---------------- Torrent clients ----------------"
fastInstall transmission deluge rtorrent

echo "---------------- Install X-server ---------------"
fastInstall xauth
X11CONFIG="/etc/ssh/sshd_config"
if [ -e "$X11CONFIG" ]; then
  replaceLineOrAddEndFile $X11CONFIG "AllowTcpForwarding " "AllowTcpForwarding yes"
  replaceLineOrAddEndFile $X11CONFIG "X11Forwarding " "X11Forwarding yes"
  replaceLineOrAddEndFile $X11CONFIG "X11DisplayOffset " "X11DisplayOffset 10"
  replaceLineOrAddEndFile $X11CONFIG "X11UseLocalhost " "X11UseLocalhost yes"
  replaceLineOrAddEndFile $X11CONFIG "AddressFamily " "AddressFamily inet"
  fastInstall x11-apps
  echo "X-Server created, please launch X11-client in your computer if you use SSH"
  waitUserAction
  echo "A clock should soon appear in your screen. If not, something went wrong"
  xclock &
  waitUserAction
else
  echo "Impossible to configure X11 server (no SSH installed)"
fi

echo "------------ Install VirtualBox guest -----------"
echo "Do you use Linux as a VirtualBox guest?"
select yn in "Yes" "No"; do
  case $yn in
    Yes ) replaceLineOrAddEndFile /etc/apt/sources.list "download.virtualbox.org" "\n# VirtualBox\ndeb http://download.virtualbox.org/virtualbox/debian stretch contrib non-free";
          wget -q http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc -O- | apt-key add -;
          updateAndUpgrade;
          fastInstall build-essential module-assistant;
          m-a prepare;
          echo "Please insert Guest Additions CD";
          waitUserAction;
          sh /media/cdrom/VBoxLinuxAdditions.run;
          break;;
    No ) echo "No need to install VirtualBox packages";
         break;;
  esac
done

echo "---------- End of the installation step ---------"
