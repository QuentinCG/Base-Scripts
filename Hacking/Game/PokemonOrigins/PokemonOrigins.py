#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Do actions on pokemon-origins.com website
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2017/10/13)"
__status__ = "Usable"
__dependency__ = "request & bs4"

import logging
import sys, getopt
import sys
import time
import requests
from bs4 import BeautifulSoup

class PokemonOrigins:
  """Class to do actions on pokemon-origins.com
  """
  __WAIT_AFTER_REQUEST = 1 # Sec
  __BASE_WEBSITE = "http://www.pokemon-origins.com"

  def __init__(self):
    self.session = requests.Session()

  def connect(self, login, password):
    """Connect to the website with specific identification

    Keyword arguments:
      login -- (str) Login
      password -- (str) Password

    return: (bool) Is connected?
    """
    login_url = "{}/connexion.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "pseudo": login,
               "mdp": password,
               "action": "identification",
               "identification": "identification"
              }

    post_login = self.session.post(url=login_url, data=payload)

    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    result = ("Vous êtes maintenant connecté." in post_login.text)
    if result:
      logging.debug("Connected to {}".format(login))
    else:
      logging.warning("Could not connect to {}".format(login))

    return result

  def disconnect(self):
    """Disconnect from the website

    return: (bool) Is disconnected?
    """
    disconnection_url = "{}/deconnexion.php".format(PokemonOrigins.__BASE_WEBSITE)
    disconnection_status = self.session.get(url=disconnection_url)

    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    result = ("Votre session a bien été arretée!" in disconnection_status.text)
    if result:
      logging.debug("Disconnected")
    else:
      logging.warning("Could not disconnect")

    return result

  def doAllBonus(self):
    """Do all 3 bonus to get in-game gold
    """
    bonus_uris = {
                   "bonus1.php",
                   "bonus2.php",
                   "bonus3.php"
                 }

    for bonus_uri in bonus_uris:
      # Get base bonus page and check if it is possible to get the bonus
      if bonus_uri in self.session.get("{}/bonus.php".format(PokemonOrigins.__BASE_WEBSITE)).text:
        time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
        # Then get the bonus
        self.session.get("{}/{}".format(PokemonOrigins.__BASE_WEBSITE, bonus_uri))
        time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
        logging.debug("Bonus {} done.".format(bonus_uri))
      else:
        logging.warning("No bonus possible for {} (already done)".format(bonus_uri))
        time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

  def getAvailableMissionsAndPokemons(self):
    """Get a list of all available missions and pokemons available to do missions

    return:
      available_missions -- (list) List of available missions
      available_pokemons -- (list) List of available pokemons
    """
    available_missions = []
    available_pokemons = []

    mission_url = "{}/missions.php".format(PokemonOrigins.__BASE_WEBSITE)

    missions_data = BeautifulSoup(self.session.get(url=mission_url).text, "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Get the list of all missions and usable pokemons
    all_forms = missions_data.findAll("form")
    for form in all_forms:
      inputs = form.findAll("input")
      # Add the mission id to the list of possible missions
      try:
        id_mission = str(form.find('input', {'name': 'id_mission'}).get("value"))
        available_missions.append(id_mission)
      except AttributeError:
        pass

      # Add all available pokemons (if not already done)
      if len(available_pokemons) <= 0:
        try:
          for id_pokemon in form.findAll("option"):
            available_pokemons.append(id_pokemon['value'])
        except AttributeError:
          pass

    logging.debug("Available missions: {}".format(available_missions))
    logging.debug("Available pokemons: {}".format(available_pokemons))

    return available_missions, available_pokemons

  def doMission(self, mission, pokemon):
    """Do a mission with a pokemon

    Keyword arguments:
      mission -- (str) Mission to do
      pokemon -- (str) Pokemon to use for the mission

    return: (bool) Done?
    """
    payload = {
                "id_liste_pokemons": pokemon,
                "id_mission": mission,
                "action" : "inscription"
              }
    try:
      post_mission = self.session.post(url="{}/missions.php".format(PokemonOrigins.__BASE_WEBSITE), data=payload)

    except requests.exceptions.ContentDecodingError:
      # This error may occur but should not break all the process
      logging.error("Error while trying to parse data from mission {} with pokemon {}".format(missions[0], pokemons[0]))
      time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
      return False

    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    result = ("Votre pokémon est revenu de mission" in post_mission.text)
    if result:
      logging.debug("Mission {} with pokemon {} done".format(mission, pokemon))
    else:
      logging.warning("Could not perform mission {} with pokemon {}".format(mission, pokemon))

    return result

  def doAllMissions(self):
    """Do all missions with all pokemons
    """
    missions = []
    pokemons = []

    missions, pokemons = self.getAvailableMissionsAndPokemons()

    while len(pokemons) > 0:
      while len(missions) > 0 and len(pokemons) > 0:
        self.doMission(mission=missions[0], pokemon=pokemons[0])
        pokemons.remove(pokemons[0])
        missions.remove(missions[0])

      missions, pokemons = self.getAvailableMissionsAndPokemons()

      # It may occur that there is no missions left for available pokemons
      # Just wait before some missions becomes available
      if len(missions) <= 0 and len(pokemons) > 0:
        time.sleep(60)

  def goToInMap(self, x, y):
    """Move to specific coordonates in the map

    Keyword arguments:
      x -- (int) Horizontal coordonates
      y -- (int) Vertical coordonates

    return: (bool) Done?
    """
    move_url = "{}/carte2.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "horizontal": int(x),
               "vertical": int(y)
              }

    self.session.get(url=move_url, params=payload)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Since info in previous request are now up to date, check result with an other request
    check_move_url = "{}/carte.php".format(PokemonOrigins.__BASE_WEBSITE)
    move_status = self.session.get(url=check_move_url)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    result = ("Vous êtes actuellement en ({},{})".format(str(int(y)), str(int(x))) in move_status.text)

    if result:
      logging.debug("Moved to ({},{})".format(str(int(x)), str(int(y))))
    else:
      logging.warning("Could not move to ({},{})".format(str(int(x)), str(int(y))))

    return result

  def stopTips(self):
    """Stop showing tips in the map page
    """
    stop_tips_url = "{}/carte.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "action": "end_astuces"
              }

    self.session.get(url=stop_tips_url, params=payload)

  def getOwnedGoldAndDollars(self):
    """Get the dollars and gold amount of the account

    return:
      result -- (bool) The retrieved data are correct
      gold -- (int) Gold (-1 if error)
      dollars -- (int) Dollars (-1 if error)
    """
    gold = -1
    dollars = -1

    all_data = BeautifulSoup(self.session.get(url=PokemonOrigins.__BASE_WEBSITE).text,
                             "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Parse dollars and gold values from the html data
    all_bold = all_data.findAll("b")
    next_is_gold = False
    for bold in all_bold:
      if "$" in bold.text:
        data_dollars = bold.text.replace(" ", "")
        data_dollars = data_dollars.replace("$", "")
        dollars=int(data_dollars)
        logging.debug("Found {} dollars in this account".format(str(dollars)))
        next_is_gold = True
      elif next_is_gold:
        data_gold = bold.text.replace(" ", "")
        gold = int(data_gold)
        logging.debug("Found {} gold in this account".format(str(gold)))
        return True, gold, dollars

    return False, gold, dollars

  def getOwnedPokemons(self):
    """Get the pokemons of the account

    return:
      result -- (bool) The retrieved data are correct
      active_pokemon -- (int) Current pokemon
      inactive_pokemons -- (list) List of all owned pokemons (not active)
    """
    active_pokemon = -1
    inactive_pokemons = []

    all_data = BeautifulSoup(self.session.get(url=PokemonOrigins.__BASE_WEBSITE).text,
                             "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Parse dollars and gold values from the html data
    all_links = all_data.findAll("a")
    for link in all_links:
      if "vos_pokemons.php?id=" in link['href']:
        active_pokemon = int(link['href'].replace("vos_pokemons.php?id=", ""))
        logging.debug("Found active pokemon: {}".format(str(active_pokemon)))
      elif "carte.php?pokemon_actif=" in link['href']:
        inactive_pokemon = int(link['href'].replace("carte.php?pokemon_actif=", ""))
        inactive_pokemons.append(inactive_pokemon)
        logging.debug("Found inactive pokemon: {}".format(str(inactive_pokemon)))

    return (active_pokemon != -1), active_pokemon, inactive_pokemons

if __name__ == "__main__":
  """Demo on how to periodically connect and do actions to the website"""

  # Add Logs
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  # Get the login and the password from command line
  arg_login = ""
  arg_password = ""
  try:
    opts, args = getopt.getopt(sys.argv[1:], "l:p:", ["login=", "password="])
  except getopt.GetoptError as err:
    print("[ERROR] "+str(err))
    sys.exit(1)
  for o, a in opts:
    if o in ("-l", "--login"):
      arg_login = str(a)
    elif o in ("-p", "--password"):
      arg_password = str(a)
    else:
      print("[ERROR] Not handled parameters (only login (-l) and password (-p) available.")
  if arg_login == "" or arg_password == "":
    print("[ERROR] Login (-l) and password (-p) must be provided.")
    sys.exit(1)

  # Instantiate the class
  pkm_orig = PokemonOrigins()

  # Connect
  if (pkm_orig.connect(login=arg_login, password=arg_password)):
    # Do some actions in the website
    pkm_orig.doAllBonus()
    pkm_orig.doAllMissions()
    pkm_orig.getOwnedGoldAndDollars()
    pkm_orig.getOwnedPokemons()
    pkm_orig.disconnect()

    # Quit the program without error
    sys.exit(0)

  # Could not connect...
  sys.exit(2)