#!/usr/bin/env bash

#@brief Post install step 3:
#  - Install FTP server
#  - Change FTP server port
#  - Add SSL certificate to FTP and allow only secured connection
#
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 4 August 2016
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2016 Quentin Comte-Gaz

source ../utils/functions.sh

echo "--------------- Install FTP server --------------"
echo "Choose 'standalone' for the FTP server mode"
waitUserAction
install proftpd openssl
echo "Add more security on the FTP server (allow only /home/username/ access and use port 2121)"
replaceLineOrAddEndFile /etc/proftpd/proftpd.conf "DefaultRoot" "DefaultRoot  ~"
replaceLineOrAddEndFile /etc/proftpd/proftpd.conf "Port " "Port  2121"
echo "Add a public FTP access in /home/public_ftp/"
sudo mkdir /home/public_ftp/
echo "[!] ONE RULE IN THIS PUBLIC FTP SERVER:
[!] If you don't know me, please leave this server." | sudo tee /home/public_ftp/welcome.msg
echo "<Anonymous /home/public_ftp>
  User  ftp
  Group  nogroup
  # We want clients to be able to login with \"anonymous\" as well as \"ftp\"
  UserAlias  anonymous ftp
  # Cosmetic changes, all files belongs to ftp user
  DirFakeUser on ftp
  DirFakeGroup on ftp

  RequireValidShell  off

  # Limit the maximum number of anonymous logins
  MaxClients  10

  # We want 'welcome.msg' displayed at login
  DisplayLogin  welcome.msg

  # Deny WRITE everywhere in the anonymous chroot
  <Directory *>
    <Limit WRITE>
      DenyAll
    </Limit>
  </Directory>
</Anonymous>" | sudo tee /etc/proftpd/proftpd.conf

echo "Add SSL authentification for FTP (fill it with valid info)"
waitUserAction
sudo openssl req -new -x509 -days 36500 -nodes -out /etc/ssl/certs/proftpd.cert -keyout /etc/ssl/private/proftpd.key
sudo chmod 640 /etc/ssl/private/proftpd.key
echo "<IfModule mod_tls.c>
  TLSEngine on
  TLSLog /var/log/proftpd/tls.log

  # TLSv1 only
  # TLSProtocol TLSv1

  # Allow only secured connection
  TLSRequired on

  # Give certificate location
  TLSRSACertificateFile /etc/ssl/certs/proftpd.cert
  TLSRSACertificateKeyFile /etc/ssl/private/proftpd.key

  # Client does not need to have certificate
  TLSVerifyClient off
  TLSRenegotiate none

</IfModule>" | sudo tee /etc/proftpd/conf.d/tls.conf
sudo service proftpd restart

echo "---------- End of the installation step ---------"
