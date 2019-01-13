import sys
import bluetooth
import Adafruit_DHT
import datetime
import time
import paho.mqtt.publish as publish
import threading
from Crypto.Cipher import AES

#Establishing Bluetooth Connection
sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
bt_addr=sys.argv[1]
port = 0x1001
sock.connect((bt_addr, port))
print("Connected to %s on PSM 0x%X" % (bt_addr, port))
sock.send("connection opened")
#Establishing MQTT connection
MQTT_SERVER = "192.168.88.200"
MQTT_PATH = "TemperatureHumidity" 

def do_encrypt(message):
    """
    Encrypts data
    """
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    ciphertext = obj.encrypt(message)
    return ciphertext

def switch():
    """
    Controls the switching between protocols by setting and clearing flags
    """
    while True:
	if mqttFlag.is_set() == True:
        	mqttFlag.clear()
        bluetoothFlag.set()
        print('bluetooth set, mqtt cleared')
        time.sleep(120)
        bluetoothFlag.clear()
        mqttFlag.set()
        print('bluetooth cleared, mqtt set')
        time.sleep(120)
        
def Protocols():
    """
    Loops to check which protocols is being used, then enters a loop and runs that protocol until the time limit is reached
    """
        while True:
                while bluetoothFlag.is_set():
                    #executes while bluetooth flag is set
                    humidity, temperature = Adafruit_DHT.read(sensor=11, pin=4)
                    now = datetime.datetime.now()
                    data= "{}, Protocol=Bluetooth \tSensorID=Eimear, Temperature={}, Humidity={}".format(now, temperature, humidity)
                    #Checking length of data to be sent
                    if len(data)%16 !=0:
				        modulus = len(data)%16
				        additionalBytes= 16-modulus
                        #adding additional bytes to ensure data to be encrypted is factor of 16 bytes long
				        for i in range(0,additionalBytes):
                            data += " "
                    #Encrypting data
                    encrypt_message = do_encrypt(data)
                    #Send data through bluetooth socket
                    sock.send(encrypt_message)
                    time.sleep(4.5)
                while mqttFlag.is_set():
                    #executes while mqtt flag is set
                    humidity, temperature = Adafruit_DHT.read(sensor=11, pin=4)
                    now = datetime.datetime.now()
                    data= "{}, Protocol=MQTT \tSensorID=Eimear, Temperature={}, Humidity={}".format(now, temperature, humidity)
                    #Checking length of data to be sent
                    if len(data)%16 !=0:
                            modulus = len(data)%16
                            additionalBytes= 16-modulus
                            #adding additional bytes to ensure data to be encrypted is factor of 16 bytes long
                            for i in range(0,additionalBytes):
                                    data += " "
                    #Encrypting data
                    encrypt_message = do_encrypt(data)
                    #Publish data to channel
                    publish.single(MQTT_PATH, encrypt_message, hostname=MQTT_SERVER)
                    time.sleep(4.5)

#Defining flag events         
bluetoothFlag = threading.Event()
mqttFlag = threading.Event()
#Defining threads
switchProtocols = threading.Thread(target =switch)
startProtocols = threading.Thread(target = Protocols)
#Starting threads
switchProtocols.start()
startProtocols.start()