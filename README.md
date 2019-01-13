# IoT_Programming
Three projects that were carried out as part of the IoT module. 
All assignments make use of a DHT11 sensor connected to the RaspberryPi to record temperature and humidity data. The Adafruit library is used and code is written in Python.
Each part of the project builds on the previous part.

Part1 - Simple reading from one sensor and logging the information to a text file. 

Part2 - Linking two Raspberry Pis and two sensors. One client script and one server script. The connection is made between the Pis via Bluetooth. (Bluez library) Data is logged to Rapid7 where tags were created to label the data and allow for further analysis.

Part 3 - Linking two Raspberry Pis via Bluetooth and Wifi. MQTT if used as a wifi protocol and a broker is bypassed with just a publisher and subscriber. The publisher also sends data via Bluetooth to the subscriber script. Flags are used to handle timing of switches between protocols which run for 120 seconds at a time. Data is encrypted before being sent and decrypted once received. All data is then logged to Rapid7 log files as in Part 2. 
