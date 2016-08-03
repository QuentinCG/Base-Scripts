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

# Go to home directory
alias ~="cd ~"

# List files and folders
alias ll="ls -FGlAhp"

# Clear terminal display
alias c="clear"

# Show all executable paths
alias path="echo -e ${PATH//:/\\n}"

# Full recursive directory listing
alias lr='ls -R | grep ":$" | sed -e '\''s/:$//'\'' -e '\''s/[^-][^\/]*\//--/g'\'' -e '\''s/^/   /'\'' -e '\''s/-/|/'\'' | less'

# Find all files in current sub-folders containing specific string
alias findIn="find . -type f -print0 | xargs -0 grep -l"
