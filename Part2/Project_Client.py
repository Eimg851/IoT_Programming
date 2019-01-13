import sys
import bluetooth
import Adafruit_DHT
import datetime
import time

sensor = 11
pin = 4

#Integrating with older Python versions if necessary
if sys.version < '3':
    input = raw_input

sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)

#Check Bluetooth Address was provided
if len(sys.argv) < 2:
    print("Bluetooth Address required as parameter")
    sys.exit(2)

#Variable assignment
bt_addr=sys.argv[1]
port = 0x1001
print("Trying to connect to %s on PSM 0x%X" % (bt_addr, port))

try:
    sock.connect((bt_addr, port))
    while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, delay_seconds=4)
            now = datetime.datetime.now()
            data= "{} \tSensorID=Amy Temperature={}, Humidity={}\n".format(now, temperature, int(humidity))
            sock.send(data)
    sock.close()
except:
    print("Connection failed. Please try again")

