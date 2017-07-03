#!/usr/bin/env bash

#@brief Post install step 5:
#  - Install teamspeak
#  - Add teamspeak website
#
# This script must be called by root user
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 3 July 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/user_functions.sh
source ../utils/functions.sh

TEAMSPEAK_USERNAME="teamspeak"
TEAMSPEAK_SERVER_FOLDER_NAME="teamspeak3-server"
TEAMSPEAK_SERVER_VERSION="3.0.13.6"

APACHE_DIR="/var/www"
TEAMSPEAK_SUBPATH="teamspeak"
TEAMSPEAK_FULL_PATH="$APACHE_DIR/$TEAMSPEAK_SUBPATH"

read -p 'Specify teamspeak.comte-gaz.com address (teamspeak.comte-gaz.com if not for test): ' TEAMSPEAK_ADDRESS
read -p 'Specify teamspeak@comte-gaz.com mail (teamspeak@comte-gaz.com if not for test): ' TEAMSPEAK_MAIL

echo "---------Copying teamspeak zipped website to apache dir----------"
cp ../files/teamspeak_website.zip $APACHE_DIR

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

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "--------- Install $TEAMSPEAK_ADDRESS website ---------"
cd $APACHE_DIR
mkdir $TEAMSPEAK_SUBPATH
mv teamspeak_website.zip $TEAMSPEAK_SUBPATH
cd $TEAMSPEAK_SUBPATH
unzip teamspeak_website.zip
rm teamspeak_website.zip

echo "--------- Set proper rights to $TEAMSPEAK_ADDRESS website ---------"
cd $APACHE_DIR
chmod -R g+x $TEAMSPEAK_SUBPATH
chgrp -R www-data $TEAMSPEAK_SUBPATH

echo "---------Adding $TEAMSPEAK_ADDRESS website URL----------"
echo "Adding the server information: (www.)$TEAMSPEAK_ADDRESS website:"
cd /etc/apache2/sites-available/

echo "<VirtualHost *:80>
  ServerAdmin  $TEAMSPEAK_MAIL
  ServerName  $TEAMSPEAK_ADDRESS
  ServerAlias www.$TEAMSPEAK_ADDRESS

  # Stored website
  DocumentRoot $TEAMSPEAK_FULL_PATH

  # Website options (<=>.htaccess)
  <Directory $TEAMSPEAK_FULL_PATH>
    # Allow .htaccess to override config
    AllowOverride All
    # Allow everybody to see the website
    Order allow,deny
    allow from all
  </Directory>

  # Logs (IPs, sent files, errors, ...)
  ErrorLog /var/log/apache2/teamspeak-error_log
  TransferLog /var/log/apache2/teamspeak-access_log
</VirtualHost>" > teamspeak.conf

echo "---------Enable Teamspeak website and restart apache----------"
echo "Enabling the new website"
a2ensite teamspeak.conf

echo "Restarting Apache2"
service apache2 reload
/etc/init.d/apache2 restart
