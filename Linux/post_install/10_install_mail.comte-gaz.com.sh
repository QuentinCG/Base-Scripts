#!/usr/bin/env bash

#@brief Post install step 10:
#  - Install mail.comte-gaz.com website
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 1 July 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

APACHE_DIR="/var/www"
MAIL_SUBPATH="mail"
MAIL_FULL_PATH="$APACHE_DIR/$MAIL_SUBPATH"

read -p 'Specify mail.comte-gaz.com address (mail.comte-gaz.com if not for test): ' MAIL_ADDRESS
read -p 'Specify mail@comte-gaz.com mail (mail@comte-gaz.com if not for test): ' MAIL_MAIL

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "--------- Install mail.comte-gaz.com website ---------"
cd $APACHE_DIR
git clone https://github.com/QuentinCG/OVH-Email-Manager-Website.git
mv OVH-Email-Manager-Website $MAIL_SUBPATH

echo "--------- Edit mail website config file ---------"
cd $MAIL_SUBPATH
cp config_example.php config.php
echo "--------- You'll be asked to edit mail config file (please press a key) ------------"
waitUserAction
vim config.php

echo "--------- Set proper rights to mail.comte-gaz.com website ---------"
chmod -R g+x $MAIL_SUBPATH
chgrp -R www-data $MAIL_SUBPATH

echo "---------Adding mail.comte-gaz.com website URL----------"
echo "Adding the server information: (www.)$MAIL_ADDRESS website:"
cd /etc/apache2/sites-available/

echo "<VirtualHost *:80>
  ServerAdmin  $MAIL_MAIL
  ServerName  $MAIL_ADDRESS
  ServerAlias www.$MAIL_ADDRESS

  # Stored website
  DocumentRoot $MAIL_FULL_PATH

  # Website options (<=>.htaccess)
  <Directory $MAIL_FULL_PATH>
    # Allow .htaccess to override config
    AllowOverride All
    # Allow everybody to see the website
    Order allow,deny
    allow from all
  </Directory>

  # Logs (IPs, sent files, errors, ...)
  ErrorLog /var/log/apache2/mail-error_log
  TransferLog /var/log/apache2/mail-access_log
</VirtualHost>" > mail.conf

echo "---------Enable Mail website and restart apache----------"
echo "Enabling the new website"
a2ensite mail.conf

echo "Restarting Apache2"
service apache2 reload
/etc/init.d/apache2 restart
