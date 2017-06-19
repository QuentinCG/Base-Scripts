#!/usr/bin/env bash

#@brief Post install step 8:
#  - Install and configure GitLab
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

echo "--------- Update and upgrade the system ----------"
updateAndUpgrade

echo "--------- Installing GitLab dependencies ----------"
install curl openssh-server ca-certificates postfix

echo "-------- Add the GitLab package server and install the package ---------"
curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
install gitlab-ce

echo "-------- Please edit email informations and external URL values ---------"
echo "-------- GitLab config file will be oppened when after you pressend Enter ---------"
echo "-------- Note: external_url can be modified from 'xxxx.com' to 'xxxxx.com:port_value' if needed ---------"
waitUserAction
vim /etc/gitlab/gitlab.rb

echo "-------- Configuring GitLab ---------"
sudo gitlab-ctl reconfigure
