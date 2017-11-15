#!/usr/bin/env bash

#@brief Some aliases for Linux daily use
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 3 August 2016
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2016 Quentin Comte-Gaz
#
#@note Put those aliases in ~/.bashrc to use them after login

# Go back
alias cd..="cd ../" # (for fast typers)
alias ..="cd .."
alias ..2="cd ../.."
alias ..3="cd ../../.."
alias ..4="cd ../../../.."
alias ..5="cd ../../../../.."
alias ..6="cd ../../../../../.."

alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."
alias .......="cd ../../../../../.."

# Set vim as default text editor
alias vi="vim"
alias edit="vim"

# Try to continue download before normal download
alias wget='wget -c'

# Directory shortcuts
alias home="cd ~/"
alias ~="cd ~"
alias localhost="cd /var/www"

# List files and folders
alias ll="ls -FGlAhp"

# Clear terminal display
alias c="clear"

# Show all executable paths
alias path="echo -e ${PATH//:/\\n}"

# Find all files in current sub-folders containing specific string
alias findIn="find . -type f -print0 | xargs -0 grep -l"

# Git
alias push="git push origin master"
alias pull="git pull"

# Spelling typos
alias xs='cd'
alias vf='cd'
alias moer='more'
alias moew='more'
alias kk='ll'
alias mm='ll'

# Show IP
alias myIp="curl ipinfo.io/ip"

# Apt
alias update="apt-get update"
alias upgrade="apt-get upgrade"
#alias install="apt-get install" # (already in functions)

# Network config
alias ipconfig='ifconfig'
