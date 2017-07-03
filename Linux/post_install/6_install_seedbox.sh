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

read -p 'Specify seedbox login: ' SEEDBOX_LOGIN
read -p 'Specify seedbox password: ' SEEDBOX_PASSWORD
read -p 'Specify seedbox port (example: 9001): ' SEEDBOX_PORT
read -p 'Specify seedbox files domain (example: files.comte-gaz.com): ' SEEDBOX_FILES_DOMAIN
read -p 'Specify seedbox domain (example: torrent.comte-gaz.com): ' SEEDBOX_TORRENT_DOMAIN
read -p 'Specify seedbox download folder (example: /home/public_ftp/download): ' SEEDBOX_DOWNLOAD_FOLDER_NAME

echo "---------Installing dependency packages for h5ai----------"
fastInstall ffmpeg
fastInstall imagemagick
fastInstall tar zip

echo "---------Add Digest authentification for Apache---------"
sudo ln -s /etc/apache2/mods-available/auth_digest.load /etc/apache2/mods-enabled/
sudo /etc/init.d/apache2 force-reload

echo "---------Adding seedbox user----------"
addNewLinuxUser $SEEDBOX_USERNAME $WITH_NORMAL_SHELL
cd /home/$SEEDBOX_USERNAME

echo "---------Installing seedbox----------"
fastInstall transmission-daemon sudo
sudo service transmission-daemon stop

sudo usermod -a -G debian-transmission $SEEDBOX_USERNAME
sudo mkdir /home/$SEEDBOX_USERNAME/incomplete
sudo chown -R $SEEDBOX_USERNAME:debian-transmission /home/$SEEDBOX_USERNAME
sudo chgrp debian-transmission $SEEDBOX_DOWNLOAD_FOLDER_NAME
sudo chmod -R 775 /home/$SEEDBOX_USERNAME
sudo chmod -R 775 /home/$SEEDBOX_DOWNLOAD_FOLDER_NAME

echo "---------Configuring seedbox----------"

echo "
{
  \"alt-speed-down\": 50,
  \"alt-speed-enabled\": false,
  \"alt-speed-time-begin\": 540,
  \"alt-speed-time-day\": 127,
  \"alt-speed-time-enabled\": false,
  \"alt-speed-time-end\": 1020,
  \"alt-speed-up\": 50,
  \"bind-address-ipv4\": \"0.0.0.0\",
  \"bind-address-ipv6\": \"::\",
  \"blocklist-enabled\": false,
  \"blocklist-url\": \"http://www.example.com/blocklist\",
  \"cache-size-mb\": 4,
  \"dht-enabled\": true,
  \"download-dir\": \"$SEEDBOX_DOWNLOAD_FOLDER_NAME\",
  \"download-queue-enabled\": true,
  \"download-queue-size\": 5,
  \"encryption\": 1,
  \"idle-seeding-limit\": 30,
  \"idle-seeding-limit-enabled\": false,
  \"incomplete-dir\": \"/home/$SEEDBOX_USERNAME/incomplete\",
  \"incomplete-dir-enabled\": true,
  \"lpd-enabled\": false,
  \"message-level\": 1,
  \"peer-congestion-algorithm\": \"\",
  \"peer-id-ttl-hours\": 6,
  \"peer-limit-global\": 200,
  \"peer-limit-per-torrent\": 50,
  \"peer-port\": 51413,
  \"peer-port-random-high\": 65535,
  \"peer-port-random-low\": 49152,
  \"peer-port-random-on-start\": false,
  \"peer-socket-tos\": \"default\",
  \"pex-enabled\": true,
  \"port-forwarding-enabled\": true,
  \"preallocation\": 1,
  \"prefetch-enabled\": 1,
  \"queue-stalled-enabled\": true,
  \"queue-stalled-minutes\": 30,
  \"ratio-limit\": 20,
  \"ratio-limit-enabled\": false,
  \"rename-partial-files\": true,
  \"rpc-authentication-required\": true,
  \"rpc-bind-address\": \"0.0.0.0\",
  \"rpc-enabled\": true,
  \"rpc-password\": \"$SEEDBOX_PASSWORD\",
  \"rpc-port\": $SEEDBOX_PORT,
  \"rpc-url\": \"/transmission/\",
  \"rpc-username\": \"$SEEDBOX_LOGIN\",
  \"rpc-whitelist\": \"127.0.0.1\",
  \"rpc-whitelist-enabled\": false,
  \"scrape-paused-torrents-enabled\": true,
  \"script-torrent-done-enabled\": false,
  \"script-torrent-done-filename\": \"\",
  \"seed-queue-enabled\": false,
  \"seed-queue-size\": 10,
  \"speed-limit-down\": 100,
  \"speed-limit-down-enabled\": false,
  \"speed-limit-up\": 100,
  \"speed-limit-up-enabled\": false,
  \"start-added-torrents\": true,
  \"trash-original-torrent-files\": false,
  \"umask\": 18,
  \"upload-slots-per-torrent\": 14,
  \"utp-enabled\": true
}" | sudo tee /etc/transmission-daemon/settings.json

