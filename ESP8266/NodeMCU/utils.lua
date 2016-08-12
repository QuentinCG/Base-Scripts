-- \brief Utility functions for ESP8266 device with NodeMCU
--
-- \author Quentin Comte-Gaz <quentin@comte-gaz.com>
-- \date 12 August 2016
-- \license MIT License (contact me if too restrictive)
-- \copyright Copyright (c) 2016 Quentin Comte-Gaz
-- \version 1.0

-- \brief Show configuration of the device
--
-- \param nil
-- \return nil
function showBaseConfiguration()
  local maj_ver, minor_ver, dev_ver, chip_id, flash_id, flash_size, flash_mode, flash_speed = node.info()
  print("Station Mode: "..tostring(wifi.getmode()))
  print("MAC Address: "..tostring(wifi.sta.getmac()))
  print("Heap Size: "..tostring(node.heap()).." bytes")
  print("NodeMCU version: "..tostring(maj_ver).."."..tostring(minor_ver).."."..tostring(dev_ver))
  print("Chip ID: "..tostring(chip_id))
  print("Flash ID: "..tostring(flash_id))
  print("Flash Size: "..tostring(flash_size).." bytes")
  print("Flash Mode: "..tostring(flash_mode))
  print("Flash Speed: "..tostring(flash_speed).." Hz")
  print("Vcc: "..tostring(adc.readvdd33()).." mV")
end

-- \brief Connect to the Wifi with auto reconnection
--
-- \param ssid (string): SSID of the Wifi to connect
-- \param pass (string): Pass of the Wifi to connect
-- \param function_to_load_after_connection (optional function): Function to load once wifi is connected
--
-- \return nil
function connectToWifi(ssid, pass, function_to_load_after_connection)
  -- Put Wifi into station mode to connect to network
  wifi.setmode(wifi.STATION)

  wifi.sta.config(ssid, pass)

  -- Auto-reconnect in case of disconnection
  wifi.sta.autoconnect(1)

  -- Count times you tried to connect to the network
  local wifi_counter = 0

  -- Create an alarm to poll the wifi.sta.getip() function once a second
  tmr.alarm(0, 1000, 1, function()
    if wifi.sta.getip() == nil then
      wifi_counter = wifi_counter + 1;
      print("Checking if connected to wifi for the last "..tostring(wifi_counter).." sec, may take few sec)")
    else
      tmr.stop(0) -- Stop the polling loop
      print("Connected to wifi")
      -- Debug info
      ip, nm, gw = wifi.sta.getip()
      print("IP Address: "..tostring(ip))
      print("Net-mask: "..tostring(nm))
      print("Gateway: "..tostring(gw))

      -- Continue to function after network connection
      if function_to_load_after_connection == nil then
        return
      end
      function_to_load_after_connection()
    end
  end)
end
