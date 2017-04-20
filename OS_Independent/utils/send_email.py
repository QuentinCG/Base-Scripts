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
import sys, getopt
import ast

def sendEmail(host, port, using_tls, username, password, from_addr, from_name,
              to_addresses_and_names, subject, message):
  """Send an email

    Keyword arguments:
      host -- (string) Host name (for example: "smtp.gmail.com" for Gmail)
      port -- (int) SMTP port (for example: 587 for Gmail secured connection)
      using_tls -- (bool) Use encryption (for Gmail account, you also need to check this option: https://myaccount.google.com/lesssecureapps?pli=1)
      username -- (string) SMTP username (for example: "test" for Gmail account "test@gmail.com")
      password -- (string) SMTP password
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

  if using_tls:
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


################################# HELP FUNCTION ################################
def __help(filename=__file__):
  # Help
  print("HELP (-h, --help): Give information to use the email sender script")
  print("HOST (-o, --host): Host name (for example: 'smtp.gmail.com' for Gmail)")
  print("PORT (-p, --port): SMTP port (for example: 587 for Gmail secured connection)")
  print("USING TLS (-t, --usingTls): Use encryption (for Gmail account, you also need to check this option: https://myaccount.google.com/lesssecureapps?pli=1)")
  print("USERNAME (-u, --username): SMTP username (for example: 'test' for Gmail account 'test@gmail.com')")
  print("PASSWORD (-w, --password): SMTP password")
  print("ADDRESS FROM (-f, --fromAddr): Address from which the email will be sent")
  print("NAME FROM (-n, --fromName): Name of the email from which the email will be sent")
  print("RECEIVERS ADDRESS AND NAME (-t, --toAddressesAndNames): Table of receiver email addresses and receiver names (example: [['receiver1@domain.com', 'receiver 1'], ['receiver2@domain.com', 'receiver 2']])")
  print("SUBJECT (-s, --subject): Email subject")
  print("MESSAGE (-m, --message): Email message")
  print("\n\n")
  print("Example: python send_email.py --host smtp.gmail.com --port 587 --using_tls True --username dummy --password epicPass --fromAddr dummy@gmail.com --fromName Dummmmmyyy --toAddressesAndNames [['receiver1@domain.com', 'receiver 1']] --subject 'Hi' --message 'Wowowowo\nWowowowowowo'")


################################# MAIN FUNCTION ###############################
def main():
  """Shell Email utility function"""

  # Set the log level (no log will be shown if "logging.CRITICAL" is used)
  logger = logging.getLogger()
  logger.setLevel(logging.CRITICAL)

  # Have input() function compatible with python 2+ and 3+
  try:
    input = raw_input
  except NameError:
    pass

  _host = ""
  _port = 587
  _using_tls = True
  _username = ""
  _password = ""
  _from_addr = ""
  _from_name = ""
  _to_addresses_and_names = [[]]
  _subject = ""
  _message = ""

  # Get options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "o:p:t:u:w:f:n:t:s:m:",
                               ["host=", "port=", "usingTls=", "username=", "password=",
                                "fromAddr=", "fromName=", "toAddressesAndNames=", "subject=", "message="])
  except getopt.GetoptError as err:
    print("[ERROR] "+str(err))
    __help()
    sys.exit(1)

  # Show help (if requested)
  for o, a in opts:
    if o in ("-h", "--help"):
      __help()
      sys.exit(0)

  # Get base parameters
  for o, a in opts:
    if o in ("-o", "--host"):
      _host = str(a)
      continue
    if o in ("-p", "--port"):
      port = int(a)
      continue
    if o in ("-t", "--usingTls"):
      _using_tls = bool(a)
      continue
    if o in ("-u", "--username"):
      _username = str(a)
      continue
    if o in ("-w", "--password"):
      _password = str(a)
      continue
    if o in ("-f", "--fromAddr"):
      _from_addr = str(a)
      continue
    if o in ("-n", "--fromName"):
      _from_name = str(a)
      continue
    if o in ("-t", "--toAddressesAndNames"):
      _to_addresses_and_names = ast.literal_eval(a)
      continue
    if o in ("-s", "--subject"):
      _subject = str(a)
      continue
    if o in ("-m", "--message"):
      _message = str(a)
      continue

  return_value = sendEmail(host=_host, port=_port, using_tls=_using_tls, username=_username,
                           password=_password, from_addr=_from_addr, from_name=_from_name,
                           to_addresses_and_names=_to_addresses_and_names, subject=_subject,
                           message=_message)
  print("Send email: {}".format(str(return_value)))

if __name__ == "__main__":
    main()
