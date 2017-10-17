#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Test PokemonOrigins class (please specify a valid login and password)
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2017/10/13)"
__status__ = "Usable"
__dependency__ = "request & bs4"

import unittest
import logging
import PokemonOrigins

class TestPokemonOrigins(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.login = "TO MODIFY"
    self.password = "TO MODIFY"

  def setUp(self):
    self.conn = PokemonOrigins.PokemonOrigins()
    self.assertTrue(self.conn.connect(login=self.login, password=self.password))

  def tearDown(self):
    self.conn.disconnect()

  @unittest.skip("Comment this line to test")
  def testConnectAndDisconnect(self):
    conn_ok = PokemonOrigins.PokemonOrigins()
    self.assertTrue(conn_ok.connect(login=self.login, password=self.password))
    self.assertTrue(conn_ok.disconnect())

  # Not done since it could be seen as hacking
  #conn_fail = PokemonOrigins.PokemonOrigins()
  #self.assertFalse(conn_fail.connect(login="admin", password="admin"))
  #self.assertTrue(conn_fail.disconnect())

  @unittest.skip("Comment this line to test")
  def testDoAllBonus(self):
    self.conn.doAllBonus()

  @unittest.skip("Comment this line to test")
  def testMissions(self):
    available_missions = []
    available_pokemons = []
    self.conn.getAvailableMissionsAndPokemons(available_missions=available_missions,
                                              available_pokemons=available_pokemons)
    if len(available_pokemons) > 0:
      self.assertTrue(len(available_missions) > 0)

    # Not done since it could be seen as hacking
    #self.assertFalse(self.conn.doMission(0, 0))

    if len(available_pokemons) > 0 and len(available_missions) > 0:
      self.assertTrue(self.conn.doMission(mission=available_missions[0],
                                          pokemon=available_pokemons[0]))

    self.conn.doAllMissions()

  @unittest.skip("Comment this line to test")
  def testMap(self):
    self.assertTrue(self.conn.goToInMap(x=96, y=19))
    self.assertTrue(self.conn.goToInMap(x=95, y=20))

    # Not done since it could be seen as hacking
    #self.assertFalse(self.conn.goToInMap(x=100, y=20))

  @unittest.skip("Comment this line to test")
  def testStopTips(self):
    self.conn.stopTips()

if __name__ == '__main__':
  # Add Logs
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  # Launch all test
  unittest.main()
