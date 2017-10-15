#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Cheat demo for pokemon-origins.com website
  How to use: {filename}.py --login MyLoginHere --password MyPasswordHere
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

WAIT_AFTER_REQUEST = 1 # Sec
BASE_WEBSITE = "http://www.pokemon-origins.com"

def connect(login, password, session):
  """Connect to the website with specific identification

  Keyword arguments:
    login -- (str) Login
    password -- (str) Password
    session -- (requests.Session) Session

  return: (bool) Is connected?
  """
  login_url = "{}/connexion.php".format(BASE_WEBSITE)
  payload = {
             "pseudo": login,
             "mdp": password,
             "action": "identification",
             "identification": "identification"
            }

  post_login = session.post(url=login_url,
                            data=payload)

  time.sleep(WAIT_AFTER_REQUEST)

  return ("Vous êtes maintenant connecté." in post_login.text)

def disconnect(session):
  """Disconnect from the website

  Keyword arguments:
    session -- (request.Session) Session

  return: (bool) Is disconnected?
  """
  disconnection_url = "{}/deconnexion.php".format(BASE_WEBSITE)
  disconnection_status = session.get(url=disconnection_url)

  time.sleep(WAIT_AFTER_REQUEST)

  return ("Votre session a bien été arretée!" in disconnection_status.text)

def doAllBonus(session):
  """Do all 3 bonus to get in-game gold

  Keyword arguments:
    session -- (request.Session) Session
  """
  bonus_uris = {
                 "bonus1.php",
                 "bonus2.php",
                 "bonus3.php"
               }

  for bonus_uri in bonus_uris:
    # Get base bonus page and check if it is possible to get the bonus
    if bonus_uri in session.get("{}/bonus.php".format(BASE_WEBSITE)).text:
      time.sleep(WAIT_AFTER_REQUEST)
      # Then get the bonus
      session.get("{}/{}".format(BASE_WEBSITE, bonus_uri))
      time.sleep(WAIT_AFTER_REQUEST)
      logging.debug("Bonus {} done.".format(bonus_uri))
    else:
      logging.warning("No bonus possible for {} (already done)".format(bonus_uri))
      time.sleep(WAIT_AFTER_REQUEST)

def getAvailableMissionsAndPokemons(available_missions, available_pokemons, session):
  """Get a list of all available missions and pokemons available to do missions

  Keyword arguments:
    available_missions -- (out, list) List of available missions
    available_pokemons -- (out, list) List of available pokemons
    session -- (request.Session) Session
  """
  mission_url = "{}/missions.php".format(BASE_WEBSITE)

  missions_data = BeautifulSoup(session.get(url=mission_url).text, "html.parser")
  time.sleep(WAIT_AFTER_REQUEST)

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

def doMission(mission, pokemon, session):
  """Do a mission with a pokemon

  Keyword arguments:
    mission -- (str) Mission to do
    pokemon -- (str) Pokemon to use for the mission
    session -- (request.Session) Session
  """
  logging.debug("Doing mission {} with pokemon {}".format(mission, pokemon))
  payload = {
              "id_liste_pokemons": pokemon,
              "id_mission": mission,
              "action" : "inscription"
            }
  post_mission = session.post(url="{}/missions.php".format(BASE_WEBSITE), data=payload)
  time.sleep(WAIT_AFTER_REQUEST)

  return ("Votre pokémon est revenu de mission" in post_mission.text)

def doAllMissions(session):
  """Do all missions with all pokemons

  Keyword arguments:
    session -- (request.Session) Session
  """
  missions = []
  pokemons = []

  getAvailableMissionsAndPokemons(available_missions=missions,
                                  available_pokemons=pokemons,
                                  session=session)

  while len(pokemons) > 0:
    while len(missions) > 0 and len(pokemons) > 0:
      try:
        if not doMission(mission=missions[0],
                         pokemon=pokemons[0],
                         session=session):
          logging.warning("Could not do mission {} with pokemon {}".format(missions[0], pokemons[0]))
      except requests.exceptions.ContentDecodingError:
        # This error may occur but should not break all the process
        logging.error("Error while trying to parse data from mission {} with pokemon {}".format(missions[0], pokemons[0]))

      pokemons.remove(pokemons[0])
      missions.remove(missions[0])

    getAvailableMissionsAndPokemons(
      available_missions=missions,
      available_pokemons=pokemons,
      session=session)

    # It may occur that there is no missions left for available pokemons
    # Just wait before some missions becomes available
    if len(missions) <= 0 and len(pokemons) > 0:
      time.sleep(60)

if __name__ == "__main__":
  """Demo on how to periodically connect and do actions to the website

    Usecase: {filename}.py --login MyLoginHere --password MyPasswordHere
  """

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

  # Create a session
  my_session = requests.Session()

  # Connect
  if (connect(login=arg_login, password=arg_password, session=my_session)):
    logging.debug("Connected with {}".format(arg_login))

    doAllBonus(session=my_session)
    logging.debug("All bonus done")

    doAllMissions(session=my_session)
    logging.debug("All missions done")

    if disconnect(session=my_session):
      logging.debug("Disconnected from {}".format(arg_login))
    else:
      logging.warning("Could not disconnect from {}".format(arg_login))

    # Quit the program without error
    sys.exit(0)

  logging.warning("Could not connect with {}".format(arg_login))
  sys.exit(2)
