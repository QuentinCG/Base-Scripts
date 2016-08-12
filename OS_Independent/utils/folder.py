#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Utility functions for folders handling
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2016)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2016/08/12)"
__status__ = "Usable for any project"

import os
import shutil
import logging

def createFolder(path):
  """Create a new directory

  Keyword arguments:
      path -- (string) name of the folder to create (relative or absolute)
  """
  try:
    os.stat(path)
  except:
    os.mkdir(path)
    logging.debug("Folder "+path+" created")
  else:
    logging.debug("Folder "+path+" already exist")

def removeFolder(path):
  """Delete an existing directory

  Keyword arguments:
      path -- (string) Name of the folder to delete (relative or absolute)
                       Only last folder of the path will be deleted
  """
  # Check if folder exists
  if os.path.exists(path):
    # Remove if exists
    shutil.rmtree(path)
    logging.debug("Folder "+path+" removed")
  else:
    logging.debug("Folder "+path+" does not exist")

def main():
  """Demo of the folder utility functions"""

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  folder_path = "testFolderToDelete"
  #"../testFolderToDelete"
  #"C:/testFolderToDelete"
  #"/home/testFolderToDelete"

  print("\n----------------------------------------------------")
  print("-----------Folder utility functions demo------------")
  print("----------------------------------------------------")

  print("\n-----------------Create folder----------------------")
  createFolder(folder_path)

  print("\n-----------------Delete folder----------------------")
  removeFolder(folder_path)

  print("\n----------------------------------------------------")
  print("-------------------End of demo----------------------")
  print("----------------------------------------------------\n")

if __name__ == "__main__":
    main()
