#!/usr/bin/env bash

#@brief Post install last step:
#  - Install and configure Let's Encrypt
#  - Add auto renew cert with Let's Encrypt
#
# This script must be called by a sudo user
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 1 July 2017
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2017 Quentin Comte-Gaz

source ../utils/functions.sh

echo "--------- Update and upgrade the system ----------"
updateAndUpgrade

echo "--------- Installing Let's Encrypt ----------"
fastInstall python-certbot-apache

echo "-------- Create the certificates ---------"
sudo certbot --apache

echo "- Install automatic Let's Encrypt renew (daily) -"
echo "date +'----------------- Lets Encrypt cron began at %d-%m-%y at %H:%M:%S -----------------' >> /var/log/letsencrypt/letsencrypt-renew.log
sudo certbot renew >> /var/log/letsencrypt/letsencrypt-renew.log 2>&1
sudo service mosquitto restart >> /var/log/letsencrypt/letsencrypt-renew.log 2>&1
sudo service proftpd restart >> /var/log/letsencrypt/letsencrypt-renew.log 2>&1
date +'----------------- Lets Encrypt cron done at %d-%m-%y at %H:%M:%S -----------------' >> /var/log/letsencrypt/letsencrypt-renew.log" | sudo tee /etc/cron.weekly/letsencrypt-renew
sudo chmod 755 /etc/cron.weekly/letsencrypt-renew

# Deprecated way to install Let's Encrypt certificates:
#echo "--------- Installing Let's Encrypt dependencies ----------"
#fastInstall git
#echo "-------- Download Let's Encrypt ---------"
#sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt --depth=1
#echo "-------- Upgrade Let's Encrypt ---------"
#cd /opt/letsencrypt
#sudo git pull
#echo "-------- Launch Let's Encrypt ---------"
#sudo /opt/letsencrypt/letsencrypt-auto
#echo "- Install automatic Let's Encrypt renew (weekly) -"
#echo "date +'----------------- Lets Encrypt cron began at %d-%m-%y at %H:%M:%S -----------------' >> /var/log/letsencrypt/letsencrypt-renew.log
#sudo /opt/letsencrypt/certbot-auto renew --no-self-upgrade >> /var/log/letsencrypt/letsencrypt-renew.log 2>&1
#sudo service mosquitto restart >> /var/log/letsencrypt/letsencrypt-renew.log 2>&1
#sudo service proftpd restart >> /var/log/letsencrypt/letsencrypt-renew.log 2>&1
#date +'----------------- Lets Encrypt cron done at %d-%m-%y at %H:%M:%S -----------------' >> /var/log/letsencrypt/letsencrypt-renew.log" | sudo tee /etc/cron.weekly/letsencrypt-renew
#sudo chmod 755 /etc/cron.weekly/letsencrypt-renew
