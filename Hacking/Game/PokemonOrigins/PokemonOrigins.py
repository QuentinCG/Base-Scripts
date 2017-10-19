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
import re #RegExp
import random

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

  def __getAvailableMissionsAndPokemonsForMission(self):
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

  def __doMission(self, mission, pokemon):
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

    missions, pokemons = self.__getAvailableMissionsAndPokemonsForMission()

    while len(pokemons) > 0:
      while len(missions) > 0 and len(pokemons) > 0:
        self.__doMission(mission=missions[0], pokemon=pokemons[0])
        pokemons.remove(pokemons[0])
        missions.remove(missions[0])

      missions, pokemons = self.__getAvailableMissionsAndPokemonsForMission()

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
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

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
      active_pokemon -- ({"pokemon":int, "action_points":int}) Current pokemon
      inactive_pokemons -- ([{"pokemon":int, "action_points":int}, ...]) List of all owned pokemons (not active)
      is_level_100 -- (bool) Check if the level of the current pokemon is 100
      can_level_up -- (bool) Check if the current pokemon can level up
    """
    active_pokemon = {"id":-1, "action_points":-1}
    inactive_pokemons = []
    is_level_100 = False
    can_level_up = False

    response = self.session.get(url=PokemonOrigins.__BASE_WEBSITE)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Parse active and inactive pokemons from the html data
    all_pokemons = BeautifulSoup(response.text, "html.parser")
    all_links = all_pokemons.findAll("a")
    for link in all_links:
      if "vos_pokemons.php?id=" in link['href']:
        active_pokemon['id'] = int(link['href'].replace("vos_pokemons.php?id=", ""))
        logging.debug("Found active pokemon: {}".format(str(active_pokemon['id'])))

    table_inactive = all_pokemons.find("table", id="table_pokemons_inactifs")
    for pokemon in table_inactive.findAll("tr"):
      if pokemon.find("a"):
        link = pokemon.find("a")['href']
        if "carte.php?pokemon_actif=" in link:
          # Get the inactive pokemon ID
          inactive_pokemon_id = int(link.replace("carte.php?pokemon_actif=", ""))

          # Get the action points of the inactive pokemon
          found_action_points = False
          for tr in pokemon:
            if tr.find("img"):
              inactive_pokemon_action_point = int(re.sub("[^0-9]", "", str(tr.text)))
              inactive_pokemons.append({'id':inactive_pokemon_id, 'action_points': inactive_pokemon_action_point})
              logging.debug("Found inactive pokemon: {} with {} action points".format(str(inactive_pokemon_id), str(inactive_pokemon_action_point)))
              found_action_points = True
          if not found_action_points:
              logging.warning("Could not get the action points of pokemon {}".format(str(inactive_pokemon_id)))

    # Get info to know if current pokemon is level 100
    if "px;\"> lvl 100" in response.text:
      is_level_100 = True
      logging.debug("Current pokemon is level 100")
    else:
      logging.debug("Current pokemon is not level 100")

    # Get info to know if current pokemon can level up
    result_xp = re.search('XP :</b> (.*)<br', response.text)
    result_xp = re.sub("[^0-9/]", "", str(result_xp.group(1)))
    current_xp, xp_to_lvl_up = result_xp.split("/")
    if (int(current_xp) > int(xp_to_lvl_up)):
      can_level_up = True
      logging.debug("Current pokemon can level up")
    else:
      logging.debug("Current pokemon can't level up")

    # Get info to know the remaining action points
    result_action_points = re.search('Points d\'action :</b> (.*)<br', response.text)
    result_action_points = re.sub("[^0-9/]", "", str(result_action_points.group(1)))
    current_action_points, max_action_points = result_action_points.split("/")
    active_pokemon['action_points'] = current_action_points
    logging.debug("Action points of active pokemon: {}".format(str(active_pokemon['action_points'])))

    return (active_pokemon['id'] != -1), active_pokemon, inactive_pokemons, is_level_100, can_level_up

  def selectMainPokemon(self, pokemon_id):
    """Select main pokemon and get some important data on it

    Keyword arguments:
      pokemon_id -- (int) Inactive pokemon id to set as active

    return:
      result -- (bool) The retrieved data are correct
    """
    select_url = "{}/carte.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "pokemon_actif": pokemon_id
              }

    response = self.session.get(url=select_url, params=payload)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Confirm change
    res, active, not_actives, is_level_100, can_level_up = self.getOwnedPokemons()

    if (active['id'] == pokemon_id):
      logging.debug("Active pokemon is now {}".format(str(pokemon_id)))
      return True

    logging.warning("Could not set pokemon {} as active".format(str(pokemon_id)))
    return False

  def __levelUpPokemon(self, pokemon_id):
    """Level up a pokemon (if < 100) else upgrade caracteristics

    Keyword arguments:
      pokemon_id -- (int) Pokemon id to level up

    return:
      result -- (bool) Pokemon level up
    """
    if self.selectMainPokemon(pokemon_id=pokemon_id):
      res, active_pokemon, inactive_pokemons, is_level_100, can_level_up = self.getOwnedPokemons()
      if res:
        if can_level_up:
          if is_level_100:
            lvl_up_url = "{}/update_lvl_100.php".format(PokemonOrigins.__BASE_WEBSITE)

            possible_caract = ["pv", "att", "def", "vit", "attspe", "defspe"]
            payload = {
               "action": "augmenter",
               "caracteristique": possible_caract[random.randint(0, 5)]
            }
            params = {
               "id": pokemon_id
            }
            post_lvl_up = self.session.post(url=lvl_up_url, data=payload, params=params)
            time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

            if ("Les caractéristiques ont bien été mises à jour" in post_lvl_up.text):
              # Level up again and again until it is fully upgraded
              while self.__levelUpPokemon(pokemon_id):
                logging.debug("Trying again to upgrade Pokemon {}".format(str(pokemon_id)))
              logging.debug("Pokemon {} caracteristics upgraded".format(str(pokemon_id)))
              return True
            else:
              logging.warning("Pokemon {} caracteristics not upgraded".format(str(pokemon_id)))
              return False
          else:
            lvl_up_url = "{}/update_lvl.php".format(PokemonOrigins.__BASE_WEBSITE)
            payload = {
               "id": pokemon_id,
              }
            post_lvl_up = self.session.post(url=lvl_up_url, data=payload)
            time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

            if ("Le pokémon gagn" in post_lvl_up.text):
              logging.debug("Pokemon {} leveled up".format(str(pokemon_id)))
              return True
            else:
              logging.warning("Pokemon {} did not level up".format(str(pokemon_id)))
              return False
        else:
          # Can't level up, pass
          logging.debug("Pokemon {} does not need to level up".format(str(pokemon_id)))
          return False
      else:
        return False
    else:
      return False

    return False

  def levelUpAllPokemons(self):
    """Level up all pokemons (if < 100) else upgrade caracteristics

    return:
      result -- (bool) All pokemon tried to level up
    """
    res, active_pokemon, inactive_pokemons, is_level_100, can_level_up = self.getOwnedPokemons()
    if res:
      logging.debug("Trying to level up pokemon {}".format(str(active_pokemon['id'])))
      self.__levelUpPokemon(active_pokemon['id'])
      for pokemon in inactive_pokemons:
        logging.debug("Trying to level up pokemon {}".format(str(inactive_pokemons)))
        self.__levelUpPokemon(pokemon['id'])

    return res

  def __getPokemonsThatCanEvolve(self):
    """Get a list of all pokemons that can evolve

    return:
      pokemons -- (list) All pokemon that can evolve
    """
    all_pokemons_that_can_evolve = []

    pokemons_url = "{}/vos_pokemons.php".format(PokemonOrigins.__BASE_WEBSITE)
    all_data = BeautifulSoup(self.session.get(url=pokemons_url).text, "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    for form in all_data.findAll("form"):
      # Find the right form
      if form.find('input', {'name': 'action'}):
        if form.find('input', {'name': 'action'}).get("value") == "voir_pokemon":
          for id_pokemon in form.findAll("option"):
            if "(peut évoluer)" in id_pokemon.text:
              logging.debug("Pokemon {} with ID {} can evolve"
                .format(id_pokemon.text.replace(" (peut évoluer)", ""),
                        id_pokemon['value']))
              all_pokemons_that_can_evolve.append(id_pokemon['value'])

    return all_pokemons_that_can_evolve

  def evolveAllPokemons(self):
    """Evolve all pokemons

    return:
      evolved -- (bool) All pokemons evolved properly
    """
    pokemons_url = "{}/vos_pokemons.php".format(PokemonOrigins.__BASE_WEBSITE)

    all_evolved_properly = True
    pokemons_to_evolve = self.__getPokemonsThatCanEvolve()

    while len(pokemons_to_evolve) > 0:
      for pokemon in pokemons_to_evolve:
        payload = {
                    "action": "voir_pokemon",
                    "pokemon": pokemon
                  }
        pokemon_data = BeautifulSoup(self.session.post(url=pokemons_url, data=payload).text, "html.parser")
        time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

        for form in pokemon_data.findAll("form"):
          # Find the right form
          if form.find('input', {'name': 'id_pokedex_evo'}) and \
             form.find('input', {'name': 'id'}) and \
             form.find('input', {'name': 'evolution'}) and \
             form.find('input', {'name': 'action'}) and \
             form.find('input', {'name': 'pokemon'}) and \
             form.find('input', {'name': 'id'}):
            id_pokedex_evo = form.find('input', {'name': 'id_pokedex_evo'}).get("value")
            id = form.find('input', {'name': 'id'}).get("value")
            evolution = form.find('input', {'name': 'evolution'}).get("value")
            action = form.find('input', {'name': 'action'}).get("value")
            pokemon = form.find('input', {'name': 'pokemon'}).get("value")
            payload = {
                        "id_pokedex_evo": id_pokedex_evo,
                        "id": id,
                        "evolution": evolution,
                        "action": action,
                        "pokemon": pokemon
                      }
            evolve_result = self.session.post(url=pokemons_url, data=payload).text
            time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
            if "a bien évolué" in evolve_result:
              logging.debug("Pokemon {} evolved".format(pokemon))
            else:
              logging.warning("Pokemon {} did not evolve".format(pokemon))
              all_evolved_properly = False
      pokemons_to_evolve = self.__getPokemonsThatCanEvolve()

    logging.debug("All pokemons evolved properly: {}".format(str(all_evolved_properly)))
    return all_evolved_properly

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
    #pkm_orig.doAllBonus()
    #pkm_orig.doAllMissions()
    #pkm_orig.getOwnedGoldAndDollars()
    #pkm_orig.getOwnedPokemons()
    #pkm_orig.levelUpAllPokemons()
    #pkm_orig.evolveAllPokemons()
    pkm_orig.disconnect()

    # Quit the program without error
    sys.exit(0)

  # Could not connect...
  sys.exit(2)
