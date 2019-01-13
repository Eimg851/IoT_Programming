
import bluetooth
from r7insight import R7InsightHandler
import logging
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt
from datetime import datetime
import threading
from Crypto.Cipher import AES

#Establishing connection with Rapid7 Insight Ops log
log = logging.getLogger('r7insight')
log.setLevel(logging.INFO)
test = R7InsightHandler('76f50ffb-f011-4ce3-bce6-542fb9474fdc', 'eu')
log.addHandler(test)
log.info("Info message")


def do_decrypt(ciphertext):
    """
    Decrypts cipher text
    """
    obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    message = obj2.decrypt(ciphertext)
    return message

#Connecting to Bluetooth
server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )
port = 0x1001
server_sock.bind(("",port))
server_sock.listen(1)
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

#Connecting to MQTT Publisher Channel
MQTT_SERVER = "localhost"
MQTT_PATH = "TemperatureHumidity"  


def on_connect(client, userdata, flags, rc):
    """
    Subscribing to channel
    """
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    """
    Listening for new publish messages
    """
    #decrypting the data
    data = do_decrypt(str(msg.paylod))
    #logging data to Rapid 7
    log.info(data)

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
            print("bluetooth starting")
            data = client_sock.recv(1024)
            #decrypting data
            data = do_decrypt(data)
            #logging data to Rapid7 Inisght Ops
            log.info(data)
            #Getting sensor reading
            humidity, temperature = Adafruit_DHT.read(sensor=11, pin=4)
            timestamp = datetime.datetime.now()
            #Logging local reading to Rapid 7
            log.info("{} \tSensorID=Amy, Temperature={}, Humidity={}".format(timestamp, temperature, int(humidity)))
            time.sleep(4.5)
        while mqttFlag.is_set():
            #executes while mqtt flag is set
            client.loop_start()
            #Getting sensor reading
            humidity, temperature = Adafruit_DHT.read(sensor=11, pin=4)
            timestamp = datetime.datetime.now()
            #Logging local reading to Rapid 7
            log.info("{} \tSensorID=Amy, Temperature={}, Humidity={}".format(timestamp, temperature, int(humidity)))
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

