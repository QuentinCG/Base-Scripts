#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions for minimalistic Linux
This library is designed for minimalistic Linux system which does
not support the psutils library.

Used unix command: top, ifconfig, ping, grep, head, awk, cut, cat.
/!\ Be sure those commands are available on your Linux device (those are
basic linux commands which should be installed by default).

/!\ Execute getNetworkInUsage() and getNetworkOutUsage() with root rights
(ifconfig requires root privilege to be executed)

Note: Tested on some Linux device:
        - ARM Linux 2.6
        - Debian (Linux 3.1+)
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2016)"
__python_version__ = "2.7+" #TODO: Make this lib compatible with Python 3.x
__version__ = "1.0 (2016/03/27)"
__status__ = "Usable for any linux project"

import subprocess # For linux command
import socket # For port scan
import logging # For log

def __getLinuxFirstLineOutputResult(cmd):
  """(Internal function) Execute linux command and give first line result

  Keyword arguments:
    cmd -- (string) Linux command

  return: (string) First line in stdout (without potential '\n' at the end)
  """
  process = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
  return process.stdout.readline().rstrip('\n')

def isRoot():
  """Check if script has root privilege

  return: (bool) Script has root privilege
  """
  is_root = True
  try:
    with open('/etc/foo', 'a'):
      pass
  except IOError:
    is_root = False
  return is_root

def getLoadAverage():
  """Get the load average for the last 15min

  return: (float) Load average or -1 if impossible to get the load average
  """
  cmd = "cat /proc/loadavg | awk '{print $3}'"
  try:
    load_average = __getLinuxFirstLineOutputResult(cmd)
    return float(load_average)
  except:
    logging.error("getLoadAverage: Can't retrieve the load average... \n"\
                  "Try to execute \""+cmd+"\" on your computer to check "\
                  "if the result is a load average.")
  return -1

def getCpuUsage():
  """Get the current CPU usage

  return: (float) CPU usage (in %) or -1 if impossible to get the CPU usage
  """
  cmds = [
    "top -b -d1 -n1|grep -i 'CPU:'|head -c20|awk '{print $2}'|cut -d '%' -f1",
    "top -b -d1 -n1|grep -i 'Cpu(s)'|head -c20|awk '{print $2}'|cut -d '%' -f1"
  ]

  for cmd in cmds:
    try:
      cpu_usage = __getLinuxFirstLineOutputResult(cmd)
      return float(cpu_usage)/100.0
    except:
      pass
  logging.error("getCpuUsage: Can't retrieve the CPU usage... \n"\
                "Try to execute \"top -b -d1 -n1\" on your computer to check "\
                "if the result is a CPU usage line.")
  return -1

def getFreeRam():
  """Get the free RAM (in kB)

  return: (float) Free RAM (in kB) or -1 if impossible to get the free RAM
  """
  try:
    free_mem = \
      float(__getLinuxFirstLineOutputResult("grep MemFree /proc/meminfo | awk '{print $2}'")) + \
      float(__getLinuxFirstLineOutputResult("grep Buffers /proc/meminfo | awk '{print $2}'")) + \
      float(__getLinuxFirstLineOutputResult("grep Cached /proc/meminfo | awk '{print $2}'"))
    return free_mem
  except:
    logging.error("getFreeRam: Can't retrieve the free RAM... \n"\
                  "Try to execute \"grep MemFree /proc/meminfo | awk '{print $2}'\" "\
                  "on your computer to check if the result is a part of the free RAM.")
  return -1

def getTotalRam():
  """Get the total RAM (in kB)

  return: (float) Total RAM (in kB) or -1 if impossible to get the total RAM
  """
  try:
    total_mem = \
      float(__getLinuxFirstLineOutputResult("grep MemTotal /proc/meminfo | awk '{print $2}'"))
    return total_mem
  except:
    logging.error("getTotalRam: Can't retrieve the total RAM... \n"\
                  "Try to execute \"grep MemTotal /proc/meminfo | awk '{print $2}'\" "\
                  "on your computer to check if the result is the total RAM.")
  return -1

def getPercentFreeRam(total_ram = getTotalRam(), free_ram = getFreeRam()):
  """Get the free RAM

  Keyword arguments:
    total_ram -- (float, optional) Total RAM (in kB)
    free_ram -- (float, optional) Free RAM (in kB)

  return: (float) Free RAM (in %) or -1 if impossible to get the free RAM
  """
  if total_ram <= 0 or free_ram < 0:
    logging.error("getFreeRam: Can't retrieve the free RAM... \n"\
                  "Try to execute \"grep MemTotal /proc/meminfo | awk '{print $2}'\" "\
                  "on your computer to check if the result is the total RAM.")
    return -1

  return free_ram/total_ram

