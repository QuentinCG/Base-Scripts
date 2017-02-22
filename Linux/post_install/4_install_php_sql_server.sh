#!/usr/bin/env bash

#@brief Post install step 4:
#  - Install Apache/PHP/SQL server
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 22 February 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

APACHE_SECURIY = "/etc/apache2/apache2.conf" #"/etc/apache2/conf.d/security"
APACHE_DIR = "/var/www"
PHPMYADMIN_PATH = "$APACHE_DIR/phpmyadmin"

PHPMYADMIN_ADDRESS = "phpmyadmin.comte-gaz.com"
PHPMYADMIN_MAIL = "phpmyadmin@comte-gaz.com"

echo "--------------------------------------------"
echo "---------Install PHP & SQL server-----------"
echo "--------------------------------------------"

echo "---------Check we have root access----------"
checkRoot

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "---------Install Apache----------"
fastInstall apache2 apache2-utils

echo "---------Install PHP5----------"
apt-cache search php5
fastInstall php5 php5-dev php5-gd php5-mysql php5-json php5-curl php5-gd php5-intl php-pear php5-imagick php5-imap php5-mcrypt php5-memcache php5-ming php5-ps php5-pspell php5-recode php5-snmp php5-sqlite php5-tidy php5-xmlrpc php5-xsl

echo "---------Install MySQL server----------"
echo "We will now install MySQL server (you'll have to write a new SQL password)"
waitUserAction
install mysql-server mysql-client
echo "MySQL installed"

echo "---------Install PHPMyAdmin----------"
echo "Installing PHPMyAdmin (please check 'APACHE2' then 'NO')"
waitUserAction
install phpmyadmin
ln -s /usr/share/phpmyadmin $PHPMYADMIN_PATH

echo "---------Optimize server security----------"
echo "Adding maximum security into apache2 config"
if [ -e "$APACHE_SECURIY" ]; then
	replaceLineOrAddEndFile $APACHE_SECURIY "ServerTokens " "ServerTokens Prod"
	replaceLineOrAddEndFile $APACHE_SECURIY "ServerSignature " "ServerSignature Off"
	replaceLineOrAddEndFile $APACHE_SECURIY "TraceEnable " "TraceEnable Off"
else
	echo "ERROR: IMPOSSIBLE TO CONFIGURE APACHE SECURITY!"
	echo "PLEASE EDIT $APACHE_SECURIY BY YOURSELF!"
fi

echo "---------Adding PHPMyAdmin website URL----------"
echo "Adding the server information: (www.)$PHPMYADMIN_ADDRESS website:"
cd /etc/apache2/sites-available/

echo "<VirtualHost *:80>
	ServerAdmin  $PHPMYADMIN_MAIL
	ServerName  $PHPMYADMIN_ADDRESS
	ServerAlias www.$PHPMYADMIN_ADDRESS

	# Stored website\n
	DocumentRoot $PHPMYADMIN_PATH

	# Website options (<=>.htaccess)
	<Directory $PHPMYADMIN_PATH>
		#Allow everybody to see the website
		Order allow,deny
		allow from all
	</Directory>

	# Logs (IPs, sent files, errors, ...)
	ErrorLog /var/log/apache2/phpmyadmin-error_log
	TransferLog /var/log/apache2/phpmyadmin-access_log
</VirtualHost>" > phpmyadmin.conf

echo "---------Enable PHPMyAdmin website and restart apache----------"
echo "Enabling the new website"
a2ensite phpmyadmin.conf

echo "Restarting Apache2"
service apache2 reload
/etc/init.d/apache2 restart

echo "Installation of Apache & PHP5 & SQL & PhpMyAdmin done"
