#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Utility functions and class for date display
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2016)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2016/08/12)"
__status__ = "Usable for any project"

import time
import datetime
import logging
import threading
import thread
from threading import Thread

def getDate():
  """Get current date (%Y-%m-%d format)

  return: (str) Current date
  """
  return str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

def getTime():
  """Get current time (%H:%M:%S format)

  return: (str) Current time
  """
  return str(datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))

class printCurrentTimePeriodicallyThread(threading.Thread):
  """Show date and/or time periodically asynchronously from the rest of the app

  example:
    '''
    time_thread = printCurrentTimePeriodicallyThread(time_sec=1, show_date = True, show_time = True)
    time_thread.start()
    print("Doing some stuff here without being blocked")
    time.sleep(10)
    print("Stopping time thread because not needed anymore")
    time_thread.stop()
    '''
  """

  def __init__(self, time_sec, show_date = True, show_time = True):
    """Initialize the thread

    Keyword arguments:
        time_sec -- (int) Delay beween every display of the time or/and date
        show_date -- (bool, optional) Show date
        show_time -- (bool, optional) Show time

    Note: At least one of show_date and show_time must be True and time_sec must be >= 1
    """
    threading.Thread.__init__(self)

    self.show_date = show_date
    self.show_time = show_time

    if (time_sec >= 1 and (show_date or show_time)):
      self.time_sec = time_sec
      self.is_running = True
    else:
      logging.error("Wrong parameters")
      self.time_sec = 0
      self.is_running = False

  def run(self):
    while self.is_running:
      date_to_show = ""
      if (self.show_date):
        date_to_show += getDate()
      if (self.show_time):
        if date_to_show != "":
          date_to_show += " "
        date_to_show += getTime()

      print("------ "+str(date_to_show)+" ------")
      time.sleep(self.time_sec)

  def stop(self):
    """Stop the thread (it may take up to time_sec seconds to be effective)"""
    self.is_running = False

def main():
  """Demo of the date and time utility functions"""

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  print("\n----------------------------------------------------")
  print("-------Date and time utility functions demo---------")
  print("----------------------------------------------------")

  print("\n---------------Get current date---------------------")
  print("Date: "+getDate())

  print("\n---------------Get current time---------------------")
  print("Time: "+getTime())

  print("\n---Show time every sec for 10sec (asynchronously)---")
  time_thread = printCurrentTimePeriodicallyThread(time_sec=1, show_date = True,
                                                   show_time = True)
  time_thread.start()
  time.sleep(5)
  print("Hello from main() function")
  time.sleep(5)
  print("Stopping time thread from main() function")
  time_thread.stop()

  print("\n----------------------------------------------------")
  print("-------------------End of demo----------------------")
  print("----------------------------------------------------\n")

if __name__ == "__main__":
    main()
