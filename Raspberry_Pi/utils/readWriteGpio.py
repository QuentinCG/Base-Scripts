#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Read/write Raspberry Pi GPIO from shell
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2017/05/02)"
__status__ = "Usable for any project"
__dependency__ = "RPi.GPIO (use 'pip install RPi.GPIO' to install package)"

import RPi.GPIO as GPIO # RPI GPIO library
import argparse # Manage program arguments
import sys # Use exit calls
import logging # Add logging

if __name__ == "__main__":
  # Parse received parameters
  parser = argparse.ArgumentParser(description='Read/Write Raspberry Pi GPIO from shell')
  parser.add_argument('-g', '--gpio', type=int, help='GPIO pin (BOARD numbering system)')
  parser.add_argument('-r', '--read', action='store_true', help='Read value from GPIO (result will be printed to shell)')
  parser.add_argument('-w', '--write', type=int, default=-1, help='Write value to GPIO (Value to write: 0/1)')
  parser.add_argument('-p', '--pullUp', default="DOWN", help='Pull-up/down mode for INPUT (UP/DOWN, default: DOWN, useless for output)')
  parser.add_argument('-v', '--verbose', action='store_true', help='Show debug information (optional, default: Not verbose)')
  args = parser.parse_args()

  # Show more information if in debug mode
  if args.verbose:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

  # Show warnings if in debug mode
  GPIO.setwarnings(args.verbose)

  # Throw error in case the arguments are not valid
  if not args.gpio:
    logging.error("No GPIO pin specified.")
    sys.exit(1)
  if (not args.read) and (args.write == -1):
    logging.error("No read/write mode selected.")
    sys.exit(1)
  if (args.read) and (args.write != -1):
    logging.error("Both read and write mode selected, please select only one.")
    sys.exit(1)
  if (args.pullUp != "DOWN") and (args.pullUp != "UP"):
    logging.error("Pull up/down mode must be 'UP' or 'DOWN'.")
    sys.exit(1)
  if (args.write < -1) or (args.write > 1):
    logging.error("You must write element 0 or 1 (or -1 to not use write mode).")
    sys.exit(1)

  # Set GPIO mode to use "Board PIN number" as reference
  GPIO.setmode(GPIO.BOARD)

  # Setup mode
  if args.read:
    pull_up_mode = GPIO.PUD_DOWN
    if args.pullUp == "UP":
      pull_up_mode = GPIO.PUD_UP
      logging.debug("Setting IN mode to PIN {} with pull-down mode.".format(str(args.gpio)))
    else:
      logging.debug("Setting IN mode to PIN {} with pull-down mode.".format(str(args.gpio)))
    GPIO.setup(args.gpio, GPIO.IN, pull_up_down=pull_up_mode)
  else:
    logging.debug("Setting OUT mode to PIN.".format(str(args.gpio)))
    GPIO.setup(args.gpio, GPIO.OUT)

  # Read/Write value
  if args.read:
    read_value = GPIO.input(args.gpio)
    logging.debug("Reading value {}.".format(str(read_value)))
    print(read_value)
  else:
    output_value = GPIO.LOW
    if args.write == 1:
      output_value = GPIO.HIGH
    GPIO.output(args.gpio, output_value)
    logging.debug("PIN set to {}.".format(str(output_value)))

  # Clean all GPIO changes made in this script
  GPIO.cleanup()

  # Quit the program without error
  sys.exit(0)
