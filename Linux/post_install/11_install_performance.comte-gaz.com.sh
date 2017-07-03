#!/usr/bin/env bash

#@brief Post install step 11:
#  - Install performnace.comte-gaz.com website
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 3 July 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

APACHE_DIR="/var/www"
PERFORMANCE_SUBPATH="performance"
PERFORMANCE_FULL_PATH="$APACHE_DIR/$PERFORMANCE_SUBPATH"

read -p 'Specify performance.comte-gaz.com address (performance.comte-gaz.com if not for test): ' PERFORMANCE_ADDRESS
read -p 'Specify performance@comte-gaz.com mail (performance@comte-gaz.com if not for test): ' PERFORMANCE_MAIL
read -p 'Specify performance website login (example: meAndMe): ' TEAMSPEAK_WEBSITE_LOGIN
read -p 'Specify performance website password (example: azerty): ' TEAMSPEAK_WEBSITE_PASSWORD

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "--------- Install $PERFORMANCE_ADDRESS website ---------"
cd $APACHE_DIR
git clone https://github.com/shevabam/ezservermonitor-web.git
mv ezservermonitor-web $PERFORMANCE_SUBPATH

echo "--------- Edit performance website config file ---------"
echo "--------- You'll be asked to edit performance config file (please press a key) ------------"
waitUserAction
vim $PERFORMANCE_FULL_PATH/conf/esm.config.json

echo "--------- Set proper rights to $PERFORMANCE_ADDRESS website ---------"
chmod -R g+x $PERFORMANCE_SUBPATH
chgrp -R www-data $PERFORMANCE_SUBPATH

echo "-----Adding login and password to protect website access ------"
echo "---------Please specify '$TEAMSPEAK_WEBSITE_PASSWORD' as password------------"
waitUserAction
sudo htdigest -c $PERFORMANCE_FULL_PATH/.htdigest "Access restricted" $TEAMSPEAK_WEBSITE_LOGIN

echo "---------Adding $PERFORMANCE_ADDRESS website URL----------"
echo "Adding the server information: (www.)$PERFORMANCE_ADDRESS website:"
cd /etc/apache2/sites-available/

echo "<VirtualHost *:80>
  ServerAdmin  $PERFORMANCE_MAIL
  ServerName  $PERFORMANCE_ADDRESS
  ServerAlias www.$PERFORMANCE_ADDRESS

  # Stored website\n
  DocumentRoot $PERFORMANCE_FULL_PATH

  # Website options (<=>.htaccess)
  <Directory $PERFORMANCE_FULL_PATH>
    # Folder requiring ID and password
    AuthType Digest
    AuthName \"Access restricted\"
    AuthDigestProvider file
    AuthUserFile $PERFORMANCE_FULL_PATH/.htdigest
    Require valid-user
  </Directory>

  # Logs (IPs, sent files, errors, ...)
  ErrorLog /var/log/apache2/performance-error_log
  TransferLog /var/log/apache2/performance-access_log
</VirtualHost>" > performance.conf

echo "---------Enable Performance website and restart apache----------"
echo "Enabling the new website"
a2ensite performance.conf

echo "Restarting Apache2"
service apache2 reload
/etc/init.d/apache2 restart
