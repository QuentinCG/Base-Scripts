#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Do actions on pokemon-origins.com website
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
import sys, getopt
import sys
import time
import requests
from bs4 import BeautifulSoup
import re #RegExp
import random

# Python 2-3 compatibility (in order to use xrange)
try:
  xrange
except NameError:
  xrange = range

class PokemonOrigins:
  """Class to do numerous actions on pokemon-origins.com automatically
  """
  __WAIT_AFTER_REQUEST = 1 # Sec
  __BASE_WEBSITE = "http://www.pokemon-origins.com"

  class eItemIds:
    POKEBALL = 1
    SUPERBALL = 2
    HYPERBALL = 3
    MASTERBALL = 4
    POTION = 10
    SUPER_POTION = 11
    HYPER_POTION = 12
    MAX_POTION = 13

  class eDracoportLocalization:
    BOURG_PALETTE = 1
    JADIELLE = 2
    WEST_JADIELLE = 3
    SOUTH_JADIELLE = 4
    SOUTH_ARGENTA = 5
    EST_ARGENTA = 6
    ARGENTA = 7
    MINE = 8
    AZURIA = 9
    SOUTH_EST_AZURIA = 10
    BREEDERS_HOUSE = 11
    SAFRANIA = 12
    EST_SAFRANIA = 13
    CARMIN_SUR_MER = 14
    CELADOPOLE = 15
    BICYCLE = 16
    SOUTH_BICYCLE = 17
    MIDDLE_BICYCLE = 18
    PARMANIE = 19
    SAFARI_PARK = 20
    EST_CARMIN_SUR_MER = 21
    EST_PARMANIE = 22
    ICE_ISLAND = 23
    CRAMOISILE = 24
    VICTORY_ROAD = 25
    SOUTH_VICTORY_ROAD = 26
    POKEMON_LEAGUE = 27
    BOURG_GEON = 28
    MAUVILLE = 29
    ECORSIA = 30
    DOUBLONVILLE = 31
    # Undefined id 32
    ACAJOU = 33
    ROSALIA = 34
    EBENELLE = 35
    OLIVILLE = 36
    IRISIA = 37
    BOURG_EN_VOL = 38

  def __init__(self):
    self.session = requests.Session()

################### Connection settings ###################

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

########################## Bonus ##########################

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

######################## Missions #########################

  def getAvailableMissionsAndPokemonsForMission(self):
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

    missions, pokemons = self.getAvailableMissionsAndPokemonsForMission()

    while len(pokemons) > 0:
      while len(missions) > 0 and len(pokemons) > 0:
        self.doMission(mission=missions[0], pokemon=pokemons[0])
        pokemons.remove(pokemons[0])
        missions.remove(missions[0])

      missions, pokemons = self.getAvailableMissionsAndPokemonsForMission()

      # It may occur that there is no missions left for available pokemons
      # Just wait before some missions becomes available
      if len(missions) <= 0 and len(pokemons) > 0:
        time.sleep(60)

########################### Map ############################

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

########################## Utils ##########################

  def stopTips(self):
    """Stop showing tips in the map page
    """
    stop_tips_url = "{}/carte.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "action": "end_astuces"
              }

    self.session.get(url=stop_tips_url, params=payload)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

  def getAccountInfo(self):
    """Get the dollars and gold amount of the account

    return:
      result -- (bool) The retrieved data are correct
      gold -- (int) Gold (-1 if error)
      dollars -- (int) Dollars (-1 if error)
      score -- (int) Score (-1 if error)
      rank -- (int) Rank (-1 if error)
      owned_pokemons -- (int) Number of owned pokemons (-1 if error)
      max_pokemons -- (int) Number of maximum pokemons the account can have (-1 if error)
    """
    gold = -1
    dollars = -1
    score = -1
    rank = -1
    owned_pokemons = -1
    max_pokemons = -1

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
        next_is_gold = False
        logging.debug("Found {} gold in this account".format(str(gold)))
      elif "Score : " in bold.text:
        score = int(bold.text.replace("Score : ", ""))
        logging.debug("Found score of {} on this account".format(str(score)))
      elif "Rang : " in bold.text:
        rank = int(bold.text.replace("Rang : ", ""))
        logging.debug("Found rank of {} on this account".format(str(rank)))
      elif "BDS : " in bold.text:
        res = re.sub("[^0-9/]", "", str(bold.text)).split("/")
        if len(res) == 2:
          owned_pokemons = int(res[0])
          max_pokemons = int(res[1])
          logging.debug("{}/{} pokemons available on this account".format(str(owned_pokemons), str(max_pokemons)))
          return True, gold, dollars, score, rank, owned_pokemons, max_pokemons
        else:
          logging.warning("Error while getting the number of owned pokemons and max pokemons")
          return False, gold, dollars, score, rank, owned_pokemons, max_pokemons

    return False, gold, dollars, score, rank, owned_pokemons, max_pokemons