def getFreeSwap():
  """Get the free SWAP (in kB)

  return: (float) Free Swap (in kB) or -1 if impossible to get the free SWAP
  """
  try:
    free_swap = \
      float(__getLinuxFirstLineOutputResult("grep SwapFree /proc/meminfo | awk '{print $2}'"))
    return free_swap

  except:
    logging.error("getFreeSwap: Can't retrieve the free SWAP... \n"\
                  "Try to execute \"grep SwapFree /proc/meminfo | awk '{print $2}'\" "\
                  "on your computer to check if the result is the free SWAP.")
  return -1

def getTotalSwap():
  """Get the total SWAP (in kB)

  return: (float) Total Swap (in kB) or -1 if impossible to get the total SWAP
  """
  try:
    free_swap = \
      float(__getLinuxFirstLineOutputResult("grep SwapTotal /proc/meminfo | awk '{print $2}'"))
    return free_swap

  except:
    logging.error("getFreeSwap: Can't retrieve the total SWAP... \n"\
                  "Try to execute \"grep SwapTotal /proc/meminfo | awk '{print $2}'\" "\
                  "on your computer to check if the result is the total SWAP.")
  return -1

def getPercentFreeSwap(total_swap = getTotalSwap(), free_swap = getFreeSwap()):
  """Get the free SWAP (in %)

  Keyword arguments:
    total_swap -- (float, optional) Total Swap (in kB)
    free_swap -- (float, optional) Free Swap (in kB)

  return: (float) Free Swap (in %) or -1 if impossible to get the free SWAP
  """
  if total_swap <= 0 or free_swap < 0:
    logging.error("getFreeSwap: Can't retrieve the free SWAP... \n"\
                  "Try to execute \"grep SwapTotal /proc/meminfo | awk '{print $2}'\" "\
                  "on your computer to check if the result is the total SWAP.")
    return -1

  return free_swap/total_swap

def getUpTime():
  """Get the time since the computer was started

  return: (float) Up time (in hours) or -1 if impossible to get up time
  """
  cmd = "cat /proc/uptime | awk '{print $1}'"
  try:
    up_time = __getLinuxFirstLineOutputResult(cmd)
    return float(up_time)/3600.0
  except:
    logging.error("getUpTime: Can't retrieve the up time... \n"\
                  "Try to execute \""+cmd+"\" on your computer to check "\
                  "if the result is the up time in sec.")
  return -1

def getDiskUsage(disk):
  """Get the disk usage of a specific directory

  Keyword arguments:
    disk -- (string) Path to the disk

  return: (float) Disk usage (in %) or -1 if impossible to get the disk usage
  """
  cmd = "df "+disk+"|grep /|awk '{print $5}'|cut -d '%' -f1"
  try:
    disk_usage = __getLinuxFirstLineOutputResult(cmd)
    return float(disk_usage)/100.0
  except:
    logging.error("getDiskUsage: Can't retrieve the disk "+disk+" usage... \n"\
                  "Try to execute \""+cmd+"\" on your computer to check "\
                  "if the result is the a disk usage.")
  return -1

def getNetworkInUsage(interface):
  """Get the network IN usage (<!> requires root rights)

  Keyword arguments:
    interface -- (string) Network interface (eth0, ...)

  return: (int) Network IN usage (in MB) or -1 if impossible to get the network IN usage
  """
  cmd = "sudo ifconfig "+interface+"|grep 'RX bytes'|cut -d ':' -f2 |awk  '{print $1}'"
  try:
    net_usage = __getLinuxFirstLineOutputResult(cmd)
    return float(net_usage)/(1048576.0) #1MB = 1024*1024B = 1048576B
  except:
    logging.error("getNetworkInUsage: Can't retrieve "+interface+" network " \
                  "information...\nTry to execute \""+cmd+"\" on your " \
                  "computer to check if the result is the IN network used " \
                  "size in bytes.")
  return -1

def getNetworkOutUsage(interface):
  """Get the network OUT usage (<!> requires root rights)

  Keyword arguments:
    interface -- (string) Network interface (eth0, ...)

  return: (int) Network OUT usage (in MB) or -1 if impossible to get the network OUT usage
  """
  cmd = "sudo ifconfig "+interface+"|grep 'TX bytes'|cut -d ':' -f3 |awk  '{print $1}'"
  try:
    net_usage = __getLinuxFirstLineOutputResult(cmd)
    return float(net_usage)/(1048576.0) #1MB = 1024*1024B = 1048576B
  except:
    logging.error("getNetworkOutUsage: Can't retrieve "+interface+" network " \
                  "information...\nTry to execute \""+cmd+"\" on your " \
                  "computer to check if the result is the OUT network used " \
                  "size in bytes.")
  return -1

