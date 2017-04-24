#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Utility functions to upload/download file to/from dropbox
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2017/04/24)"
__status__ = "Usable for any project"
__dependency__ = "Dropbox (use 'pip install dropbox' to install package)"

import sys, getopt, logging
import dropbox

def uploadFileToDropbox(oauth2_token, file_from, dropbox_file_to):
  """Upload a file to Dropbox

    Keyword arguments:
      oauth2_token -- (string) Dropbox OAuth 2 access token (https://dropbox.com/developers/apps)
      file_from -- (string) File to send to dropbox
      dropbox_file_to -- (string) File path in dropbox cloud

  return: (bool) File uploaded
  """
  return_value = False

  # Initialize the dropbox connection
  client = dropbox.client.DropboxClient(str(oauth2_token))

  try:
    # Upload file to dropbox
    f = open(file_from, 'rb')
    response = client.put_file(str(dropbox_file_to), f)
    logging.debug("File {} uploaded: {}".format(str(file_from), str(response)))
    f.close()
    return_value = True
  except IOError:
    logging.warning("File {} does not exist.".format(str(file_from)))
  except dropbox.rest.ErrorResponse as err:
    logging.warning("Dropbox error: {}".format(str(err)))

  return return_value


def downloadFileFromDropbox(oauth2_token, dropbox_file_from, file_to):
  """Download a file from Dropbox

    Keyword arguments:
      oauth2_token -- (string) Dropbox OAuth 2 access token (https://dropbox.com/developers/apps)
      dropbox_file_from -- (string) File to download from dropbox
      file_to -- (string) File path to save the file

  return: (bool) File downloaded
  """
  return_value = False

  # Initialize the dropbox connection
  client = dropbox.client.DropboxClient(str(oauth2_token))

  try:
    # Download file from dropbox
    f, metadata = client.get_file_and_metadata(str(dropbox_file_from))
    out = open(str(file_to), 'wb')
    out.write(f.read())
    out.close()
    logging.debug("File {} metadata: {}".format(str(dropbox_file_from), str(metadata)))
    return_value = True
  except IOError:
    logging.warning("Could not write file {}.".format(file_to))
  except dropbox.rest.ErrorResponse as err:
    logging.warning("Dropbox error: {}".format(str(err)))

  return return_value


################################# HELP FUNCTION ################################
def __help():
  # Help
  print("HELP (-h, --help): Give information to use dropbox script")
  print("TOKEN (-t, --token): Dropbox OAuth 2 access token (https://dropbox.com/developers/apps)")
  print("IN (-i, --in): Input file (file to send from dropbox or computer)")
  print("OUT (-o, --out): Output file (file to write to dropbox or computer)")
  print("UPLOAD (-u, --upload): Upload file from the computer to dropbox")
  print("DOWNLOAD (-d, --download): Download file from dropbox to the computer")
  print("\n\n")
  print("Example (upload): python dropbox_handler.py --token \"{token key here}\" --in \"/home/user/test.txt\" --out \"/test.txt\" --upload")
  print("Example (download): python dropbox_handler.py --token \"{token key here}\" --in \"/test.txt\" --out \"/home/user/test.txt\" --download")


################################# MAIN FUNCTION ###############################
def main():
  """Shell dropbox utility function"""

  # Set the log level (no log will be shown if "logging.CRITICAL" is used)
  logger = logging.getLogger()
  logger.setLevel(logging.CRITICAL)

  # Have input() function compatible with python 2+ and 3+
  try:
    input = raw_input
  except NameError:
    pass

  _in = ""
  _out = ""
  _oauth2_token = ""
  _download = False
  _upload = False

  # Get options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:i:o:ud",
                               ["help", "token=", "in=", "out=", "upload", "download"])
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
    if o in ("-i", "--in"):
      _in = str(a)
      continue
    if o in ("-o", "--out"):
      _out = str(a)
      continue
    if o in ("-t", "--token"):
      _oauth2_token = str(a)
      continue
    if o in ("-u", "--upload"):
      _upload = True
      continue
    if o in ("-d", "--download"):
      _download = True
      continue

  if _oauth2_token == "":
    print("[ERROR] No authentification token specified")
    __help()
    sys.exit(1)
  if _in == "":
    print("[ERROR] No input file specified")
    __help()
    sys.exit(1)
  if _out == "":
    print("[ERROR] No output file specified")
    __help()
    sys.exit(1)
  if _download == False and _upload == False:
    print("[ERROR] You need to upload or download a file")
    __help()
    sys.exit(1)
  if _download == True and _upload == True:
    print("[ERROR] You can't download and upload a file at the same time")
    __help()
    sys.exit(1)

  return_value = False
  if _download:
    return_value = downloadFileFromDropbox(oauth2_token=_oauth2_token, dropbox_file_from=_in, file_to=_out)
  else:
    return_value = uploadFileToDropbox(oauth2_token=_oauth2_token, file_from=_in, dropbox_file_to=_out)

  if return_value:
    sys.exit(0)

  sys.exit(1)

if __name__ == "__main__":
    main()
