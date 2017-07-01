#!/usr/bin/env bash

#@brief Post install step 4:
#  - Install Apache and SQL server
#  - Install PHP7 support
#  - Install PHPMyAdmin
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 22 February 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

APACHE_SECURIY="/etc/apache2/apache2.conf" #"/etc/apache2/conf.d/security"
APACHE_DIR="/var/www"
PHPMYADMIN_PATH="$APACHE_DIR/phpmyadmin"

read -p 'Specify phpMyAdmin address (example: phpmyadmin.comte-gaz.com): ' PHPMYADMIN_ADDRESS
read -p 'Specify phpMyAdmin mail (example: phpmyadmin@comte-gaz.com): ' PHPMYADMIN_MAIL
read -p 'Specify phpMyAdmin login (example: phpmyadmin): ' PHPMYADMIN_LOGIN
read -p 'Specify phpMyAdmin password (example: testtest): ' PHPMYADMIN_PASSWORD

echo "--------------------------------------------"
echo "---------Install PHP & SQL server-----------"
echo "--------------------------------------------"

echo "---------Check we have root access----------"
isRoot

echo "--------- Update and upgrade the system ---------"
updateAndUpgrade

echo "---------Install Apache----------"
fastInstall apache2 apache2-utils

echo "---------Install PHP7----------"
#apt-cache search php7
fastInstall php7.0 php7.0-dev php7.0-cli php7.0-common libapache2-mod-php7.0 php7.0-fpm php7.0-bz2 php7.0-gd php7.0-mysql php7.0-json php7.0-curl php7.0-intl php-pear php-imagick php7.0-imap php7.0-mcrypt php-memcache php7.0-ps php-pspell php7.0-recode php7.0-snmp php7.0-sqlite3 php7.0-tidy php7.0-xmlrpc php7.0-xsl

echo "---------Install MySQL server----------"
install mysql-server mysql-client
sudo mysql --user=root mysql -e "CREATE USER '$PHPMYADMIN_LOGIN'@'localhost' IDENTIFIED BY '$PHPMYADMIN_PASSWORD'; GRANT ALL PRIVILEGES ON *.* TO '$PHPMYADMIN_LOGIN'@'localhost' WITH GRANT OPTION; FLUSH PRIVILEGES;"
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

echo "Installation of Apache & PHP7 & SQL & PhpMyAdmin done"