def ping(host):
  """Ping an host (result in ms)

  Keyword arguments:
    host -- (string) Address or IP of the host

  return: (int) Ping result (in ms) or -1 if impossible to ping the host
  """
  cmds = [
    "ping -w 1 -qc 1 "+host+" |grep ' ms'|cut -d '/' -f4",
    "ping -w 1 -qc 1 "+host+" |grep ' ms'|cut -d '/' -f5"
  ]
  for cmd in cmds:
    try:
      ping_result = __getLinuxFirstLineOutputResult(cmd)
      return float(ping_result)
    except:
      pass
  logging.debug("ping: Host "+host+" is not answering to ping.")
  return -1

def pingBool(host):
  """Ping an host (bool result)

  Keyword arguments:
    host -- (string) Address or IP of the host

  return: (bool) Ping is a success
  """
  result = ping(host)
  return False if result == -1 else True

def scanLocalPort(port):
  """Check if a local port is open

  Keyword arguments:
    port -- (int) Port of the localhost to scan

  return: (bool) Port is open
  """
  sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
  result = sock.connect_ex(("localhost", port))

  if result == 0:
    return True
  return False

def main():
  """Demo of the linux utility functions"""

  logger = logging.getLogger()
  logger.setLevel(logging.CRITICAL) # Use logging.DEBUG for more details

  print("\n----------------------------------------------------")
  print("------------Linux utility functions demo------------")
  print("----------------------------------------------------")

  print("\n----------------Root privilege----------------------")
  root_privilege = isRoot()
  if root_privilege:
    print("You have root privilege")
  else:
    print("You don't have root privilege...\n"
          "Some of the functions will not be usable")

  print("\n-----------------Load Average-----------------------")
  print("Load Average (15 min): "+str(getLoadAverage()))

  print("\n--------------------CPU Usage-----------------------")
  print("CPU Usage: "+str(getCpuUsage()*100)+" %")

  print("\n------------------------RAM-------------------------")
  print("Free RAM: "+str(getFreeRam()/1024)+" MB")
  print("Total RAM: "+str(getTotalRam()/1024)+" MB")
  print("Free RAM: "+str(getPercentFreeRam()*100)+" %")

  print("\n-----------------------SWAP-------------------------")
  print("Free Swap: "+str(getFreeSwap()/1024)+" MB")
  print("Total Swap: "+str(getTotalSwap()/1024)+" MB")
  print("Free Swap: "+str(getPercentFreeSwap()*100)+" %")

  print("\n---------------------Up Time------------------------")
  print("Up time: "+str(getUpTime())+" hours")

  print("\n-------------------Disk Usage-----------------------")
  disks = ["/", "/root", "/dev/md1", "/dev/md2", "/dev/sda1", "/dev/sda2"]
  for disk in disks:
    disk_usage = getDiskUsage(disk)
    if disk_usage >= 0:
      print("Disk Usage of "+disk+": "+str(disk_usage*100)+" %")
    else:
      print("Disk Usage of "+disk+": Error")

  print("\n-----------------Network Usage----------------------")
  if root_privilege:
    network_interfaces = ["eth0", "egiga0"]
    for interface in network_interfaces:
      network_in = getNetworkInUsage(interface)
      network_out = getNetworkOutUsage(interface)

      if network_in >= 0:
        print("Network In of "+interface+": "+str(network_in)+" MB")
      else:
        print("Network In of "+interface+": Error")

      if network_out >= 0:
        print("Network Out of "+interface+": "+str(network_out)+" MB")
      else:
        print("Network Out of "+interface+": Error")
  else:
    print("This part requires root privilege.")

  print("\n----------------------Ping--------------------------")
  ping_addresses = \
    ["8.8.8.8", "google-public-dns-b.google.com",
     "ns1.telstra.net", "127.0.0.1", "111.111.111.111"]
  for address in ping_addresses:
    ping_result = ping(address)
    if ping_result >= 0:
      print("Ping "+address+": "+str(ping_result)+" ms")
    else:
      print("Ping "+address+": Timeout")
  false_address = "123.123.123.123"
  print("Bool ping of "+false_address+" returns "+str(pingBool(false_address)))
  print("\n----------------Local Port scan---------------------")
  ports = [21, 22, 80, 443, 2121, 2222, 8080]
  for port in ports:
    print("Port "+str(port)+" open: "+str(scanLocalPort(port)))

  print("\n----------------------------------------------------")
  print("-------------------End of demo----------------------")
  print("----------------------------------------------------\n")

if __name__ == "__main__":
    main()
