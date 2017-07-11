#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Utility functions to send message/image with Facebook messenger (can also be called with shell)
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "3.+ (SSL not supported correctly with 2.7+)"
__version__ = "1.0 (2017/04/25)"
__status__ = "Usable for any project"
__dependency__ = "fbchat (use 'pip install fbchat' to install package)"

import sys, getopt, logging
import fbchat
from fbchat.models import *

def sendWithFacebookMessenger(email_address, password, receiver_id, message, image_path, debug=True):
  """Send message and or image via Facebook Messenger

    Keyword arguments:
      email_address -- (string) Facebook email address
      password -- (string) Facebook password
      receiver_id -- (string) ID of the user receiving the file
      message -- (string) Message to send
      image_path -- (string) Path of the file to send
      debug -- (bool, optional) Show debug information

  return: (bool) Image and or message sent
  """
  return_value = False

  # Initialize the dropbox connection
  client = fbchat.Client(email_address, password)

  if message != "" and image_path == "":
    try:
      client.sendMessage(message, thread_id=receiver_id, thread_type=ThreadType.USER)
      return_value = True
    # TODO: Be more precise in exceptions (but a lot of exceptions can occure with client.send)
    except Exception:
      pass
  elif image_path != "":
    try:
      client.sendLocalImage(image_path, message=message, thread_id=receiver_id, thread_type=ThreadType.USER)
      return_value = True
    # TODO: Be more precise in exceptions (but a lot of exceptions can occure with client.send)
    except Exception:
      pass

  return return_value


################################# HELP FUNCTION ################################
def __help():
  # Help
  print("HELP (-h, --help): Give information to use facebook messenger script")
  print("EMAIL (-e, --email): Email (of the sender)")
  print("PASSWORD (-p, --password): Password (of the sender)")
  print("RECEIVER (-r, --receiver): Receiver ID")
  print("MESSAGE (-m, --message): Message to send")
  print("IMAGE (-i, --image): Image to send")
  print("\n\n")
  print("Example (send image AND message): python fb_messenger_send.py --email \"{email here}\" --password \"{password here}\" --receiver \"{receiver id here}\" --message \"Hello World\" --image \"/tmp/dummy.png\"")


################################# MAIN FUNCTION ###############################
def main():
  """Shell facebook messenger utility function"""

  # Set the log level (no log will be shown if "logging.CRITICAL" is used)
  logger = logging.getLogger()
  logger.setLevel(logging.CRITICAL)

  # Have input() function compatible with python 2+ and 3+
  try:
    input = raw_input
  except NameError:
    pass

  _email = ""
  _password = ""
  _receiver = ""
  _message = ""
  _image = ""

  # Get options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "he:p:r:m:i:",
                               ["help", "email=", "password=", "receiver=", "message=", "image="])
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
    if o in ("-e", "--email"):
      _email = str(a)
      continue
    if o in ("-p", "--password"):
      _password = str(a)
      continue
    if o in ("-r", "--receiver"):
      _receiver = str(a)
      continue
    if o in ("-m", "--message"):
      _message = str(a)
      continue
    if o in ("-i", "--image"):
      _image = str(a)
      continue

  if _email == "":
    print("[ERROR] No authentification email specified")
    __help()
    sys.exit(1)
  if _password == "":
    print("[ERROR] No authentification password specified")
    __help()
    sys.exit(1)
  if _receiver == "" or (_message == "" and _image == ""):
    print("[ERROR] No receiver or message/image specified")
    __help()
    sys.exit(1)

  return_value = sendWithFacebookMessenger(email_address=_email, password=_password, receiver_id=_receiver, message=_message, image_path=_image, debug=True)

  if return_value:
    sys.exit(0)

  sys.exit(1)

if __name__ == "__main__":
    main()
