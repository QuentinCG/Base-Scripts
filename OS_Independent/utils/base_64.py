#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions for base 64 conversion
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2016)"
__python_version__ = "2.7+ and 3.+"
__version__ = "0.1 (2016/03/27)"
__status__ = "Usable for any project"

import base64 # For base 64 conversion

def encodeDataToBase64(data):
  """Encore data to base 64 data

  Keyword arguments:
    data -- (string) Normal data string

  return: (string) Base 64 encoded data
  """
  return base64.b64encode(data)

def decodeDataFromBase64(data):
  """Decode data from base 64

  Keyword arguments:
    data -- string, Base 64 encoded data

  return: (string) Normal data string
  """
  return base64.b64decode(data)

def convertFileToBase64(file_name):
  """Encore file to base 64 data

  Keyword arguments:
    data -- string, Normal file name

  return: (string) Base 64 encoded data from file
  """
  with open(file_name, "rb") as _file:
    file_data = _file.read()
    return encodeDataToBase64(file_data)

def convertBase64ToFile(base64_encoded_data, file_name):
  """Decode data from base 64 to file

  Keyword arguments:
    data -- (string) Base 64 encoded data
  """
  reconstructed_data = decodeDataFromBase64(base64_encoded_data)
  with open(file_name, "wb") as _file:
    _file.write(reconstructed_data)

def main():
  """Demo of the base 64 encoding utility functions"""

  print("\n----------------------------------------------------")
  print("--Base 64 Encoding/decoding utility functions demo--")
  print("----------------------------------------------------")

  print("\n------------Encode data to base 64------------------")
  data = "Normal string"
  encoded_data = encodeDataToBase64(data)
  print("Base 64 encoded string of \""+data+"\": \""+encoded_data+"\"")

  print("\n------------Decode data from base 64----------------")
  decoded_data = decodeDataFromBase64(encoded_data)
  print("Base 64 decoded string of \""+encoded_data+"\": \""+decoded_data+"\"")

  print("\n-------Decode data from base 64 to file-------------")
  dummy_file = "dummy_file.txt"
  print("Convert \""+encoded_data+"\" encoded string to file "+dummy_file)
  convertBase64ToFile(encoded_data, dummy_file)
  with open(dummy_file, "rb") as _file:
    print("Data contained in file "+dummy_file+": \""+_file.read()+"\"")

  print("\n-------Encode data from file to base 64-------------")
  file_encoded_data = convertFileToBase64(dummy_file)
  print("Encoded data from file "+dummy_file+": \""+file_encoded_data+"\"")

  print("\n----------------------------------------------------")
  print("-------------------End of demo----------------------")
  print("----------------------------------------------------\n")

if __name__ == "__main__":
    main()
