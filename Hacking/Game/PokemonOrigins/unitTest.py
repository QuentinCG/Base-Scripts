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
    self.login = "testPy"
    self.password = "testPy"

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
  #self.assertFalse(conn_fail.connect(login=self.login, password="{}notPass".format(self.password)))
  #self.assertTrue(conn_fail.disconnect())

  @unittest.skip("Comment this line to test")
  def testDoAllBonus(self):
    self.conn.doAllBonus()

  @unittest.skip("Comment this line to test")
  def testMissions(self):
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

  @unittest.skip("Comment this line to test")
  def testGoldAndDollars(self):
    res, gold, dollars = self.conn.getOwnedGoldAndDollars()
    self.assertTrue(res)
    self.assertNotEqual(gold, -1)
    self.assertNotEqual(dollars, -1)

  @unittest.skip("Comment this line to test")
  def testOwnedPokemonsAndSelectMain(self):
    res, active_pokemon, inactive_pokemons, is_level_100, can_level_up = self.conn.getOwnedPokemons()
    self.assertTrue(res)
    self.assertNotEqual(active_pokemon['id'], -1)

    # Try to change active pokemon by an other
    if len(inactive_pokemons) > 0:
      self.assertTrue(self.conn.selectMainPokemon(inactive_pokemons[0]['id']))
      res, active_pokemon_2, inactive_pokemons_2, is_level_100, can_level_up = self.conn.getOwnedPokemons()
      self.assertTrue(res)
      self.assertEqual(inactive_pokemons[0]['id'], active_pokemon_2['id'])

  @unittest.skip("Comment this line to test")
  def testLevelUp(self):
    self.conn.levelUpAllPokemons()

  @unittest.skip("Comment this line to test")
  def testEvolveAllPokemons(self):
    self.conn.evolveAllPokemons()

  @unittest.skip("Comment this line to test")
  def testFindWildPokemons(self):
    self.conn.findWildPokemons(x=95, y=20)
    self.conn.findWildPokemonsInArea(x1=95, y1=20, x2=96, y2=19)

if __name__ == '__main__':
  # Add Logs
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  # Launch all test
  unittest.main()
