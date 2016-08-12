#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Utility functions for USB camera support on Linux

  Used unix command: fswebcam
  /!\ Be sure this command is available on your Linux device.
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2016)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2016/04/04)"
__status__ = "Usable for any Linux project with an USB camera"

import subprocess # For linux command
import logging # For log

import base_64 # For base 64 conversion (custom lib)

def takePictureUSBCamera(title = "", image_name = "picture.jpg",
                         device = "/dev/video0", input = "0",
                         resolution = "1280x720"):
  """Take a picture and return the stored image name

  Keyword arguments:
    title -- (string, optional) Title to put on the picture
    image_name -- (string, optional) Name of the picture to take
    device -- (string, optional) Webcam device name
    input -- (string or int, optional) Input webcam number
    resolution -- (string, optional) Resolution of the picture to take

  return: (string) Name of the taken picture
                   (empty string if not possible to take one)
  """
  cmd = "fswebcam --device \""+device+"\" --input "+input+" --palette MJPEG " \
        "--resolution "+resolution+" --skip 20 --bottom-banner --title " \
        "\""+title+"\" --timestamp \"%d-%m-%Y %H:%M:%S (%Z)\" --jpeg 95 " \
        "--save "+image_name+" --set lights=on"

  process = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

  out, err = process.communicate()
  result = str(out)+str(err)
  if ("Writing JPEG image to" in result):
    logging.debug("Picture "+image_name+" taken from USB camera.")
    return image_name
  else:
    logging.error("Picture from USB camera not taken...\n"
                  "Be sure 'fswebcam' is installed and "
                  "your parameters are valid.")
  return ""

def getBase64PictureUSBCamera(title = "", device = "/dev/video0", input = 0,
                              resolution = "1280x720"):
  """Take a picture and returns it as a base 64 string

  Keyword arguments:
    title -- (string, optional) Title to put on the picture
    device -- (string, optional) Webcam device name
    input -- (string or int, optional) Input webcam number
    resolution -- (string, optional) Resolution of the picture to take

  return: (string) Base 64 encoded picture
                   (empty string if not possible to take one)
  """
  image_name = takePictureUSBCamera(title, "temp_picture.jpg",
                                    device, str(input), resolution)
  if image_name:
    logging.debug("Converting image "+image_name+" to base 64.")
    return base_64.convertFileToBase64(image_name)
  logging.error("Can't retrieve image information to convert to base 64.")
  return ""

def main():
  """Demo of the Linux USB camera utility functions"""

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  print("\n----------------------------------------------------")
  print("--------Linux camera utility functions demo---------")
  print("----------------------------------------------------")

  print("\n----------------Take a picture----------------------")
  image_name = takePictureUSBCamera(title="This is a dummy picture description")
  print("Image name: "+image_name)

  print("\n--------Take base 64 camera image-------------------")
  image_data = getBase64PictureUSBCamera(title="My dummy image description")
  if image_data:
    print("First 15 char of the encoded image: "+str(image_data[:15]))
  else:
    print("Wrong picture data")

  print("\n----------------------------------------------------")
  print("-------------------End of demo----------------------")
  print("----------------------------------------------------\n")

if __name__ == "__main__":
    main()
