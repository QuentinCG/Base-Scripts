#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Utility functions to send emails with SMTP protocol
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2017/04/19)"
__status__ = "Usable for any project"

import smtplib
import logging

def sendEmail(host, port, using_tsl, username, password, from_addr, from_name,
              to_addresses_and_names, subject, message):
  """Send an email

    Keyword arguments:
      host -- (string) Host name (for example: "smtp.gmail.com" for Gmail)
      port -- (int) SMTP port
      using_tsl -- (bool) Use encryption (for Gmail account, you also need to check this option: https://myaccount.google.com/lesssecureapps?pli=1)
      username -- (string) SMTP username (for example: "test" for Gmail account "test@gmail.com")
      password -- (string) SMTP password (for example: 587 for Gmail secured connection)
      from_addr -- (string) Email address of the sender (for example: "test@gmail.com")
      from_name -- (string) Name of the sender
      to_addresses_and_names -- (table) Table of receiver email addresses and receiver names [[email addr 1, email name 1], ...]
      subject -- (string) Mail subject
      message -- (string) Mail message

  return: (bool) Email sent
  """
  return_value = True

  # Initialize the SMTP connection
  server = smtplib.SMTP(host, port)

  if using_tsl:
    server.starttls()
  # Log in to the server
  try:
    server.login(username, password)
  except smtplib.SMTPHeloError:
    return_value = False
    logging.warning("The server didn’t reply properly to the HELO greeting.")
  except smtplib.SMTPAuthenticationError:
    return_value = False
    logging.warning("The server didn’t accept the username/password combination.")
  except smtplib.SMTPException:
    return_value = False
    logging.warning("No suitable authentication method was found.")

  # Create the message to send
  if return_value:
    to_addresses = ""
    to_addr_and_names_display = ""
    for addr in to_addresses_and_names:
      if to_addresses != "":
        to_addresses += ", "
        to_addr_and_names_display += ", "
      to_addresses += addr[0]
      to_addr_and_names_display += "{}<{}>".format(addr[1], addr[0])

    header  = "From: {}\nTo: {}\nSubject: {}\n\n".format("{}<{}>".format(from_name, from_addr),
                                                         to_addr_and_names_display,
                                                         subject)
    message = header + message

    #Send the email
    try:
      server.sendmail(from_addr, to_addresses, message)
    except smtplib.SMTP.SMTPRecipientsRefused:
      return_value = False
      logging.warning("All recipients were refused. Nobody got the mail.")
    except smtplib.SMTPHeloError:
      return_value = False
      logging.warning("The server didn’t reply properly to the HELO greeting.")
    except smtplib.SMTPSenderRefused:
      return_value = False
      logging.warning("The server didn’t accept from_addr={}.".format(from_addr))
    except smtplib.SMTPDataError:
      return_value = False
      logging.warning("The server replied with an unexpected error code.")

  # End SMTP connection
  server.quit()

  return return_value


def main():
  """Demo of the email utility functions"""

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  # Have input() function compatible with python 2+ and 3+
  try:
    input = raw_input
  except NameError:
    pass

  print("\n----------------------------------------------------")
  print("-----------Email utility functions demo-------------")
  print("----------------------------------------------------")

  print("\n-----------------Send an email--------------------")
  _host = str(input("Host (smtp.gmail.com for example): "))
  _port = int(input("Port (587 for example): "))
  _using_tsl = bool(input("Using TSL (0 for no, 1 for yes): "))
  _username = str(input("Username: "))
  _password = str(input("Password: "))
  _from_addr = str(input("Sender address: "))
  _from_name = str(input("Sender name: "))
  _to_address = str(input("Receiver address: "))
  _to_name = str(input("Receiver name: "))
  _subject =str(input("Subject: "))
  _message = str(input("Message: "))
  print("Send email: {}".format(sendEmail(host=_host,
                                          port=_port,
                                          using_tsl=_using_tsl,
                                          username=_username,
                                          password=_password,
                                          from_addr=_from_addr,
                                          from_name=_from_name,
                                          to_addresses_and_names=[[_to_address, _to_name]],
                                          subject=_subject,
                                          message=_message)))

  print("\n----------------------------------------------------")
  print("-------------------End of demo----------------------")
  print("----------------------------------------------------\n")

if __name__ == "__main__":
    main()
