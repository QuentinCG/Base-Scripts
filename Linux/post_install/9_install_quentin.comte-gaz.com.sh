#!/usr/bin/env bash

#@brief Post install step 9:
#  - Install quentin.comte-gaz.com website
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 1 July 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

APACHE_DIR="/var/www"
QUENTIN_SUBPATH="quentin"
QUENTIN_FULL_PATH="$APACHE_DIR/$QUENTIN_SUBPATH"

read -p 'Specify quentin.comte-gaz.com address (quentin.comte-gaz.com if not for test): ' QUENTIN_ADDRESS
read -p 'Specify quentin@comte-gaz.com mail (quentin@comte-gaz.com if not for test): ' QUENTIN_MAIL

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "--------- Install quentin.comte-gaz.com website ---------"
cd $APACHE_DIR
git clone https://github.com/QuentinCG/quentin.comte-gaz.com.git
mv quentin.comte-gaz.com $QUENTIN_SUBPATH

echo "--------- Set proper rights to quentin.comte-gaz.com website ---------"
chmod -R g+x $QUENTIN_SUBPATH
chgrp -R www-data $QUENTIN_SUBPATH

echo "---------Adding Quentin.comte-gaz.com website URL----------"
echo "Adding the server information: (www.)$QUENTIN_ADDRESS website:"
cd /etc/apache2/sites-available/

echo "<VirtualHost *:80>
  ServerAdmin  $QUENTIN_MAIL
  ServerName  $QUENTIN_ADDRESS
  ServerAlias www.$QUENTIN_ADDRESS

  # Stored website\n
  DocumentRoot $QUENTIN_FULL_PATH

  # Website options (<=>.htaccess)
  <Directory $QUENTIN_FULL_PATH>
    # Allow .htaccess to override config
    AllowOverride All
    # Allow everybody to see the website
    Order allow,deny
    allow from all
  </Directory>

  # Logs (IPs, sent files, errors, ...)
  ErrorLog /var/log/apache2/quentin-error_log
  TransferLog /var/log/apache2/quentin-access_log
</VirtualHost>" > quentin.conf

echo "---------Enable Quentin website and restart apache----------"
echo "Enabling the new website"
a2ensite quentin.conf

echo "Restarting Apache2"
service apache2 reload
/etc/init.d/apache2 restart
