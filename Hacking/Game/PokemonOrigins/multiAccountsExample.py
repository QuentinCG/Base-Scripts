#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Do minimalistics actions in pokemon-origins.com website with multiple accounts
  Note: accounts variable must be filled in the source code (line 21)
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "3.+"
__version__ = "1.0 (2017/10/22)"
__status__ = "Usable"
__dependency__ = "request & bs4"

import logging
import PokemonOrigins

# Please put all your pokemon-origins.com logins and passwords here
accounts = [
  {"login": "YOUR_LOGIN_1_HERE", "password": "YOUR_PASSWORD_1_HERE"},
  {"login": "YOUR_LOGIN_2_HERE", "password": "YOUR_PASSWORD_2_HERE"},
  # and so on... (as many accounts as you want)
]

if __name__ == '__main__':
  # Add Logs
  logger = logging.getLogger()
  logger.setLevel(logging.WARNING)

  # Do the actions with all specified accounts
  for account in accounts:
    conn = PokemonOrigins.PokemonOrigins()
    if conn.connect(login=account['login'], password=account['password']):
      print("Connected to {}".format(account['login']))
      conn.doAllBonus()
      print("All bonus done")
      conn.doAllMissions()
      print("All missions done")

      if conn.disconnect():
        print("Disconnected")
      else:
        print("Not disconnected...")
    else:
      print("Could not connect to {}".format(account['login']))
