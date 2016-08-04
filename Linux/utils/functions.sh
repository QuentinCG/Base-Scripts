#!/usr/bin/env bash

#@brief Some functions for Linux daily use and scripts
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 3 August 2016
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2016 Quentin Comte-Gaz
#
#@note Use "source filename_here.sh" to use functions in shell

#@brief waitUserAction Wait user to press any key to continue
function waitUserAction()
{
  read -p "Press any key to continue" -n1 -s
  echo ""
}
export -f waitUserAction

#@brief checkRoot Check if root
#
#@return 0 if root else 1
function isRoot()
{
  if [[ $EUID -ne 0 ]]; then
    echo "You don't have root privilege" 2>&1
    return 1
  fi

  echo "You have root privilege" 2>&1
  return 0
}
export -f isRoot

#@brief fastInstall Install Packages without human interaction (automatic)
#
# Try to install all specified packages (even if some of them can't be installed)
#
#@param List of package to install
#
#@return All package are installed (1) else 0
#
#@example "fastInstall vim sudo htop"
function fastInstall()
{
  INSTALL_OPTIONS="-y -qq"
  if [ -z "$1" ]; then
    echo "Wrong parameters in fastInstall()"
    return 0
  fi
  return_value=1
  for ARG in "$@"
  do
    if apt-get --simulate install $INSTALL_OPTIONS $ARG > /dev/null; then
      sudo apt-get install $INSTALL_OPTIONS $ARG  > /dev/null
      echo "Package '$ARG' installed"
    else
      echo "Impossible to install '$ARG'. Is this package valid?"
      return_value=0
    fi
  done
  return $return_value
}
export -f fastInstall

#@brief install Install Packages with human visible information (automatic)
#
# Try to install all specified packages (even if some of them can't be installed)
#
#@param List of package to install
#
#@return All package are installed (1) else 0
#
#@example "install vim sudo htop"
function install()
{
  if [ -z "$1" ]; then
    echo "Wrong parameters in install()"
    return 0
  fi
  return_value=1
  for ARG in "$@"
  do
    if apt-get --simulate install $INSTALL_OPTIONS $ARG > /dev/null; then
      sudo apt-get install -y $ARG
      echo "Package '$ARG' installed"
    else
      echo "Impossible to install '$ARG'. Is this package valid?"
      return_value=0
    fi
  done
  return $return_value
}
export -f install

#@brief updateAndUpgrade Update and upgrade the system without human interaction
function updateAndUpgrade(){
  sudo apt-get update --yes
  sudo apt-get dist-upgrade --yes
}
export -f updateAndUpgrade

#@brief replaceLineOrAddEndFile Replace line containing $2 by $3 in file $1
#                               if $2 not found, add $3 at the end of the file
#
# If file does not exist, it will be created
#
#@param $1 Filename
#@param $2 String to find in the file
#@param $3 String that will replace line containing $2
#
#@return 1 (wrong args) / 0 (valid args)
#
#@example 'replaceLineOrAddEndFile /etc/ssh/sshd_config "Port 22" "Port 50555"'
function replaceLineOrAddEndFile()
{
  if [ "$#" -ne 3 ]; then
    echo "Wrong parameters in replaceLineOrAddEndFile()"
    return 1
  fi
  if grep -q $2 "$1"; then
    sed -i '/'"$2"'/c\'"$3"'' $1
  else
    echo "$3" >> $1
  fi
  return 1
}
export -f replaceLineOrAddEndFile

#@brief extract Extract file $1 (no need to care about the compression format)
#
#@param $1 File to extract
#
#@return 1 (file not supported) / 0 (file supported)
#
#@example 'extract my_file.zip'
function extract()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2) tar xjf $1    ;;
      *.tar.gz)  tar xzf $1    ;;
      *.bz2)     bunzip2 $1    ;;
      *.rar)     unrar e $1    ;;
      *.gz)      gunzip $1     ;;
      *.tar)     tar xf $1     ;;
      *.tbz2)    tar xjf $1    ;;
      *.tgz)     tar xzf $1    ;;
      *.zip)     unzip $1      ;;
      *.Z)       uncompress $1 ;;
      *.7z)      7z x $1       ;;
      *)         echo "'$1' cannot be extracted via extract()"
                 return 1      ;;
    esac
    return 0
  else
    echo "'$1' is not a valid file"
    return 1
  fi

  return 1
}
export -f extract

#@brief zipf Compress a specific file or folder (zip format)
#
#@param $1 File or folder to compress
function zipf() {
  zip -r "$1".zip "$1"
}
export -f zipf

#@brief mkdircd Recursive folder creation and then go in it
#
#@param $1 folders to create and go in
#
#@example ~> mkdircd numerous/folders/hehe/hehe
#         ~/numerous/folders/hehe/hehe>
function mkdircd()
{
  mkdir -p "$1" && eval cd "\"\$1\"";
}
export -f mkdircd
alias cdmkdir="mkdircd"
alias mcd="mkdircd"

#@brief findName Find all files which filenames contains $1
#
#@param $1 string contained in filenames to find
function findName()
{
  find . -name "*$1*"
}
export -f findName

#@brief sanitize Make directories and files access rights sane (recursively)
#
#@param $@ files/folders to have proper access rights
function sanitize()
{
  chmod -R u=rwX,g=rX,o= "$@";
}

#@brief netInfo Show network information
netInfo()
{
  /sbin/ifconfig | awk /'inet addr/ {print $2}'
  echo ""
  /sbin/ifconfig | awk /'Bcast/ {print $3}'
  echo ""
  /sbin/ifconfig | awk /'inet addr/ {print $4}'
  echo ""
  /sbin/ifconfig | awk /'HWaddr/ {print $4,$5}'
}

#@brief showWeather Show weather of city $1
#
#@param $1 City name
showWeather()
{
  curl wttr.in/"$1"
}