echo "---------Restarting seedbox----------"
sudo service transmission-daemon start
sudo service transmission-daemon reload

echo "---------Enable mod for apache proxy with seedbox port----------"
sudo a2enmod rewrite proxy proxy_http
sudo service apache2 restart

echo "-----Installing web browser for seedbox------"
mkdir $SEEDBOX_DOWNLOAD_FOLDER_NAME
cd $SEEDBOX_DOWNLOAD_FOLDER_NAME

# Alternative to considere (pretty but does not allow to upload/delete files)
wget https://release.larsjung.de/h5ai/h5ai-0.29.0.zip
extract h5ai-0.29.0.zip
rm h5ai-0.29.0.zip

# Alternative to considere (can upload/delete files but not pretty)
#wget https://raw.githubusercontent.com/alexantr/filemanager/master/filemanager.php
#mv filemanager.php index.php
#echo "---------You'll have to edit file manager file-----------"
#waitUserAction
#vim index.php

# Alternatives to considere (can upload/delete files but not pretty)
#wget https://raw.githubusercontent.com/jcampbell1/simple-file-manager/master/index.php

# Alternative (does not allow to upload/delete files and not pretty)
#wget https://raw.githubusercontent.com/marekrei/encode-explorer/master/index.php

sudo chmod -R g+x $SEEDBOX_DOWNLOAD_FOLDER_NAME
sudo chown -R debian-transmission:www-data $SEEDBOX_DOWNLOAD_FOLDER_NAME

echo "-----Adding login and password to protect files access ------"
echo "---------Please specify '$SEEDBOX_PASSWORD' as password------------"
waitUserAction
sudo htdigest -c /home/$SEEDBOX_USERNAME/.htdigest "Access restricted" $SEEDBOX_LOGIN

echo "---Adding the server information: $SEEDBOX_FILES_DOMAIN and $SEEDBOX_TORRENT_DOMAIN websites:---"
cd /etc/apache2/sites-available/

echo "<VirtualHost *:80>
  ServerName  $SEEDBOX_FILES_DOMAIN
  ServerAlias www.$SEEDBOX_FILES_DOMAIN

  DocumentRoot $SEEDBOX_DOWNLOAD_FOLDER_NAME

  <Directory ${SEEDBOX_DOWNLOAD_FOLDER_NAME}>
    # Allow to show folder content
    Options +Indexes

    # Folder requiring ID and password
    AuthType Digest
    AuthName \"Access restricted\"
    AuthDigestProvider file
    AuthUserFile /home/${SEEDBOX_USERNAME}/.htdigest
    Require valid-user

    # On surcharge l'interface Apache avec h5ai
    DirectoryIndex index.html index.php /_h5ai/public/index.php
  </Directory>

  CustomLog /dev/null \"combined\"
  ErrorLog /var/log/apache2/dl-error.log
</VirtualHost>" > files.conf

echo "<VirtualHost *:80>
        ServerName $SEEDBOX_TORRENT_DOMAIN
        ServerAlias www.$SEEDBOX_TORRENT_DOMAIN

        RewriteEngine On
        RewriteRule ^/$ /web/ [L,R=301]

        ProxyPass / http://127.0.0.1:$SEEDBOX_PORT/
        ProxyPassReverse / http://127.0.0.1:$SEEDBOX_PORT/
</VirtualHost>" > torrent.conf

echo "Enabling the new website"
sudo a2ensite files.conf
sudo a2ensite torrent.conf

echo "Restarting Apache2"
sudo service apache2 reload
sudo /etc/init.d/apache2 restart