######################## Dracoport ########################

  def useDracoport(self, dracoport_localization):
    """Go to a specific place with the dracoport

    Keyword arguments:
      dracoport_localization -- (PokemonOrigins.eDracoportLocalization) Dracoport localization

    return:
      success -- (bool) Used dracoport with success
    """
    dracoport_url = "{}/dracoport.php".format(PokemonOrigins.__BASE_WEBSITE)

    # Grab all data needed to go to a specific place
    id = int(dracoport_localization)
    price = -1
    x = -1
    y = -1
    found_data = 0
    all_data = BeautifulSoup(self.session.get(url=dracoport_url).text, "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
    data = all_data.find("table", id="profil")
    for form in data.findAll("form"):
      if form.find('input', {'name': 'id'}):
        if int(form.find('input', {'name': 'id'}).get("value")) == int(dracoport_localization):
          # Found the right localization to go, sol let's grab all inputs needed to go to this place
          for input in form.findAll("input"):
            if input.get("name") == "cout":
              price = int(input.get("value"))
              found_data = found_data + 1
            if input.get("name") == "pos_hor":
              x = int(input.get("value"))
              found_data = found_data + 1
            if input.get("name") == "pos_ver":
              y = int(input.get("value"))
              found_data = found_data + 1

    # Be sure we grabbed all data needed for the request to use dracoport
    if found_data == 3:
      payload = {
                  "id": id,
                  "cout": price,
                  "pos_hor": x,
                  "pos_ver": y
                }
      result = self.session.post(url=dracoport_url, data=payload)
      time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
      success = "Vous êtes arrivé à destination!" in result.text
      if success:
        logging.debug("You used the dracoport to go to place {}".format(str(dracoport_localization)))
      else:
        logging.warning("Could not use the dracoport to go to place {} (x={}, y={}, price={})".format(str(dracoport_localization), str(x), str(y), str(price)))
    else:
      logging.warning("Could not find data relative to the localization you want to go")
      return False

    return success

######################## Pokemons #########################

  def getOwnedPokemons(self, auto_level_up=True):
    """Get the pokemons of the account

    return:
      result -- (bool) The retrieved data are correct
      active_pokemon -- ({"id":int, "action_points":int}) Current pokemon
      inactive_pokemons -- ([{"id":int, "action_points":int, "level":int}, ...]) List of all owned pokemons (not active)
      is_level_100 -- (bool) Check if the level of the current pokemon is 100
      can_level_up -- (bool) Check if the current pokemon can level up
    """
    active_pokemon = {"id":-1, "action_points":-1, "level":-1}
    inactive_pokemons = []
    is_level_100 = False
    can_level_up = False

    response = self.session.get(url=PokemonOrigins.__BASE_WEBSITE)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    # Parse active and inactive pokemons from the html data
    all_pokemons = BeautifulSoup(response.text, "html.parser")
    for link in all_pokemons.findAll("a"):
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
          found_pokemon_level = False
          dict_pokemon = {}
          dict_pokemon['id'] = int(inactive_pokemon_id)
          for tr in pokemon:
            if tr.find("img"):
              dict_pokemon['action_points'] = int(re.sub("[^0-9]", "", str(tr.text)))
              found_action_points = True
            if "lvl " in tr.text:
              dict_pokemon['level'] = int(tr.text.replace("lvl ", ""))
              found_pokemon_level = True
          if not found_action_points:
              logging.warning("Could not get the action points of pokemon {}".format(str(inactive_pokemon_id)))
          if not found_pokemon_level:
              logging.warning("Could not get the level of pokemon {}".format(str(inactive_pokemon_id)))

          if found_action_points and found_pokemon_level:
            inactive_pokemons.append(dict_pokemon)

    # Get info to know if current pokemon is level 100
    if "px;\"> lvl 100" in response.text:
      is_level_100 = True
      active_pokemon['level'] = 100
      logging.debug("Current pokemon is level 100")
    else:
      logging.debug("Current pokemon is not level 100")
      index_level = response.text.index("px;\"> lvl ") + 10
      found_level = response.text[index_level:index_level+3]
      active_pokemon['level'] = int(re.sub("[^0-9]", "", found_level))
      logging.debug("Current pokemon is level {}".format(str(active_pokemon['level'])))

    # Get info to know if current pokemon can level up
    result_xp = re.search('XP :</b> (.*)<br', response.text)
    result_xp = re.sub("[^0-9/]", "", str(result_xp.group(1)))
    current_xp, xp_to_lvl_up = result_xp.split("/")
    if (int(current_xp) > int(xp_to_lvl_up)):
      can_level_up = True
      logging.debug("Current pokemon can level up")
      if auto_level_up:
        self.levelUpPokemon(active_pokemon['id'])
    else:
      logging.debug("Current pokemon can't level up")

    # Get info to know the remaining action points
    result_action_points = re.search('Points d\'action :</b> (.*)<br', response.text)
    result_action_points = re.sub("[^0-9/]", "", str(result_action_points.group(1)))
    current_action_points, max_action_points = result_action_points.split("/")
    active_pokemon['action_points'] = int(current_action_points)
    logging.debug("Action points of active pokemon: {}".format(str(active_pokemon['action_points'])))

    return (active_pokemon['id'] != -1), active_pokemon, inactive_pokemons, is_level_100, can_level_up

  def getOwnedPokemonsWithActionPoints(self, level_requirement=-1):
    """Get the pokemons of the account having action points

    Keyword arguments:
      level_requirement -- (int, optional) If specified, get only pokemons with level >= level_requirement

    return:
      pokemons_with_ap -- ([]) List of all owned pokemons (active and inactive) having action points
    """
    result, active_pokemon, inactive_pokemons, is_level_100, can_level_up = self.getOwnedPokemons()

    pokemons_with_ap = []
    if not result:
      logging.warning("An error occured while getting the pokemon informations")
      return pokemons_with_ap

    if active_pokemon['action_points'] > 0:
      if level_requirement == -1 or active_pokemon['level'] >= level_requirement:
        pokemons_with_ap.append(active_pokemon['id'])

    for pokemon in inactive_pokemons:
      if pokemon['action_points'] > 0:
        if level_requirement == -1 or pokemon['level'] >= level_requirement:
          pokemons_with_ap.append(pokemon['id'])

    logging.debug("Pokemons with AP: {}".format(str(pokemons_with_ap)))
    return pokemons_with_ap

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

  def selectAnyMainPokemonWithAp(self, level_requirement=-1):
    """Select a random pokemon which has AP

    Keyword arguments:
      level_requirement -- (int, optional) If specified, use only pokemons with level >= level_requirement

    return:
      result -- (bool) A pokemon with AP is the main pokemon
    """
    pokemons = self.getOwnedPokemonsWithActionPoints(level_requirement=level_requirement)
    if len(pokemons) > 0:
      return self.selectMainPokemon(pokemons[0])
    else:
      return False

  def levelUpPokemon(self, pokemon_id):
    """Level up a pokemon (if < 100) else upgrade caracteristics

    Keyword arguments:
      pokemon_id -- (int) Pokemon id to level up

    return:
      result -- (bool) Pokemon level up
    """
    if self.selectMainPokemon(pokemon_id=pokemon_id):
      res, active_pokemon, inactive_pokemons, is_level_100, can_level_up = self.getOwnedPokemons(auto_level_up=False)
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
              while self.levelUpPokemon(pokemon_id):
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

    warning: This function is very slow as there is no way to optimize leveling up
             For now, two pages are loaded for any pokemon you have even if
             it can't level up or upgrade caracteristics (just to select the pokemon
             and then check if it can level up).

    return:
      result -- (bool) All pokemon tried to level up
    """
    res, active_pokemon, inactive_pokemons, is_level_100, can_level_up = self.getOwnedPokemons()
    if res:
      logging.debug("Trying to level up pokemon {}".format(str(active_pokemon['id'])))
      self.levelUpPokemon(active_pokemon['id'])
      for pokemon in inactive_pokemons:
        logging.debug("Trying to level up pokemon {}".format(str(inactive_pokemons)))
        self.levelUpPokemon(pokemon['id'])

    return res

  def getPokemonsThatCanEvolve(self):
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
    pokemons_to_evolve = self.getPokemonsThatCanEvolve()

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
      pokemons_to_evolve = self.getPokemonsThatCanEvolve()

    logging.debug("All pokemons evolved properly: {}".format(str(all_evolved_properly)))
    return all_evolved_properly

################ Wild pokemons information ################

  def findWildPokemons(self, x, y):
    """Find wild pokemon in specific coordonates

    Keyword arguments:
      x -- (int) Horizontal position
      y -- (int) Vertical position

    return:
      all_pokemons_found -- (bool) All pokemons in coordonates found (no error)
      wild_pokemons -- (list) Wild pokemons
    """
    wild_pokemons = []
    all_pokemons_found = False

    if self.goToInMap(x=x, y=y):
      wild_pokemons_url = "{}/carte.php".format(PokemonOrigins.__BASE_WEBSITE)
      wild_pokemons_data = BeautifulSoup(self.session.get(url=wild_pokemons_url).text, "html.parser")
      time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

      # Get the list of all wild pokemons
      div_wild_pokemons = wild_pokemons_data.find("div", {"id": "affichage_pokemons"})
      if div_wild_pokemons:
        for link in div_wild_pokemons.findAll("a"):
          if "carte_action.php?id=" in link['href']:
            wild_pokemon = int(link['href'].replace("carte_action.php?id=", ""))
            wild_pokemons.append(wild_pokemon)
            logging.debug("Found wild pokemon: {}".format(str(wild_pokemon)))
        all_pokemons_found = True
      else:
        logging.warning("Could not parse map ({}, {}) to get wild pokemons".format(str(x), str(y)))
    else:
      logging.warning("Could not move to ({}, {}) in order to find pokemons".format(str(x), str(y)))

    return all_pokemons_found, wild_pokemons

  def findWildPokemonsInArea(self, x1, y1, x2, y2):
    """Find wild pokemon in specific rectangle (x1, y1) -> (x2, y2)
    Even if an error occured in a coordonate, other coordonates will be checked but
    returned all_pokemons_found value will be False.

    Keyword arguments:
      x1 -- (int) Horizontal position of first dot of the rectangle
      y1 -- (int) Vertical position of first dot of the rectangle
      x2 -- (int) Horizontal position of second dot of the rectangle
      y2 -- (int) Vertical position of second dot of the rectangle

    return:
      all_pokemons_found -- (bool) All pokemons in coordonates found (no error)
      wild_pokemons -- ([{'x':pos_x, 'y':pos_y, 'pokemons':{id1, id2, ...}}, ...]) Wild pokemons with coordonates
    """
    wild_pokemons = []
    all_pokemons_found = True

    if x1 >= x2:
      x_min = int(x2)
      x_max = int(x1)
    else:
      x_min = int(x1)
      x_max = int(x2)

    if y1 >= y2:
      y_min = int(y2)
      y_max = int(y1)
    else:
      y_min = int(y1)
      y_max = int(y2)

    for x in xrange(x_min, x_max + 1):
      for y in xrange(y_min, y_max + 1):
        ok, pokemons = self.findWildPokemons(x=x, y=y)
        if ok:
          # Fill list with coordonates that have pokemons
          if len(pokemons) > 0:
            wild_pokemons.append({"x":x, "y":y, "pokemons":pokemons})
        else:
          all_pokemons_found = False
          logging.warning("Could not get wild pokemons in coordonates ({}, {})".format(str(x), str(y)))

    return all_pokemons_found, wild_pokemons

################### Attacks for battle ####################

  def getAllAttackIds(self):
    """Get a list of all attack IDs in the game

    return:
      attack_ids -- ([attack_id_1, ...]) List of all attack ids
    """
    attack_ids = []

    attack_url = "{}/pokedex_attaques.php".format(PokemonOrigins.__BASE_WEBSITE)
    attack_ids_data = BeautifulSoup(self.session.post(url=attack_url).text, "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    for form in attack_ids_data.findAll("form"):
      # Find the right form
      if form.find('input', {'name': 'action'}):
        if str(form.find('input', {'name': 'action'}).get("value")) == "voir_attaque":
          # This is the right form
          for id_attack in form.findAll("option"):
            attack_ids.append(int(id_attack['value']))

    return attack_ids

  def getAllAttacksInfo(self):
    """Get a dictionnary of all attacks in the game

    Note:
    The function returns a static dictionary as it is slow to grab all
    those data (check method below).
    The used algorithm to grab the data is shown below but is a very slow
    method to get all attack informations since it needs to parse a page
    for each attack. It was used only only once to design the static
    dictionnary returned by this function.

    return:
      attacks -- ({
                    id_attack:
                      {
                        'name':attack_name,
                        'type':attack_type,
                        'power':attack_power,
                        'precision':attack_precision,
                        'class':attack_class
                      },
                    ...
                  }) Dictionary of all attack
    """
    return \
      {
        16: {'name': 'coupe', 'type': 'normal', 'power': 50, 'precision': 95, 'class': 'physique'},
        17: {'name': 'vol', 'type': 'vol', 'power': 90, 'precision': 95, 'class': 'physique'},
        18: {'name': 'surf', 'type': 'eau', 'power': 95, 'precision': 100, 'class': 'speciale'},
        19: {'name': 'force', 'type': 'normal', 'power': 80, 'precision': 100, 'class': 'physique'},
        20: {'name': 'flash', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        21: {'name': 'mitra-poing', 'type': 'combat', 'power': 150, 'precision': 100, 'class': 'physique'},
        22: {'name': 'dracogriffe', 'type': 'dragon', 'power': 80, 'precision': 100, 'class': 'physique'},
        23: {'name': 'vibraqua', 'type': 'eau', 'power': 60, 'precision': 100, 'class': 'speciale'},
        24: {'name': 'plénitude', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        25: {'name': 'hurlement', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        26: {'name': 'toxik', 'type': 'poison', 'power': 0, 'precision': 85, 'class': 'autre'},
        27: {'name': 'grêle', 'type': 'glace', 'power': 0, 'precision': 100, 'class': 'autre'},
        28: {'name': 'gonflette', 'type': 'combat', 'power': 0, 'precision': 100, 'class': 'autre'},
        29: {'name': 'balle graine', 'type': 'plante', 'power': 10, 'precision': 100, 'class': 'physique'},
        30: {'name': 'puissance cachée', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'speciale'},
        31: {'name': 'zenith', 'type': 'feu', 'power': 0, 'precision': 100, 'class': 'autre'},
        32: {'name': 'laser glace', 'type': 'glace', 'power': 95, 'precision': 100, 'class': 'speciale'},
        33: {'name': 'blizzard', 'type': 'glace', 'power': 120, 'precision': 70, 'class': 'speciale'},
        34: {'name': 'ultralaser', 'type': 'normal', 'power': 150, 'precision': 90, 'class': 'speciale'},
        35: {'name': 'mur lumiêre', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        36: {'name': 'abri', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        37: {'name': 'danse pluie', 'type': 'eau', 'power': 0, 'precision': 100, 'class': 'autre'},
        38: {'name': 'giga-sangsue', 'type': 'plante', 'power': 60, 'precision': 100, 'class': 'speciale'},
        39: {'name': 'rune protect', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        40: {'name': 'lance-soleil', 'type': 'plante', 'power': 120, 'precision': 100, 'class': 'speciale'},
        41: {'name': 'queue de fer', 'type': 'acier', 'power': 100, 'precision': 75, 'class': 'physique'},
        42: {'name': 'tonnerre', 'type': 'electrique', 'power': 95, 'precision': 100, 'class': 'speciale'},
        43: {'name': 'fatal-foudre', 'type': 'electrique', 'power': 120, 'precision': 70, 'class': 'speciale'},
        44: {'name': 'seisme', 'type': 'sol', 'power': 100, 'precision': 100, 'class': 'physique'},
        45: {'name': 'tunnel', 'type': 'sol', 'power': 80, 'precision': 100, 'class': 'physique'},
        46: {'name': 'psyko', 'type': 'psy', 'power': 90, 'precision': 100, 'class': 'speciale'},
        47: {'name': "ball'ombre", 'type': 'spectre', 'power': 80, 'precision': 100, 'class': 'speciale'},
        48: {'name': 'casse brique', 'type': 'combat', 'power': 75, 'precision': 100, 'class': 'physique'},
        49: {'name': 'reflet', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        50: {'name': 'protection', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        51: {'name': 'onde de choc', 'type': 'electrique', 'power': 60, 'precision': 100, 'class': 'speciale'},
        52: {'name': 'lance flamme', 'type': 'feu', 'power': 95, 'precision': 100, 'class': 'speciale'},
        53: {'name': 'bomb-beurk', 'type': 'poison', 'power': 90, 'precision': 100, 'class': 'speciale'},
        54: {'name': 'déflagration', 'type': 'feu', 'power': 120, 'precision': 85, 'class': 'speciale'},
        55: {'name': 'tomberoche', 'type': 'roche', 'power': 50, 'precision': 80, 'class': 'physique'},
        56: {'name': 'aéropique', 'type': 'vol', 'power': 60, 'precision': 100, 'class': 'physique'},
        57: {'name': 'repos', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        58: {'name': 'attraction', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        59: {'name': 'charge', 'type': 'normal', 'power': 35, 'precision': 95, 'class': 'physique'},
        60: {'name': 'rugissement', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        61: {'name': 'vampigraine', 'type': 'plante', 'power': 0, 'precision': 90, 'class': 'autre'},
        62: {'name': 'fouet liane', 'type': 'plante', 'power': 35, 'precision': 100, 'class': 'physique'},
        63: {'name': 'poudre dodo', 'type': 'plante', 'power': 0, 'precision': 75, 'class': 'autre'},
        64: {'name': 'poudre toxik', 'type': 'poison', 'power': 0, 'precision': 75, 'class': 'autre'},
        65: {'name': "tranch'herbe", 'type': 'plante', 'power': 55, 'precision': 95, 'class': 'physique'},
        66: {'name': 'doux parfum', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        67: {'name': 'croissance', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        68: {'name': 'synthêse', 'type': 'plante', 'power': 0, 'precision': 100, 'class': 'autre'},
        69: {'name': 'canon graine', 'type': 'plante', 'power': 80, 'precision': 100, 'class': 'physique'},
        70: {'name': 'griffe', 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'physique'},
        71: {'name': 'flammêche', 'type': 'feu', 'power': 40, 'precision': 100, 'class': 'speciale'},
        72: {'name': 'brouillard', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        73: {'name': 'grimace', 'type': 'normal', 'power': 0, 'precision': 90, 'class': 'autre'},
        74: {'name': 'crocs feu', 'type': 'feu', 'power': 65, 'precision': 95, 'class': 'physique'},
        75: {'name': 'tranche', 'type': 'normal', 'power': 70, 'precision': 100, 'class': 'physique'},
        76: {'name': 'danse flamme', 'type': 'feu', 'power': 15, 'precision': 70, 'class': 'speciale'},
        77: {'name': 'cru-aile', 'type': 'vol', 'power': 60, 'precision': 100, 'class': 'physique'},
        78: {'name': 'mimi-queue', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        79: {'name': 'écume', 'type': 'eau', 'power': 20, 'precision': 100, 'class': 'speciale'},
        80: {'name': 'repli', 'type': 'eau', 'power': 0, 'precision': 100, 'class': 'autre'},
        81: {'name': 'pistolet A 0', 'type': 'eau', 'power': 40, 'precision': 100, 'class': 'speciale'},
        82: {'name': 'morsure', 'type': 'tenebre', 'power': 60, 'precision': 100, 'class': 'physique'},
        83: {'name': 'tour rapide', 'type': 'normal', 'power': 20, 'precision': 100, 'class': 'physique'},
        84: {'name': "coud'krane", 'type': 'normal', 'power': 100, 'precision': 100, 'class': 'physique'},
        85: {'name': 'hydrocanon', 'type': 'eau', 'power': 120, 'precision': 80, 'class': 'speciale'},
        86: {'name': 'secretion', 'type': 'insecte', 'power': 0, 'precision': 95, 'class': 'autre'},
        87: {'name': 'armure', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        88: {'name': 'choc mental', 'type': 'psy', 'power': 50, 'precision': 100, 'class': 'speciale'},
        89: {'name': 'para-spore', 'type': 'plante', 'power': 0, 'precision': 75, 'class': 'autre'},
        90: {'name': 'ultrason', 'type': 'normal', 'power': 0, 'precision': 55, 'class': 'autre'},
        91: {'name': 'tornade', 'type': 'vol', 'power': 40, 'precision': 100, 'class': 'speciale'},
        92: {'name': 'cyclone', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        93: {'name': 'rafale psy', 'type': 'psy', 'power': 65, 'precision': 100, 'class': 'speciale'},
        94: {'name': 'dard-venin', 'type': 'poison', 'power': 15, 'precision': 100, 'class': 'physique'},
        95: {'name': 'furie', 'type': 'normal', 'power': 15, 'precision': 85, 'class': 'physique'},
        96: {'name': 'puissance', 'type': 'poison', 'power': 0, 'precision': 100, 'class': 'physique'},
        97: {'name': 'double-dard', 'type': 'insecte', 'power': 50, 'precision': 100, 'class': 'physique'},
        98: {'name': 'dard-nuée', 'type': 'insecte', 'power': 14, 'precision': 85, 'class': 'physique'},
        99: {'name': 'hâte', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        100: {'name': 'direct toxik', 'type': 'poison', 'power': 80, 'precision': 100, 'class': 'physique'},
        101: {'name': 'jet de sable', 'type': 'sol', 'power': 0, 'precision': 100, 'class': 'autre'},
        102: {'name': 'vive-attaque', 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'physique'},
        103: {'name': 'ouragan', 'type': 'dragon', 'power': 40, 'precision': 100, 'class': 'speciale'},
        104: {'name': 'danse plume', 'type': 'vol', 'power': 0, 'precision': 100, 'class': 'autre'},
        105: {'name': "lame d'air", 'type': 'vol', 'power': 75, 'precision': 95, 'class': 'speciale'},
        106: {'name': 'croc de mort', 'type': 'normal', 'power': 80, 'precision': 90, 'class': 'physique'},
        107: {'name': 'machouille', 'type': 'tenebre', 'power': 80, 'precision': 100, 'class': 'physique'},
        108: {'name': 'croc fatal', 'type': 'normal', 'power': 0, 'precision': 90, 'class': 'physique'},
        109: {'name': 'damoclês', 'type': 'normal', 'power': 120, 'precision': 100, 'class': 'physique'},
        110: {'name': 'danse-lames', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        111: {'name': 'picpic', 'type': 'vol', 'power': 35, 'precision': 100, 'class': 'physique'},
        112: {'name': "groz'yeux", 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        113: {'name': 'bec vrille', 'type': 'vol', 'power': 80, 'precision': 100, 'class': 'physique'},
        114: {'name': 'ligotage', 'type': 'normal', 'power': 15, 'precision': 85, 'class': 'physique'},
        115: {'name': 'intimidation', 'type': 'normal', 'power': 0, 'precision': 75, 'class': 'autre'},
        116: {'name': 'grincement', 'type': 'normal', 'power': 0, 'precision': 85, 'class': 'autre'},
        117: {'name': 'acide', 'type': 'poison', 'power': 40, 'precision': 100, 'class': 'speciale'},
        118: {'name': 'boue-bombe', 'type': 'sol', 'power': 65, 'precision': 85, 'class': 'speciale'},
        119: {'name': 'détricanon', 'type': 'poison', 'power': 120, 'precision': 70, 'class': 'physique'},
        120: {'name': 'éclair', 'type': 'electrique', 'power': 40, 'precision': 100, 'class': 'speciale'},
        121: {'name': 'cage-éclair', 'type': 'electrique', 'power': 0, 'precision': 100, 'class': 'autre'},
        122: {'name': 'souplesse', 'type': 'normal', 'power': 80, 'precision': 75, 'class': 'physique'},
        123: {'name': "coup d'jus", 'type': 'electrique', 'power': 80, 'precision': 100, 'class': 'speciale'},
        124: {'name': 'météores', 'type': 'normal', 'power': 60, 'precision': 100, 'class': 'speciale'},
        125: {'name': 'combo-griffe', 'type': 'normal', 'power': 18, 'precision': 80, 'class': 'physique'},
        126: {'name': 'tourbi-sable', 'type': 'sol', 'power': 15, 'precision': 70, 'class': 'autre'},
        127: {'name': 'éclategriffe', 'type': 'normal', 'power': 75, 'precision': 95, 'class': 'physique'},
        128: {'name': 'double-pied', 'type': 'combat', 'power': 60, 'precision': 100, 'class': 'physique'},
        129: {'name': 'crochetvenin', 'type': 'poison', 'power': 50, 'precision': 100, 'class': 'physique'},
        130: {'name': 'plaquage', 'type': 'normal', 'power': 85, 'precision': 100, 'class': 'physique'},
        131: {'name': 'telluriforce', 'type': 'sol', 'power': 90, 'precision': 100, 'class': 'speciale'},
        132: {'name': "koud'korne", 'type': 'normal', 'power': 65, 'precision': 100, 'class': 'physique'},
        133: {'name': "empal'korne", 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'physique'},
        134: {'name': 'megacorne', 'type': 'insecte', 'power': 120, 'precision': 85, 'class': 'physique'},
        135: {'name': "écras'face", 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'physique'},
        136: {'name': 'berceuse', 'type': 'normal', 'power': 0, 'precision': 55, 'class': 'autre'},
        137: {'name': 'torgnoles', 'type': 'normal', 'power': 15, 'precision': 85, 'class': 'physique'},
        138: {'name': 'lilliput', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        139: {'name': 'force cosmik', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        140: {'name': 'métronome', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        141: {'name': 'rayon lune', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        142: {'name': 'poing météore', 'type': 'acier', 'power': 100, 'precision': 85, 'class': 'physique'},
        143: {'name': 'feu follet ', 'type': 'feu', 'power': 0, 'precision': 75, 'class': 'autre'},
        144: {'name': 'onde folie', 'type': 'spectre', 'power': 0, 'precision': 100, 'class': 'autre'},
        145: {'name': 'mégaphone', 'type': 'normal', 'power': 90, 'precision': 100, 'class': 'speciale'},
        146: {'name': 'vampirisme', 'type': 'insecte', 'power': 20, 'precision': 100, 'class': 'physique'},
        147: {'name': 'etonnement', 'type': 'spectre', 'power': 30, 'precision': 100, 'class': 'physique'},
        148: {'name': "tranch'air", 'type': 'vol', 'power': 55, 'precision': 95, 'class': 'speciale'},
        149: {'name': "lame d'air", 'type': 'vol', 'power': 75, 'precision': 95, 'class': 'speciale'},
        150: {'name': 'vol-vie', 'type': 'plante', 'power': 20, 'precision': 100, 'class': 'speciale'},
        151: {'name': 'mega-sangsue', 'type': 'plante', 'power': 40, 'precision': 100, 'class': 'speciale'},
        152: {'name': 'spore', 'type': 'plante', 'power': 0, 'precision': 100, 'class': 'autre'},
        153: {'name': 'aromatherapi', 'type': 'plante', 'power': 0, 'precision': 100, 'class': 'autre'},
        154: {'name': 'plaie-croix', 'type': 'insecte', 'power': 80, 'precision': 100, 'class': 'physique'},
        155: {'name': "psykoud'boul", 'type': 'psy', 'power': 80, 'precision': 90, 'class': 'physique'},
        156: {'name': "coud'boue", 'type': 'sol', 'power': 20, 'precision': 100, 'class': 'speciale'},
        157: {'name': 'abîme', 'type': 'sol', 'power': 0, 'precision': 100, 'class': 'physique'},
        158: {'name': 'triplattaque', 'type': 'normal', 'power': 80, 'precision': 100, 'class': 'speciale'},
        159: {'name': 'feinte', 'type': 'tenebre', 'power': 60, 'precision': 100, 'class': 'physique'},
        160: {'name': 'jackpot', 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'physique'},
        161: {'name': 'tranche-nuit', 'type': 'tenebre', 'power': 70, 'precision': 100, 'class': 'physique'},
        162: {'name': 'amnésie', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        163: {'name': 'poing-karate', 'type': 'combat', 'power': 50, 'precision': 100, 'class': 'physique'},
        164: {'name': 'frappe atlas', 'type': 'combat', 'power': 1, 'precision': 100, 'class': 'physique'},
        165: {'name': 'coup-croix', 'type': 'combat', 'power': 100, 'precision': 80, 'class': 'physique'},
        166: {'name': 'roue de feu', 'type': 'feu', 'power': 60, 'precision': 100, 'class': 'physique'},
        167: {'name': 'vitesse extreme', 'type': 'normal', 'power': 80, 'precision': 100, 'class': 'physique'},
        168: {'name': 'hypnose', 'type': 'psy', 'power': 0, 'precision': 60, 'class': 'autre'},
        169: {'name': 'dynamopoing', 'type': 'combat', 'power': 100, 'precision': 50, 'class': 'physique'},
        170: {'name': "bulles d'O", 'type': 'eau', 'power': 65, 'precision': 100, 'class': 'speciale'},
        171: {'name': 'tir de boue', 'type': 'sol', 'power': 55, 'precision': 95, 'class': 'speciale'},
        172: {'name': 'téléport', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        173: {'name': 'télékinésie', 'type': 'psy', 'power': 0, 'precision': 80, 'class': 'autre'},
        174: {'name': 'soin', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        175: {'name': 'coupe psycho', 'type': 'psy', 'power': 70, 'precision': 100, 'class': 'physique'},
        176: {'name': 'tempeteverte', 'type': 'plante', 'power': 140, 'precision': 90, 'class': 'speciale'},
        177: {'name': 'bouclier', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        178: {'name': 'lance-boue', 'type': 'sol', 'power': 0, 'precision': 100, 'class': 'autre'},
        179: {'name': 'poliroche', 'type': 'roche', 'power': 0, 'precision': 100, 'class': 'autre'},
        180: {'name': 'jet-pierres', 'type': 'roche', 'power': 50, 'precision': 90, 'class': 'physique'},
        181: {'name': 'destruction', 'type': 'normal', 'power': 200, 'precision': 100, 'class': 'speciale'},
        182: {'name': 'boule roc', 'type': 'roche', 'power': 25, 'precision': 80, 'class': 'physique'},
        183: {'name': 'explosion', 'type': 'normal', 'power': 250, 'precision': 100, 'class': 'physique'},
        184: {'name': 'lame de roc', 'type': 'roche', 'power': 100, 'precision': 80, 'class': 'physique'},
        185: {'name': 'éboulement', 'type': 'roche', 'power': 75, 'precision': 90, 'class': 'physique'},
        186: {'name': 'écrasement', 'type': 'normal', 'power': 65, 'precision': 100, 'class': 'physique'},
        187: {'name': 'boutefeu', 'type': 'feu', 'power': 120, 'precision': 100, 'class': 'physique'},
        188: {'name': 'paresse', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        189: {'name': 'strido-son', 'type': 'acier', 'power': 0, 'precision': 95, 'class': 'autre'},
        190: {'name': 'sonicboom', 'type': 'normal', 'power': 1, 'precision': 90, 'class': 'speciale'},
        191: {'name': 'étincelle', 'type': 'electrique', 'power': 65, 'precision': 100, 'class': 'physique'},
        192: {'name': 'elecanon', 'type': 'electrique', 'power': 120, 'precision': 50, 'class': 'speciale'},
        193: {'name': 'éclair', 'type': 'electrique', 'power': 40, 'precision': 100, 'class': 'speciale'},
        194: {'name': 'coup double', 'type': 'normal', 'power': 70, 'precision': 90, 'class': 'physique'},
        195: {'name': 'vent glace', 'type': 'glace', 'power': 55, 'precision': 95, 'class': 'speciale'},
        196: {'name': 'éclats glace', 'type': 'glace', 'power': 40, 'precision': 100, 'class': 'physique'},
        197: {'name': 'onde boréale', 'type': 'glace', 'power': 65, 'precision': 100, 'class': 'speciale'},
        198: {'name': 'aqua-jet', 'type': 'eau', 'power': 40, 'precision': 100, 'class': 'physique'},
        199: {'name': 'plongee', 'type': 'eau', 'power': 60, 'precision': 100, 'class': 'physique'},
        200: {'name': 'hydroqueue', 'type': 'eau', 'power': 90, 'precision': 90, 'class': 'physique'},
        201: {'name': 'glaciation', 'type': 'glace', 'power': 0, 'precision': 100, 'class': 'speciale'},
        202: {'name': 'detritus', 'type': 'poison', 'power': 65, 'precision': 100, 'class': 'speciale'},
        203: {'name': 'acidarmure', 'type': 'poison', 'power': 0, 'precision': 100, 'class': 'autre'},
        204: {'name': 'stalagtite', 'type': 'glace', 'power': 10, 'precision': 100, 'class': 'physique'},
        205: {'name': 'mur de fer', 'type': 'acier', 'power': 0, 'precision': 100, 'class': 'autre'},
        206: {'name': 'picanon', 'type': 'normal', 'power': 20, 'precision': 100, 'class': 'physique'},
        207: {'name': 'lechouille', 'type': 'spectre', 'power': 20, 'precision': 100, 'class': 'physique'},
        208: {'name': 'tenebres', 'type': 'spectre', 'power': 1, 'precision': 100, 'class': 'speciale'},
        209: {'name': 'devoreve', 'type': 'psy', 'power': 100, 'precision': 100, 'class': 'speciale'},
        210: {'name': 'cauchemar', 'type': 'spectre', 'power': 0, 'precision': 100, 'class': 'autre'},
        211: {'name': 'poing ombre', 'type': 'spectre', 'power': 60, 'precision': 100, 'class': 'physique'},
        212: {'name': 'dracosouffle', 'type': 'dragon', 'power': 60, 'precision': 100, 'class': 'speciale'},
        213: {'name': 'yoga', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'autre'},
        214: {'name': 'force poigne', 'type': 'normal', 'power': 55, 'precision': 100, 'class': 'physique'},
        215: {'name': 'griffe acier', 'type': 'acier', 'power': 50, 'precision': 95, 'class': 'physique'},
        216: {'name': 'guillotine', 'type': 'normal', 'power': 0, 'precision': 30, 'class': 'speciale'},
        217: {'name': 'pince-masse', 'type': 'eau', 'power': 90, 'precision': 85, 'class': 'physique'},
        218: {'name': 'pilonnage', 'type': 'normal', 'power': 15, 'precision': 85, 'class': 'physique'},
        219: {'name': "bomb'oeuf", 'type': 'normal', 'power': 100, 'precision': 75, 'class': 'physique'},
        220: {'name': 'martobois', 'type': 'plante', 'power': 120, 'precision': 100, 'class': 'physique'},
        221: {'name': "massd'os", 'type': 'sol', 'power': 65, 'precision': 85, 'class': 'physique'},
        222: {'name': 'osmerang', 'type': 'sol', 'power': 100, 'precision': 90, 'class': 'physique'},
        223: {'name': 'charge-os', 'type': 'sol', 'power': 25, 'precision': 80, 'class': 'physique'},
        224: {'name': 'mawashi geri', 'type': 'combat', 'power': 60, 'precision': 85, 'class': 'physique'},
        225: {'name': 'pied brûleur', 'type': 'feu', 'power': 85, 'precision': 90, 'class': 'physique'},
        226: {'name': 'ultimawashi', 'type': 'normal', 'power': 120, 'precision': 75, 'class': 'physique'},
        227: {'name': 'pied sauté', 'type': 'combat', 'power': 70, 'precision': 95, 'class': 'physique'},
        228: {'name': 'poing comête', 'type': 'normal', 'power': 18, 'precision': 85, 'class': 'physique'},
        229: {'name': 'pisto-poing', 'type': 'acier', 'power': 40, 'precision': 100, 'class': 'physique'},
        230: {'name': 'mach punch', 'type': 'combat', 'power': 40, 'precision': 100, 'class': 'physique'},
        231: {'name': 'poing de feu', 'type': 'feu', 'power': 75, 'precision': 100, 'class': 'physique'},
        232: {'name': 'poing-éclair', 'type': 'electrique', 'power': 75, 'precision': 100, 'class': 'physique'},
        233: {'name': 'poinglace', 'type': 'glace', 'power': 75, 'precision': 100, 'class': 'physique'},
        234: {'name': 'stratopercut', 'type': 'combat', 'power': 85, 'precision': 90, 'class': 'physique'},
        235: {'name': 'ultimapoing', 'type': 'normal', 'power': 80, 'precision': 85, 'class': 'physique'},
        236: {'name': 'regeneration', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        237: {'name': 'megafouet', 'type': 'plante', 'power': 120, 'precision': 85, 'class': 'physique'},
        238: {'name': 'puredpois', 'type': 'poison', 'power': 20, 'precision': 70, 'class': 'speciale'},
        239: {'name': 'e-coque', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        240: {'name': 'chatouille', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        241: {'name': 'danse draco', 'type': 'dragon', 'power': 0, 'precision': 100, 'class': 'autre'},
        242: {'name': 'dracochoc', 'type': 'dragon', 'power': 90, 'precision': 100, 'class': 'speciale'},
        243: {'name': 'cascade', 'type': 'eau', 'power': 80, 'precision': 100, 'class': 'physique'},
        244: {'name': 'grobisou', 'type': 'normal', 'power': 0, 'precision': 75, 'class': 'autre'},
        245: {'name': 'poudreuse', 'type': 'glace', 'power': 40, 'precision': 100, 'class': 'speciale'},
        246: {'name': 'croco larme', 'type': 'tenebre', 'power': 0, 'precision': 100, 'class': 'autre'},
        247: {'name': 'giga impact', 'type': 'normal', 'power': 150, 'precision': 90, 'class': 'physique'},
        248: {'name': 'crocs givre', 'type': 'glace', 'power': 65, 'precision': 95, 'class': 'physique'},
        249: {'name': 'hydroqueue', 'type': 'eau', 'power': 90, 'precision': 90, 'class': 'physique'},
        250: {'name': 'trempette', 'type': 'acier', 'power': 0, 'precision': 100, 'class': 'speciale'},
        251: {'name': 'morphing', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        252: {'name': 'lutte', 'type': 'normal', 'power': 100, 'precision': 100, 'class': 'physique'},
        253: {'name': 'feuillemagik', 'type': 'plante', 'power': 60, 'precision': 100, 'class': 'speciale'},
        254: {'name': 'ebullilave', 'type': 'feu', 'power': 80, 'precision': 100, 'class': 'speciale'},
        255: {'name': 'surpuissance', 'type': 'combat', 'power': 120, 'precision': 100, 'class': 'physique'},
        256: {'name': 'megaphone', 'type': 'normal', 'power': 90, 'precision': 100, 'class': 'speciale'},
        257: {'name': 'bélier', 'type': 'normal', 'power': 90, 'precision': 85, 'class': 'physique'},
        258: {'name': 'extrasenseur', 'type': 'psy', 'power': 80, 'precision': 100, 'class': 'speciale'},
        259: {'name': 'mach punch', 'type': 'combat', 'power': 40, 'precision': 100, 'class': 'physique'},
        260: {'name': 'vent argente', 'type': 'insecte', 'power': 60, 'precision': 100, 'class': 'speciale'},
        261: {'name': 'bourdon', 'type': 'insecte', 'power': 90, 'precision': 100, 'class': 'speciale'},
        262: {'name': 'eco-sphere', 'type': 'plante', 'power': 80, 'precision': 100, 'class': 'speciale'},
        263: {'name': 'surchauffe', 'type': 'feu', 'power': 140, 'precision': 90, 'class': 'speciale'},
        264: {'name': 'griffe ombre', 'type': 'spectre', 'power': 70, 'precision': 100, 'class': 'physique'},
        265: {'name': 'eboulement', 'type': 'roche', 'power': 75, 'precision': 90, 'class': 'speciale'},
        266: {'name': 'rayon charge', 'type': 'electrique', 'power': 50, 'precision': 90, 'class': 'speciale'},
        267: {'name': "aile d'acier", 'type': 'acier', 'power': 70, 'precision': 90, 'class': 'physique'},
        268: {'name': 'vampipoing', 'type': 'combat', 'power': 75, 'precision': 100, 'class': 'speciale'},
        269: {'name': 'ombre portee', 'type': 'spectre', 'power': 40, 'precision': 100, 'class': 'physique'},
        270: {'name': 'etreinte', 'type': 'normal', 'power': 15, 'precision': 75, 'class': 'physique'},
        271: {'name': 'vibrobscur', 'type': 'tenebre', 'power': 80, 'precision': 100, 'class': 'speciale'},
        272: {'name': 'rayon signal', 'type': 'insecte', 'power': 75, 'precision': 100, 'class': 'speciale'},
        273: {'name': 'ecume', 'type': 'eau', 'power': 20, 'precision': 100, 'class': 'speciale'},
        274: {'name': 'charme', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        275: {'name': 'doux baiser', 'type': 'normal', 'power': 0, 'precision': 75, 'class': 'autre'},
        276: {'name': 'machination', 'type': 'tenebre', 'power': 0, 'precision': 100, 'class': 'autre'},
        277: {'name': 'pouvoir antique', 'type': 'roche', 'power': 60, 'precision': 100, 'class': 'speciale'},
        278: {'name': 'vent mauvais', 'type': 'spectre', 'power': 60, 'precision': 100, 'class': 'speciale'},
        279: {'name': 'spore coton', 'type': 'plante', 'power': 0, 'precision': 85, 'class': 'autre'},
        280: {'name': 'rayon gemme', 'type': 'roche', 'power': 70, 'precision': 100, 'class': 'speciale'},
        281: {'name': 'lame-feuille', 'type': 'plante', 'power': 90, 'precision': 100, 'class': 'physique'},
        282: {'name': 'eclate-roc', 'type': 'roche', 'power': 40, 'precision': 100, 'class': 'physique'},
        283: {'name': 'marto-poing', 'type': 'combat', 'power': 100, 'precision': 90, 'class': 'physique'},
        284: {'name': 'exploforce', 'type': 'combat', 'power': 120, 'precision': 70, 'class': 'speciale'},
        285: {'name': "siffl'herbe", 'type': 'plante', 'power': 0, 'precision': 55, 'class': 'autre'},
        286: {'name': 'Ocroupi', 'type': 'eau', 'power': 95, 'precision': 85, 'class': 'speciale'},
        287: {'name': 'aboiement', 'type': 'tenebre', 'power': 55, 'precision': 95, 'class': 'speciale'},
        288: {'name': 'crocs eclair', 'type': 'electrique', 'power': 65, 'precision': 95, 'class': 'physique'},
        289: {'name': 'aeroblast', 'type': 'vol', 'power': 100, 'precision': 95, 'class': 'speciale'},
        290: {'name': 'draco-rage', 'type': 'dragon', 'power': 0, 'precision': 100, 'class': 'speciale'},
        291: {'name': 'tunnelier', 'type': 'sol', 'power': 80, 'precision': 95, 'class': 'physique'},
        292: {'name': 'mania', 'type': 'normal', 'power': 90, 'precision': 100, 'class': 'physique'},
        293: {'name': 'danse-fleur', 'type': 'plante', 'power': 120, 'precision': 100, 'class': 'speciale'},
        294: {'name': 'tourniquet', 'type': 'eau', 'power': 0, 'precision': 100, 'class': 'autre'},
        295: {'name': 'constriction', 'type': 'normal', 'power': 10, 'precision': 100, 'class': 'physique'},
        296: {'name': "coup d'boule", 'type': 'normal', 'power': 70, 'precision': 100, 'class': 'physique'},
        297: {'name': 'balayage', 'type': 'combat', 'power': 0, 'precision': 100, 'class': 'physique'},
        298: {'name': 'frénésie', 'type': 'normal', 'power': 20, 'precision': 100, 'class': 'physique'},
        299: {'name': 'cadeau', 'type': 'normal', 'power': 0, 'precision': 90, 'class': 'physique'},
        300: {'name': 'gribouille', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        301: {'name': 'riposte', 'type': 'combat', 'power': 0, 'precision': 100, 'class': 'physique'},
        302: {'name': 'voile miroir', 'type': 'psy', 'power': 0, 'precision': 100, 'class': 'speciale'},
        303: {'name': 'tempetesable', 'type': 'roche', 'power': 0, 'precision': 100, 'class': 'autre'},
        304: {'name': "ball'meteo", 'type': 'normal', 'power': 50, 'precision': 100, 'class': 'speciale'},
        305: {'name': 'prélevement destin', 'type': 'spectre', 'power': 0, 'precision': 100, 'class': 'autre'},
        306: {'name': 'affutage', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        307: {'name': 'ampleur', 'type': 'sol', 'power': 0, 'precision': 100, 'class': 'physique'},
        308: {'name': 'aurore', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        310: {'name': 'balance', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        311: {'name': 'ball-brûme', 'type': 'psy', 'power': 70, 'precision': 100, 'class': 'speciale'},
        312: {'name': 'blabla dodo', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        313: {'name': 'boost', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        314: {'name': "boul'armure", 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        315: {'name': "ecras'face", 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'physique'},
        316: {'name': 'détection', 'type': 'combat', 'power': 0, 'precision': 0, 'class': 'autre'},
        317: {'name': 'frustration', 'type': 'acier', 'power': 0, 'precision': 100, 'class': 'physique'},
        318: {'name': 'retour', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'physique'},
        319: {'name': 'façade', 'type': 'normal', 'power': 70, 'precision': 100, 'class': 'physique'},
        320: {'name': 'force cachée', 'type': 'normal', 'power': 70, 'precision': 100, 'class': 'physique'},
        321: {'name': 'canicule', 'type': 'feu', 'power': 100, 'precision': 90, 'class': 'speciale'},
        322: {'name': 'cognobidon', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        323: {'name': 'colêre', 'type': 'dragon', 'power': 120, 'precision': 100, 'class': 'physique'},
        324: {'name': 'contre', 'type': 'combat', 'power': 0, 'precision': 100, 'class': 'physique'},
        325: {'name': 'coupe-vent', 'type': 'normal', 'power': 80, 'precision': 100, 'class': 'speciale'},
        326: {'name': 'danse-folle', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        327: {'name': 'effort', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'physique'},
        328: {'name': 'electacle', 'type': 'electrique', 'power': 120, 'precision': 100, 'class': 'physique'},
        329: {'name': 'éruption', 'type': 'feu', 'power': 0, 'precision': 100, 'class': 'speciale'},
        330: {'name': 'faux-chage', 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'physique'},
        331: {'name': 'feu sacré', 'type': 'feu', 'power': 100, 'precision': 95, 'class': 'physique'},
        332: {'name': 'flatterie', 'type': 'tenebre', 'power': 0, 'precision': 100, 'class': 'speciale'},
        333: {'name': 'fléau', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'physique'},
        334: {'name': 'gaz toxik', 'type': 'poison', 'power': 0, 'precision': 55, 'class': 'autre'},
        335: {'name': 'gicledo', 'type': 'eau', 'power': 0, 'precision': 100, 'class': 'speciale'},
        336: {'name': 'grondement', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        337: {'name': 'hydroblast', 'type': 'eau', 'power': 150, 'precision': 90, 'class': 'speciale'},
        338: {'name': 'lait à boire', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        339: {'name': 'lumi-eclat', 'type': 'psy', 'power': 70, 'precision': 100, 'class': 'speciale'},
        340: {'name': 'lumiqueue', 'type': 'insecte', 'power': 0, 'precision': 100, 'class': 'autre'},
        341: {'name': 'octazooka', 'type': 'eau', 'power': 65, 'precision': 85, 'class': 'speciale'},
        342: {'name': 'piqué', 'type': 'acier', 'power': 140, 'precision': 90, 'class': 'physique'},
        343: {'name': 'poing dard', 'type': 'plante', 'power': 60, 'precision': 100, 'class': 'physique'},
        344: {'name': 'psycho boost', 'type': 'psy', 'power': 140, 'precision': 90, 'class': 'speciale'},
        345: {'name': 'queue poison', 'type': 'poison', 'power': 50, 'precision': 100, 'class': 'physique'},
        346: {'name': 'rafale feu', 'type': 'feu', 'power': 150, 'precision': 90, 'class': 'speciale'},
        347: {'name': 'ronflement', 'type': 'normal', 'power': 40, 'precision': 100, 'class': 'speciale'},
        348: {'name': 'sacrifice', 'type': 'combat', 'power': 80, 'precision': 80, 'class': 'physique'},
        349: {'name': 'ténacité', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        350: {'name': 'triple pied', 'type': 'combat', 'power': 60, 'precision': 90, 'class': 'physique'},
        351: {'name': 'uppercut', 'type': 'combat', 'power': 70, 'precision': 100, 'class': 'physique'},
        352: {'name': 'vantardise', 'type': 'normal', 'power': 0, 'precision': 100, 'class': 'autre'},
        353: {'name': 'végé-attak', 'type': 'plante', 'power': 150, 'precision': 90, 'class': 'speciale'},
        354: {'name': 'écrasement', 'type': 'normal', 'power': 65, 'precision': 100, 'class': 'physique'}
      }

    # Function used to grab the dictionary:
    """
    dict_attacks = {}
    for id_attack in self.getAllAttackIds():
      current_attack = {}

      attack_url = "{}/pokedex_attaques.php".format(PokemonOrigins.__BASE_WEBSITE)
      payload = {
                  "action": "voir_attaque",
                  "id": id_attack
                }
      attack_data = BeautifulSoup(self.session.post(url=attack_url, data=payload).text, "html.parser")
      time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

      for current_tab in attack_data.findAll("table"):
        if "Attributs" in current_tab.text:
          next_is_name = False
          next_is_type = False
          next_is_power = False
          next_is_precision = False
          next_is_class = False
          for current_td in current_tab.findAll("td"):
            if "Nom :" in current_td.text:
              next_is_name = True
            elif next_is_name:
              current_attack["name"] = str(current_td.text)
              next_is_name = False
            elif "Type :" in current_td.text:
              next_is_type = True
            elif next_is_type:
              current_attack["type"] = str(current_td.text)
              next_is_type = False
            elif "Puissance :" in current_td.text:
              next_is_power = True
            elif next_is_power:
              current_attack["power"] = int(current_td.text)
              next_is_power = False
            elif "Précision :" in current_td.text:
              next_is_precision = True
            elif next_is_precision:
              current_attack["precision"] = int(current_td.text)
              next_is_precision = False
            elif "Classe :" in current_td.text:
              next_is_class = True
            elif next_is_class:
              current_attack["class"] = str(current_td.text)
              next_is_class = False

      # Insert the attack caracteristics in all attacks dictionnary
      logging.debug("Found data for attack {}: {}".format(str(id_attack), str(current_attack)))
      dict_attacks[id_attack] = current_attack

    return dict_attacks
    """

  def getBestAttack(self, attack_ids):
    """Get the best attack from a list of attack ids

    Keyword arguments:
      attack_ids -- ([]) List of all attack ids to check in order to find the best

    return:
      no_error -- (bool) No error during the function
      attack_id -- (int) Id of the best attack
    """
    all_attacks = self.getAllAttacksInfo()
    all_attack_ids = all_attacks.keys()

    best_attack = -1
    best_attack_value = -1

    for attack_id in attack_ids:
      if attack_id in all_attack_ids:
        current_attack_value = all_attacks[attack_id]['power'] + 0.5 * all_attacks[attack_id]['precision']
        if current_attack_value > best_attack_value:
          best_attack_value = current_attack_value
          best_attack = attack_id
      else:
        logging.error("Impossible to find attack id {} in known attack ids".format(str(attack_id)))
        return False, best_attack

    if best_attack != -1:
      logging.debug("Best attack is {}".format(str(best_attack)))
      return True, best_attack
    else:
      logging.warning("Impossible to find the best attack...")
      return False, best_attack

######################### Battle ##########################

  def beginWildPokemonBattle(self, wild_pokemon_id, x=-1, y=-1):
    """Begin a battle againsy a wild pokemon

    Keyword arguments:
      wild_pokemon_id -- (int) ID of the wild pokemon to attack
      x -- (int, optional) Horizontal position of the pokemon
      y -- (int, optional) Vertical position of the pokemon

    return:
      battle_began -- (bool) No error during the function
    """
    if x != -1 and y != -1:
      if not self.goToInMap(x, y):
        logging.warning("Impossible to go to pokemon localisation ({}, {})".format(str(x), str(y)))
        return False

    begin_fight_url = "{}/combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "id": wild_pokemon_id,
               "action": "combat"
              }

    post_begin_fight = self.session.post(url=begin_fight_url, data=payload).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    success = (not "Le pokémon n'est plus là." in post_begin_fight) and ("Utiliser une attaque" in post_begin_fight)
    if success:
      logging.debug("Fight with pokemon {} began".format(str(wild_pokemon_id)))
    else:
      logging.warning("Impossible to fight pokemon {} (not there or current pokemon can't fight)".format(str(wild_pokemon_id)))

    return success

  def runAwayFromBattle(self):
    """Run away from battle

    return:
      no_error -- (bool) You ran away
    """
    surrender_url = "{}/carte.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {"action": "abandon"}
    result = self.session.get(url=surrender_url, params=payload).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    success = "Vous êtes actuellement en" in result
    if success:
      logging.debug("You ran away from battle")
    else:
      logging.warning("Could not run away from battle")
    return success

  def useItemInBattle(self, id_item, is_quest=False):
    """Use specific item in battle

    Keyword arguments:
      id_item -- (int) Id of the item to use
      is_quest -- (bool, optional) Is it a quest battle? By default it is not
    """
    if is_quest:
      fight_url = "{}/quetes_combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    else:
      fight_url = "{}/combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "id_item": id_item,
               "action": "objet"
              }

    self.session.post(url=fight_url, data=payload)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

  def catchPokemonInBattle(self, items, retry_until_catched=True):
    """Try to catch a pokemon during a battle

    Keyword arguments:
      items -- ({'item1':quantity, ...}) Provide items available in the fight
      retry_until_catched -- (bool, optional) Retry until pokemon is catched or there is no pokeball left

    return:
      no_error -- (bool) No error during the function
      catched -- (bool) The pokemon is catched
    """
    # Find cheapest available pokeball in items
    id_pokeball = -1
    item_ids = items.keys()
    if PokemonOrigins.eItemIds.POKEBALL in item_ids:
      if items[PokemonOrigins.eItemIds.POKEBALL] > 0:
        id_pokeball = PokemonOrigins.eItemIds.POKEBALL
    elif PokemonOrigins.eItemIds.SUPERBALL in item_ids:
      if items[PokemonOrigins.eItemIds.SUPERBALL] > 0:
        id_pokeball = PokemonOrigins.eItemIds.SUPERBALL
    elif PokemonOrigins.eItemIds.HYPERBALL in item_ids:
      if items[PokemonOrigins.eItemIds.HYPERBALL] > 0:
        id_pokeball = PokemonOrigins.eItemIds.HYPERBALL
    elif PokemonOrigins.eItemIds.MASTERBALL in item_ids:
      if items[PokemonOrigins.eItemIds.MASTERBALL] > 0:
        id_pokeball = PokemonOrigins.eItemIds.MASTERBALL

    if id_pokeball == -1:
      logging.debug("No pokeballs availaible in order to catch a pokemon")
      return True, False

    catch_url = "{}/combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "id_item": id_pokeball,
               "action": "objet"
              }

    post_catch = self.session.post(url=catch_url, data=payload).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    if "Félicitations! Vous avez capturé" in post_catch:
      logging.debug("Pokemon catched")
      return True, True
    elif not "Quel dommage! Il parvient à sortir de là!" in post_catch:
      logging.warning("An error occured during the catch of the pokemon")
      return False, False
    elif retry_until_catched:
      # Reduce the items by one item of id_pokeball and retry as long as needed
      items[id_pokeball] = items[id_pokeball] - 1
      return self.catchPokemonInBattle(items=items,
                                       retry_until_catched=retry_until_catched)

    # Pokemon not catched (and no error)
    return True, False

  def changePokemonInBattle(self, id_pokemon, is_quest=False):
    """Change the curent pokemon of the battle

    Keyword arguments:
      id_pokemon -- ([]) Id of the new pokemon to use
      is_quest -- (bool, optional) Is it a quest battle? By default it is not
    """
    if is_quest:
      fight_url = "{}/quetes_combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    else:
      fight_url = "{}/combat.php".format(PokemonOrigins.__BASE_WEBSITE)

    payload = {
               "pokemon": id_pokemon,
               "action": "changer_pokemon"
              }

    self.session.post(url=fight_url, data=payload)
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

  def attackInBattle(self, id_attack, is_quest=False):
    """Attack the current pokemon with a specific attack

    Keyword arguments:
      id_attack -- (int) Attack to use
      is_quest -- (bool, optional) Is it a quest battle? By default it is not

    return:
      no_error -- (bool) No error during the function
      attack_success -- (bool) The attack was a success
      ennemy_is_dead -- (bool) The ennemy pokemon is dead (does not mean the
                               fight is over if fighting someone with more than
                               1 pokemon)
      ennemy_went_away -- (bool) The ennemy pokemon went away (battle is finished)
      you_are_dead -- (bool) Your current pokemon is dead
    """
    if is_quest:
      attack_url = "{}/quetes_combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    else:
      attack_url = "{}/combat.php".format(PokemonOrigins.__BASE_WEBSITE)

    payload = {
               "attaque": id_attack,
               "action": "attaque"
              }

    post_attack = self.session.post(url=attack_url, data=payload).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    if "Le pokémon n'est plus là" in post_attack:
      logging.warning("An error occured during the attack, the pokemon is not here anymore")
      return False, False, False, True, False

    ennemy_is_dead = ("Vous avez gagné!" in post_attack) or ("Vous avez vaincu" in post_attack)
    ennemy_went_away = ("Le pokémon prend la fuite" in post_attack)
    you_are_dead = ("Votre pokémon est K.O." in post_attack)

    soup_post_attack = BeautifulSoup(post_attack, "html.parser")
    if soup_post_attack.find("div", id="description_combat"):
      if soup_post_attack.find("div", id="description_combat").find("div"):
        if not "l'attaque a échoué." in soup_post_attack.find("div", id="description_combat").find("div").text:
          attack_success = True
        else:
          attack_success = False
      else:
        attack_success = True
    else:
      attack_success = True

    # If ennemy is dead, check if we can continue the fight (if more than one pokemon)
    if "Vous avez vaincu" in post_attack:
        logging.debug("Continue fight with the next pokemon")
        payload = {
                    "entree": "on",
                    "action": "pokemon_suivant"
                  }
        self.session.post(url=attack_url, data=payload).text

    logging.debug("Attack success: {}".format(str(attack_success)))
    logging.debug("Ennemy is dead: {}".format(str(ennemy_is_dead)))
    logging.debug("Ennemy went away: {}".format(str(ennemy_went_away)))
    logging.debug("Your pokemon is dead: {}".format(str(you_are_dead)))
    return True, attack_success, ennemy_is_dead, ennemy_went_away, you_are_dead

  def getBattleInformations(self, is_quest=False):
    """Get important informations from the battle

    Keyword arguments:
      is_quest -- (bool, optional) Is it a quest battle? By default it is not

    return:
      still_in_battle -- (bool) There is still a battle taking place
      attacks -- ([]) List of available attacks to use from current pokemon
      items -- ({item_id1:quantity1, ...}) List of all items with associated quantity
      other_pokemons -- ([]) List of other pokemons usable in the fight
      current_life -- (int) Current life of current pokemon (in %)
      ennemy_life -- (int) Life of ennemy pokemon (in %)
    """
    if is_quest:
      attack_url = "{}/quetes_combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    else:
      attack_url = "{}/combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    get_attack = self.session.get(url=attack_url).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    attacks = []
    items = {}
    other_pokemons = []
    current_life = -1
    ennemy_life = -1

    still_in_battle = (not "Le pokémon n'est plus là" in get_attack) and (not "Vous avez abandonné" in get_attack)
    if not still_in_battle:
      logging.debug("There is no fight")
      return False, attacks, items, other_pokemons, current_life, ennemy_life

    battle_data = BeautifulSoup(get_attack, "html.parser")

    for form in battle_data.findAll("form"):
      inputs = form.findAll("input")
      if form.find('input', {'name': 'attaque'}):
        # Grab attacks
        for attack in form.findAll('input', {'name': 'attaque'}):
          attacks.append(int(attack['value']))
      elif form.find('select', {'name': 'pokemon'}):
        # Grab other pokemons
        for pokemon in form.findAll('option'):
          other_pokemons.append(int(pokemon['value']))
      elif form.find('input', {'name': 'id_item'}):
        # Grab items (ids and number of elements of each item then combine them together)
        item_numbers = [int(s) for s in form.text.replace('(', ' ').replace(')', ' ').split() if s.isdigit()]
        for item in form.findAll('input', {'name': 'id_item'}):
          items[int(item['value'])] =  item_numbers.pop(0)
        if len(item_numbers) > 0:
          logging.error("An error occured during the parsing to get fight data")
          return False, attacks, items, other_pokemons, current_life, ennemy_life

    # Grab current life
    for status_img in battle_data.find('p', id="texte_combat_bas").findAll('img'):
      if "images/barre/" in status_img['src']:
        current_life = int(status_img['src'].replace("images/barre/", "").replace(".png", ""))

    # Grab ennemy life
    for status_ennemy_img in battle_data.find('p', id="texte_combat_haut").findAll('img'):
      if "images/barre/" in status_ennemy_img['src']:
        ennemy_life = int(status_ennemy_img['src'].replace("images/barre/", "").replace(".png", ""))

    logging.debug("Fight is active")
    logging.debug("Attacks: {}".format(str(attacks)))
    logging.debug("Items: {}".format(str(items)))
    logging.debug("Other pokemons: {}".format(str(other_pokemons)))
    logging.debug("Current pokemon life: {}%".format(str(current_life)))
    logging.debug("Ennemy life: {}%".format(str(ennemy_life)))
    return True, attacks, items, other_pokemons, current_life, ennemy_life

  def fightAllPokemonsInBattle(self, request_catch=False, is_quest=False):
    """Fight all pokemons of the battle or catch the pokemon

    The algorithm will try to kill/catch pokemons in an optimized way even if it is not perfect.

    Warning: Be sure your current pokemon has enough AP else it will not work

    Keyword arguments:
      request_catch -- (bool, optional) Catch the pokemon (by default, it's not trying to catch it)
      is_quest -- (bool, optional) Is it a quest battle? By default it is not

    return:
      fight_won -- (bool) The fight was won (if pokemon catched, the fight is considered as won)
      pokemon_catched -- (bool) Pokemon catched (will always be false if catching pokemon was not requested)
    """
    already_used_pokemons = []
    still_in_battle, attacks, items, other_pokemons, current_life, ennemy_life = self.getBattleInformations(is_quest=is_quest)

    while still_in_battle:
      # Try to catch pokemon if it is low and it is requested
      if request_catch and ennemy_life < 30:
        if self.catchPokemonInBattle(items):
          logging.debug("Pokemon catched!")
          return True, True
        else:
          logging.warning("Could not catch the pokemon, let's try to kill it")
          request_catch = False

      # Attack the pokemon
      no_error, attack_success, ennemy_is_dead, ennemy_went_away, you_are_dead = self.attackInBattle(self.getBestAttack(attacks), is_quest=is_quest)
      # Update all data
      still_in_battle, attacks, items, other_pokemons, current_life, ennemy_life = self.getBattleInformations(is_quest=is_quest)
      if not no_error:
        logging.warning("An error occured during attack, aborting...")
        return False, False
      if ennemy_went_away:
        logging.warning("Ennemy went away... This is the end of the battle")
        return False, False

      # Change pokemon if low chance to win or dead
      if (current_life <= 20 and ennemy_life > current_life) or you_are_dead:
        if len(other_pokemons) > 0 and len(already_used_pokemons) < len(other_pokemons):
          res, active, not_actives, is_level_100, can_level_up = self.getOwnedPokemons()
          if res:
            already_used_pokemons.append(active['id'])
          other_pokemons = [x for x in other_pokemons if x not in already_used_pokemons]
          self.changePokemonInBattle(other_pokemons[0], is_quest=is_quest)
        else:
          logging.warning("All our pokemons are low life or dead, running away from the fight")
          self.runAwayFromBattle()
          return False, False
      elif current_life < 35:
        # Try to use a potion if the pokemon is low life but not that much
        potion_used = False
        item_ids = items.keys()
        if PokemonOrigins.eItemIds.POTION in items.keys():
          if items[PokemonOrigins.eItemIds.POTION] > 0:
            self.useItemInBattle(PokemonOrigins.eItemIds.POTION, is_quest=is_quest)
            potion_used = True
        if (not potion_used) and PokemonOrigins.eItemIds.SUPER_POTION in items.keys():
          if items[PokemonOrigins.eItemIds.SUPER_POTION] > 0:
            self.useItemInBattle(PokemonOrigins.eItemIds.SUPER_POTION, is_quest=is_quest)
            potion_used = True
        if (not potion_used) and PokemonOrigins.eItemIds.HYPER_POTION in items.keys():
          if items[PokemonOrigins.eItemIds.HYPER_POTION] > 0:
            self.useItemInBattle(PokemonOrigins.eItemIds.HYPER_POTION, is_quest=is_quest)
            potion_used = True
        if (not potion_used) and PokemonOrigins.eItemIds.MAX_POTION in items.keys():
          if items[PokemonOrigins.eItemIds.MAX_POTION] > 0:
            self.useItemInBattle(PokemonOrigins.eItemIds.MAX_POTION, is_quest=is_quest)
            potion_used = True

        if not potion_used:
          logging.warning("No available potion to heal the pokemon")

      # Update all data
      still_in_battle, attacks, items, other_pokemons, current_life, ennemy_life = self.getBattleInformations(is_quest=is_quest)

    logging.debug("Battle won!")
    return True, False

  def fightWildPokemon(self, wild_pokemon_id, x=-1, y=-1, request_catch=False):
    """Launch the fight with a wild pokemon and try to kill/catch it with an internal algorithm

    Warning: Be sure your current pokemon has enough AP else it will not work

    Keyword arguments:
      wild_pokemon_id -- (int) ID of the wild pokemon to attack
      x -- (int, optional) Horizontal position of the pokemon
      y -- (int, optional) Vertical position of the pokemon
      request_catch -- (bool, optional) Catch the pokemon (by default, it's not trying to catch it)

    return:
      fight_won -- (bool) The fight was won (if pokemon catched, the fight is considered as won)
      pokemon_catched -- (bool) Pokemon catched (will always be false if catching pokemon was not requested)
    """
    if self.beginWildPokemonBattle(wild_pokemon_id=wild_pokemon_id, x=x, y=y):
      return self.fightAllPokemonsInBattle(request_catch=request_catch)
    else:
      return False, False

  def fightAnyWildPokemonInAreaWithAnyPokemon(self, x1, y1, x2, y2, request_catch=False, number_of_requested_win_or_catch=1, level_requirement=-1):
    """Try to kill/catch a specific number of pokemons in a specific area (all intelligence is in the function)

    Keyword arguments:
      x1 -- (int) Horizontal position of first dot of the rectangle
      y1 -- (int) Vertical position of first dot of the rectangle
      x2 -- (int) Horizontal position of second dot of the rectangle
      y2 -- (int) Vertical position of second dot of the rectangle
      request_catch -- (bool, optional) Catch the pokemons (by default, it's not trying to catch them)
      number_of_requested_win_or_catch -- (int) Number of pokemons should be killed/catchedv(-1 for unlimited)
      level_requirement -- (int, optional) If specified, use only pokemons with level >= level_requirement

    return:
      no_error -- (bool) No error during the function call
      number_of_won_fights -- (int) Number of won fights (may be less than the requested fights to win)
      number_of_catched_pokemons -- (int)  Number of won catched pokemons (may be less than the requested fights to win)
    """
    number_of_won_fights = 0
    number_of_catched_pokemons = 0

    # Call this function in order to not do time consuming actions for nothing
    if not self.selectAnyMainPokemonWithAp(level_requirement=level_requirement):
      logging.warning("No pokemon available for the fights")
      return False, number_of_won_fights, number_of_catched_pokemons

    all_pokemons_found, areas = self.findWildPokemonsInArea(x1=x1, y1=y1, x2=x2, y2=y2)
    if (len(areas) != 0) or number_of_requested_win_or_catch == -1:
      for area in areas:
        for wild_pokemon in area['pokemons']:
          # Check if we are done with requirements (number of pokemons to kill/catch)
          if request_catch and number_of_catched_pokemons >= number_of_requested_win_or_catch and number_of_requested_win_or_catch != -1:
            logging.debug("{} pokemons catched".format(str(number_of_catched_pokemons)))
            return True, number_of_won_fights, number_of_catched_pokemons
          elif (not request_catch) and number_of_won_fights >= number_of_requested_win_or_catch and number_of_requested_win_or_catch != -1:
            logging.debug("{} wild pokemons killed".format(str(number_of_won_fights)))
            return True, number_of_won_fights, number_of_catched_pokemons
          # Use a pokemon with enough AP
          elif self.selectAnyMainPokemonWithAp(level_requirement=level_requirement):
            # Try to kill/catch the wild pokemon
            fight_won, pokemon_catched = self.fightWildPokemon(wild_pokemon_id=wild_pokemon, x=area['x'], y=area['y'], request_catch=request_catch)
            if fight_won:
              number_of_won_fights = number_of_won_fights + 1
            if pokemon_catched:
              number_of_catched_pokemons = number_of_catched_pokemons + 1
          else:
            logging.warning("No pokemon with AP remaining.")
            return True, number_of_won_fights, number_of_catched_pokemons
    else:
      logging.warning("Request is impossible as there is no pokemon")
      return False, 0, 0

    return True, number_of_won_fights, number_of_catched_pokemons

######################### Quest ##########################

  def doSpeakQuest(self, id, x=-1, y=-1, is_principal_quest=True):
    """Do quest which requires to speak

    Keyword arguments:
      id -- (int) ID of the quest
      x -- (int, optional) Horizontal position of the quest
      y -- (int, optional) Vertical position of the quest
      is_principal_quest -- (bool, optional) Is it a principal or secondary quest? (default: principal)

    return:
      success -- (bool) The quest is a success
    """
    if x != -1 and y != -1:
      if not self.goToInMap(x, y):
        logging.warning("Impossible to go to quest localisation ({}, {})".format(str(x), str(y)))
        return False

    if is_principal_quest:
      quest_url = "{}/quetes_principales.php".format(PokemonOrigins.__BASE_WEBSITE)
    else:
      quest_url  = "{}/quetes_secondaires.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
               "action": "parler"
              }
    params = {
               "id": id
             }
    post_quest = self.session.post(url=quest_url, data=payload, params=params).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    return (not "Vous n'avez pas accès à ces informations" in post_quest) and (not "c'est mal de tricher avec les liens" in post_quest)

  def doFightQuest(self, id, x=-1, y=-1):
    """Do quest which requires to fight

    Keyword arguments:
      id -- (int) ID of the quest
      x -- (int, optional) Horizontal position of the quest
      y -- (int, optional) Vertical position of the quest

    return:
      success -- (bool) The quest is a success
    """
    # Go to quest localisation
    if x != -1 and y != -1:
      if not self.goToInMap(x, y):
        logging.warning("Impossible to go to quest localisation ({}, {})".format(str(x), str(y)))
        return False

    # Get data to request the fight
    quest_url = "{}/quetes_principales.php".format(PokemonOrigins.__BASE_WEBSITE)
    params = {"id": id}
    quest_data = BeautifulSoup(self.session.get(url=quest_url, params=params).text, "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
    id_quete = ""
    entree = ""
    type_quete = ""
    action = ""
    for form in quest_data.findAll("form"):
      if form.find('input', {'name': 'action'}):
        if form.find('input', {'name': 'action'}).get("value") == "combat":
          id_quete = form.find('input', {'name': 'id_quete'}).get("value")
          entree = form.find('input', {'name': 'entree'}).get("value")
          type_quete = form.find('input', {'name': 'type_quete'}).get("value")
          action = form.find('input', {'name': 'action'}).get("value")
          break
    if len(id_quete) == 0 or len(entree) == 0 or len(type_quete) == 0 or len(action) == 0:
      logging.warning("Impossible to get all informations in order to request the fight")
      return False

    # Request the fight
    fight_quest_url = "{}/quetes_combat.php".format(PokemonOrigins.__BASE_WEBSITE)
    payload = {
                "action": action,
                "id_quete": id_quete,
                "type_quete": type_quete,
                "entree": entree
              }
    res_request_fight = self.session.post(url=fight_quest_url, data=payload).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)
    if not ("à combattre à votre adversaire." in res_request_fight):
      logging.warning("Error while requesting the fight")
      return False

    # Fight
    fight_won, pokemon_catched = self.fightAllPokemonsInBattle(request_catch=False, is_quest=True)

    return fight_won

  def speakToPnj(self, id, x=-1, y=-1):
    """Speak with a pnj

    Keyword arguments:
      id -- (int) ID of the pnj
      x -- (int, optional) Horizontal position of the quest
      y -- (int, optional) Vertical position of the quest

    return:
      success -- (bool) Speaking with the pnj is a success
    """
    # Go to quest localisation
    if x != -1 and y != -1:
      if not self.goToInMap(x, y):
        logging.warning("Impossible to go to pnj localisation ({}, {})".format(str(x), str(y)))
        return False

    # Get data to request the fight
    quest_url = "{}/pnj.php".format(PokemonOrigins.__BASE_WEBSITE)
    params = {"id": id}
    pnj_data = self.session.get(url=quest_url, params=params).text
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    return not ("Il est interdit" in pnj_data)

  def doPrincipalQuest(self, quest_id, permissive=False):
    """Automatically try to achieve the quest

    Keyword arguments:
      quest_id -- (int) ID of the principal quest
      permissive -- (int, optional) Try all elements of the quest even if one fails

    return:
      success -- (bool) Quest success
    """
    # Quest 1
    if quest_id == 1:
      if not self.doSpeakQuest(id=1, x=97, y=20):
        logging.warning("Could not do speak quest 1 for principal quest 1...")
        if not permissive:
          return False
      # Try to catch 3 pokemons in order to be more prepared for fight with chen later
      no_error, number_of_won_fights, number_of_catched_pokemons = self.fightAnyWildPokemonInAreaWithAnyPokemon(x1=94, y1=19, x2=94, y2=21, number_of_requested_win_or_catch=3, request_catch=True)
      if not (no_error and number_of_catched_pokemons >= 1):
        logging.warning("Could not capture a pokemon for the principal quest 1...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=2, x=97, y=20):
        logging.warning("Could not do speak quest 2 (1/2) for principal quest 1...")
        if not permissive:
          return False
      if not self.speakToPnj(id=1, x=96, y=23):
        logging.warning("Could not speak to pnj 1 for principal quest 1...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=2, x=96, y=23):
        logging.warning("Could not do speak quest 2 (2/2) for principal quest 1...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=3, x=97, y=20):
        logging.warning("Could not do speak quest 3 for principal quest 1...")
        if not permissive:
          return False
      no_error, number_of_won_fights, number_of_catched_pokemons = self.fightAnyWildPokemonInAreaWithAnyPokemon(x1=94, y1=19, x2=94, y2=21, number_of_requested_win_or_catch=3)
      if not (no_error and number_of_won_fights >= 3):
        logging.warning("Could not kill 3 pokemons for the principal quest 1...")
        if not permissive:
          return False
      if not self.doFightQuest(id=4, x=97, y=20):
        logging.warning("Could not do win fight quest 1 for principal quest 1...")
        return False
      else:
        logging.debug("Principal quest 1 success!")
        return True
    # Quest 2
    elif quest_id == 2:
      if not self.doSpeakQuest(id=5, x=97, y=20):
        logging.warning("Could not do speak quest 5 for principal quest 2...")
        return False
      if not self.speakToPnj(id=2, x=68, y=22):
        logging.warning("Could not do speak pnj 2 for principal quest 2...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=5):
        logging.warning("Could not do speak quest 5 for principal quest 2...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=6):
        logging.warning("Could not do speak quest 6 (1/2) for principal quest 2...")
        if not permissive:
          return False
      if not self.speakToPnj(id=3, x=78, y=22):
        logging.warning("Could not do speak pnj 2 for principal quest 2...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=6):
        logging.warning("Could not do speak quest 6 (2/2) for principal quest 2...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=7, x=68, y=22):
        logging.warning("Could not do speak quest 7 (1/2) for principal quest 2...")
        if not permissive:
          return False
      if not self.speakToPnj(id=4, x=97, y=20):
        logging.warning("Could not do speak pnj 4 for principal quest 2...")
        if not permissive:
          return False
      if not self.doSpeakQuest(id=7):
        logging.warning("Could not do speak quest 7 (2/2) for principal quest 2...")
        return False
      else:
        logging.debug("Principal quest 2 success!")
        return True
    # Unhandled quests
    else:
      logging.warning("Principal quest {} is not handled yet...".format(str(quest_id)))
      return False

  def getAccountPrincipalQuest(self):
    """Get the current principal quest of the account

    return:
      current_quest -- (int) Current quest of the account (-1 if an error occured)
    """
    quests_url = "{}/journaldesquetes.php".format(PokemonOrigins.__BASE_WEBSITE)

    quests_data = BeautifulSoup(self.session.get(url=quests_url).text, "html.parser")
    time.sleep(PokemonOrigins.__WAIT_AFTER_REQUEST)

    current_quest = -1

    if "Vous devriez aller voir le professeur Chen." in quests_data.text:
      current_quest = 0
    else:
      # Get the list of all missions and usable pokemons
      for b in quests_data.findAll("b"):
        if "Quête n°" in b.text:
          quest = int(re.sub("[^0-9/]", "", str(b.text)))
          if quest > current_quest:
            current_quest = quest
      if current_quest == -1:
        logging.error("Could not find the current quest of this account...")
        return current_quest

    logging.debug("Current quest of this account is {}".format(str(current_quest)))
    return current_quest

if __name__ == "__main__":
  """Demo on how to connect and do actions to the website"""

  # Add Logs
  logger = logging.getLogger()
  logger.setLevel(logging.WARNING)

  # Get the login and the password from command line
  arg_login = ""
  arg_password = ""
  arg_do_bonus = False
  arg_evolve_all_pokemons = False
  arg_level_up_all_pokemons = False
  arg_demo_fight = False
  arg_do_all_missions = False
  try:
    opts, args = getopt.getopt(sys.argv[1:], "u:p:belfm", ["username=", "password=", "bonus", "evolve", "levelup", "fight", "missions"])
  except getopt.GetoptError as err:
    print("[ERROR] "+str(err))
    sys.exit(1)
  for o, a in opts:
    if o in ("-u", "--username"):
      arg_login = str(a)
    elif o in ("-p", "--password"):
      arg_password = str(a)
    elif o in ("-b", "--bonus"):
      arg_do_bonus = True
    elif o in ("-e", "--evolve"):
      arg_evolve_all_pokemons = True
    elif o in ("-l", "--levelup"):
      arg_level_up_all_pokemons = True
    elif o in ("-f", "--fight"):
      arg_demo_fight = True
    elif o in ("-m", "--missions"):
      arg_do_all_missions = True
    else:
      print("[ERROR] Not handled parameters. (only username (-u) and password (-p) available.")
      print("[ERROR] Mandatory: username (-u) and password (-p)")
      print("[ERROR] Optional: bonus (-b), evolve (-e), levelup (-l), fight (-f) and missions (-m)")
      sys.exit(1)
  if arg_login == "" or arg_password == "":
    print("[ERROR] At least username (-u) and password (-p) must be provided.")
    print("[ERROR] Optional: bonus (-b), evolve (-e), levelup (-l), fight (-f) and missions (-m)")
    sys.exit(1)

  # Instantiate the class
  pkm_orig = PokemonOrigins()

  # Connect
  if (pkm_orig.connect(login=arg_login, password=arg_password)):
    print("Connected to {}".format(arg_login))
    # Do some actions in the website
    if arg_do_bonus:
      pkm_orig.doAllBonus()
      print("All bonus done")
    if arg_evolve_all_pokemons:
      print("All pokemon evolved: {}".format(str(pkm_orig.evolveAllPokemons())))
    if arg_demo_fight:
      print("----- Fighting demo begin -----")
      # Go to pokemon league by foot or with dracoport
      if not pkm_orig.goToInMap(x=28, y=-10):
        print("Need to use the dracoport to go to the pokemon league...")
        pkm_orig.useDracoport(PokemonOrigins.eDracoportLocalization.POKEMON_LEAGUE)
      else:
        print("Going to the pokemon league by foot")

      # Pokemon league
      if pkm_orig.goToInMap(x=28, y=-10):
        print("Fighting pokemons in the pokemon league area")
        pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=28, y1=-10, x2=29, y2=-7, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
        pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=28, y1=-4, x2=29, y2=-3, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
        pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=26, y1=2, x2=27, y2=-3, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
        # Going into cave near pokemon league
        if pkm_orig.goToInMap(x=30, y=-5):
          print("Fighting pokemons in the pokemon cave area")
          pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=30, y1=-5, x2=30, y2=-5, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
          pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=31, y1=-9, x2=31, y2=2, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
          pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=32, y1=-9, x2=32, y2=2, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
          pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=33, y1=-9, x2=33, y2=2, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
          pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=34, y1=-9, x2=34, y2=2, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
          pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=35, y1=-9, x2=35, y2=2, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=50)
          if pkm_orig.goToInMap(x=36, y=-4):
            print("Fighting pokemons in the pokemon victory road area")
            pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=36, y1=-4, x2=36, y2=-4, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=40)
            pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=40, y1=-8, x2=41, y2=3, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=35)
            pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=43, y1=-8, x2=44, y2=3, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=30)
            pkm_orig.fightAnyWildPokemonInAreaWithAnyPokemon(x1=46, y1=-8, x2=47, y2=3, request_catch=True, number_of_requested_win_or_catch=-1, level_requirement=30)
            # Go back to first place
            print("Trying to go back to the pokemon league by foot")
            if pkm_orig.goToInMap(x=41, y=-4):
              if pkm_orig.goToInMap(x=35, y=-4):
                if pkm_orig.goToInMap(x=30, y=-5):
                  if pkm_orig.goToInMap(x=28, y=-10):
                    print("All fight demo done with success")
                  else:
                    print("Impossible to go back to (28, -10)")
                else:
                  print("Impossible to go back to (30, -5)")
              else:
                print("Impossible to go back to (35, -4)")
            else:
              print("Impossible to go back to (41, -4)")

        if not pkm_orig.goToInMap(x=28, y=-10):
          if pkm_orig.useDracoport(PokemonOrigins.eDracoportLocalization.POKEMON_LEAGUE):
            print("Used dracoport to go back to pokemon league...")
          else:
            print("Impossible to go back to pokemon league...")

      print("----- Fighting demo end -----")

    if arg_level_up_all_pokemons:
      print("All pokemon leveled up: {}".format(str(pkm_orig.levelUpAllPokemons())))
    if arg_do_all_missions:
      pkm_orig.doAllMissions()
      print("All missions done")

    if pkm_orig.disconnect():
      print("Disconnected")
    else:
      print("Could not disconnect...")

    # Quit the program without error
    sys.exit(0)

  # Could not connect...
  print("Could not connect to {}...".format(arg_login))
  sys.exit(2)
