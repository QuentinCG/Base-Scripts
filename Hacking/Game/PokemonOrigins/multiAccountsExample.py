#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Do minimalistics actions in pokemon-origins.com website with multiple accounts
  Note: accounts variables must be filled in the source code (line 21 and 22)
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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# Please put all your pokemon-origins.com logins and passwords here
main_account = {"login": "MAIN_LOGIN_HERE", "password": "MAIN_PASS_HERE"}
accounts = [
  {"login": "YOUR_LOGIN_1_HERE", "password": "YOUR_PASSWORD_1_HERE"},
  {"login": "YOUR_LOGIN_2_HERE", "password": "YOUR_PASSWORD_2_HERE"},
  # and so on... (as many accounts as you want)
]
email_sender_address = "emailaddresshere@gmail.com"
email_receiver_address = "receiverhere@gmail.com"
smtp_login = "emailaddresshere@gmail.com"
smtp_password = "PASSHERE"
smtp_server = "smtp.gmail.com"
smtp_port = 587

if __name__ == '__main__':
  # Add Logs
  logger = logging.getLogger()
  logger.setLevel(logging.WARNING)

  # Send only email if it is 10AM
  send_email = (datetime.datetime.now().hour == 10)
  if send_email:
    html_error_output = "<p>List of usernames that can't log in: "
    html_table_output = "<p>List of all accounts:<br/><table border=1, cellpadding=3 cellspacing=1>"
    html_table_output += "<tr><td>Username</td><td>Gold</td><td>Dollars</td><td>Score</td><td>Rank</td><td>Pokemons</td><td>Current principal quest</td></tr>"

    conn_main = PokemonOrigins.PokemonOrigins()
    if conn_main.connect(login=main_account['login'], password=main_account['password']):
        print("Connected to {}".format(main_account['login']))
        success, gold, dollars, score, rank, owned_pokemons, max_pokemons = conn_main.getAccountInfo()
        current_quest = conn_main.getAccountPrincipalQuest()
        if success:
          print("This account has {} gold and {} dollars".format(str(gold), str(dollars)))
          html_table_output += "<tr><td>{} (main account)</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}/{}</td><td>{}</td></tr>".format(main_account['login'],
                                 str(gold), str(dollars), str(score), str(rank), str(owned_pokemons), str(max_pokemons), str(current_quest))
        else:
          print("Could not get gold and dollars from the account...")
          html_error_output += "{}, ".format(main_account['login'])
    else:
      print("Could not connect to {}".format(main_account['login']))

  # Do the actions with all specified accounts
  for account in accounts:
    conn = PokemonOrigins.PokemonOrigins()
    if conn.connect(login=account['login'], password=account['password']):
      print("Connected to {}".format(account['login']))
      conn.doAllBonus()
      print("All bonus done")
      conn.doAllMissions()
      print("All missions done")

      if send_email:
        success, gold, dollars, score, rank, owned_pokemons, max_pokemons = conn.getAccountInfo()
        current_quest = conn.getAccountPrincipalQuest()
        if success:
          print("This account has {} gold and {} dollars".format(str(gold), str(dollars)))
          html_table_output += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}/{}</td><td>{}</td></tr>".format(account['login'],
                                 str(gold), str(dollars), str(score), str(rank), str(owned_pokemons), str(max_pokemons), str(current_quest))
        else:
          print("Could not get gold and dollars from the account...")

      if conn.disconnect():
        print("Disconnected")
      else:
        print("Not disconnected...")
    else:
      print("Could not connect to {}".format(account['login']))
      if send_email:
        html_error_output += "{}, ".format(account['login'])

  if send_email:
    html_table_output += "</table></p>"
    html_error_output += "</p>"

    html_full = "<html><head></head><body>"
    html_full += html_table_output
    html_full += html_error_output
    html_full += "</body></html>"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Pokemon-Origins logs"
    msg['From'] = email_sender_address
    msg['To'] = email_receiver_address
    msg.attach(MIMEText(html_full, 'html'))

    smtp_conn = smtplib.SMTP("{}:{}".format(smtp_server, str(smtp_port)))
    smtp_conn.ehlo()
    smtp_conn.starttls()
    smtp_conn.login(smtp_login, smtp_password)
    smtp_conn.send_message(msg)
