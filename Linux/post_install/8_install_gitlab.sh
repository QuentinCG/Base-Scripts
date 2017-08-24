#!/usr/bin/env bash

#@brief Post install step 8:
#  - Install and configure GitLab
#  - Install website proxy to use GitLab
#
# This script must be called by a sudo user
#
#@note Inspired from https://about.gitlab.com/installation/#debian
#
#@todo Add TLS (https://about.gitlab.com/2016/04/11/tutorial-securing-your-gitlab-pages-with-tls-and-letsencrypt/)
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 19 June 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

APACHE_DIR="/var/www"
GITLAB_SUBPATH="gitlab"
GITLAB_FULL_PATH="$APACHE_DIR/$GITLAB_SUBPATH"

read -p 'Specify GitLab port (example: 1276): ' GITLAB_PORT
read -p 'Specify GitLab domain address (example: gitlab.comte-gaz.com): ' GITLAB_DOMAIN
read -p 'Specify GitLab mail address (example: gitlab@comte-gaz.com): ' GITLAB_MAIL

echo "--------- Update and upgrade the system ----------"
updateAndUpgrade

echo "--------- Installing GitLab dependencies ----------"
install curl openssh-server ca-certificates postfix

echo "-------- Add the GitLab package server and install the package ---------"
curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
install gitlab-ce

echo "-------- Please edit email informations and external URL values ---------"
echo "-------- GitLab config file will be opened when after you press Enter ---------"
echo "-------- Note: external_url must be modified into 'http(s)://xxxxx.com:$GITLAB_PORT' ---------"
waitUserAction
vim /etc/gitlab/gitlab.rb

echo "-------- Configuring GitLab ---------"
sudo gitlab-ctl reconfigure

#echo "---------Enable mod for apache proxy with Gitlab port----------"
#sudo a2enmod rewrite proxy proxy_http
#sudo service apache2 restart

echo "---Adding the server information: $GITLAB_DOMAIN website:---"

cd $APACHE_DIR
mkdir GITLAB_SUBPATH
echo '<meta http-equiv="refresh" content="0; url=http://$GITLAB_DOMAIN:$GITLAB_PORT" />' > $GITLAB_FULL_PATH/index.php

cd /etc/apache2/sites-available/
echo "<VirtualHost *:80>
  ServerAdmin  $GITLAB_MAIL
  ServerName  $GITLAB_DOMAIN
  ServerAlias www.$GITLAB_DOMAIN

  # Stored website
  DocumentRoot $GITLAB_FULL_PATH

  # Website options (<=>.htaccess)
  <Directory $GITLAB_FULL_PATHb>
    # Allow .htaccess to override config
    AllowOverride All
    # Allow everybody to see the website
    Order allow,deny
    allow from all
  </Directory>

  # Logs (IPs, sent files, errors, ...)
  ErrorLog /var/log/apache2/gitlab-error_log
  TransferLog /var/log/apache2/gitlab-access_log
</VirtualHost>" > gitlab.conf

echo "Enabling the new website"
sudo a2ensite gitlab.conf

echo "Restarting Apache2"
sudo service apache2 reload
sudo /etc/init.d/apache2 restart

echo "If you want secured Gitlab (HTTPS), edit /etc/gitlab/gitlab.rb as followed:"
echo "external_url 'https://$GITLAB_DOMAIN:$GITLAB_PORT'"
echo "nginx['enable'] = true"
echo "nginx['redirect_http_to_https'] = true"
echo "nginx['redirect_http_to_https_port'] = 1277"
echo "nginx['ssl_certificate'] = '/etc/letsencrypt/live/xxxxxx/cert.pem'"
echo "nginx['ssl_certificate_key'] = '/etc/letsencrypt/live/xxxxxx/privkey.pem'"
echo "Also edit $GITLAB_FULL_PATH/index.php to use HTTPS instead of HTTP"
