#!/usr/bin/env bash

#@brief Some commands to make Linux daily use easier
#@author Quentin Comte-Gaz <quentin@comte-gaz.com>
#@date 3 August 2016
#@license MIT License (contact me if too restrictive)
#@copyright Copyright (c) 2016 Quentin Comte-Gaz
#
#@note Put those commands in ~/.bashrc to launch them when logged

# Auto-correct "cd" errors with dir names
shopt -s cdspell

# Display a 80 characters line between every command in the shell
export PS1="_______________________________________________________________________________\n\u@\h:\w#"
